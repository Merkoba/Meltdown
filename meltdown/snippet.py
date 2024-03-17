# Modules
from .config import config
from .output import Output

# Libraries
import pyperclip  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any


class Snippet(tk.Frame):
    def __init__(self, parent: Output, content: str, language: str) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0)
        self.content = content

        self.header = tk.Frame(self)
        self.header.configure(background=config.snippet_header_color)

        header_text = f"Language: {language}"
        self.header_text = tk.Label(self.header, text=header_text, font=config.get_snippet_font(True))
        self.header_text.configure(foreground=config.snippet_header_text)
        self.header_text.configure(background=config.snippet_header_color)
        self.header_text.configure(cursor="arrow")
        self.header_text.pack(side=tk.LEFT, padx=5)

        self.header_copy = tk.Label(self.header, text="Copy", font=config.get_snippet_font(True))
        self.header_copy.configure(cursor="hand2")
        self.header_copy.bind("<Button-1>", lambda e: self.copy_all())
        self.header_copy.pack(side=tk.RIGHT, padx=5)
        self.header_copy.configure(foreground=config.snippet_header_text)
        self.header_copy.configure(background=config.snippet_header_color)

        self.header_select = tk.Label(self.header, text="Select", font=config.get_snippet_font(True))
        self.header_select.configure(cursor="hand2")
        self.header_select.bind("<Button-1>", lambda e: self.select_all())
        self.header_select.pack(side=tk.RIGHT, padx=5)
        self.header_select.configure(foreground=config.snippet_header_text)
        self.header_select.configure(background=config.snippet_header_color)

        self.header.pack(side=tk.TOP, fill=tk.X)
        self.text = tk.Text(self, wrap="none", state="normal")
        self.text.configure(borderwidth=0, highlightthickness=0)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", self.content)
        self.text.configure(state="disabled")
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar = ttk.Scrollbar(self, style="Normal.Horizontal.TScrollbar", orient=tk.HORIZONTAL)
        self.scrollbar.configure(cursor="hand2")
        self.text.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(fill=tk.X)
        self.parent = parent

        num_lines = int(self.text.index("end-1c").split(".")[0])
        self.text.configure(height=num_lines)

        self.configure(background=config.snippet_background)
        self.text.configure(background=config.snippet_background)
        self.text.configure(foreground=config.snippet_foreground)
        self.text.configure(font=config.get_snippet_font())

        self.scrollbar.configure(command=self.text.xview)
        self.update_size()

        def scroll_up(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_left()
            else:
                self.parent.scroll_up(True)

            return "break"

        def scroll_down(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_right()
            else:
                self.parent.scroll_down(True)

            return "break"

        def bind_scroll_events(widget: tk.Widget) -> None:
            widget.bind("<Button-4>", lambda e: scroll_up(e))
            widget.bind("<Button-5>", lambda e: scroll_down(e))
            widget.bind("<Button-3>", lambda e: self.parent.display.show_output_menu(e))

            for child in widget.winfo_children():
                bind_scroll_events(child)

        bind_scroll_events(self)

    def update_size(self) -> None:
        char_width = self.text.tk.call("font", "measure", self.text.cget("font"), "0")
        width_pixels = self.parent.winfo_width() - self.parent.scrollbar.winfo_width()
        width_pixels = int(width_pixels * 0.98)
        width_chars = int(width_pixels / char_width)
        self.text.configure(width=width_chars)

    def update_font(self) -> None:
        self.text.configure(font=config.get_snippet_font())
        self.header_text.configure(font=config.get_snippet_font(True))
        self.header_copy.configure(font=config.get_snippet_font(True))
        self.header_select.configure(font=config.get_snippet_font(True))
        self.update_size()

    def scroll_left(self) -> None:
        self.text.xview_scroll(-2, "units")

    def scroll_right(self) -> None:
        self.text.xview_scroll(2, "units")

    def copy_all(self) -> None:
        pyperclip.copy(self.content)
        self.header_copy.configure(text="Copied!")
        self.after(1000, lambda: self.header_copy.configure(text="Copy"))

    def select_all(self) -> None:
        self.text.tag_add("sel", "1.0", tk.END)

    def deselect_all(self) -> None:
        self.text.tag_remove("sel", "1.0", tk.END)
