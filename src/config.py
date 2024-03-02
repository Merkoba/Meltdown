# Standard
from pathlib import Path
import tkinter as tk


class Config:
    def __init__(self):
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
        self.model = "/media/storage3/models/phi-2.Q5_K_M.gguf"
        self.name_1 = "👽 You"
        self.name_2 = "😎 Melt"
        self.max_tokens = 180
        self.temperature = 0.8
        self.system = "You are the situation"
        self.model_loaded = False
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.button_background = "#446CA1"
        self.button_foreground = "white"
        self.input_background = "#2B303B"
        self.input_foreground = "white"
        self.text_background = "#2B303B"
        self.text_foreground = "white"

    def prepare(self, main_file: str) -> None:
        self.root = Path(main_file).parent.parent
        self.app = tk.Tk()
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(3, weight=1)
        self.font = (self.font_family, self.font_size)
        self.font_button = (self.font_family, self.font_size_button)


config = Config()
