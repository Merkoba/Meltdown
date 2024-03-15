# Modules
from .config import config

# Standard
import tkinter as tk


class SeparatorBox(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent, height=1)
        self.configure(background=config.separator_color)
