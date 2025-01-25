# Standard
import tkinter as tk

# Modules
from .app import app


class SnippetLabel(tk.Label):
    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent, text=text)

        font = app.theme.get_output_font(True)
        fg_color = app.theme.snippet_header_foreground
        bg_color = app.theme.snippet_header_background

        self.configure(font=font)
        self.configure(cursor="arrow")
        self.pack(side=tk.LEFT, padx=5)
        self.configure(foreground=fg_color)
        self.configure(background=bg_color)


class SnippetButton(tk.Label):
    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent, text=text)

        font = app.theme.get_output_font(True)
        underline = app.theme.get_output_font(True, True)
        fg_color = app.theme.snippet_header_foreground
        bg_color = app.theme.snippet_header_background

        self.configure(font=font)
        self.configure(cursor="hand2")
        self.pack(side=tk.RIGHT, padx=5)
        self.configure(foreground=fg_color)
        self.configure(background=bg_color)

        def on_enter(e) -> None:
            self.configure(font=underline)

        def on_leave(e) -> None:
            self.configure(font=font)

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
