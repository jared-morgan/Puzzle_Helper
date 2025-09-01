import pygame
from pathlib import Path

class Sounds:
    def __init__(self, src_path: Path):
        self.src_path = src_path
        self.sounds = {"trade_chat_sound": "trade_chat_sound.ogg",
                       "plank_swabbie": "plank_swabbie.mp3",
                       "warning": "warning.ogg"
                       }
        self.volume = 1
        

    def play_sound(self, sound_text: str):
        if sound_text in self.sounds:
            sound_text = self.sounds[sound_text]
        try:
            sound_audio = pygame.mixer.Sound(self.src_path / Path("media", sound_text))
            sound_audio.set_volume(self.volume)
            pygame.mixer.Sound.play(sound_audio)
        except Exception as e:
            print(e)


    def set_volume(self, volume: int):
        self.volume = volume
        