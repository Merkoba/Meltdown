# Modules
from .config import config

# Standard
import inspect
import tkinter as tk
from typing import Any, Callable, Optional


class ButtonBox(tk.Frame):
    def __init__(self, parent: tk.Frame, text: str,
                 command: Optional[Callable[..., Any]] = None, when: str = "release") -> None:
        super().__init__(parent)
        self.text = text
        self.make()
        self.style("normal")

        if command:
            self.set_bind(when, command)

    def make(self) -> None:
        self.label = tk.Label(self, text=self.text, font=config.font_button, width=8, cursor="hand2")
        self.label.grid(sticky="nsew")
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
        if when == "release":
            when_ = "<ButtonRelease-1>"
        else:
            when_ = "<Button-1>"

        # Check if press/release happens on top of the button
        def on_top(event: Any) -> bool:
            widget = event.widget
            x = widget.winfo_x()
            y = widget.winfo_y()
            width = widget.winfo_width()
            height = widget.winfo_height()
            return bool((x <= event.x <= x + width) and (y <= event.y <= y + height))

        def cmd(event: Any) -> None:
            if not on_top(event):
                return

            if inspect.signature(command).parameters:
                command(event)
            else:
                command()

        self.bind(when_, lambda e: cmd(e))
        self.label.bind(when_, lambda e: cmd(e))

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
