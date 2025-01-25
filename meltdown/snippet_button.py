# Standard
import tkinter as tk

# Modules
from .app import app


class SnippetButton(tk.Label):
    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent, text=text)

        font_header = app.theme.get_output_font(True)
        header_fg = app.theme.snippet_header_foreground
        header_bg = app.theme.snippet_header_background

        self.configure(font=font_header)
        self.configure(cursor="hand2")
        self.pack(side=tk.RIGHT, padx=5)
        self.configure(foreground=header_fg)
        self.configure(background=header_bg)
