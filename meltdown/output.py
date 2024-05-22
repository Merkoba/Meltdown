# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional, Dict, Tuple

# Modules
from .config import config
from .app import app
from .args import args
from .utils import utils
from .gestures import Gestures
from .autoscroll import autoscroll


class Output(tk.Text):
    clicked_number = 0
    marker_user = "\u200b\u200b\u200b"
    marker_ai = "\u200c\u200c\u200c"
    marker_separator = "\u200d\u200d\u200d"
    marker_space = "\u00a0"
    words = ""

    @staticmethod
    def current_output() -> Optional["Output"]:
        from .display import display

        return display.get_current_output()

    @staticmethod
    def custom_menu(event: Any) -> None:
        from .menumanager import custom_menu

        custom_menu.show(event)

    @staticmethod
    def delete_items(mode: str = "normal") -> None:
        from . import delete

        output = Output.current_output()

        if not output:
            return

        tab_id = output.tab_id
        arg = str(Output.clicked_number)
        delete.delete_items(tab_id=tab_id, number=arg, mode=mode)

    @staticmethod
    def select_item(number: Optional[int] = None) -> None:
        output = Output.current_output()

        if not output:
            return

        if number is None:
            number = Output.clicked_number

        start_ln, end_ln = output.get_item_text(number)

        if start_ln == 0:
            return

        output.select_lines(start_ln, end_ln)

    @staticmethod
    def copy_item() -> None:
        from . import itemops

        output = Output.current_output()

        if not output:
            return

        tab_id = output.tab_id
        arg = str(Output.clicked_number)
        itemops.action("copy", tab_id=tab_id, number=arg)

    @staticmethod
    def open_url() -> None:
        words = Output.get_words()

        if words:
            app.open_url(words)

    @staticmethod
    def repeat_prompt(no_history: bool = False) -> None:
        from . import itemops

        output = Output.current_output()

        if not output:
            return

        tab_id = output.tab_id
        arg = str(Output.clicked_number)
        itemops.action("repeat", tab_id=tab_id, number=arg, no_history=no_history)

    @staticmethod
    def get_words() -> str:
        return Output.words.strip()

    @staticmethod
    def use_url() -> None:
        from .widgets import widgets

        path = Output.get_words()
        widgets.set_file(path)

    @staticmethod
    def copy_words() -> None:
        output = Output.current_output()

        if not output:
            return

        text = Output.get_words()
        output.deselect_all()
        utils.copy(text, command=True)

    @staticmethod
    def custom_prompt(text: str) -> None:
        from .model import model

        output = Output.current_output()

        if not output:
            return

        words = Output.get_words()
        output.deselect_all()

        if not words:
            return

        quoted = utils.smart_quotes(words)
        text = utils.replace_keywords(text, words=quoted)
        tab_id = output.tab_id
        model.stream({"text": text}, tab_id)

    @staticmethod
    def explain_words() -> None:
        Output.custom_prompt(args.explain_prompt)

    @staticmethod
    def get_selected() -> str:
        output = Output.current_output()

        if not output:
            return ""

        return output.get_selected_text().strip()

    @staticmethod
    def explain_selected() -> None:
        text = Output.get_selected()

        if not text:
            return

        Output.words = text
        Output.explain_words()

    @staticmethod
    def new_selected() -> None:
        text = Output.get_selected()

        if not text:
            return

        Output.words = text
        Output.new_tab()

    @staticmethod
    def search_selected() -> None:
        text = Output.get_selected()

        if not text:
            return

        Output.words = text
        Output.search_words()

    @staticmethod
    def copy_selected() -> None:
        text = Output.get_selected()

        if not text:
            return

        Output.words = text
        Output.copy_words()

    @staticmethod
    def search_words() -> None:
        output = Output.current_output()

        if not output:
            return

        words = Output.get_words()
        output.deselect_all()

        if not words:
            return

        quoted = utils.smart_quotes(words)
        app.search_text(quoted)

    @staticmethod
    def new_tab() -> None:
        from .display import display
        from .model import model

        output = Output.current_output()

        if not output:
            return

        words = Output.get_words()
        output.deselect_all()

        if not words:
            return

        quoted = utils.smart_quotes(words)
        text = utils.replace_keywords(args.new_prompt, words=quoted)
        tab_id = display.make_tab()

        if not tab_id:
            return

        model.stream({"text": text}, tab_id)

    @staticmethod
    def get_prompt(who: str, show_avatar: bool = True, colon_space: bool = True) -> str:
        name = getattr(config, f"name_{who}")
        avatar = getattr(config, f"avatar_{who}")

        colons = (
            f"{Output.marker_space}:{Output.marker_space}"
            if colon_space
            else f":{Output.marker_space}"
        )

        if args.avatars and show_avatar and avatar:
            if name:
                prompt = f"{avatar} {name}{colons}"
            else:
                prompt = f"{avatar}{colons}"
        elif name:
            prompt = f"{name}{colons}"
        else:
            prompt = f"Anon{colons}"

        return prompt

    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        from .snippet import Snippet

        super().__init__(parent, state="disabled", wrap="word")
        self.set_font()
        self.scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
        self.scrollbar.configure(cursor="arrow")
        self.tab_id = tab_id
        self.snippets: List[Snippet] = []
        self.auto_bottom = True
        self.update_size_after = ""
        self.separator = Output.marker_separator + args.separator
        self.checked_markers_user: List[int] = []
        self.checked_markers_ai: List[int] = []
        self.last_scroll_args: Optional[Tuple[str, str]] = None

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)
        self.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        if args.scrollbars:
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.setup()

    def setup(self) -> None:
        from .display import display
        from .markdown import Markdown

        self.display = display
        self.markdown = Markdown(self)

        def on_tag_click(event: Any) -> None:
            self.deselect_all()
            self.show_word_menu(event)

        tags = (
            "bold",
            "italic",
            "highlight",
            "quote",
            "header_1",
            "header_2",
            "header_3",
        )

        for tag in tags:
            self.tag_bind(tag, "<ButtonRelease-1>", lambda e: on_tag_click(e))

        self.tag_bind(
            "name_user",
            "<ButtonRelease-1>",
            lambda e: self.on_name_click(e),
        )

        self.tag_bind(
            "name_ai",
            "<ButtonRelease-1>",
            lambda e: self.on_name_click(e),
        )

        def on_url_click(event: Any) -> None:
            from .keyboard import keyboard
            from .menumanager import url_menu

            if not args.url_menu:
                return

            Output.words = self.get_tagwords("url", event)

            if keyboard.ctrl:
                Output.open_url()
                return

            url_menu.show(event)

        self.tag_bind("url", "<ButtonRelease-1>", lambda e: on_url_click(e))

        def on_path_click(event: Any) -> None:
            from .keyboard import keyboard
            from .menumanager import url_menu

            if not args.path_menu:
                return

            Output.words = self.get_tagwords("path", event)

            if keyboard.ctrl:
                Output.open_url()
                return

            url_menu.show(event)

        self.tag_bind("path", "<ButtonRelease-1>", lambda e: on_path_click(e))

        self.bind("<Motion>", lambda e: self.on_motion(e))

        def mousewheel_up() -> str:
            self.scroll_up(True)
            autoscroll.disable()
            return "break"

        def mousewheel_down() -> str:
            self.scroll_down(True)
            autoscroll.disable()
            return "break"

        def scroll_up(more: bool = False) -> str:
            self.scroll_up(True, more=more)
            autoscroll.disable()
            return "break"

        def scroll_down(more: bool = False) -> str:
            self.scroll_down(True, more=more)
            autoscroll.disable()
            return "break"

        def home() -> str:
            self.to_top()
            return "break"

        def end() -> str:
            self.to_bottom()
            return "break"

        self.gestures = Gestures(self, self, self.on_right_click)

        self.bind("<Button-1>", lambda e: self.on_click())
        self.bind("<Button-2>", lambda e: self.on_middle_click(False, False))
        self.bind("<Control-Button-2>", lambda e: self.on_middle_click(True, False))
        self.bind("<Shift-Button-2>", lambda e: self.on_middle_click(False, True))

        self.bind(
            "<Control-Shift-Button-2>", lambda e: self.on_middle_click(True, True)
        )

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

        self.scrollbar.bind("<Button-1>", lambda e: self.on_scrollbar_click())

        def on_scroll(*args: Any) -> None:
            if self.last_scroll_args == args:
                return

            self.on_scroll_action(*args)

        self.scrollbar.configure(command=self.yview)
        self.configure(yscrollcommand=on_scroll)

        self.configure(
            background=app.theme.output_background,
            foreground=app.theme.output_foreground,
        )

        self.configure(border=4, highlightthickness=0, relief="flat")
        self.configure_tags()

        for tag in (
            "bold",
            "italic",
            "highlight",
            "quote",
            "url",
            "path",
            "name_user",
            "name_ai",
            "header_1",
            "header_2",
            "header_3",
        ):
            self.tag_lower(tag)

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

    def reset(self) -> None:
        self.set_text("")
        self.snippets = []
        self.checked_markers_user = []
        self.checked_markers_ai = []

    def to_top(self) -> None:
        self.auto_bottom = False
        self.yview_moveto(0.0)

    def to_bottom(self, check: bool = False) -> None:
        if check and (not self.auto_bottom):
            return

        self.auto_bottom = True
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

    def scroll_up(self, check: bool = False, more: bool = False) -> None:
        lines = self.get_scroll_lines()

        if more:
            lines *= 2

        self.yview_moveto(self.yview()[0] - lines)

        if check:
            self.check_autoscroll("up")

    def scroll_down(self, check: bool = False, more: bool = False) -> None:
        lines = self.get_scroll_lines()

        if more:
            lines *= 2

        self.yview_moveto(self.yview()[0] + lines)

        if check:
            self.check_autoscroll("down")

    def get_tab(self) -> Optional[Any]:
        return self.display.get_tab(self.tab_id)

    def format_text(self, mode: str = "normal") -> None:
        tab = self.get_tab()

        if not tab:
            return

        if not tab.modified:
            return

        if tab.mode == "ignore":
            if mode == "normal":
                return

        self.enable()

        if mode == "all":
            self.markdown.format_all()
        else:
            self.markdown.format()

        self.disable()
        self.update_idletasks()
        self.to_bottom(True)

    def update_font(self) -> None:
        self.set_font()
        self.configure_tags()
        self.update_snippet_fonts()

    def update_size(self) -> None:
        if not self.winfo_exists():
            return

        if self.update_size_after:
            app.root.after_cancel(self.update_size_after)

        self.update_size_after = app.root.after(100, lambda: self.do_update_size())

    def do_update_size(self) -> None:
        for snippet in self.snippets:
            snippet.update_size()

        if self.last_scroll_args:
            self.on_scroll_action(*self.last_scroll_args)

    def check_autoscroll(self, direction: str) -> None:
        if direction == "up":
            self.auto_bottom = False
        elif direction == "down":
            if self.yview()[1] >= 1.0:
                self.auto_bottom = True

    def enable(self) -> None:
        if self.cget("state") != "normal":
            self.configure(state="normal")

    def disable(self) -> None:
        if self.cget("state") != "disabled":
            self.configure(state="disabled")

    def copy_all(self) -> None:
        utils.copy(self.get_text(), command=True)

    def to_text(self) -> str:
        from .display import display

        tabconvo = display.get_tab_convo(self.tab_id)

        if not tabconvo:
            return ""

        return tabconvo.convo.to_text()

    def prompt(self, who: str) -> None:
        from .display import display

        prompt = Output.get_prompt(who)
        prepend = ""

        if args.item_numbers:
            number = display.num_user_prompts()
            prepend = f"({number + 1})"

        if prepend:
            text = f"{prepend} {prompt}"
        else:
            text = prompt

        # Add invisible markers
        if who == "user":
            text = f"{Output.marker_user}{text}"
        elif who == "ai":
            text = f"{Output.marker_ai}{text}"

        self.print(text)
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
        from .menumanager import word_menu
        from .keyboard import keyboard

        if not args.word_menu:
            return False

        if not widget:
            widget = self

        current_index = widget.index(tk.CURRENT)
        tags = widget.tag_names(current_index)

        for tag in tags:
            if (tag == "name_user") or (tag == "name_ai"):
                self.on_name_click(event)
                return True

        seltext = self.get_selected_text(widget)

        Output.words = ""

        if seltext:
            Output.words = seltext.strip()
        elif tags:
            Output.words = self.get_tagwords(tags[0], event).strip()

        if not Output.words:
            return False

        if keyboard.ctrl:
            Output.explain_words()
            return True

        word_menu.show(event)
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

    def get_snippet_index_2(self, snippet: tk.Widget) -> Tuple[str, int]:
        index = 0

        for element in self.dump("1.0", "end"):
            if element[0] == "window":
                if element[1] in str(snippet):
                    return element[2], index

                index += 1

        return ("1.0", 0)

    def find_text(self, query: str) -> str:
        return self.search(query, "1.0", tk.END, regexp=True, nocase=True)

    def get_markers(self) -> Tuple[List[Dict[str, Any]], int]:
        markers = []
        lines = self.get_text().split("\n")
        number_user = 0
        number_ai = 0

        for i, line in enumerate(lines):
            start_ln = i + 1

            if line.startswith(Output.marker_user):
                number_user += 1

                if number_user in self.checked_markers_user:
                    continue

                self.checked_markers_user.append(number_user)
                markers.append({"who": "user", "line": start_ln})
            elif line.startswith(Output.marker_ai):
                number_ai += 1

                if number_ai in self.checked_markers_ai:
                    continue

                self.checked_markers_ai.append(number_ai)

                markers.append({"who": "ai", "line": start_ln})

        return (markers, len(lines))

    def reset_drag(self) -> None:
        self.gestures.reset_drag()

        for snippet in self.snippets:
            snippet.gestures.reset_drag()

    def on_right_click(self, event: Any, widget: Optional[tk.Text] = None) -> None:
        from .menumanager import tab_menu

        if not self.show_word_menu(event, widget):
            tab_menu.show(event)

    def on_click(self) -> None:
        app.hide_all(hide_dialog=False)
        self.deselect_all()
        self.reset_drag()

    def on_middle_click(self, ctrl: bool = False, shift: bool = False) -> str:
        from .commands import commands

        if ctrl and shift:
            if args.on_ctrl_shift_middle_click:
                commands.exec(args.on_ctrl_shift_middle_click)
                return "break"
        elif ctrl:
            if args.on_ctrl_middle_click:
                commands.exec(args.on_ctrl_middle_click)
                return "break"
        elif shift:
            if args.on_shift_middle_click:
                commands.exec(args.on_shift_middle_click)
                return "break"

        return ""

    def tab_left(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.tab_left()
        return "break"

    def tab_right(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.tab_right()
        return "break"

    def increase_font(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.increase_font()
        return "break"

    def decrease_font(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.decrease_font()
        return "break"

    def move_left(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.move_tab_left()
        return "break"

    def move_right(self) -> str:
        if not args.output_wheel:
            return ""

        self.display.move_tab_right()
        return "break"

    def on_name_click(self, event: Any) -> None:
        from .menumanager import item_menu
        from .keyboard import keyboard

        self.deselect_all()

        if not args.name_menu:
            return

        number = self.get_number()

        if number == 0:
            return

        Output.clicked_number = number

        if keyboard.ctrl or keyboard.shift:
            Output.select_item()
            return

        item_menu.show(event)

    def get_number(self) -> int:
        line_number = int(self.index("current").split(".")[0])
        count = 0

        for i in range(1, line_number + 1):
            line = self.get(f"{i}.0", f"{i}.end")

            if line.startswith(Output.marker_user):
                count += 1

        return count

    def separate(self) -> None:
        self.print(self.separator)

    def select_lines(self, start_ln: int, end_ln: int) -> None:
        self.tag_add("sel", f"{start_ln}.0", f"{end_ln}.end")

    def get_item_text(self, number: int) -> Tuple[int, int]:
        lines = self.get_text().split("\n")
        start_ln = 0
        end_ln = 0
        count = 0

        for i, line in enumerate(lines):
            if line.startswith(Output.marker_user):
                count += 1

                if start_ln == 0:
                    if count == number:
                        start_ln = i + 1
                else:
                    end_ln = i
                    break
            elif line.startswith(Output.marker_separator):
                if start_ln > 0:
                    end_ln = i
                    break

        if start_ln == 0:
            return (0, 0)

        if end_ln == 0:
            end_ln = len(lines)

        return start_ln, end_ln

    def configure_tags(self) -> None:
        self.tag_configure(
            "sel",
            background=app.theme.output_selection_background,
            foreground=app.theme.output_selection_foreground,
        )

        self.tag_configure("highlight", underline=True)
        self.tag_configure("url", underline=True)
        self.tag_configure("path", underline=True)
        self.tag_configure("bold", font=app.theme.get_bold_font())
        self.tag_configure("italic", font=app.theme.get_italic_font())
        self.tag_configure("quote", font=app.theme.get_bold_font())
        self.tag_configure("header_1", font=app.theme.get_header_font(1))
        self.tag_configure("header_2", font=app.theme.get_header_font(2))
        self.tag_configure("header_3", font=app.theme.get_header_font(3))
        self.tag_configure("separator", font=app.theme.get_separator_font())

        if args.colors:
            if args.user_color == "auto":
                self.tag_configure("name_user", foreground=app.theme.user_color)
            else:
                self.tag_configure("name_user", foreground=args.user_color)
            if args.ai_color == "auto":
                self.tag_configure("name_ai", foreground=app.theme.ai_color)
            else:
                self.tag_configure("name_ai", foreground=args.ai_color)

    def set_font(self) -> None:
        self.configure(font=app.theme.get_output_font())

    def update_snippet_fonts(self) -> None:
        for snippet in self.snippets:
            snippet.update_font()

    def on_scroll_action(self, *args: Any) -> None:
        self.last_scroll_args = args
        self.display.check_scroll_buttons(tab_id=self.tab_id)
        self.scrollbar.set(*args)

    def on_scrollbar_click(self) -> None:
        self.on_click()
        autoscroll.disable()
