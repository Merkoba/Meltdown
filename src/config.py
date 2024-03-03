# Standard
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import List


class ConfigDefaults:
    name_user = "👽 You"
    name_ai = "😎 Melt"
    max_tokens = 180
    temperature = 0.8
    system = "Respond as gentleman and a scholar who is a bit unhinged"
    top_k = 40
    top_p = 0.95
    model = ""
    context = 0


class Config:
    def __init__(self) -> None:
        self.program = "meltdown"
        self.app = tk.Tk()
        self.width = 960
        self.height = 730
        self.padx = 5
        self.pady = 8
        self.frame_padx = 0
        self.frame_pady = 0
        self.input_width = 11
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
            "Welcome to Meltdown",
            "Type a prompt and press Enter to continue",
            "The specified model will load automatically",
        ]

        self.app.geometry(f"{self.width}x{self.height}")
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(3, weight=1)

        style = ttk.Style()
        style.configure("TCombobox", foreground="white")
        style.map("TCombobox", fieldbackground=[("readonly", self.button_background)], fieldforeground=[("readonly", "white")])
        style.map("TCombobox", selectbackground=[("readonly", "transparent")], selectforeground=[("readonly", "white")])
        style.configure("TCombobox", borderwidth=0)
        style.configure("TCombobox.Listbox", padding=0)
        self.app.option_add("*TCombobox*Listbox.font", ("sans", 13))


config = Config()
