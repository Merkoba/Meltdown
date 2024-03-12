# Modules
from .app import app
from .config import config

# Standard
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Any, Optional


class MenuItem:
    def __init__(self, text: str,
                 command: Optional[Callable[..., Any]] = None,
                 separator: bool = False, disabled: bool = False):
        self.text = text
        self.command = command
        self.separator = separator
        self.disabled = disabled


class Menu:
    current_menu: Optional["Menu"] = None
    current_widget: Optional[tk.Widget] = None
    current_command: Optional[Callable[..., Any]] = None

    @staticmethod
    def hide_all() -> None:
        if Menu.current_menu:
            Menu.current_menu.hide()

    def __init__(self) -> None:
        self.menu: Optional[tk.Frame] = None
        self.items: List[MenuItem] = []

    def add(self, text: str, command: Optional[Callable[..., Any]] = None, disabled: bool = False) -> None:
        self.items.append(MenuItem(text, command, disabled=disabled))

    def separator(self) -> None:
        self.items.append(MenuItem("", lambda: None, separator=True))

    def clear(self) -> None:
        self.items = []

    def make(self, event: Any) -> None:
        self.menu = tk.Frame(bg="white")
        self.menu.lift()

        Menu.current_widget = None
        Menu.current_command = None

        def cmd() -> None:
            if Menu.current_command:
                self.hide()
                Menu.current_command()

        def on_motion(event: Any) -> None:
            widget = event.widget.winfo_containing(event.x_root, event.y_root)

            if not widget:
                return

            if isinstance(widget, ttk.Separator):
                return

            if Menu.current_widget != widget:
                if Menu.current_widget:
                    Menu.current_widget.event_generate("<<Custom-Leave>>")

                Menu.current_widget = widget

                if Menu.current_widget:
                    Menu.current_widget.event_generate("<<Custom-Enter>>")

        def make_item(item: MenuItem) -> None:
            if item.separator:
                separator = ttk.Separator(self.menu, orient="horizontal")
                separator.pack(expand=True, fill="x", padx=6, pady=2)
                separator.bind("<Motion>", lambda e: on_motion(e))
            else:
                frame = tk.Frame(self.menu, background="white")

                if item.disabled:
                    foreground = "#3D4555"
                    hover_background = "white"
                else:
                    foreground = "black"
                    hover_background = "lightgray"

                label = tk.Label(frame, text=item.text, background="white", foreground=foreground,
                                 wraplength=600, justify=tk.LEFT, anchor="w", font=config.font)

                def on_enter() -> None:
                    frame["background"] = hover_background
                    label["background"] = hover_background
                    Menu.current_command = item.command

                def on_leave() -> None:
                    frame["background"] = "white"
                    label["background"] = "white"

                frame.bind("<ButtonRelease-1>", lambda e: cmd())
                label.bind("<ButtonRelease-1>", lambda e: cmd())
                frame.bind("<Motion>", lambda e: on_motion(e))
                label.bind("<Motion>", lambda e: on_motion(e))
                frame.bind("<<Custom-Enter>>", lambda e: on_enter())
                label.bind("<<Custom-Enter>>", lambda e: on_enter())
                frame.bind("<<Custom-Leave>>", lambda e: on_leave())
                label.bind("<<Custom-Leave>>", lambda e: on_leave())
                label.pack(expand=True, fill="x", padx=6, pady=0)
                frame.pack(fill="x", expand=True)

        for item in self.items:
            make_item(item)

        self.menu.bind("<FocusOut>", lambda e: self.hide())

        self.menu.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        menu_width = self.menu.winfo_reqwidth()
        menu_height = self.menu.winfo_reqheight()
        x = event.x_root - app.root.winfo_rootx()
        y = event.y_root - app.root.winfo_rooty()

        if x < 0:
            x = 0
        elif x + menu_width > window_width:
            x = window_width - menu_width

        if y < 0:
            y = 0
        elif y + menu_height > window_height:
            y = window_height - menu_height

        self.menu.place(x=x, y=y)

    def show(self, event: Any) -> None:
        Menu.hide_all()

        def do_show() -> None:
            if self.menu:
                self.menu.update_idletasks()
                self.menu.focus_set()

        if not self.items:
            return

        self.make(event)
        Menu.current_menu = self
        app.root.after(100, do_show)

    def hide(self) -> None:
        if self.menu:
            self.menu.place_forget()
            self.menu.destroy()
            Menu.current_menu = None
