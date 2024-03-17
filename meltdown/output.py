# Modules
from .config import config
from .app import app

# Libraries
import pyperclip  # type: ignore

# Standard
import re
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional


class Output(tk.Text):
    @staticmethod
    def get_prompt(who: str) -> str:
        avatar = getattr(config, f"avatar_{who}")
        name = getattr(config, f"name_{who}")

        if name:
            prompt = f"\n{avatar} {name} : "
        else:
            prompt = f"\n{avatar} : "

        return prompt

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
        self.position = "1.0"
        self.pack(fill=tk.BOTH, expand=True, padx=0, pady=1)
        self.tag_config("highlight", background=config.highlight_background,
                        foreground=config.highlight_foreground)
        self.setup()

    def setup(self) -> None:
        from .widgets import widgets
        self.display = widgets.display

        def scroll_up() -> str:
            self.scroll_up(True)
            return "break"

        def scroll_down() -> str:
            self.scroll_down(True)
            return "break"

        def home() -> str:
            self.to_top()
            return "break"

        def end() -> str:
            self.to_bottom()
            return "break"

        self.bind("<Button-1>", lambda e: self.deselect_all())
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

        if "`" in last_line:
            highlights = re.findall(r"`([^`]+)`", last_line)
        else:
            highlights = []

        self.insert(tk.END, text)

        if last_line == "```\n":
            self.format_text()
        elif highlights:
            self.format_text()

        self.disable()
        self.to_bottom(True)
        self.debounce_format()

    def debounce_format(self) -> None:
        self.cancel_format_debouncer()
        self.format_debouncer = self.after(self.format_debouncer_delay, lambda: self.format_text())

    def cancel_format_debouncer(self) -> None:
        if self.format_debouncer is not None:
            self.after_cancel(self.format_debouncer)
            self.format_debouncer = None

    def clear_text(self) -> None:
        self.set_text("")

    def to_top(self) -> None:
        self.auto_scroll = False
        self.yview_moveto(0.0)

    def to_bottom(self, check: bool = False) -> None:
        if check and (not self.auto_scroll):
            return

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

        for snippet in self.snippets:
            snippet.deselect_all()

    def get_text(self) -> str:
        return self.get("1.0", "end-1c").strip()

    def scroll_up(self, check: bool = False) -> None:
        self.yview_scroll(-2, "units")

        if check:
            self.check_autoscroll("up")

    def scroll_down(self, check: bool = False) -> None:
        self.yview_scroll(2, "units")

        if check:
            self.check_autoscroll("down")

    def get_tab(self) -> Optional[Any]:
        return self.display.get_tab(self.tab_id)

    def format_text(self) -> None:
        self.cancel_format_debouncer()

        self.enable()
        self.format_snippets()
        self.format_backticks()
        self.disable()

        app.update()
        self.to_bottom(True)

    def format_snippets(self) -> None:
        from .snippet import Snippet
        start_index = self.position
        text = self.get(start_index, "end-1c")
        pattern = r"^```([\w#]*)\n(.*?)\n```$"
        matches = []

        for match in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            language = match.group(1)
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end, language))

        for content_start, content_end, language in reversed(matches):
            start_line_col = self.index_at_char(content_start, start_index)
            end_line_col = self.index_at_char(content_end, start_index)
            snippet_text = self.get(start_line_col, end_line_col)
            self.delete(f"{start_line_col} - 1 lines linestart", f"{end_line_col} + 1 lines lineend")

            snippet = Snippet(self, snippet_text, language)
            self.window_create(f"{start_line_col} - 1 lines", window=snippet)
            self.snippets.append(snippet)

    def format_backticks(self) -> None:
        start_index = self.position

        while True:
            start_index = self.search("`", start_index, "end")

            if not start_index:
                break

            if self.get(start_index + "+1c") == "`":
                start_index += "+2c"
                continue
            end_index = self.search("`", start_index + "+1c", "end")

            if not end_index:
                break

            if self.get(end_index + "+1c") == "`":
                start_index = end_index + "+2c"
                continue

            self.tag_add("highlight", start_index, end_index + "+1c")
            self.tag_lower("highlight")

            self.delete(start_index, start_index + "+1c")
            end_index = end_index + "-1c"
            self.delete(end_index, end_index + "+1c")

            start_index = end_index + "+1c"

    def index_at_char(self, char_index: int, start_index: str) -> str:
        o_line = int(start_index.split(".")[0])
        line_start = 0

        for i, line in enumerate(self.get(start_index, "end-1c").split("\n")):
            line_end = line_start + len(line)

            if line_start <= char_index <= line_end:
                return f"{i + o_line}.{char_index - line_start}"

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

    def copy_all(self) -> None:
        text = self.to_log()

        if not text:
            return

        pyperclip.copy(text)

    def to_log(self) -> str:
        from .session import session
        tab = self.display.get_tab(self.tab_id)

        if not tab:
            return ""

        document = session.get_document(tab.document_id)

        if not document:
            return ""

        return document.to_log()

    def update_position(self) -> None:
        self.position = self.index(tk.INSERT)

    def prompt(self, who: str) -> None:
        prompt = Output.get_prompt(who)
        self.print(prompt, False)
        start_index = self.index(f"end - {len(prompt)}c")
        end_index = self.index("end - 3c")
        self.tag_add(f"name_{who}", start_index, end_index)
        self.update_position()

    def print(self, text: str, linebreak: bool = False) -> None:
        left = ""
        right = ""

        if self.text_length() and (self.last_character() != "\n"):
            left = "\n"

        if linebreak:
            right = "\n"

        text = left + text + right
        self.insert_text(text)
        self.to_bottom()
