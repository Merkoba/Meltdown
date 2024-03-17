# Modules
from .config import config
from .snippet import Snippet

# Standard
import re
import tkinter as tk
from tkinter import ttk
from typing import Any


class Output(tk.Text):
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        super().__init__(parent, state="disabled", wrap="word", font=config.get_output_font())
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_debouncer = None
        self.debounce_delay = 200
        self.tab_id = tab_id
        self.snippets = []
        self.pack(fill=tk.BOTH, padx=0, pady=1)
        self.setup()

    def setup(self) -> None:
        from .widgets import widgets
        self.display = widgets.display

        def scroll_up() -> str:
            self.scroll_up()
            return "break"

        def scroll_down() -> str:
            self.scroll_down()
            return "break"

        def home() -> str:
            self.to_top()
            return "break"

        def end() -> str:
            self.to_bottom()
            return "break"

        self.bind("<Button-3>", lambda e: self.display.show_output_menu(e))
        self.bind("<Prior>", lambda e: scroll_up())
        self.bind("<Next>", lambda e: scroll_down())
        self.bind("<KeyPress-Home>", lambda e: home())
        self.bind("<KeyPress-End>", lambda e: end())
        self.bind("<Configure>", lambda e: self.update_size())

        def on_scroll(*args: Any) -> None:
            self.display.check_scroll_buttons()
            self.scrollbar.set(*args)

        self.scrollbar.configure(command=self.yview)
        self.configure(yscrollcommand=on_scroll)
        self.configure(background=config.text_background, foreground=config.text_foreground)
        self.configure(bd=4, highlightthickness=0, relief="flat")

        self.tag_config("name_user", foreground="#87CEEB")
        self.tag_config("name_ai", foreground="#98FB98")

    def set_text(self, text: str) -> None:
        self.configure(state="normal")
        self.delete("1.0", tk.END)
        self.insert("1.0", str(text))
        self.configure(state="disabled")
        self.debounce()

    def insert_text(self, text: str) -> None:
        self.configure(state="normal")
        self.insert(tk.END, str(text))
        self.configure(state="disabled")
        self.debounce()

    def debounce(self) -> None:
        if self.text_debouncer is not None:
            self.after_cancel(self.text_debouncer)

        self.text_debouncer = self.after(self.debounce_delay, lambda: self.format_text())

    def clear_text(self) -> None:
        self.set_text("")

    def to_top(self) -> None:
        self.yview_moveto(0.0)

    def to_bottom(self) -> None:
        self.yview_moveto(1.0)

    def last_character(self) -> str:
        text = self.get("1.0", "end-1c")
        return text[-1] if text else ""

    def text_length(self) -> int:
        return len(self.get("1.0", "end-1c"))

    def select_all(self) -> None:
        self.tag_add("sel", "1.0", tk.END)

    def deselect_all(self) -> None:
        self.tag_remove("sel", "1.0", tk.END)

    def get_text(self) -> str:
        return self.get("1.0", "end-1c").strip()

    def scroll_up(self) -> None:
        self.yview_scroll(-3, "units")

    def scroll_down(self) -> None:
        self.yview_scroll(3, "units")

    def format_text(self):
        text = self.get("1.0", "end-1c")
        pattern = r"```(\w*)\n(.*?)\n```"
        self.configure(state="normal")
        matches = []

        for match in re.finditer(pattern, text, flags=re.DOTALL):
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end))

        for content_start, content_end in reversed(matches):
            start_line_col = self.index_at_char(content_start)
            end_line_col = self.index_at_char(content_end)
            snippet_text = self.get(start_line_col, end_line_col)
            self.delete(f"{start_line_col} - 1 lines", f"{end_line_col} + 1 lines")

            snippet = Snippet(self, snippet_text)
            self.window_create(f"{start_line_col} - 1 lines", window=snippet)
            self.snippets.append(snippet)

        self.configure(state="disabled")

    def index_at_char(self, char_index):
        line_start = 0

        for i, line in enumerate(self.get("1.0", "end-1c").split("\n")):
            line_end = line_start + len(line)

            if line_start <= char_index <= line_end:
                return f"{i + 1}.{char_index - line_start}"

            line_start = line_end + 1

    def update_font(self) -> None:
        self.configure(font=config.get_output_font())

        for snippet in self.snippets:
            snippet.update_font()

    def update_size(self) -> None:
        for snippet in self.snippets:
            snippet.update_size()
