import pygame
from pathlib import Path
import pickle
import pyperclip
# from code.listener import KeyListener

class Fray:
    def __init__(self, src_path: Path):
        self.length_of_a_minute = 60 # Just used for quick debugging
        self.load_punch_dictionary(src_path)
        self.fray_minutes = 0
        self.fray_seconds = 0
        self.minute_approaching_sound_played = False

        self.groups_needed = {0: "14-15", 1: "10-13", 2: "9-10", 3: "7-9", 4: "7-8",  5: "6-7", 6: "5-7", 7: "5-6", 8: "5-6", 9: "4-5", 10: "4-5", 11: "4-5"} # key is minutes passed, value is groups recommended
        self.homun_count = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "purple": 0, "orange": 0, "white": 0, "very_black": 0}
        self.homun_colour_translate = {"red": "red", "green": "yellow", "blue": "red", "yellow": "blue", "purple": "green", "orange": "green", "white": "blue", "very_black": "yellow"}
        self.homun_true_count = {"red": 0, "green": 0, "blue": 0, "yellow": 0}

    def load_punch_dictionary(self, src_path: Path):
        rumble_dictionary_locaton = src_path / Path("media", "rumble_dictionary.pkl")
        with open(rumble_dictionary_locaton, 'rb') as file:            
            self.rumble_dictionary = pickle.load(file)


    def calculate_fray_duration(self, fray_time):
        fray_duration = (pygame.time.get_ticks() - fray_time) // 1000 # time in seconds
        self.fray_minutes, self.fray_seconds = divmod(fray_duration, self.length_of_a_minute) # length_of_a_minute for quick debugging


    def should_it_play_warning(self, main):
        if self.fray_seconds >49 and not self.minute_approaching_sound_played:
            main.sounds.play_sound("warning")
            self.minute_approaching_sound_played = True                     
    

    def update_rumble(self, main):
        self.calculate_fray_duration(main.rumble_active)
        self.should_it_play_warning(main)
        main.gui.update_fray_time(self.fray_minutes, self.fray_seconds, "rumble")
        if main.configs.mini_rumble:
            main.gui.update_mini_rumble_groups(self.groups_needed[min(11, self.fray_minutes)]) # Pointless for longer than 11 minutes, honestly less.
        else:
            main.gui.draw_rumble_table(main, min(15, self.fray_minutes + 1), self.rumble_dictionary)


    def update_sf(self, main):            
        self.calculate_fray_duration(main.sf_active)
        main.gui.update_fray_time(self.fray_minutes, self.fray_seconds, "sf")


    def check_for_homun_click(self, main, pos, button):
        for colour, rect in main.gui.homun_colour_bars.items():
            if rect.collidepoint(pos):
                self.add_homun(main, colour, button)

    
    def add_homun(self, main, colour, button):
        if main.configs.mode != "CI" or not main.sf_active: return
        sf_colour = self.homun_colour_translate[colour]
        if button == 1:
            self.homun_count[colour] += 1
            self.homun_true_count[sf_colour] += 1
        elif button == 3:
            if self.homun_count[colour] > 0:
                self.homun_true_count[sf_colour] = max(0, self.homun_true_count[sf_colour] - 1)
            self.homun_count[colour] = max(0, self.homun_count[colour] - 1)
        elif button == 2:
            self.copy_homun_colours(sf_colour)


    def reset_homun(self):
        for colour in self.homun_count:
            self.homun_count[colour] = 0
        for colour in self.homun_true_count:
            self.homun_true_count[colour] = 0

    
    def copy_homun_colours(self, targetting : str=""):
        homun_count = "/ve ."
        sorted_homu_count = dict(sorted(self.homun_true_count.items(), key=lambda item: item[1], reverse=True))
        for colour in sorted_homu_count:
            count = sorted_homu_count[colour]
            if count > 0:
                homun_count += f"\n{count} {colour.upper()}"
            if targetting == colour:
                homun_count += " <-- target"
        pyperclip.copy(homun_count)