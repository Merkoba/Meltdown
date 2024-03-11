# Modules
from .app import app

# Standard
import re
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, Tuple


def clean_string(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class ToolTip:
    current_tooltip: Optional["ToolTip"] = None

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = clean_string(text)
        self.tooltip: Optional[tk.Toplevel] = None
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

        self.id = self.widget.after(400, lambda: self.show_tooltip())
        ToolTip.current_tooltip = self

    def show_tooltip(self) -> None:
        from .widgets import widgets
        event = self.current_event

        if widgets.menu_open:
            return

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.withdraw()
        label = tk.Label(self.tooltip, text=self.text, background="white",
                         wraplength=250, justify=tk.LEFT)
        label.pack()

        self.tooltip.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        tooltip_width = self.tooltip.winfo_reqwidth()
        tooltip_height = self.tooltip.winfo_reqheight()
        window_x = app.root.winfo_x()
        window_y = app.root.winfo_y()
        left_edge = window_x
        right_edge = window_x + window_width
        top_edge = window_y
        bottom_edge = window_y + window_height
        x = event.x_root - (tooltip_width // 2)
        y = event.y_root + 20

        if x < left_edge:
            x = left_edge
        elif x + tooltip_width > right_edge:
            x = right_edge - tooltip_width

        if y < top_edge:
            y = top_edge
        elif y + tooltip_height > bottom_edge:
            y = event.y_root - tooltip_height - 20

        self.tooltip.wm_geometry(f"+{x}+{y}")

        def show() -> None:
            if self.tooltip:
                self.tooltip.deiconify()

        app.root.after(100, lambda: show())

    def hide_tooltip(self, event: Any = None) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = ""

        ToolTip.current_tooltip = None
