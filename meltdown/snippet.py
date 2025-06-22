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
from .model import model
from .inputcontrol import inputcontrol
from .dialogs import Dialog
from .variables import variables


class SnippetLabel(tk.Label):
    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent, text=text)

        font = app.theme.get_output_font(True)
        fg_color = app.theme.snippet_header_foreground
        bg_color = app.theme.snippet_header_background

        self.configure(font=font)
        self.configure(cursor="arrow")
        self.pack(side=tk.LEFT, padx=5)
        self.configure(foreground=fg_color)
        self.configure(background=bg_color)


class SnippetButton(tk.Label):
    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent, text=text)

        font = app.theme.get_output_font(True)
        underline = app.theme.get_output_font(True, True)
        fg_color = app.theme.snippet_header_foreground
        bg_color = app.theme.snippet_header_background

        self.configure(font=font)
        self.configure(cursor="hand2")
        self.pack(side=tk.RIGHT, padx=5)
        self.configure(foreground=fg_color)
        self.configure(background=bg_color)

        def on_enter(event: Any) -> None:
            self.configure(font=underline)

        def on_leave(event: Any) -> None:
            self.configure(font=font)

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)


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

        self.header_text = SnippetLabel(self.header, header_text)
        self.header_copy = SnippetButton(self.header, "Copy")
        self.header_select = SnippetButton(self.header, "Select")
        self.header_find = SnippetButton(self.header, "Find")
        self.header_explain = SnippetButton(self.header, "Explain")
        self.header_view = SnippetButton(self.header, "View")
        self.header_use = SnippetButton(self.header, "Use")

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
        self.header_explain.bind("<Button-1>", lambda e: self.explain())
        self.header_use.bind("<Button-1>", lambda e: self.use_variable())
        self.header_view.bind("<Button-1>", lambda e: self.view_text())
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

    def get_sample(self) -> str:
        sample = self.content[0 : args.explain_sample]
        return sample.replace("\n", " ").strip()

    def explain(self) -> None:
        sample = self.get_sample()
        text = f"Explain this snippet: {sample}"
        model.stream({"text": text}, self.parent.tab_id)

    def use_variable(self) -> None:
        sample = self.get_sample()
        variables.do_set_variable("snippet", sample, feedback=False)
        v = variables.varname("snippet")
        inputcontrol.set(v)

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
        self.parent.display.unpick()

    def scroll_up(self) -> str:
        self.parent.scroll_up(True)
        return "break"

    def scroll_down(self) -> str:
        self.parent.scroll_down(True)
        return "break"

    def find(self) -> None:
        from .findmanager import findmanager

        app.hide_all()
        findmanager.find(tab_id=self.parent.tab_id, widget=self.text)

    def on_right_click(self, event: Any) -> None:
        self.parent.on_right_click(event, self.text)

    def view_text(self) -> None:
        text = self.content
        text = utils.remove_multiple_lines(text)

        def cmd_ok(text: str) -> None:
            pass

        Dialog.show_textbox("snippet_view", "Raw Text", cmd_ok, value=text)
