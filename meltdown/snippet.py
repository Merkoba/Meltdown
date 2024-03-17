# Modules
from .config import config
from .output import Output

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any


class Snippet(tk.Frame):
    def __init__(self, parent: Output, text: str) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0)
        self.parent = parent
        self.scrollbar = ttk.Scrollbar(self, style="Normal.Horizontal.TScrollbar", orient=tk.HORIZONTAL)

        self.text = tk.Text(self)
        self.text.configure(wrap="none")
        self.text.configure(state="normal")
        self.text.configure(borderwidth=0)
        self.text.configure(highlightthickness=1)
        self.text.configure(highlightbackground=config.snippet_border)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.text.configure(state="disabled")
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text.configure(xscrollcommand=self.scrollbar.set)
        num_lines = int(self.text.index("end-1c").split(".")[0])
        self.text.configure(height=num_lines)
        self.text.configure(background=config.snippet_background)
        self.text.configure(foreground=config.snippet_foreground)
        self.text.configure(font=config.get_snippet_font())
        self.scrollbar.configure(command=self.text.xview)
        self.update_size()

        def scroll_up(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_left()
            else:
                self.parent.scroll_up()

            return "break"

        def scroll_down(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_right()
            else:
                self.parent.scroll_down()

            return "break"

        self.text.bind("<Button-4>", lambda e: scroll_up(e))
        self.text.bind("<Button-5>", lambda e: scroll_down(e))

    def update_size(self) -> None:
        char_width = self.text.tk.call("font", "measure", self.text.cget("font"), "0")
        width_pixels = self.parent.winfo_width() - self.parent.scrollbar.winfo_width()
        width_pixels = int(width_pixels * 0.98)
        width_chars = int(width_pixels / char_width)
        self.text.configure(width=width_chars)

    def update_font(self) -> None:
        self.text.configure(font=config.get_snippet_font())

    def scroll_left(self) -> None:
        self.text.xview_scroll(-2, "units")

    def scroll_right(self) -> None:
        self.text.xview_scroll(2, "units")
