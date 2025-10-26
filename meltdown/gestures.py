from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any
from collections.abc import Callable

# Modules
from .args import args
from .commands import commands
from .menus import Menu


class Gestures:
    def __init__(
        self,
        widget: tk.Widget,
        text: tk.Text,
        on_right_click: Callable[..., Any],
    ) -> None:
        self.on_right_click = on_right_click
        self.text = text

        def bind_events(wid: tk.Widget | tk.Toplevel) -> None:
            self.bind(wid)

            for child in wid.winfo_children():
                bind_events(child)

        bind_events(widget)

    def bind(self, widget: tk.Widget | tk.Toplevel) -> None:
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
        if args.gestures:
            x_diff = abs(self.drag_x - self.drag_x_start)
            y_diff = abs(self.drag_y - self.drag_y_start)

            if x_diff > y_diff:
                if x_diff >= args.gestures_threshold:
                    if (self.drag_x < self.drag_x_start) and args.gestures_left:
                        Menu.hide_all()
                        commands.exec(args.gestures_left)
                    elif args.gestures_right:
                        commands.exec(args.gestures_right)

                    return
            elif y_diff >= args.gestures_threshold:
                if (self.drag_y < self.drag_y_start) and args.gestures_up:
                    Menu.hide_all()
                    commands.exec(args.gestures_up)
                elif args.gestures_down:
                    Menu.hide_all()
                    commands.exec(args.gestures_down)

                return

        if event.widget == self.text:
            self.on_right_click(event)
