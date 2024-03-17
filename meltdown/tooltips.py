# Modules
from .app import app
from .menus import Menu
from . import timeutils

# Standard
import re
import tkinter as tk
from typing import Any, Optional


def clean_string(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class ToolTip:
    current_tooltip: Optional["ToolTip"] = None
    block_date = 0.0

    @staticmethod
    def block() -> None:
        ToolTip.block_date = timeutils.now()

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.id = ""
        self.widget = widget
        self.delay = 600
        self.text = clean_string(text)
        self.tooltip: Optional[tk.Frame] = None
        self.current_event: Optional[Any] = None

        self.widget.bind("<Enter>", lambda e: self.schedule_tooltip())
        self.widget.bind("<Leave>", lambda e: self.hide_tooltip())
        self.widget.bind("<Button-1>", lambda e: self.hide_tooltip())

        def bind_scroll_events(widget: tk.Widget) -> None:
            widget.bind("<Motion>", lambda e: self.update_event(e))

            for child in widget.winfo_children():
                bind_scroll_events(child)

        bind_scroll_events(self.widget)

    def update_event(self, event: Any) -> None:
        self.current_event = event

    def schedule_tooltip(self) -> None:
        if ToolTip.current_tooltip is not None:
            ToolTip.current_tooltip.hide_tooltip()

        if (timeutils.now() - ToolTip.block_date) < 0.8:
            return

        self.id = self.widget.after(self.delay, lambda: self.show_tooltip())
        ToolTip.current_tooltip = self

    def show_tooltip(self) -> None:
        event = self.current_event

        if event is None:
            return

        if Menu.current_menu:
            return

        self.tooltip = tk.Frame(app.root)
        self.tooltip.lift()
        label = tk.Label(self.tooltip, text=self.text, background="white",
                         wraplength=250, justify=tk.LEFT)
        label.pack()

        self.tooltip.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        tooltip_width = self.tooltip.winfo_reqwidth()
        tooltip_height = self.tooltip.winfo_reqheight()
        x = event.x_root - app.root.winfo_rootx() - (tooltip_width // 2)
        y = event.y_root - app.root.winfo_rooty() + 20

        if x < 0:
            x = 0
        elif x + tooltip_width > window_width:
            x = window_width - tooltip_width

        if y < 0:
            y = 0
        elif y + tooltip_height > window_height:
            y = event.y_root - app.root.winfo_rooty() - tooltip_height - 20

        self.tooltip.place(x=x, y=y)

    def hide_tooltip(self) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = ""

        ToolTip.current_tooltip = None
        self.current_event = None
