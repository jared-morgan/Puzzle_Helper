import pygame
from pathlib import Path

class Sounds:
    def __init__(self, src_path: Path):
        self.sounds = {"trade_chat_sound": pygame.mixer.Sound(src_path / Path("media", "trade_chat_sound.ogg")),
                       "plank_swabbie": pygame.mixer.Sound(src_path / Path("media", "plank_swabbie.mp3")),
                       "warning": pygame.mixer.Sound(src_path / Path("media", "warning.ogg"))
                       }
        

def play_sound(self, sound: str):
    try:
        if sound in self.sounds:
            pygame.mixer.Sound.play(self.sounds[sound])
    except Exception as e:
        print(e)


def set_volume(self, volume: int):
    try:
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)
    except Exception as e:
        print(e)
    