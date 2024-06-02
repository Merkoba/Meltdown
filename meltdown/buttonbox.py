from __future__ import annotations

# Standard
import inspect
import tkinter as tk
from typing import Any, Optional
from collections.abc import Callable

# Modules
from .app import app
from .menus import Menu


class ButtonBox(tk.Frame):
    def __init__(
        self,
        parent: tk.Frame,
        text: str,
        command: Optional[Callable[..., Any]] = None,
        when: Optional[str] = None,
        style: Optional[str] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(parent)
        self.text = text
        style = style if style else "normal"
        when = when if when else "<ButtonRelease-1>"
        self.custom_width = width is not None
        self.width = width if width else app.theme.button_width
        self.command = command
        self.make()
        self.set_style(style)

        if command:
            self.set_bind(when, command)

    def prepare_text(self, text: str) -> str:
        if (not self.custom_width) and (len(text) < 4):
            space = " "
            text = f"{space}{text}{space}"

        return text

    def make(self) -> None:
        pady = 0
        padx = app.theme.button_padx
        text = self.prepare_text(self.text)

        self.label = tk.Label(
            self, text=text, font=app.theme.font("button"), padx=padx, pady=pady
        )

        self.label.grid(sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label.bind("<Enter>", lambda e: self.on_enter())
        self.label.bind("<Leave>", lambda e: self.on_leave())

    def on_enter(self) -> None:
        if self.style == "normal":
            self.set_background(app.theme.button_hover_background)
        elif self.style == "highlight":
            self.set_background(app.theme.button_highlight_hover_background)
        elif self.style == "active":
            self.set_background(app.theme.button_active_hover_background)
        elif self.style == "alt":
            self.set_background(app.theme.button_alt_hover_background)

    def on_leave(self) -> None:
        if self.style == "normal":
            self.set_background(app.theme.button_background)
        elif self.style == "highlight":
            self.set_background(app.theme.button_highlight_background)
        elif self.style == "active":
            self.set_background(app.theme.button_active_background)
        elif self.style == "disabled":
            self.set_background(app.theme.button_disabled_background)
        elif self.style == "alt":
            self.set_background(app.theme.button_alt_background)

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
                if (when == "<Button-1>") or (when == "<ButtonRelease-1>"):
                    Menu.hide_all()
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
        self.label.configure(foreground=app.theme.button_foreground)

        if style == "normal":
            self.set_background(app.theme.button_background)
            self.configure(cursor="hand2")
        elif style == "highlight":
            self.set_background(app.theme.button_highlight_background)
            self.configure(cursor="hand2")
        elif style == "active":
            self.set_background(app.theme.button_active_background)
            self.configure(cursor="hand2")
        elif style == "disabled":
            self.set_background(app.theme.button_disabled_background)
            self.configure(cursor="arrow")
        elif style == "alt":
            self.set_background(app.theme.button_alt_background)
            self.configure(cursor="hand2")

        self.style = style

    def set_text(self, text: str) -> None:
        self.text = text.strip()
        text = self.prepare_text(self.text)
        self.label.configure(text=text)

    def get_text(self) -> str:
        return self.text

    def set_font(self, font: tuple[str, int, str]) -> None:
        self.label.configure(font=font)
