# Modules
from .config import config

# Standard
import tkinter as tk
from typing import Any

class Snippet(tk.Text):
    def __init__(self, parent: tk.Text, text: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.configure(parent, state="normal")
        self.delete("1.0", tk.END)
        self.insert("1.0", text)
        self.configure(state="disabled")
        num_lines = int(self.index("end-1c").split(".")[0])
        self.configure(height=num_lines)
        self.configure(background=config.snippet_background)
        self.configure(foreground=config.snippet_foreground)
        self.configure(font=config.get_snippet_font())

    def update_font(self) -> None:
        pass
