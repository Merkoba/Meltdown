# Standard
from pathlib import Path
import tkinter as tk
from typing import List


class ConfigDefaults:
    name_1 = "👽 You"
    name_2 = "😎 Melt"
    max_tokens = 180
    temperature = 0.8
    system = "Respond as gentleman and a scholar who is a bit unhinged"
    top_k = 40
    top_p = 0.95
    model = ""


class Config:
    def __init__(self) -> None:
        self.program = "meltdown"
        self.app = tk.Tk()
        self.width = 960
        self.height = 730
        self.padx = 5
        self.pady = 10
        self.frame_padx = 0
        self.frame_pady = 0
        self.input_width = 11
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
        self.config_path = Path(self.config_file).expanduser().resolve()
        self.models_path = Path(self.models_file).expanduser().resolve()
        self.models: List[str] = []

        self.model = ConfigDefaults.model
        self.name_1 = ConfigDefaults.name_1
        self.name_2 = ConfigDefaults.name_2
        self.max_tokens = ConfigDefaults.max_tokens
        self.temperature = ConfigDefaults.temperature
        self.system = ConfigDefaults.system
        self.top_k = ConfigDefaults.top_k
        self.top_p = ConfigDefaults.top_p
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(3, weight=1)


config = Config()
