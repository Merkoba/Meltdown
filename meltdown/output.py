# Modules
from .config import config
from .app import app

# Standard
import re
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional


class Output(tk.Text):
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        from .snippet import Snippet
        super().__init__(parent, state="disabled", wrap="word", font=config.get_output_font())
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.format_debouncer: Optional[str] = None
        self.format_debouncer_delay = 500
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_scroll = True
        self.pack(fill=tk.BOTH, expand=True, padx=0, pady=1)
        self.tag_config("highlight", background=config.highlight_background,
                        foreground=config.highlight_foreground)
        self.setup()

    def setup(self) -> None:
        from .widgets import widgets
        self.display = widgets.display

        def scroll_up() -> str:
            self.scroll_up()
            self.check_autoscroll("up")
            return "break"

        def scroll_down() -> str:
            self.scroll_down()
            self.check_autoscroll("down")
            return "break"

        def home() -> str:
            self.to_top()
            return "break"

        def end() -> str:
            self.to_bottom()
            return "break"

        self.bind("<Button-3>", lambda e: self.display.show_output_menu(e))
        self.bind("<Button-4>", lambda e: scroll_up())
        self.bind("<Button-5>", lambda e: scroll_down())
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
        self.enable()
        self.delete("1.0", tk.END)
        self.insert("1.0", str(text))
        self.disable()
        self.debounce_format()

    def insert_text(self, text: str) -> None:
        self.enable()
        last_line = self.get("end-2l", "end-1c")
        self.insert(tk.END, str(text))

        if last_line == "```\n":
            self.format_text()

        self.disable()

        if self.auto_scroll:
            self.to_bottom()

        self.debounce_format()

    def debounce_format(self) -> None:
        self.cancel_format_debouncer()

        def action() -> None:
            self.format_text()

        self.format_debouncer = self.after(self.format_debouncer_delay, lambda: action())

    def cancel_format_debouncer(self) -> None:
        if self.format_debouncer is not None:
            self.after_cancel(self.format_debouncer)
            self.format_debouncer = None

    def clear_text(self) -> None:
        self.set_text("")

    def to_top(self) -> None:
        self.auto_scroll = False
        self.yview_moveto(0.0)

    def to_bottom(self) -> None:
        self.auto_scroll = True
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
        self.yview_scroll(-2, "units")

    def scroll_down(self) -> None:
        self.yview_scroll(2, "units")

    def format_text(self) -> None:
        self.cancel_format_debouncer()
        self.format_snippets()
        self.format_backticks()

    def format_snippets(self) -> None:
        from .snippet import Snippet
        text = self.get("1.0", "end-1c")
        pattern = r"```(\w*)\n(.*?)\n```"
        self.enable()
        matches = []

        for match in re.finditer(pattern, text, flags=re.DOTALL):
            language = match.group(1)
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end, language))

        for content_start, content_end, language in reversed(matches):
            start_line_col = self.index_at_char(content_start)
            end_line_col = self.index_at_char(content_end)
            snippet_text = self.get(start_line_col, end_line_col)
            self.delete(f"{start_line_col} - 1 lines linestart", f"{end_line_col} + 1 lines lineend")

            snippet = Snippet(self, snippet_text, language)
            self.window_create(f"{start_line_col} - 1 lines", window=snippet)
            self.snippets.append(snippet)

        self.disable()
        app.update()
        self.to_bottom()

    def format_backticks(self) -> None:
        self.enable()
        start_index = "1.0"

        while True:
            # Find the start and end indices of the next occurrence of text enclosed in backticks
            start_index = self.search("`", start_index, "end")
            if not start_index:
                break
            # Check if the next character is also a backtick
            if self.get(start_index + "+1c") == "`":
                start_index += "+2c"
                continue
            end_index = self.search("`", start_index + "+1c", "end")

            # If the end index is not found, break the loop
            if not end_index:
                break

            # Check if the character after the end index is also a backtick
            if self.get(end_index + "+1c") == "`":
                start_index = end_index + "+2c"
                continue

            # Add the "highlight" tag to the found occurrence
            self.tag_add("highlight", start_index, end_index + "+1c")
            self.tag_lower("highlight")

            # Remove the backticks
            self.delete(start_index, start_index + "+1c")
            end_index = end_index + "-1c"
            self.delete(end_index, end_index + "+1c")

            # Update the start index for the next search
            start_index = end_index + "+1c"

        self.disable()

    def index_at_char(self, char_index: int) -> str:
        line_start = 0

        for i, line in enumerate(self.get("1.0", "end-1c").split("\n")):
            line_end = line_start + len(line)

            if line_start <= char_index <= line_end:
                return f"{i + 1}.{char_index - line_start}"

            line_start = line_end + 1

        return ""

    def update_font(self) -> None:
        self.configure(font=config.get_output_font())

        for snippet in self.snippets:
            snippet.update_font()

    def update_size(self) -> None:
        for snippet in self.snippets:
            snippet.update_size()

    def check_autoscroll(self, direction: str) -> None:
        if direction == "up":
            self.auto_scroll = False
        elif direction == "down":
            if self.yview()[1] >= 1.0:
                self.auto_scroll = True

    def enable(self) -> None:
        self.configure(state="normal")

    def disable(self) -> None:
        self.configure(state="disabled")
