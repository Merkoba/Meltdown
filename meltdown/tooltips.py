# Modules
from .app import app
from .menus import Menu

# Standard
import re
import tkinter as tk
from typing import Any, Optional


def clean_string(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class ToolTip:
    current_tooltip: Optional["ToolTip"] = None

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = clean_string(text)
        self.tooltip: Optional[tk.Frame] = None
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.update_event)
        self.widget.bind("<Button-1>", self.hide_tooltip)
        self.id = ""

    def update_event(self, event: Any) -> None:
        self.current_event = event

    def schedule_tooltip(self, event: Any) -> None:
        if ToolTip.current_tooltip is not None:
            ToolTip.current_tooltip.hide_tooltip()

        self.id = self.widget.after(500, lambda: self.show_tooltip())
        ToolTip.current_tooltip = self

    def show_tooltip(self) -> None:
        event = self.current_event

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

    def hide_tooltip(self, event: Any = None) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = ""

        ToolTip.current_tooltip = None
