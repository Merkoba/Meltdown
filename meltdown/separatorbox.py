# Standard
import tkinter as tk

# Modules
from .app import app


class SeparatorBox(tk.Frame):
    def __init__(
        self, parent: tk.Widget, background: str, padx: int, pady: int
    ) -> None:
        super().__init__(parent, background=background)
        line = tk.Frame(self, height=1, background=app.theme.separator_color)
        line.pack(fill="x", padx=padx, pady=pady)
