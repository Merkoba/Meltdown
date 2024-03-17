# Modules
from .config import config

# Standard
import re
import tkinter as tk
from tkinter import ttk
from typing import Any


class Output(tk.Text):
    def __init__(self, parent: tk.Frame, **kwargs: Any) -> None:
        super().__init__(parent, state="disabled", **kwargs)
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup(self, tab_id: str) -> None:
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
        self.bind("<Button-4>", lambda e: self.display.on_output_scroll(tab_id, "up"))
        self.bind("<Button-5>", lambda e: self.display.on_output_scroll(tab_id, "down"))
        self.bind("<Prior>", lambda e: scroll_up())
        self.bind("<Next>", lambda e: scroll_down())
        self.bind("<KeyPress-Home>", lambda e: home())
        self.bind("<KeyPress-End>", lambda e: end())

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

    def insert_text(self, text: str) -> None:
        self.configure(state="normal")
        self.insert(tk.END, str(text))
        self.configure(state="disabled")

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

    def markdown(self) -> None:
        text = self.get("1.0", "end-1c")

        if not text:
            return

        lines = text.split("\n")
        start_index = 1

        while True:
            start_pos = text.find("```", start_index)

            if start_pos == -1:
                break

            end_pos = text.find("```", start_pos + 3)

            if end_pos == -1:
                break

            # Convert character positions to line and column positions
            start_line_col = self.index_at_char(start_pos)
            end_line_col = self.index_at_char(end_pos)

            self.tag_add("code", f"{start_line_col}+3c", f"{end_line_col}")
            start_index = end_pos + 3

    def format_text(self):
        text = self.get("1.0", "end-1c")
        pattern = r"```(\w*)\n(.*?)\n```"
        self.configure(state="normal")
        sep = "-----------------------------"
        matches = []

        for match in re.finditer(pattern, text, flags=re.DOTALL):
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end))

        for content_start, content_end in reversed(matches):
            start_line_col = self.index_at_char(content_start)
            end_line_col = self.index_at_char(content_end)
            self.delete(f"{start_line_col} - 1 line linestart", f"{start_line_col} - 1 line lineend")
            self.delete(f"{end_line_col} + 1 line linestart", f"{end_line_col} + 1 line lineend")

            code_text = self.get(start_line_col, end_line_col)
            self.delete(start_line_col, end_line_col)
            subtext = tk.Text(self)
            self.window_create(start_line_col, window=subtext)
            subtext.configure(state="normal")
            subtext.delete("1.0", tk.END)
            subtext.insert("1.0", code_text)
            subtext.configure(state="disabled")
            num_lines = int(subtext.index("end-1c").split(".")[0])
            subtext.configure(height=num_lines)

        self.configure(state="disabled")

    def index_at_char(self, char_index):
        line_start = 0

        for i, line in enumerate(self.get("1.0", "end-1c").split("\n")):
            line_end = line_start + len(line)

            if line_start <= char_index <= line_end:
                return f"{i + 1}.{char_index - line_start}"

            line_start = line_end + 1