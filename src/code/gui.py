from pathlib import Path
import pygame

class GUI:
    def __init__(self, src_path: Path):

        self.colours = {"black": (31, 31, 31),
                        "white": (255, 255, 255),
                        "blue": (0, 0, 102),
                        "grey": (160, 160, 160),
                        "yellow": (255, 255, 84),
                        "gold": (235, 161, 52),
                        "red": (255, 0, 0),
                        }


        Roboto_regular = src_path / Path("media", "cmuntt.ttf")
        self.my_font_84 = pygame.font.Font(Roboto_regular, 84)
        self.my_font_48 = pygame.font.Font(Roboto_regular, 48)
        self.my_font_32 = pygame.font.Font(Roboto_regular, 32)
        self.my_font_22 = pygame.font.Font(Roboto_regular, 22)

        mode_list = ["CI", "VL", "WW", "EV"]
        self.modes = {}
        for mode in mode_list:
            self.modes[mode] = self.my_font_32.render(mode, True, self.colours["grey"])

        self.looting_timer = self.my_font_84.render("0", True, self.colours["white"])
        
        plank_swabbie_text = self.my_font_32.render("Plank Swabbie!", True, self.colours["white"])
        

    def update_mode_text(self, new_mode):
        for mode in self.modes.keys():
            colour = self.colours["white"] if mode == new_mode else self.colours["grey"]
            self.modes[mode] = self.my_font_32.render(mode, True, colour)


    def update_gui(self, main):
        mode_x_offset = 30
        mode_x = 0
        for mode in self.modes.values():
            main.pygame_display.blit(mode, (mode_x, 0))
            mode_x += mode_x_offset
        if main.looting_active:
            main.pygame_display.blit(self.looting_timer, (0, 50))
        if main.plank_swabbie:
            main.pygame_display.blit(self.plank_swabbie_text, (30, 0))

    
    def update_time_passed_text(self, main, time_passed):
        time_passed = str(round(time_passed / 1000, main.configs.timer_decimals))
        self.looting_timer = self.my_font_84.render(time_passed, True, self.colours["white"])


    def update_plank_swabbie_text(self, main, plank_swabbie_colour):
        colour = self.colours["white"] if plank_swabbie_colour else self.colours["red"]
        self.plank_swabbie_text = self.my_font_32.render("Plank Swabbie!", True, colour)