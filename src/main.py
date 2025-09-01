import pygame
from pathlib import Path
import timeit

from code.gui import GUI
from code.sounds import Sounds
from code.configs import Configs
from code.chatlogs import Chatlogs
from code.fray import Fray

class Main:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Pirate Helper')
        self.pygame_display = pygame.display.set_mode((200, 600))
        self.clock = pygame.time.Clock()

        self.crashed = False

        self.src_path = Path.cwd() / "src"
        # self.puzzles_image_path = self.src_dir / "media" / "global" / "puzzle_previews_small.png"
        # self.img_puzzles_image = pygame.image.load(self.puzzles_image_path)

        self.configs = Configs()
        self.gui = GUI(self.src_path)
        self.sounds = Sounds(self.src_path)
        self.chatlogs = Chatlogs()
        self.fray = Fray(self.src_path)

        self.maximum_players = [4, 4, 3, 3, 2]
        self.vampire_delay = 2800

        self.swabbies_on_board = 0
        self.plank_swabbie = False
        
        self.reset_stats()


    def reset_stats(self):
        self.players_on_board = 0
        self.landed = True
        self.overrun = False
        self.frays_won = 0
        self.rumble_active = 0
        self.sf_active = 0
        self.looting_active = 0
        self.vargas_seen = False
        self.homu_colours = {"red": 0, "green": 0, "blue": 0, "yellow": 0}

        self.swabbie_alert_last_played = 0
        self.plank_swabbie_flash_speed = 500


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True

    
    def calculate_looting_timer(self):
        time_passed = pygame.time.get_ticks() - self.looting_active
        if time_passed > 120000: # 2 minutes
            self.looting_active = 0
            if self.mode == "CI": 
                self.plank_swabbie_check()
        self.gui.update_time_passed_text(self.time_passed)

    
    def plank_swabbie_check(self):
        player_count = self.players_on_board + self.swabbies_on_board
        if player_count > self.maximum_players[self.frays_won]:
            self.plank_swabbie = True
        else:
            self.plank_swabbie = False
        if self.plank_swabbie:
            indicator_in_white = (pygame.time.get_ticks() // self.plank_swabbie_flash_speed) % 2
            self.gui.update_plank_swabbie_indicator(main, indicator_in_white)
            
            if (pygame.time.get_ticks() - swabbie_alert_last_played > 6500) and self.configs.play_swabbie_warning_sound: # Delay between voice line
                self.sounds.play_sound("plank_swabbie")
                swabbie_alert_last_played = pygame.time.get_ticks()
        

    def run(self):
        
        while not self.crashed:

            self.process_events()

            self.chatlogs.update_chatlogs(main)

            if self.chatlogs.new_lines:
                self.chatlogs.process_updated_chatlogs(main)

            if self.looting_active:
                self.calculate_looting_timer()

            elif self.rumble_active:
                self.fray.update_rumble()

            elif self.sf_active and self.configs.mode == "CI": # Only care about this for homus
                self.fray.update_sf()

            

            self.gui.update_gui(main)

            pygame.display.update()
            self.clock.tick(self.configs.fps_cap)




        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()