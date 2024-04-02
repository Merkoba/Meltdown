# Modules
from .app import app
from .config import config
from .tooltips import ToolTip

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any


class EntryBox(ttk.Entry):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.focused = False
        self.placeholder = ""
        self.key = ""

        self.bind("<FocusIn>", lambda e: self.on_focus_change("in"))
        self.bind("<FocusOut>", lambda e: self.on_focus_change("out"))
        self.bind("<Control-KeyPress-a>", lambda e: self.select_all())

        self.text_var = tk.StringVar()
        self.text_var.set("")
        self.trace_id = self.text_var.trace_add("write", self.on_write)
        self.configure(textvariable=self.text_var)
        self.placeholder_active = False
        self.name = ""

    def bind_mousewheel(self) -> None:
        self.bind("<Button-4>", lambda e: self.on_mousewheel("up"))
        self.bind("<Button-5>", lambda e: self.on_mousewheel("down"))

    def on_mousewheel(self, direction: str) -> None:
        units = 2

        if direction == "up":
            self.xview_scroll(-units, "units")
        elif direction == "down":
            self.xview_scroll(units, "units")

        ToolTip.hide_all()

    def set_name(self, name: str) -> None:
        self.name = name

    def get(self) -> str:
        if self.placeholder_active:
            return ""

        else:
            return self.text_var.get()

    def clear(self) -> None:
        self.set_text("")
        self.focus_set()

    def full_focus(self) -> None:
        self.focus_set()
        self.move_to_end()

    def move_to_end(self) -> None:
        self.icursor(tk.END)
        self.xview_moveto(1.0)

    def select_all(self) -> None:
        def do_select() -> None:
            self.selection_range(0, tk.END)
            self.icursor(tk.END)

        self.after_idle(lambda: do_select())

    def set_text(self, text: str, check_placeholder: bool = True) -> None:
        self.text_var.trace_remove("write", self.trace_id)
        self.delete(0, tk.END)
        self.insert(0, text)
        self.trace_id = self.text_var.trace_add("write", self.on_write)

        if check_placeholder:
            self.check_placeholder()

    def insert_text(self, text: str,
                    check_placeholder: bool = True,
                    index: str = "") -> None:
        if self.placeholder_active:
            self.delete(0, tk.END)

        if not index:
            index = tk.INSERT

        self.insert(index, text)

        if check_placeholder:
            self.check_placeholder()

    def delete_text(self, start: int, chars: int) -> None:
        self.delete(start, (start + chars))

    def on_focus_change(self, mode: str) -> None:
        if mode == "out":
            if self.key and (not self.placeholder_active):
                config.update(self.key)

            self.selection_clear()
            self.focused = False
        elif mode == "in":
            self.focused = True

        self.check_placeholder()

    def enable_placeholder(self) -> None:
        if self.placeholder_active:
            return

        self.placeholder_active = True
        self.set_text(self.placeholder, check_placeholder=False)
        self.configure(foreground=app.theme.entry_placeholder_color)

    def disable_placeholder(self) -> None:
        if not self.placeholder_active:
            return

        self.placeholder_active = False

        if self.text_var.get() == self.placeholder:
            self.set_text("", check_placeholder=False)

        self.configure(foreground=app.theme.entry_foreground)

    def check_placeholder(self) -> None:
        if not self.placeholder:
            return

        if self.focused:
            self.disable_placeholder()
        elif self.placeholder_active:
            if self.text_var.get() != self.placeholder:
                self.disable_placeholder()
        elif not self.text_var.get():
            self.enable_placeholder()

    def on_write(self, *args: Any) -> None:
        self.check_placeholder()
