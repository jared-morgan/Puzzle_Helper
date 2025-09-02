# I haven't decided if I will use this yet

from pynput import keyboard
import threading

class KeyListener:
    def __init__(self):
        self.listener = None
        self.running = False
        self.key_list = []

    def start(self):
        if self.running:
            return  # already listening

        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  # runs in separate thread

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.running = False

    def on_press(self, key):
        try:
            if key.char:  # only regular keys, need to ammend for the keys I choose for homun colours
                self.key_list.append(key.char)
        except AttributeError:
            pass

        if key == keyboard.Key.esc:
            self.stop()


