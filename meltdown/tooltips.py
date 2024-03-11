# Modules

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
        self.widget.bind("<Button-1>", self.hide_tooltip)
        self.id = ""

    def schedule_tooltip(self, event: Any) -> None:
        if ToolTip.current_tooltip is not None:
            ToolTip.current_tooltip.hide_tooltip()

        self.id = self.widget.after(500, lambda: self.show_tooltip(event))
        ToolTip.current_tooltip = self

    def show_tooltip(self, event: Any) -> None:
        from .widgets import widgets

        if widgets.menu_open:
            return

        box: Optional[Tuple[int, int, int, int]] = None

        if isinstance(self.widget, ttk.Combobox):
            box = self.widget.bbox("insert")
        elif isinstance(self.widget, ttk.Entry):
            box = self.widget.bbox(0)
        else:
            box = self.widget.bbox()

        if not box:
            return

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        label = tk.Label(self.tooltip, text=self.text, background="white",
                         wraplength=250, justify=tk.LEFT)
        label.pack()

        self.tooltip.update_idletasks()
        width = self.tooltip.winfo_reqwidth()
        x, y, _, _ = box
        y += self.widget.winfo_rooty() + 25
        x = event.x_root - width if event.x_root - width > 0 else event.x_root
        self.tooltip.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event: Any = None) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = ""

        ToolTip.current_tooltip = None
