# Modules
from .config import config

# Standard
import inspect
import tkinter as tk
from typing import Any, Callable, Optional


class ButtonBox(tk.Frame):
    def __init__(self, parent: tk.Frame, text: str, command: Optional[Callable[..., Any]] = None) -> None:
        super().__init__(parent)
        self.text = text
        self.make()
        self.style("normal")

        if command:
            self.set_bind("<Button-1>", command)

    def make(self) -> None:
        self.label = tk.Label(self, text=self.text, font=config.font_button, width=7)
        self.label.grid(sticky="nsew", padx=6)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label.bind("<Enter>", lambda e: self.on_enter())
        self.label.bind("<Leave>", lambda e: self.on_leave())

    def on_enter(self) -> None:
        if self.mode == "normal":
            self.set_background(config.button_background_hover)
        elif self.mode == "green":
            self.set_background(config.green_button_background_hover)

    def on_leave(self) -> None:
        if self.mode == "normal":
            self.set_background(config.button_background)
        elif self.mode == "green":
            self.set_background(config.green_background)
        elif self.mode == "disabled":
            self.set_background(config.background_disabled)

    def set_background(self, color: str) -> None:
        self.configure(background=color)
        self.label.configure(background=color)

    def set_bind(self, when: str, command: Callable[..., Any]) -> None:
        if inspect.signature(command).parameters:
            self.bind(when, lambda e: command(e))
            self.label.bind(when, lambda e: command(e))
        else:
            self.bind(when, lambda e: command())
            self.label.bind(when, lambda e: command())

    def style(self, mode: str) -> None:
        self.label.configure(foreground=config.button_foreground)

        if mode == "normal":
            self.set_background(config.button_background)
        elif mode == "green":
            self.set_background(config.green_background)
        elif mode == "disabled":
            self.set_background(config.background_disabled)

        self.mode = mode

    def set_text(self, text: str) -> None:
        self.label.configure(text=text)
