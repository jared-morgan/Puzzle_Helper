import pygame
from pathlib import Path
import os
import io
import timeit

from code.gui import GUI
from code.sounds import Sounds
from code.configs import Configs

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

        self.mode = "CI"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True
       
            

    def run(self):
        
        while not self.crashed:

            self.handle_events()

            self.gui.update_gui()

            pygame.display.update()
            self.clock.tick(self.configs.fps_cap)




        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()