# Standard
import tkinter as tk
from typing import Any, Callable

# Modules
from .args import args


class Gestures:
    def __init__(
        self, widget: tk.Widget, text: tk.Text, on_right_click: Callable[..., Any]
    ) -> None:
        self.on_right_click = on_right_click
        self.text = text

        def bind_events(wid: tk.Widget) -> None:
            self.bind(wid)

            for child in wid.winfo_children():
                bind_events(child)

        bind_events(widget)

    def bind(self, widget: tk.Widget) -> None:
        widget.bind("<ButtonPress-3>", lambda e: self.start_drag(e))
        widget.bind("<B3-Motion>", lambda e: self.on_drag(e))
        widget.bind("<ButtonRelease-3>", lambda e: self.on_drag_end(e))

    def reset_drag(self) -> None:
        self.drag_x_start = 0
        self.drag_y_start = 0
        self.drag_x = 0
        self.drag_y = 0

    def start_drag(self, event: Any) -> None:
        self.drag_x_start = event.x
        self.drag_y_start = event.y
        self.drag_x = event.x
        self.drag_y = event.y

    def on_drag(self, event: Any) -> str:
        self.drag_x = event.x
        self.drag_y = event.y
        return "break"

    def on_drag_end(self, event: Any) -> None:
        from .display import display
        from .keyboard import keyboard

        if args.gestures:
            x_diff = abs(self.drag_x - self.drag_x_start)
            y_diff = abs(self.drag_y - self.drag_y_start)

            if x_diff > y_diff:
                if x_diff >= args.gesture_threshold:
                    if self.drag_x < self.drag_x_start:
                        if keyboard.shift:
                            display.select_first_tab()
                        else:
                            display.tab_left()
                    else:
                        if keyboard.shift:
                            display.select_last_tab()
                        else:
                            display.tab_right()

                    return
            elif y_diff >= args.gesture_threshold:
                if self.drag_y < self.drag_y_start:
                    display.to_top()
                else:
                    display.to_bottom()

                return

        if event.widget == self.text:
            self.on_right_click(event)
