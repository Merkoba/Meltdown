# Modules
from .config import config

# Standard
import tkinter as tk
from typing import Any

class Snippet(tk.Text):
    def __init__(self, parent: tk.Text, text: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.parent = parent
        self.configure(parent, state="normal")
        self.delete("1.0", tk.END)
        self.insert("1.0", text)
        self.configure(state="disabled")
        num_lines = int(self.index("end-1c").split(".")[0])
        self.configure(height=num_lines)
        self.configure(background=config.snippet_background)
        self.configure(foreground=config.snippet_foreground)
        self.configure(font=config.get_snippet_font())
        self.update_size()

        def scroll_up() -> str:
            self.parent.scroll_up()
            return "break"

        def scroll_down() -> str:
            self.parent.scroll_down()
            return "break"

        self.bind("<Button-4>", lambda e: scroll_up())
        self.bind("<Button-5>", lambda e: scroll_down())

    def update_size(self) -> None:
        char_width = self.tk.call("font", "measure", self.cget("font"), "0")
        width_pixels = self.parent.winfo_width() - self.parent.scrollbar.winfo_width()
        width_pixels = width_pixels * 0.98
        width_chars = int(width_pixels / char_width)
        self.configure(width=width_chars)

    def update_font(self) -> None:
        self.configure(font=config.get_snippet_font())
