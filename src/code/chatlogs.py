import pathlib as Path
import io
import re
import pygame

class Chatlogs:
    def __init__(self):
        self.old_filesize = 0
        self.lines_to_read = 5
        self.new_line_found = False
        self.lines_history = ["" for _ in range(self.lines_to_read * 2)]
        self.new_lines = []

        self.buy_strings = ["sell", "[s]", "wts", "free", "giving"]
        self.sell_strings = ["buy", "[b]", "wtb", "lf", "looking"]
        self.end_of_ci_fray_strings = ["Ye have take", "With the isla", "Ye abandoned"]
        self.last_time_stamp = ""

        # [18:44:03] Vessels may be sunk while in these dangerous waters, enter at your own risk!
        # [18:53:49] Another draft from the rum kegs chases away the last ill effects of the vile fog.
        # [18:54:23] The crew inhales the noxious fog, and starts to lose fine motor control.
        self.island_land_string = "Ye land on the island, but an angry mob of its inhabitants stands between ye and yer rightful plunderin'!"
        self.overrun_string = "Yer vessel be overrun with zombies! All hands join the fight to save the ship!"

        self.swabbies_on_board = 0


    def tail(self, path: Path, _buffer: int = 4098) -> list[str]:
        """Tail a file and get X lines from the end."""

        lines_found = []
        block_counter = -1

        with path.open("rb") as f:  # open in binary mode for precise seek
            while len(lines_found) < self.lines_to_read:
                try:
                    f.seek(block_counter * _buffer, io.SEEK_END)
                except OSError:  # reached start of file
                    f.seek(0)
                    chunk = f.read().decode(errors="ignore")
                    lines_found = chunk.splitlines()
                    break

                chunk = f.read().decode(errors="ignore")
                lines_found = chunk.splitlines()
                block_counter -= 1

        return lines_found[-self.lines_to_read:]

    def update_chatlogs(self, main):
        self.new_lines = []
        size = main.configs.file_path.stat().st_size

        if size == self.old_filesize:
            return
        
        self.old_filesize = size
        self.check_for_new_lines(main)
        
    

    def check_for_new_lines(self, main):
        lines = self.tail(main.configs.file_path)
        for line in lines:
            if line not in self.lines_history:
                self.new_lines.append(line)
                self.lines_history.append(line)

        # print(F"New lines: {self.new_lines}")

        self.lines_history = self.lines_history[-self.lines_to_read * 2:]

    
    def split_buy_and_sell(self, message: str) -> tuple[list[str], list[str]]:
        """
        Splits the message into buy and sell parts.
        Returns (buy_parts, sell_parts)
        Each part keeps the keyword and following text until the next keyword.
        """
        all_keywords = self.buy_strings + self.sell_strings

        # Create a pattern to match any keyword
        pattern = r"(" + "|".join(all_keywords) + r")"
        parts = re.split(pattern, message, flags=re.IGNORECASE)

        buy_parts = []
        sell_parts = []
        i = 0
        while i < len(parts):
            part = parts[i].strip()
            if part.lower() in [k.lower() for k in self.buy_strings]:
                combined = part
                if i + 1 < len(parts):
                    combined += " " + parts[i + 1].strip()
                buy_parts.append(combined)
            elif part.lower() in [k.lower() for k in self.sell_strings]:
                combined = part
                if i + 1 < len(parts):
                    combined += " " + parts[i + 1].strip()
                sell_parts.append(combined)
            i += 1

        return buy_parts, sell_parts


    def save_last_time(self, line):
        time_stamp = line[1:9] # 01:33:56
        # Add one second to time_stamp
        time_stamp_seperated = [int(time_stamp[0:2]), int(time_stamp[3:5]), int(time_stamp[6:])]
        time_stamp_seperated[2] += 1 # We want to ignore the next second too
        if time_stamp_seperated[2] == 60: # Roling over seconds/minutes/hours if required
            time_stamp_seperated[1] += 1
            time_stamp_seperated[2] = 00
            if time_stamp_seperated[1] == 60:
                time_stamp_seperated[0] += 1
                time_stamp_seperated[1] = 00
                if time_stamp_seperated[0] == 24:
                    time_stamp_seperated[0] = 00
                    time_stamp_seperated[1] = 00
        for x in list(range(0,3)):
            time_stamp_seperated[x] = str(time_stamp_seperated[x])
            if len(time_stamp_seperated[x]) == 1:
                time_stamp_seperated[x] = "0" + time_stamp_seperated[x] # Converting back to integers loses leading 0s, adding them back in
        future_time_stamp = time_stamp_seperated[0] + ":" + time_stamp_seperated[1] + ":" + time_stamp_seperated[2]
        self.last_time_stamp = [time_stamp, future_time_stamp]


    def filter_chat(self, main): #TODO add ability to click to copy pirates name to clipboard
        for line in self.new_lines:
            buy_and_sell_split = False
            for search_string in main.configs.search_strings.values():
                if search_string["regex"]:
                    if re.search(search_string["regex"], line):
                        main.sounds.play_sound(search_string["sound"])
                    continue
                if search_string["channel"] and search_string["channel"] != line.split(" ")[2]:
                    continue
                if search_string["channel"] == "trade":
                    if not buy_and_sell_split:
                        buy_parts, sell_parts = self.split_buy_and_sell(line)
                        buy_and_sell_split = True
                    if search_string["buy_or_sell"] == "buy":
                        for string in search_string["strings"]:
                            for part in buy_parts:
                                if string in part:
                                    main.sounds.play_sound(search_string["sound"])
                    elif search_string["buy_or_sell"] == "sell":
                        for string in search_string["strings"]:
                            for part in sell_parts:
                                if string in part:
                                    main.sounds.play_sound(search_string["sound"])
                else:
                    for string in search_string["strings"]:
                        if string in line:
                            print(F"{search_string["sound"]}")
                            main.sounds.play_sound(search_string["sound"])

    
    def ci_chat_filter(self, main):
        for line in self.new_lines:

            if line[11:] == self.island_land_string:
                main.landed = True
                main.overrun = False
            
            elif line[11:] == self.overrun_string:
                main.overrun = True
                main.rumble_active = pygame.time.get_ticks() - main.configs.timer_offset
            
            if main.overrun and line[11:20] == "Game over":
                main.overrun = False
                main.rumble_active = False

            elif main.frays_won == 0 and line[11:20] == "Game over":
                main.swabbies_on_board = line.count(',') + 1 # Number of team members
                non_pirate_count = line.count(' ') - 4 - main.swabbies_on_board # This should be the number of non humans
                players_on_board = main.swabbies_on_board - non_pirate_count
                thralls_on_board = line.count('Thrall')
                main.swabbies_on_board -= (thralls_on_board + players_on_board)
                main.rumble_active = False

            if self.swabbies_on_board > 0:
                if "has left the vessel." in line:
                    main.swabbies_on_board -= 1

            if line[11:34] == "The islanders reclaimed":
                main.rumble_active = 0
                main.sf_active = 0

            elif line[11:20] in self.end_of_ci_fray_strings and not self.looting_active:
                main.frays_won += 1
                main.looting_active = True
                main.looting_active = pygame.time.get_ticks() - main.configs.timer_offset
                main.rumble_active = 0
                main.sf_active = 0

            elif (line[11:33] == "Enlightened One says, "):
                if not main.rumble_active:
                    self.rumble_active = pygame.time.get_ticks() + 17000 - main.configs.timer_offset

            elif " Cultist shouts" in line and not (" says, \"" in line or " tells ye, '" in line): # Cultist can be named so can't use precise string location to avoid trolling.
                if not main.sf_active:
                    self.sf_active = pygame.time.get_ticks() + 17000 - main.configs.timer_offset
                    
            elif line[11:32] == "Vargas the Mad says,":
                main.vargas_seen = True

    
    def vl_chat_filter(self, main):
        for line in self.new_lines:
            if line[11:20] == "Game over":
                if main.configs.name in line: # If name is in line, players won.
                    main.looting_active = pygame.time.get_ticks() - main.configs.timer_offset + main.vampire_delay

    
    def ww_chat_filter(self, main): # Werewolf messages in the future
        pass

    
    def ev_chat_filter(self, main):
        for line in self.new_lines:
            if "you are being pursued by " in line:   
                main.sounds.play_sound("warning")
            #TODO set sail timer?
            #TODO 3 min spawntimer?

    
    def gp_chat_filter(self, main): # Greedy Pillage in the future.
        pass


    def maa_filter_chat(self, main): # Maa messages in the future.
        pass


    def kh_filter_chat(self, main): # KH messages in the future.
        pass
        

    def process_updated_chatlogs(self, main):
        if main.configs.chat_filter_on:
            self.filter_chat(main)
            
        if main.configs.mode == "":
            return
        elif main.configs.mode == "CI":
            self.ci_chat_filter(main)
        elif main.configs.mode == "VL":
            self.vl_chat_filter(main)
        elif main.configs.mode == "WW":
            self.ww_chat_filter(main)
        elif main.configs.mode == "EV":
            self.ev_chat_filter(main)
        elif main.configs.mode == "GP":
            self.gp_chat_filter(main)
        elif main.configs.mode == "MA":
            self.maa_chat_filter(main)
        elif main.configs.mode == "KH":
            self.kh_chat_filter(main)
                

