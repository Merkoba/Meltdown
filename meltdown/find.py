# Modules
from .app import app
from .buttonbox import ButtonBox
from .entrybox import EntryBox
from .output import Output
from .tooltips import ToolTip

# Standard
import tkinter as tk
import re
from typing import Optional


class Find:
    def __init__(self, parent: tk.Frame, widget: Output) -> None:
        self.parent = parent
        self.widget = widget
        self.root = tk.Frame(parent)
        self.inner = tk.Frame(self.root)
        self.root.configure(background=app.theme.find_background)
        self.inner.configure(background=app.theme.find_background)
        self.entry = EntryBox(self.inner, style="Normal.TEntry", font=app.theme.font)
        self.entry.set_name("find")
        ToolTip(self.entry, "Enter some text and hit Enter")
        self.entry.grid(row=0, column=0, sticky="ew", padx=4)
        self.entry.bind("<Return>", lambda e: self.find_next())
        self.entry.bind("<Escape>", lambda e: self.on_esc())
        self.entry.placeholder = "Find..."
        self.entry.check_placeholder()
        self.current_match: Optional[str] = None
        self.next_i_button = ButtonBox(self.inner, "Next (i)", lambda: self.find_next())
        ToolTip(self.next_i_button, "Find next match (case insensitive)")
        self.next_i_button.grid(row=0, column=1, sticky="ew", padx=4)
        self.next_ci_button = ButtonBox(self.inner, "Next", lambda: self.find_next(False))
        ToolTip(self.next_ci_button, "Find next match (case sensitive)")
        self.next_ci_button.grid(row=0, column=2, sticky="ew", padx=4)
        self.hide_button = ButtonBox(self.inner, "Hide", lambda: self.hide())
        ToolTip(self.hide_button, "Hide the find bar")
        self.hide_button.grid(row=0, column=3, sticky="ew", padx=4)
        self.inner.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        self.root.grid(row=2, column=0, sticky="ew")
        self.root.grid_remove()

    def find_next(self, case_insensitive: bool = True, no_match: bool = False) -> None:
        self.clear()
        query = self.entry.get()

        if not query:
            return

        if self.current_match is not None:
            start_pos = self.widget.index(f"{self.current_match}+1c")
        else:
            start_pos = "1.0"

        content = self.widget.get(start_pos, "end")

        if case_insensitive:
            match = re.search(query, content, re.IGNORECASE)
        else:
            match = re.search(query, content)

        if match:
            start, end = match.span()
            start_index = self.widget.index(f"{start_pos}+{start}c")
            end_index = self.widget.index(f"{start_pos}+{end}c")
            self.widget.tag_add("find", start_index, end_index)
            self.widget.tag_config("find", background=app.theme.find_match_background)
            self.widget.tag_config("find", foreground=app.theme.find_match_foreground)
            self.widget.see(start_index)
            self.current_match = start_index
        else:
            self.current_match = None

            if no_match:
                return

            self.find_next(case_insensitive, True)

    def clear(self) -> None:
        self.widget.tag_remove("find", "1.0", "end")

    def show(self) -> None:
        self.root.grid()
        self.entry.set_text("")
        self.entry.focus_set()

    def hide(self) -> None:
        self.clear()
        self.root.grid_remove()

    def on_esc(self) -> None:
        if self.entry.get():
            self.entry.clear()
        else:
            self.hide()
