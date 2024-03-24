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
    word_menu = Menu()
    word_menu.add(text="Copy", command=lambda: Output.copy_words())
    word_menu.add(text="Explain", command=lambda: Output.explain_words())
    word_menu.add(text="Search", command=lambda: Output.search_words())
    word_menu.add(text="New", command=lambda: Output.new_tab())
    current_output: Optional["Output"] = None
    words = ""

    @staticmethod
    def get_words() -> str:
        return Output.words.strip()

    @staticmethod
    def copy_words() -> None:
        if not Output.current_output:
            return

        text = Output.get_words()
        Output.current_output.deselect_all()
        pyperclip.copy(text)

    @staticmethod
    def explain_words() -> None:
        from .model import model

        if not Output.current_output:
            return

        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        query = f"What is \"{text}\" ?"
        tab_id = Output.current_output.tab_id
        model.stream(query, tab_id)

    @staticmethod
    def search_words() -> None:
        if not Output.current_output:
            return

        from .dialogs import Dialog
        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        def action() -> None:
            app.search_text(text)

        Dialog.show_confirm("Search for this term?", lambda: action())

    @staticmethod
    def new_tab() -> None:
        from .display import display
        from .model import model
        if not Output.current_output:
            return

        from .dialogs import Dialog
        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        text = f"Tell me about \"{text}\""
        tab_id = display.make_tab()
        model.stream(text, tab_id)

    @staticmethod
    def open_url(url: str) -> None:
        from .dialogs import Dialog

        def action() -> None:
            app.open_url(url)

        Dialog.show_confirm("Open this URL??", lambda: action())

    @staticmethod
    def get_prompt(who: str) -> str:
        name = getattr(config, f"name_{who}")

        if args.avatars:
            avatar = getattr(app.theme, f"avatar_{who}")

            if name:
                prompt = f"{avatar} {name} : "
            else:
                prompt = f"{avatar} : "
        else:
            if name:
                prompt = f"{name} : "
            else:
                prompt = "Anon : "

        return prompt

    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        from .snippet import Snippet
        super().__init__(parent, state="disabled", wrap="word", font=app.theme.get_output_font())
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.configure(cursor="arrow")
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_scroll = True
        self.position = "1.0"
        self.format_text_timer = ""
        self.format_text_delay = 500

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)
        self.grid(row=0, column=0, sticky="nsew", padx=0, pady=1)

        if args.scrollbars:
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.setup()

    def setup(self) -> None:
        from .inputcontrol import inputcontrol
        from .display import display
        from .markdown import Markdown

        self.display = display
        self.markdown = Markdown(self)

        def on_tag_click(event: Any) -> None:
            self.show_word_menu(event)

        tags = ("bold", "italic", "highlight")

        for tag in tags:
            self.tag_bind(tag, "<ButtonRelease-1>", lambda e: on_tag_click(e))

        self.tag_bind("name_user", "<ButtonRelease-1>", lambda e: inputcontrol.insert_name("user"))
        self.tag_bind("name_ai", "<ButtonRelease-1>", lambda e: inputcontrol.insert_name("ai"))

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

        self.bind("<ButtonRelease-3>", lambda e: self.show_word_menu(e))
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
        self.configure(background=app.theme.output_background, foreground=app.theme.output_foreground)
        self.configure(bd=4, highlightthickness=0, relief="flat")

        if args.colors:
            self.tag_configure("name_user", foreground=app.theme.name_user)
            self.tag_configure("name_ai", foreground=app.theme.name_ai)

        self.tag_configure("highlight", underline=True)
        self.tag_configure("url", underline=True)

        if args.test:
            self.tag_configure("bold", font=app.theme.get_bold_font(), underline=True)
            self.tag_configure("italic", font=app.theme.get_italic_font(), underline=True)
        else:
            self.tag_configure("bold", font=app.theme.get_bold_font())
            self.tag_configure("italic", font=app.theme.get_italic_font())

        for tag in ("bold", "italic", "highlight", "url", "name_user", "name_ai"):
            self.tag_lower(tag)

        self.tag_configure("sel", background=app.theme.output_selection_background,
                           foreground=app.theme.output_selection_foreground)

        self.bind("<Double-Button-1>", lambda e: self.on_double_click(e))

    def set_text(self, text: str) -> None:
        self.enable()
        self.delete("1.0", tk.END)
        self.insert("1.0", str(text))
        self.disable()

    def insert_text(self, text: str, format_text: bool = False) -> None:
        self.enable()
        self.insert(tk.END, text)

        if format_text:
            checks = ("`", ":", "*", "_")

            if any([check in text for check in checks]):
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

    def last_characters(self, n: int) -> str:
        text = self.get("1.0", "end-1c")
        return text[-n:] if text else ""

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

    def format_text(self) -> None:
        if self.format_text_timer:
            return

        self.format_text_timer = self.after(self.format_text_delay, lambda: self.do_format_text())

    def do_format_text(self) -> None:
        self.format_text_timer = ""
        self.enable()
        self.markdown.format(self.position)
        self.position = self.index("end - 1c")
        self.disable()
        app.update()
        self.to_bottom(True)

    def update_font(self) -> None:
        self.configure(font=app.theme.get_output_font())

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

    def prompt(self, who: str) -> None:
        prompt = Output.get_prompt(who)
        self.print(prompt)
        start_index = self.index(f"end - {len(prompt) + 1}c")
        end_index = self.index("end - 3c")
        self.tag_add(f"name_{who}", start_index, end_index)

    def print(self, text: str) -> None:
        left = ""

        last_line_index = self.index("end-2l")
        elements = self.dump(last_line_index, "end-1c", window=True)
        widget_above = False

        for element in elements:
            if element[0] == "window":
                widget_above = True
                break

        if widget_above:
            left = "\n\n"
        else:
            if len(self.get_text()):
                last_chars = self.last_characters(2).strip(" ")

                if last_chars == "\n\n":
                    pass
                elif last_chars == "\n":
                    left = "\n"
                else:
                    left = "\n\n"

        text = left + text
        self.insert_text(text)
        self.to_bottom(True)

    def get_tagwords(self, tag: str, event: Any) -> str:
        current_index = event.widget.index(tk.CURRENT)
        ranges = self.tag_ranges(tag)

        for i in range(0, len(ranges), 2):
            start, end = ranges[i], ranges[i + 1]
            start_line, start_char = map(int, str(start).split('.'))
            end_line, end_char = map(int, str(end).split('.'))
            cur_line, cur_char = map(int, str(current_index).split('.'))

            if start_line <= cur_line < end_line or (start_line == cur_line == end_line and start_char <= cur_char < end_char):
                text = self.get(start, end)
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

    def show_word_menu(self, event: Any) -> None:
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
            Output.word_menu.show(event)

    def on_motion(self, event: Any) -> None:
        current_index = self.index(tk.CURRENT)
        tags = self.tag_names(current_index)

        if tags:
            Output.words = self.get_tagwords(tags[0], event).strip()

            if ("sel" in tags) and (len(tags) == 1):
                self.configure(cursor="xterm")
            else:
                self.configure(cursor="hand2")
        else:
            Output.words = self.get(f"{current_index} wordstart", f"{current_index} wordend")
            self.configure(cursor="xterm")

    def on_double_click(self, event: Any) -> str:
        self.show_word_menu(event)
        return "break"
