# Standard
from pathlib import Path
import tkinter as tk
import json


class Config:
    def __init__(self) -> None:
        self.program = "meltdown"
        self.app = None
        self.width = 960
        self.height = 730
        self.padx = 5
        self.pady = 10
        self.frame_padx = 0
        self.frame_pady = 0
        self.font_size = 14
        self.font_size_button = 10
        self.font_family = "sans"
        self.input_width = 11
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
        self.top_k = 40
        self.top_p = 0.95
        self.config_file = f"~/.config/{self.program}/config.json"
        self.models_file = f"~/.config/{self.program}/models.json"
        self.output_text = None
        self.input_text = None
        self.model_text = None
        self.name_1_text = None
        self.name_2_text = None
        self.max_tokens_text = None
        self.temperature_text = None
        self.system_text = None
        self.top_k_text = None
        self.top_p_text = None
        self.models = []
        self.config_path = None
        self.models_path = None
        self.saved_configs = [
            "model",
            "name_1",
            "name_2",
            "max_tokens",
            "temperature",
            "system",
            "top_k",
            "top_p",
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
        self.load_config_file()
        self.load_models_file()

    def load_config_file(self):
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

    def load_models_file(self):
        self.models_path = Path(self.models_file).expanduser().resolve()

        if not self.models_path.exists():
            self.models_path.parent.mkdir(parents=True, exist_ok=True)
            self.models_path.touch(exist_ok=True)

        with open(self.models_path, "r") as file:
            try:
                models = json.load(file)
            except BaseException:
                models = []

                if self.model:
                    models.append(self.model)

            self.models = models

    def save_config(self) -> None:
        import action
        conf = {}

        for key in self.saved_configs:
            conf[key] = getattr(self, key)

        with open(self.config_path, "w") as file:
            json.dump(conf, file, indent=4)

        action.output("Config saved.")

    def save_models(self) -> None:
        import action

        with open(self.models_path, "w") as file:
            json.dump(self.models, file, indent=4)

        action.output("Models saved.")

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
        from model import model
        model_path = self.model_text.get()

        if model_path and (model_path != self.model):
            if model.load(model_path):
                self.model = model_path
                self.save_config()
                self.add_model(model_path)

    def update_top_k(self) -> None:
        top_k = self.top_k_text.get()

        try:
            top_k = int(top_k)
        except BaseException:
            return

        if top_k and (top_k != self.top_k):
            self.top_k = top_k
            self.save_config()

    def update_top_p(self) -> None:
        top_p = self.top_p_text.get()

        try:
            top_p = float(top_p)
        except BaseException:
            return

        if top_p and (top_p != self.top_p):
            self.top_p = top_p
            self.save_config()

    def add_model(self, model_path: str) -> None:
        if model_path not in self.models:
            self.models.append(model_path)
            self.save_models()


config = Config()
