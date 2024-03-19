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
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_scroll = True
        self.position = "1.0"
        self.pack(fill=tk.BOTH, expand=True, padx=0, pady=1)
        self.tag_config("highlight", underline=True)
        self.tag_config("url", underline=True)

        def on_highlight_click(event: Any) -> None:
            text = self.get_tagwords("highlight", event)

            if text:
                self.search_text(text)

        self.tag_bind("highlight", "<ButtonRelease-1>", lambda e: on_highlight_click(e))

        def on_url_click(event: Any) -> None:
            text = self.get_tagwords("url", event)

            if text:
                self.open_url(text)

        self.tag_bind("url", "<ButtonRelease-1>", lambda e: on_url_click(e))

        def on_motion(event: Any) -> None:
            current_index = self.index(tk.CURRENT)
            # word = self.get(f"{current_index} wordstart", f"{current_index} wordend")
            tags = self.tag_names(current_index)
            if "highlight" in tags:
                self.config(cursor="hand2")
            if "url" in tags:
                self.config(cursor="hand2")
            else:
                self.config(cursor="xterm")

        self.bind("<Motion>", on_motion)
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

    def insert_text(self, text: str, complete: bool = False) -> None:
        self.enable()
        self.insert(tk.END, text)

        if complete:
            self.format_text(True)
        else:
            checks = (" ", "\n")

            if text in checks:
                self.format_text()

        self.disable()
        self.to_bottom(True)

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

    def get_fraction(self, num_lines: int = 1) -> float:
        total_lines = self.count("1.0", "end-1c lineend", "displaylines")[0]  # type: ignore
        fraction = float(num_lines / total_lines)
        return fraction

    def scroll_up(self, check: bool = False) -> None:
        fraction = self.get_fraction()
        self.yview_moveto(self.yview()[0] - fraction)

        if check:
            self.check_autoscroll("up")

    def scroll_down(self, check: bool = False) -> None:
        fraction = self.get_fraction()
        self.yview_moveto(self.yview()[0] + fraction)

        if check:
            self.check_autoscroll("down")

    def get_tab(self) -> Optional[Any]:
        return self.display.get_tab(self.tab_id)

    def format_text(self, complete: bool = False) -> None:
        self.enable()
        self.format_snippets(complete)
        self.format_highlights(complete)
        self.format_urls(complete)
        self.disable()

        app.update()
        self.to_bottom(True)

    def format_snippets(self, complete: bool) -> None:
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

    def format_highlights(self, complete: bool) -> None:
        start_index = self.position
        text = self.get(start_index, "end-1c")
        backtick = "`"
        result = ""
        code_string = ""
        in_code = False
        matches = []
        index_start = 0
        last = len(text) - 1

        def ended(i: int) -> bool:
            if complete:
                return i == last
            else:
                return False

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            in_code = False
            code_string = ""

        def rollback() -> None:
            nonlocal result
            result += backtick + code_string

        for i, char in enumerate(text):
            if char == backtick:
                prev_char = text[i - 1] if (i - 1) >= 0 else None
                next_char = text[i + 1] if (i + 1) < len(text) else None

                if in_code:
                    matches.append((index_start, i))
                    reset_code()
                elif (prev_char != backtick) and (next_char != backtick):
                    reset_code()
                    in_code = True
                    index_start = i
            else:
                if char == "\n" or ended(i):
                    if in_code:
                        rollback()
                        reset_code()

                    result += char
                else:
                    if in_code:
                        code_string += char
                    else:
                        result += char

        if matches:
            for start, end in reversed(matches):
                start_line_col = self.index_at_char(start, start_index)
                end_line_col = self.index_at_char(end, start_index)
                clean_text = self.get(f"{start_line_col} + 1c", f"{end_line_col}")
                self.delete(start_line_col, f"{end_line_col} + 1c")
                self.insert(start_line_col, clean_text)
                self.tag_add("highlight", start_line_col, end_line_col)

    def format_urls(self, complete: bool) -> None:
        start_index = self.position
        text = self.get(start_index, "end-1c")
        protocols = ("http://", "https://", "ftp://", "www.")
        stoppers = (" ", "\n")
        matches = []
        last = len(text) - 1
        word = ""

        def ended(i: int) -> bool:
            if complete:
                return i == last
            else:
                return False

        for i, char in enumerate(text):
            if char in stoppers or ended(i):
                end_index = i

                if ended(i):
                    word += char
                    end_index += 1

                if any([word.startswith(protocol) for protocol in protocols]):
                    matches.append((i - len(word), end_index))

                word = ""
            else:
                word += char

        if matches:
            for start, end in reversed(matches):
                start_line_col = self.coords_at_index(start, start_index)
                end_line_col = self.coords_at_index(end, start_index)
                self.tag_add("url", start_line_col, end_line_col)

    def coords_at_index(self, index: int, start_index: str) -> str:
        line, col = map(int, start_index.split("."))
        text = self.get(start_index, "end-1c")

        for i in range(index):
            if i >= len(text):
                break
            elif (text[i] == "\n"):
                line += 1
                col = 0
            else:
                col += 1

        return f"{line}.{col}"

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

    def search_text(self, text: str) -> None:
        import webbrowser
        import urllib.parse
        from .dialogs import Dialog

        def action() -> None:
            base_url = "https://www.google.com/search?"
            query_params = {"q": text}
            url = base_url + urllib.parse.urlencode(query_params)
            webbrowser.open_new_tab(url)

        Dialog.show_confirm("Search for this term?", lambda: action())

    def open_url(self, url: str) -> None:
        import webbrowser
        from .dialogs import Dialog

        def action() -> None:
            webbrowser.open_new_tab(url)

        Dialog.show_confirm("Open this URL??", lambda: action())

    def get_tagwords(self, tag: str, event: Any) -> str:
        adjacent = self.tag_prevrange(tag, event.widget.index(tk.CURRENT))

        if not adjacent:
            adjacent = self.tag_nextrange(tag, event.widget.index(tk.CURRENT))

        if len(adjacent) == 2:
            text = self.get(*adjacent)

            if text:
                return text

        return ""
