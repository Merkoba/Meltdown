# Standard
from pathlib import Path
import tkinter as tk
import json


class Config:
    def __init__(self):
        self.program = "meltdown"
        self.app: tk.Frame = None
        self.width = 960
        self.height = 730
        self.padx = 5
        self.pady = 10
        self.frame_padx = 0
        self.frame_pady = 0
        self.font_size = 14
        self.font_size_button = 10
        self.font_family = "sans"
        self.text_width = 60
        self.select_width = 110
        self.bigger_width = 110
        self.path_width = 150
        self.dialog_color = "#252933"
        self.font = None
        self.font_button = None
        self.frame_number = 0
        self.root = None
        self.model = ""
        self.name_1 = "👽 You"
        self.name_2 = "😎 Melt"
        self.max_tokens = 180
        self.temperature = 0.8
        self.system = "You are a gentleman and a scholar who is a bit unhinged"
        self.model_loaded = False
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.button_background = "#446CA1"
        self.button_foreground = "white"
        self.input_background = "#2B303B"
        self.input_foreground = "white"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.config_file = f"~/.config/{self.program}/config.json"
        self.saved_configs = [
            "model",
            "name_1",
            "name_2",
            "max_tokens",
            "temperature",
            "system",
        ]

    def prepare(self, main_file: str) -> None:
        self.root = Path(main_file).parent.parent
        self.app = tk.Tk()
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(3, weight=1)
        self.font = (self.font_family, self.font_size)
        self.font_button = (self.font_family, self.font_size_button)
        self.config_path = Path(self.config_file).expanduser().resolve()

        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.touch(exist_ok=True)

        with open(self.config_path, "r") as file:
            try:
                conf = json.load(file)
            except BaseException:
                conf = {}

            for key in self.saved_configs:
                setattr(self, key, conf.get(key, getattr(self, key)))

    def save_config(self) -> None:
        import action
        conf = {}

        for key in self.saved_configs:
            conf[key] = getattr(self, key)

        with open(self.config_path, "w") as file:
            json.dump(conf, file, indent=4)

        action.output("Config saved")

    def update_name_1(self) -> None:
        name_1 = self.name_1_text.get()

        if name_1 and (name_1 != self.name_1):
            self.name_1 = name_1
            self.save_config()

    def update_name_2(self) -> None:
        name_2 = self.name_2_text.get()

        if name_2 and (name_2 != self.name_2):
            self.name_2 = name_2
            self.save_config()

    def update_max_tokens(self) -> None:
        max_tokens = self.max_tokens_text.get()

        try:
            max_tokens = int(max_tokens)
        except BaseException:
            return

        if max_tokens and (max_tokens != self.max_tokens):
            self.max_tokens = max_tokens
            self.save_config()

    def update_temperature(self) -> None:
        temperature = self.temperature_text.get()

        try:
            temperature = float(temperature)
        except BaseException:
            return

        if temperature and (temperature != self.temperature):
            self.temperature = temperature
            self.save_config()

    def update_system(self) -> None:
        system = self.system_text.get()

        if system and (system != self.system):
            self.system = system
            self.save_config()

    def update_model(self) -> None:
        model = self.model_text.get()

        if model and (model != self.model):
            self.model = model
            self.save_config()


config = Config()
