# Standard
from pathlib import Path
from typing import List


class ConfigDefaults:
    name_user = "👽 You"
    name_ai = "😎 Melt"
    max_tokens = 200
    temperature = 0.8
    system = "Respond as gentleman and a scholar who is a bit unhinged"
    top_k = 40
    top_p = 0.95
    model = ""
    context = 0


class Config:
    def __init__(self) -> None:
        self.program = "meltdown"
        self.width = 1000
        self.height = 730
        self.padx = 5
        self.pady = 8
        self.frame_padx = 0
        self.frame_pady = 0
        self.input_width = 11
        self.input_width_small = 6
        self.select_width = 11
        self.dialog_color = "#252933"
        self.font = ("sans", 14)
        self.font_button = ("sans", 10)
        self.frame_number = 0
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.button_background = "#446CA1"
        self.button_foreground = "white"
        self.input_background = "#2B303B"
        self.input_foreground = "white"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.config_file = f"~/.config/{self.program}/config.json"
        self.models_file = f"~/.config/{self.program}/models.json"
        self.logs_dir = f"~/.config/{self.program}/logs/"
        self.config_path = Path(self.config_file).expanduser().resolve()
        self.models_path = Path(self.models_file).expanduser().resolve()
        self.logs_path = Path(self.logs_dir).expanduser().resolve()
        self.models: List[str] = []

        self.model = ConfigDefaults.model
        self.name_user = ConfigDefaults.name_user
        self.name_ai = ConfigDefaults.name_ai
        self.max_tokens = ConfigDefaults.max_tokens
        self.temperature = ConfigDefaults.temperature
        self.system = ConfigDefaults.system
        self.top_k = ConfigDefaults.top_k
        self.top_p = ConfigDefaults.top_p
        self.context = ConfigDefaults.context

        self.intro = [
            "Welcome to Meltdown.",
            "Type a prompt and press Enter to continue.",
            "The specified model will load automatically.",
        ]

        self.saved_configs = [
            "model",
            "name_user",
            "name_ai",
            "max_tokens",
            "temperature",
            "system",
            "top_k",
            "top_p",
            "context",
        ]


config = Config()
