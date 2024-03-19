# Modules
from .config import config

# Standard
import tkinter as tk


class SeparatorBox(tk.Frame):
    def __init__(self, parent: tk.Frame, background: str, padx: int, pady: int) -> None:
        super().__init__(parent, background=background)
        line = tk.Frame(self, height=1, bg=config.separator_color)
        line.pack(fill="x", padx=padx, pady=pady)
