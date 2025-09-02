from pathlib import Path

class Configs:
    def __init__(self):
        self.configs = {}
        self.fps_cap = 60
        self.file_path = Path(r"C:\Users\Jared\Documents\YPP Chatlogs\Jice_Emerald_x")
        self.name = self.file_path.stem.split("_")[0]
        self.search_strings = {
            # 1: {"channel": "trade", "buy_or_sell": "sell", "strings": ["ci map", "cursed island map", "cursed isles map"], "regex": r"(?=.*\bsell\w*\b)(?=.*\bci\b)"},
            1: {"name": "Buying CI map", "channel": "trade,", "buy_or_sell": "buy", "strings": ["ci map", "cursed island", "cursed isles"], "regex": "", "sound": "trade_chat_sound.ogg"},
            2: {"name": "Buying Vampire Reliq", "channel": "trade,", "buy_or_sell": "buy", "strings": ["reliq", "vamp charm", "v charm", "vampire charm", "vampiric charm", "vampirate charm"], "regex": "", "sound": "trade_chat_sound.ogg"},
            3: {"name": "Buying WWW-Finder", "channel": "trade,", "buy_or_sell": "buy", "strings": ["wayfinder", "way-finder" "wolf charm", "w charm", "ww charm", "werewolf charm", "werewolves charm"], "regex": "", "sound": "trade_chat_sound.ogg"},
            }
        self.chat_filter_on = True
        self.timer_offset = 0
        self.play_swabbie_warning_sound = True
        self.mini_rumble = False
        self.rumble_scaling = 12
        self.rumble_bars_as_natural_width = True
        self.show_drop_off_numbers = True
        self.mode = "CI"
    
    def load_configs(self):
        pass

    def save_configs(self):
        pass