# Modules
from .config import config

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

        self.text_var = tk.StringVar()
        self.text_var.set("")
        self.trace_id = self.text_var.trace_add("write", self.on_write)
        self.configure(textvariable=self.text_var)
        self.placeholder_active = False

    def set_text(self, text: str, check_placeholder: bool = True) -> None:
        self.text_var.trace_remove("write", self.trace_id)
        self.delete(0, tk.END)
        self.insert(0, text)
        self.trace_id = self.text_var.trace_add("write", self.on_write)

        if check_placeholder:
            self.check_placeholder()

    def on_focus_change(self, mode: str) -> None:
        from . import state

        if mode == "out":
            if self.key and (not self.placeholder_active):
                state.update_config(self.key)

            self.focused = False
        elif mode == "in":
            self.focused = True

        self.check_placeholder()

    def enable_placeholder(self) -> None:
        if self.placeholder_active:
            return

        self.placeholder_active = True
        self.set_text(self.placeholder, check_placeholder=False)
        self.configure(foreground=config.placeholder_color)

    def disable_placeholder(self) -> None:
        if not self.placeholder_active:
            return

        self.placeholder_active = False

        if self.text_var.get() == self.placeholder:
            self.set_text("", check_placeholder=False)

        self.configure(foreground=config.entry_foreground)

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
