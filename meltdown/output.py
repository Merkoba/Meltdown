# Modules
from .config import config
from .app import app
from .menus import Menu
from .args import args

# Libraries
import pyperclip  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional


class Output(tk.Text):
    words_menu = Menu()
    words_menu.add(text="Explain", command=lambda: Output.explain_words())
    words_menu.add(text="Search", command=lambda: Output.search_words())
    current_output: Optional["Output"] = None
    words = ""

    @staticmethod
    def get_words() -> str:
        return Output.words.strip()

    @staticmethod
    def explain_words() -> None:
        from .model import model

        if not Output.current_output:
            return

        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        query = f"What is '{text}' ?"
        tab_id = Output.current_output.tab_id
        model.stream(query, tab_id)

    @staticmethod
    def search_words() -> None:
        import webbrowser
        import urllib.parse

        if not Output.current_output:
            return

        from .dialogs import Dialog
        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        def action() -> None:
            base_url = "https://www.google.com/search?"
            query_params = {"q": text}
            url = base_url + urllib.parse.urlencode(query_params)
            webbrowser.open_new_tab(url)

        Dialog.show_confirm("Search for this term?", lambda: action())

    @staticmethod
    def open_url(url: str) -> None:
        import webbrowser
        from .dialogs import Dialog

        def action() -> None:
            webbrowser.open_new_tab(url)

        Dialog.show_confirm("Open this URL??", lambda: action())

    @staticmethod
    def get_prompt(who: str) -> str:
        name = getattr(config, f"name_{who}")

        if args.avatars:
            avatar = getattr(config, f"avatar_{who}")

            if name:
                prompt = f"\n{avatar} {name} : "
            else:
                prompt = f"\n{avatar} : "
        else:
            if name:
                prompt = f"\n{name} : "
            else:
                prompt = "\nAnon : "

        return prompt

    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        from .snippet import Snippet
        super().__init__(parent, state="disabled", wrap="word", font=config.get_output_font())
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_scroll = True
        self.position = "1.0"

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)
        self.grid(row=0, column=0, sticky="nsew", padx=0, pady=1)

        if args.scrollbars:
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.setup()

    def setup(self) -> None:
        from .widgets import widgets
        from .markdown import Markdown
        self.display = widgets.display
        self.markdown = Markdown(self)

        def on_tag_click(event: Any) -> None:
            self.show_words_menu(event)

        tags = ("bold", "italic", "highlight")

        for tag in tags:
            self.tag_bind(tag, "<ButtonRelease-1>", lambda e: on_tag_click(e))

        def on_url_click(event: Any) -> None:
            text = self.get_tagwords("url", event)

            if text:
                self.open_url(text)

        self.tag_bind("url", "<ButtonRelease-1>", lambda e: on_url_click(e))
        self.bind("<Motion>", lambda e: self.on_motion(e))

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

        self.bind("<ButtonRelease-3>", lambda e: self.show_words_menu(e))
        self.bind("<Button-1>", lambda e: self.deselect_all())
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

        if args.colors:
            self.tag_config("name_user", foreground="#87CEEB")
            self.tag_config("name_ai", foreground="#98FB98")

        self.tag_config("highlight", underline=True)
        self.tag_config("url", underline=True)
        self.tag_config("bold", font=config.get_bold_font())
        self.tag_config("italic", font=config.get_italic_font())

    def set_text(self, text: str) -> None:
        self.enable()
        self.delete("1.0", tk.END)
        self.insert("1.0", str(text))
        self.disable()

    def insert_text(self, text: str, format_text: bool = False, complete: bool = False) -> None:
        self.enable()
        self.insert(tk.END, text)

        if format_text:
            if complete:
                self.format_text(True)
            else:
                checks = ("`", ":")

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
        self.display.check_scroll_buttons(instant=True)

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

        self.check_scroll()

    def scroll_down(self, check: bool = False) -> None:
        fraction = self.get_fraction()
        self.yview_moveto(self.yview()[0] + fraction)

        if check:
            self.check_autoscroll("down")

        self.check_scroll()

    def check_scroll(self) -> None:
        self.display.check_scroll_buttons(instant=True)

    def get_tab(self) -> Optional[Any]:
        return self.display.get_tab(self.tab_id)

    def format_text(self, complete: bool = False, from_start: bool = False) -> None:
        self.enable()
        position = "1.0" if from_start else self.position
        self.markdown.format(complete, position)
        self.disable()
        app.update()
        self.to_bottom(True)

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
        if self.cget("state") != "normal":
            self.configure(state="normal")

    def disable(self) -> None:
        if self.cget("state") != "disabled":
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
        self.position = self.index("end")

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

    def get_tagwords(self, tag: str, event: Any) -> str:
        adjacent = self.tag_prevrange(tag, event.widget.index(tk.CURRENT))

        if not adjacent:
            adjacent = self.tag_nextrange(tag, event.widget.index(tk.CURRENT))

        if len(adjacent) == 2:
            text = self.get(*adjacent)

            if text:
                return text

        return ""

    def get_selected_text(self) -> str:
        try:
            start = self.index(tk.SEL_FIRST)
            end = self.index(tk.SEL_LAST)
            selected_text = self.get(start, end)
            return selected_text
        except tk.TclError:
            return ""

    def show_words_menu(self, event: Any) -> None:
        Output.current_output = self
        seltext = self.get_selected_text()

        if not seltext:
            for snippet in self.snippets:
                seltext = snippet.get_selected_text()

                if seltext:
                    break

        if seltext:
            Output.words = seltext

        if Output.words:
            Output.words_menu.show(event)

    def on_motion(self, event: Any) -> None:
        current_index = self.index(tk.CURRENT)
        tags = self.tag_names(current_index)

        if tags:
            Output.words = self.get_tagwords(tags[0], event).strip()
            self.config(cursor="hand2")
        else:
            Output.words = self.get(f"{current_index} wordstart", f"{current_index} wordend")
            self.config(cursor="xterm")
