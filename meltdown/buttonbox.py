# Modules
from .config import config

# Standard
import inspect
import tkinter as tk
from typing import Any, Callable, Optional


class ButtonBox(tk.Frame):
    def __init__(self, parent: tk.Frame, text: str,
                 command: Optional[Callable[..., Any]] = None,
                 when: Optional[str] = None, style: Optional[str] = None,
                 width: Optional[int] = None, bigger: bool = False) -> None:
        super().__init__(parent)
        self.text = text
        self.bigger = bigger
        style = style if style else "normal"
        when = when if when else "<ButtonRelease-1>"
        self.width = width if width else config.button_width
        self.make()
        self.set_style(style)

        if command:
            self.set_bind(when, command)

    def make(self) -> None:
        padx = 0
        pady = 3 if self.bigger else 0

        self.label = tk.Label(self, text=self.text,
                              font=config.font_button, width=self.width,
                              cursor="hand2", padx=padx, pady=pady)
        self.label.grid(sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label.bind("<Enter>", lambda e: self.on_enter())
        self.label.bind("<Leave>", lambda e: self.on_leave())

    def on_enter(self) -> None:
        if self.style == "normal":
            self.set_background(config.button_background_hover)
        elif self.style == "green":
            self.set_background(config.green_button_background_hover)
        elif self.style == "alt":
            self.set_background(config.button_background_hover_alt)

    def on_leave(self) -> None:
        if self.style == "normal":
            self.set_background(config.button_background)
        elif self.style == "green":
            self.set_background(config.green_background)
        elif self.style == "disabled":
            self.set_background(config.background_disabled)
        elif self.style == "alt":
            self.set_background(config.button_background_alt)

    def set_background(self, color: str) -> None:
        self.configure(background=color)
        self.label.configure(background=color)

    def set_bind(self, when: str, command: Callable[..., Any]) -> None:
        # Check if press/release happens on top of the button
        def on_top(event: Any) -> bool:
            widget = event.widget
            x = widget.winfo_x()
            y = widget.winfo_y()
            width = widget.winfo_width()
            height = widget.winfo_height()
            return bool((x <= event.x <= x + width) and (y <= event.y <= y + height))

        def cmd(event: Any) -> None:
            if self.style == "disabled":
                return

            if not on_top(event):
                return

            event.widget.focus_set()

            if inspect.signature(command).parameters:
                command(event)
            else:
                command()

        self.bind(when, lambda e: cmd(e))
        self.label.bind(when, lambda e: cmd(e))

    def set_style(self, style: str) -> None:
        self.label.configure(foreground=config.button_foreground)

        if style == "normal":
            self.set_background(config.button_background)
        elif style == "green":
            self.set_background(config.green_background)
        elif style == "disabled":
            self.set_background(config.background_disabled)
        elif style == "alt":
            self.set_background(config.button_background_alt)

        self.style = style

    def set_text(self, text: str) -> None:
        self.label.configure(text=text)

    def set_font(self, font: str) -> None:
        self.label.configure(font=font)
