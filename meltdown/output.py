# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional, Dict, Tuple

# Modules
from .config import config
from .app import app
from .menus import Menu
from .args import args
from .utils import utils
from .gestures import Gestures


class Output(tk.Text):
    word_menu = Menu()
    word_menu.add(text="Copy", command=lambda e: Output.copy_words())
    word_menu.add(text="Explain", command=lambda e: Output.explain_words())
    word_menu.add(text="Search", command=lambda e: Output.search_words())
    word_menu.add(text="New", command=lambda e: Output.new_tab())
    current_output: Optional["Output"] = None
    marker_user = "\u200b\u200b\u200b"
    marker_ai = "\u200c\u200c\u200c"
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
        utils.copy(text)

    @staticmethod
    def explain_words() -> None:
        from .model import model

        if not Output.current_output:
            return

        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        query = f'What is "{text}" ?'
        tab_id = Output.current_output.tab_id
        model.stream({"text": query}, tab_id)

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

        if args.confirm_search:
            Dialog.show_confirm("Search for this term?", lambda: action())
        else:
            action()

    @staticmethod
    def new_tab() -> None:
        from .display import display
        from .model import model

        if not Output.current_output:
            return

        text = Output.get_words()
        Output.current_output.deselect_all()

        if not text:
            return

        query = f'Tell me about "{text}"'
        tab_id = display.make_tab()
        model.stream({"text": query}, tab_id)

    @staticmethod
    def open_url(url: str) -> None:
        from .dialogs import Dialog

        def action() -> None:
            app.open_url(url)

        if args.confirm_urls:
            Dialog.show_confirm("Open this URL?", lambda: action())
        else:
            action()

    @staticmethod
    def get_prompt(
        who: str, mark: bool = False, show_avatar: bool = True, colon_space: bool = True
    ) -> str:
        name = getattr(config, f"name_{who}")
        avatar = getattr(config, f"avatar_{who}")
        colons = " : " if colon_space else ": "

        if args.avatars and show_avatar and avatar:
            if name:
                prompt = f"{avatar} {name}{colons}"
            else:
                prompt = f"{avatar}{colons}"
        elif name:
            prompt = f"{name}{colons}"
        else:
            prompt = f"Anon{colons}"

        if mark:
            # Add invisible markers
            if who == "user":
                prompt = f"{Output.marker_user}{prompt}"
            elif who == "ai":
                prompt = f"{Output.marker_ai}{prompt}"

        return prompt

    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        from .snippet import Snippet

        super().__init__(
            parent, state="disabled", wrap="word", font=app.theme.get_output_font()
        )

        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.configure(cursor="arrow")
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_scroll = True

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)
        self.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

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

        self.tag_bind(
            "name_user", "<ButtonRelease-1>", lambda e: inputcontrol.insert_name("user")
        )

        self.tag_bind(
            "name_ai", "<ButtonRelease-1>", lambda e: inputcontrol.insert_name("ai")
        )

        def on_url_click(event: Any) -> None:
            text = self.get_tagwords("url", event)

            if text:
                self.open_url(text)

        self.tag_bind("url", "<ButtonRelease-1>", lambda e: on_url_click(e))
        self.bind("<Motion>", lambda e: self.on_motion(e))

        def mousewheel_up() -> str:
            self.scroll_up(True)
            return "break"

        def mousewheel_down() -> str:
            self.scroll_down(True)
            return "break"

        def scroll_up(double: bool = False) -> str:
            self.scroll_up(True, double=double)
            return "break"

        def scroll_down(double: bool = False) -> str:
            self.scroll_down(True, double=double)
            return "break"

        def home() -> str:
            self.to_top()
            return "break"

        def end() -> str:
            self.to_bottom()
            return "break"

        self.gestures = Gestures(self, self, self.on_right_click)
        self.bind("<Button-1>", lambda e: self.on_click(e))
        self.scrollbar.bind("<Button-1>", lambda e: self.on_click(e))
        self.bind("<Button-4>", lambda e: mousewheel_up())
        self.bind("<Button-5>", lambda e: mousewheel_down())
        self.bind("<Shift-Button-4>", lambda e: self.tab_left())
        self.bind("<Shift-Button-5>", lambda e: self.tab_right())
        self.bind("<Control-Button-4>", lambda e: self.increase_font())
        self.bind("<Control-Button-5>", lambda e: self.decrease_font())
        self.bind("<Control-Shift-Button-4>", lambda e: self.move_left())
        self.bind("<Control-Shift-Button-5>", lambda e: self.move_right())
        self.bind("<Prior>", lambda e: scroll_up())
        self.bind("<Control-Prior>", lambda e: scroll_up(True))
        self.bind("<Shift-Prior>", lambda e: scroll_up(True))
        self.bind("<Next>", lambda e: scroll_down())
        self.bind("<Control-Next>", lambda e: scroll_down(True))
        self.bind("<Shift-Next>", lambda e: scroll_down(True))
        self.bind("<KeyPress-Home>", lambda e: home())
        self.bind("<KeyPress-End>", lambda e: end())
        self.bind("<Configure>", lambda e: self.update_size())

        def on_scroll(*args: Any) -> None:
            self.display.check_scroll_buttons()
            self.scrollbar.set(*args)

        self.scrollbar.configure(command=self.yview)
        self.configure(yscrollcommand=on_scroll)

        self.configure(
            background=app.theme.output_background,
            foreground=app.theme.output_foreground,
        )

        self.configure(border=4, highlightthickness=0, relief="flat")

        if args.colors:
            if args.user_color == "auto":
                self.tag_configure("name_user", foreground=app.theme.user_color)
            else:
                self.tag_configure("name_user", foreground=args.user_color)

            if args.ai_color == "auto":
                self.tag_configure("name_ai", foreground=app.theme.ai_color)
            else:
                self.tag_configure("name_ai", foreground=args.ai_color)

        self.tag_configure("highlight", underline=True)
        self.tag_configure("url", underline=True)
        self.tag_configure("bold", font=app.theme.get_bold_font())
        self.tag_configure("italic", font=app.theme.get_italic_font())

        for tag in ("bold", "italic", "highlight", "url", "name_user", "name_ai"):
            self.tag_lower(tag)

        self.tag_configure(
            "sel",
            background=app.theme.output_selection_background,
            foreground=app.theme.output_selection_foreground,
        )

    def set_text(self, text: str) -> None:
        self.enable()
        self.delete("1.0", tk.END)
        self.insert("1.0", str(text))
        self.disable()

    def insert_text(self, text: str) -> None:
        self.enable()
        self.insert(tk.END, text)
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
        lines = self.count("1.0", "end-1c lineend", "displaylines")  # type: ignore

        if not lines:
            return 0.0

        return float(num_lines / lines[0])

    def get_scroll_lines(self) -> float:
        fraction = self.get_fraction()
        return fraction * args.scroll_lines

    def scroll_up(self, check: bool = False, double: bool = False) -> None:
        lines = self.get_scroll_lines()

        if double:
            lines *= 2

        self.yview_moveto(self.yview()[0] - lines)

        if check:
            self.check_autoscroll("up")

    def scroll_down(self, check: bool = False, double: bool = False) -> None:
        lines = self.get_scroll_lines()

        if double:
            lines *= 2

        self.yview_moveto(self.yview()[0] + lines)

        if check:
            self.check_autoscroll("down")

    def get_tab(self) -> Optional[Any]:
        return self.display.get_tab(self.tab_id)

    def format_text(self) -> None:
        tab = self.get_tab()

        if not tab:
            return

        if tab.mode == "ignore":
            return

        if not tab.modified:
            return

        self.enable()
        self.markdown.format()
        self.disable()
        app.root.after(120, lambda: self.to_bottom(True))

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
        utils.copy(self.get_text())

    def to_text(self) -> str:
        from .session import session

        tab = self.display.get_tab(self.tab_id)

        if not tab:
            return ""

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return ""

        return conversation.to_text()

    def prompt(self, who: str) -> None:
        prompt = Output.get_prompt(who, mark=True)
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
        elif len(self.get_text()):
            last_chars = self.last_characters(2).strip(" ")

            if last_chars:
                if last_chars == "\n\n":
                    pass
                elif last_chars == "\n":
                    left = "\n"
                elif last_chars[-1] == "\n":
                    left = "\n"
                else:
                    left = "\n\n"

        text = left + text
        self.insert_text(text)
        self.to_bottom(True)

    def get_tagwords(self, tag: str, event: Any) -> str:
        current_index = event.widget.index(tk.CURRENT)
        char = event.widget.get(current_index)

        if char == "\n":
            return ""

        cur_line, cur_char = map(int, str(current_index).split("."))
        ranges = event.widget.tag_ranges(tag)

        for i in range(0, len(ranges), 2):
            start, end = ranges[i], ranges[i + 1]
            start_line, start_char = map(int, str(start).split("."))
            end_line, end_char = map(int, str(end).split("."))

            # If the current index is within the start and end range
            if start_line <= cur_line <= end_line:
                if cur_line == start_line and cur_char < start_char:
                    continue  # Skip if the cursor is before the start of the tagged text on the same line
                if cur_line == end_line and cur_char > end_char:
                    continue  # Skip if the cursor is after the end of the tagged text on the same line

                tagged_text = event.widget.get(start, end)
                tagged_lines = tagged_text.split("\n")

                # Return the line of the tagged text that the cursor is on
                return tagged_lines[cur_line - start_line] or ""

        return ""  # Return an empty string if no tagged word is found

    def get_selected_text(self, widget: Optional[tk.Text] = None) -> str:
        if not widget:
            widget = self

        try:
            start = widget.index(tk.SEL_FIRST)
            end = widget.index(tk.SEL_LAST)
            return widget.get(start, end)
        except tk.TclError:
            return ""

    def show_word_menu(self, event: Any, widget: Optional[tk.Text] = None) -> bool:
        if not widget:
            widget = self

        current_index = widget.index(tk.CURRENT)
        tags = widget.tag_names(current_index)
        seltext = self.get_selected_text(widget)

        Output.words = ""
        Output.current_output = self

        if seltext:
            Output.words = seltext.strip()
        elif tags:
            Output.words = self.get_tagwords(tags[0], event).strip()

        if not Output.words:
            return False

        Output.word_menu.show(event)
        return True

    def on_motion(self, event: Any) -> None:
        current_index = self.index(tk.CURRENT)
        char = self.get(current_index)

        if char == "\n":
            self.configure(cursor="arrow")
            return

        tags = self.tag_names(current_index)

        if tags:
            if ("sel" in tags) and (len(tags) == 1):
                self.configure(cursor="xterm")
            else:
                self.configure(cursor="hand2")
        else:
            self.configure(cursor="xterm")

    def get_snippet_index(self, index: int) -> str:
        num = 0

        for element in self.dump("1.0", "end"):
            if element[0] == "window":
                if num == index:
                    return element[2]

                num += 1

        return "1.0"

    def find_text(self, query: str) -> str:
        return self.search(query, "1.0", tk.END, regexp=True, nocase=True)

    def get_markers(self) -> Tuple[List[Dict[str, Any]], int]:
        markers = []
        lines = self.get_text().split("\n")

        for i, line in enumerate(lines):
            if line.startswith(Output.marker_user):
                markers.append({"who": "user", "line": i + 1})
            elif line.startswith(Output.marker_ai):
                markers.append({"who": "ai", "line": i + 1})

        return (markers, len(lines))

    def reset_drag(self) -> None:
        self.gestures.reset_drag()

        for snippet in self.snippets:
            snippet.gestures.reset_drag()

    def on_right_click(self, event: Any, widget: Optional[tk.Text] = None) -> None:
        from .menumanager import tab_menu

        if not self.show_word_menu(event, widget):
            tab_menu.show(event)

    def on_click(self, event: Any) -> None:
        app.hide_all(hide_dialog=False)
        self.deselect_all()
        self.reset_drag()

    def tab_left(self) -> str:
        self.display.tab_left()
        return "break"

    def tab_right(self) -> str:
        self.display.tab_right()
        return "break"

    def increase_font(self) -> str:
        self.display.increase_font()
        return "break"

    def decrease_font(self) -> str:
        self.display.decrease_font()
        return "break"

    def move_left(self) -> str:
        self.display.move_tab_left()
        return "break"

    def move_right(self) -> str:
        self.display.move_tab_right()
        return "break"
