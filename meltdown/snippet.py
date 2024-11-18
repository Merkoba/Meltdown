# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any

# Libraries
from pygments.lexers import get_lexer_by_name  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore
from pygments.util import ClassNotFound  # type: ignore

# Modules
from .output import Output
from .args import args
from .app import app
from .utils import utils
from .gestures import Gestures


class Snippet(tk.Frame):
    def __init__(self, parent: Output, content: str, language: str) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0)
        self.content = utils.untab_text(content)
        self.language = language

        self.header = tk.Frame(self)
        self.header.configure(background=app.theme.snippet_header_background)

        if language:
            header_text = f"Language: {language}"
        else:
            header_text = "Plain Text"

        font_header = app.theme.get_output_font(True)
        header_fg = app.theme.snippet_header_foreground
        header_bg = app.theme.snippet_header_background

        self.header_text = tk.Label(self.header, text=header_text, font=font_header)
        self.header_text.configure(foreground=header_fg)
        self.header_text.configure(background=header_bg)
        self.header_text.configure(cursor="arrow")
        self.header_text.pack(side=tk.LEFT, padx=5)

        self.header_copy = tk.Label(self.header, text="Copy", font=font_header)
        self.header_copy.configure(cursor="hand2")
        self.header_copy.pack(side=tk.RIGHT, padx=5)
        self.header_copy.configure(foreground=header_fg)
        self.header_copy.configure(background=header_bg)

        self.header_select = tk.Label(self.header, text="Select", font=font_header)
        self.header_select.configure(cursor="hand2")
        self.header_select.pack(side=tk.RIGHT, padx=5)
        self.header_select.configure(foreground=header_fg)
        self.header_select.configure(background=header_bg)

        self.header_find = tk.Label(self.header, text="Find", font=font_header)
        self.header_find.configure(cursor="hand2")
        self.header_find.pack(side=tk.RIGHT, padx=5)
        self.header_find.configure(foreground=header_fg)
        self.header_find.configure(background=header_bg)

        self.header.pack(side=tk.TOP, fill=tk.X)
        self.text = tk.Text(self, wrap="none", state="normal")
        self.text.configure(borderwidth=0, highlightthickness=0)
        self.text.delete("1.0", tk.END)

        def insert() -> None:
            self.text.insert("1.0", self.content)

        if language and args.syntax_highlighting:
            try:
                if not self.syntax_highlighter():
                    insert()
            except BaseException as e:
                utils.error(e)
                insert()
        else:
            insert()

        self.text.configure(state="disabled")
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(
            self, style="Normal.Horizontal.TScrollbar", orient=tk.HORIZONTAL
        )

        self.scrollbar.configure(cursor="arrow")
        self.text.configure(xscrollcommand=self.scrollbar.set)

        self.text.tag_configure(
            "sel",
            background=app.theme.snippet_selection_background,
            foreground=app.theme.snippet_selection_foreground,
        )

        if args.scrollbars:
            self.scrollbar.pack(fill=tk.X)

        self.parent = parent

        num_lines = int(self.text.index("end-1c").split(".")[0])
        self.text.configure(height=num_lines)

        self.configure(background=app.theme.snippet_background)
        self.text.configure(background=app.theme.snippet_background)
        self.text.configure(foreground=app.theme.snippet_foreground)
        self.text.configure(font=app.theme.get_snippet_font())
        self.scrollbar.configure(command=self.text.xview)

        self.update_size()
        self.setup_bindings()

    def setup_bindings(self) -> None:
        def bind_scroll_events(widget: tk.Widget) -> None:
            widget.bind("<Button-1>", lambda e: self.on_click())
            widget.bind("<Button-4>", lambda e: self.scroll_up())
            widget.bind("<Button-5>", lambda e: self.scroll_down())
            widget.bind("<Shift-Button-4>", lambda e: self.scroll_left())
            widget.bind("<Shift-Button-5>", lambda e: self.scroll_right())
            widget.bind("<Control-Button-4>", lambda e: self.parent.increase_font())
            widget.bind("<Control-Button-5>", lambda e: self.parent.decrease_font())

            for child in widget.winfo_children():
                bind_scroll_events(child)

        bind_scroll_events(self)

        self.header_copy.bind("<Button-1>", lambda e: self.copy_all())
        self.header_select.bind("<Button-1>", lambda e: self.select_all())
        self.header_find.bind("<Button-1>", lambda e: self.find())
        self.text.bind("<Motion>", lambda e: self.on_motion(e))
        self.gestures = Gestures(self, self.text, self.on_right_click)

    def update_size(self) -> None:
        try:
            char_width = self.text.tk.call(
                "font", "measure", self.text.cget("font"), "0"
            )
        except BaseException:
            return

        width_pixels = self.parent.winfo_width() - self.parent.scrollbar.winfo_width()
        width_pixels = int(width_pixels * 0.98)
        width_chars = int(width_pixels / char_width)
        self.text.configure(width=width_chars)

    def update_font(self) -> None:
        font_header = app.theme.get_output_font(True)
        snippet_font = app.theme.get_snippet_font()

        self.text.configure(font=snippet_font)

        self.header_text.configure(font=font_header)
        self.header_copy.configure(font=font_header)
        self.header_select.configure(font=font_header)
        self.update_size()

    def overflowed(self) -> bool:
        pos = self.scrollbar.get()
        return pos[0] != 0.0 or pos[1] != 1.0

    def scroll_left(self) -> str:
        if not self.overflowed():
            self.parent.tab_left()
            return "break"

        self.text.xview_scroll(-2, "units")
        return "break"

    def scroll_right(self) -> str:
        if not self.overflowed():
            self.parent.tab_right()
            return "break"

        self.text.xview_scroll(2, "units")
        return "break"

    def copy_all(self) -> None:
        app.hide_all()
        self.deselect_all()
        utils.copy(self.content)
        self.header_copy.configure(text="Copied!")
        self.after(1000, lambda: self.header_copy.configure(text="Copy"))

    def select_all(self) -> None:
        app.hide_all()
        self.text.tag_add("sel", "1.0", tk.END)

    def deselect_all(self) -> None:
        if not self.text:
            return

        self.text.tag_remove("sel", "1.0", tk.END)

    def on_motion(self, event: Any) -> None:
        current_index = self.text.index(tk.CURRENT)

        Output.words = self.text.get(
            f"{current_index} wordstart", f"{current_index} wordend"
        )

    def get_selected_text(self) -> str:
        try:
            start = self.text.index(tk.SEL_FIRST)
            end = self.text.index(tk.SEL_LAST)
            return self.text.get(start, end)
        except tk.TclError:
            return ""

    def syntax_highlighter(self) -> bool:
        try:
            lexer = get_lexer_by_name(self.language, stripall=True)
        except ClassNotFound:
            return False

        style = get_style_by_name(app.theme.syntax_style)
        parsed = style.list_styles()

        for key in parsed:
            if key[1]["color"] != "" and key[1]["color"] is not None:
                color = "#" + key[1]["color"]
                key_ = str(key[0])
                self.text.tag_configure(key_, foreground=color)
                self.text.tag_lower(key_)

        tokens = list(lexer.get_tokens(self.content))

        for text in tokens:
            self.text.insert(tk.END, text[1], str(text[0]))

        last_line_index = self.text.index("end-1c linestart")
        last_line_text = self.text.get(last_line_index, "end-1c")

        if not last_line_text.strip():
            self.text.delete(last_line_index, "end")

        return True

    def on_click(self) -> None:
        app.hide_all()
        self.parent.deselect_all()

    def scroll_up(self) -> str:
        self.parent.scroll_up(True)
        return "break"

    def scroll_down(self) -> str:
        self.parent.scroll_down(True)
        return "break"

    def find(self) -> None:
        from . import findmanager

        app.hide_all()
        findmanager.find(tab_id=self.parent.tab_id, widget=self.text)

    def on_right_click(self, event: Any) -> None:
        self.parent.on_right_click(event, self.text)
