# Modules
from .output import Output
from .args import args
from .app import app

# Libraries
import pyperclip  # type: ignore
from pygments.lexers import get_lexer_by_name  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any


class Snippet(tk.Frame):
    def __init__(self, parent: Output, content: str, language: str) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0)
        self.content = content.strip()
        self.language = language

        self.header = tk.Frame(self)
        self.header.configure(background=app.theme.snippet_header_background)

        if language:
            header_text = f"Language: {language}"
        else:
            header_text = "Plain Text"

        self.header_text = tk.Label(self.header, text=header_text, font=app.theme.get_snippet_font(True))
        self.header_text.configure(foreground=app.theme.snippet_header_foreground)
        self.header_text.configure(background=app.theme.snippet_header_background)
        self.header_text.configure(cursor="arrow")
        self.header_text.pack(side=tk.LEFT, padx=5)

        self.header_copy = tk.Label(self.header, text="Copy", font=app.theme.get_snippet_font(True))
        self.header_copy.configure(cursor="hand2")
        self.header_copy.pack(side=tk.RIGHT, padx=5)
        self.header_copy.configure(foreground=app.theme.snippet_header_foreground)
        self.header_copy.configure(background=app.theme.snippet_header_background)

        self.header_select = tk.Label(self.header, text="Select", font=app.theme.get_snippet_font(True))
        self.header_select.configure(cursor="hand2")
        self.header_select.pack(side=tk.RIGHT, padx=5)
        self.header_select.configure(foreground=app.theme.snippet_header_foreground)
        self.header_select.configure(background=app.theme.snippet_header_background)

        self.header.pack(side=tk.TOP, fill=tk.X)
        self.text = tk.Text(self, wrap="none", state="normal")
        self.text.configure(borderwidth=0, highlightthickness=0)
        self.text.delete("1.0", tk.END)

        if language:
            try:
                self.syntax_highlighter()
            except BaseException:
                self.text.insert("1.0", self.content)
        else:
            self.text.insert("1.0", self.content)

        self.text.configure(state="disabled")
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar = ttk.Scrollbar(self, style="Normal.Horizontal.TScrollbar", orient=tk.HORIZONTAL)
        self.scrollbar.configure(cursor="arrow")
        self.text.configure(xscrollcommand=self.scrollbar.set)

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
        from .dialogs import Dialog

        def on_click(event: Any) -> None:
            Dialog.hide_all()

        def copy_all() -> None:
            Dialog.hide_all()
            self.copy_all()

        def select_all() -> None:
            Dialog.hide_all()
            self.select_all()

        def scroll_up(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_left()
            else:
                self.parent.scroll_up(True)

            return "break"

        def scroll_down(event: Any) -> str:
            if event.state & 0x1:
                self.scroll_right()
            else:
                self.parent.scroll_down(True)

            return "break"

        def bind_scroll_events(widget: tk.Widget) -> None:
            widget.bind("<Button-1>", lambda e: on_click(e))
            widget.bind("<Button-4>", lambda e: scroll_up(e))
            widget.bind("<Button-5>", lambda e: scroll_down(e))
            widget.bind("<Button-3>", lambda e: self.parent.show_words_menu(e))

            for child in widget.winfo_children():
                bind_scroll_events(child)

        bind_scroll_events(self)

        self.header_copy.bind("<Button-1>", lambda e: copy_all())
        self.header_select.bind("<Button-1>", lambda e: select_all())
        self.text.bind("<Motion>", lambda e: self.on_motion(e))

    def update_size(self) -> None:
        char_width = self.text.tk.call("font", "measure", self.text.cget("font"), "0")
        width_pixels = self.parent.winfo_width() - self.parent.scrollbar.winfo_width()
        width_pixels = int(width_pixels * 0.98)
        width_chars = int(width_pixels / char_width)
        self.text.configure(width=width_chars)

    def update_font(self) -> None:
        self.text.configure(font=app.theme.get_snippet_font())
        self.header_text.configure(font=app.theme.get_snippet_font(True))
        self.header_copy.configure(font=app.theme.get_snippet_font(True))
        self.header_select.configure(font=app.theme.get_snippet_font(True))
        self.update_size()

    def scroll_left(self) -> None:
        self.text.xview_scroll(-2, "units")

    def scroll_right(self) -> None:
        self.text.xview_scroll(2, "units")

    def copy_all(self) -> None:
        pyperclip.copy(self.content)
        self.header_copy.configure(text="Copied!")
        self.after(1000, lambda: self.header_copy.configure(text="Copy"))

    def select_all(self) -> None:
        self.text.tag_add("sel", "1.0", tk.END)

    def deselect_all(self) -> None:
        self.text.tag_remove("sel", "1.0", tk.END)

    def on_motion(self, event: Any) -> None:
        current_index = self.text.index(tk.CURRENT)
        Output.tab_id = self.parent.tab_id
        Output.words = self.text.get(f"{current_index} wordstart", f"{current_index} wordend")

    def get_selected_text(self) -> str:
        try:
            start = self.text.index(tk.SEL_FIRST)
            end = self.text.index(tk.SEL_LAST)
            selected_text = self.text.get(start, end)
            return selected_text
        except tk.TclError:
            return ""

    def syntax_highlighter(self) -> None:
        style = get_style_by_name(app.theme.syntax_style)
        parsed = style.list_styles()

        for key in parsed:
            if key[1]["color"] != "" and key[1]["color"] is not None:
                color = "#" + key[1]["color"]
                self.text.tag_config(str(key[0]), foreground=color)

        lexer = get_lexer_by_name(self.language, stripall=True)
        tokens = list(lexer.get_tokens(self.content))

        for text in tokens:
            self.text.insert(tk.END, text[1], str(text[0]))

        last_line_index = self.text.index("end-1c linestart")
        last_line_text = self.text.get(last_line_index, "end-1c")

        if not last_line_text.strip():
            self.text.delete(last_line_index, "end")
