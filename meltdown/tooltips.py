# Modules
from .app import app
from .args import args
from . import timeutils

# Standard
import re
import tkinter as tk
from typing import Any, Optional, List


def clean_string(text: str) -> str:
    return re.sub(r" +", " ", text).strip()


class ToolTip:
    tooltips: List["ToolTip"] = []
    current_tooltip: Optional["ToolTip"] = None
    block_date = 0.0

    @staticmethod
    def hide_all() -> None:
        if ToolTip.current_tooltip:
            ToolTip.current_tooltip.hide()

    @staticmethod
    def block() -> None:
        ToolTip.block_date = timeutils.now()

    @staticmethod
    def get_tooltip(widget: tk.Widget) -> Optional["ToolTip"]:
        for tooltip in ToolTip.tooltips:
            if tooltip.widget == widget:
                return tooltip

        return None

    def __init__(self, widget: tk.Widget, text: str, bind: bool = True) -> None:
        self.debouncer = ""
        self.widget = widget
        self.delay = 600
        self.text = clean_string(text)
        self.tooltip: Optional[tk.Frame] = None
        self.current_event: Optional[Any] = None

        if bind:
            self.widget.bind("<Enter>", lambda e: self.schedule())
            self.widget.bind("<Leave>", lambda e: self.hide())
            self.widget.bind("<Button>", lambda e: self.hide())

            def bind_scroll_events(widget: tk.Widget) -> None:
                widget.bind("<Motion>", lambda e: self.update_event(e))

                for child in widget.winfo_children():
                    bind_scroll_events(child)

            bind_scroll_events(self.widget)

        ToolTip.tooltips.append(self)

    def direct(self, event: Any) -> None:
        self.current_event = event
        ToolTip.current_tooltip = self
        self.show()

    def update_event(self, event: Any) -> None:
        if not args.tooltips:
            return

        self.current_event = event

    def schedule(self) -> None:
        if not args.tooltips:
            return

        ToolTip.hide_all()

        if (timeutils.now() - ToolTip.block_date) < 0.8:
            return

        self.debouncer = self.widget.after(self.delay, lambda: self.show())
        ToolTip.current_tooltip = self

    def show(self) -> None:
        event = self.current_event

        if event is None:
            return

        self.tooltip = tk.Frame(app.main_frame)
        self.tooltip.configure(background=app.theme.tooltip_border)
        self.tooltip.lift()
        padding = app.theme.tooltip_padding

        label = tk.Label(self.tooltip, text=self.text, font=app.theme.font_tooltips,
                         background=app.theme.tooltip_background, foreground=app.theme.tooltip_foreground,
                         wraplength=480, justify=tk.LEFT, padx=padding, pady=padding)

        bwidth = app.theme.tooltip_border_width
        label.pack(padx=bwidth, pady=bwidth)
        label.bind("<Button-1>", lambda e: self.hide())

        self.tooltip.update_idletasks()
        window_width = app.main_frame.winfo_width()
        window_height = app.main_frame.winfo_height()
        tooltip_width = self.tooltip.winfo_reqwidth()
        tooltip_height = self.tooltip.winfo_reqheight()
        x = event.x_root - app.main_frame.winfo_rootx() - (tooltip_width // 2)
        y = event.y_root - app.main_frame.winfo_rooty() + 20

        if x < 0:
            x = 0
        elif x + tooltip_width > window_width:
            x = window_width - tooltip_width

        if y < 0:
            y = 0
        elif y + tooltip_height > window_height:
            y = event.y_root - app.main_frame.winfo_rooty() - tooltip_height - 20

        self.tooltip.place(x=x, y=y)

    def hide(self) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.debouncer:
            self.widget.after_cancel(self.debouncer)
            self.debouncer = ""

        ToolTip.current_tooltip = None
        self.current_event = None

    def set_text(self, text: str) -> None:
        self.text = clean_string(text)

    def append_text(self, text: str) -> None:
        self.text += f" {clean_string(text)}"
