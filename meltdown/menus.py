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

    @staticmethod
    def setup() -> None:
        app.root.bind("<Button-1>", lambda e: Menu.hide_all())

    @staticmethod
    def hide_all() -> None:
        if Menu.current_menu:
            Menu.current_menu.hide()

    def __init__(self) -> None:
        self.menu: Optional[tk.Toplevel] = None
        self.items: List[MenuItem] = []

    def add(self, text: str, command: Optional[Callable[..., Any]] = None, disabled: bool = False) -> None:
        self.items.append(MenuItem(text, command, disabled=disabled))

    def separator(self) -> None:
        self.items.append(MenuItem("", lambda: None, separator=True))

    def clear(self) -> None:
        self.items = []

    def make(self, event: Any) -> None:
        self.menu = tk.Toplevel(app.root, bg="white")
        self.menu.wm_overrideredirect(True)
        self.menu.withdraw()
        self.menu.lift()

        def make_item(item: MenuItem) -> None:

            if item.separator:
                separator = ttk.Separator(self.menu, orient="horizontal")
                separator.pack(expand=True, fill="x", padx=6, pady=2)
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

                def cmd() -> None:
                    if item.command:
                        self.hide()
                        item.command()

                def on_enter() -> None:
                    frame["background"] = hover_background
                    label["background"] = hover_background

                def on_leave() -> None:
                    frame["background"] = "white"
                    label["background"] = "white"

                frame.bind("<ButtonRelease-1>", lambda e: cmd())
                label.bind("<ButtonRelease-1>", lambda e: cmd())
                frame.bind("<Enter>", lambda e: on_enter())
                frame.bind("<Leave>", lambda e: on_leave())
                label.pack(expand=True, fill="x", padx=6, pady=2)

                frame.pack(fill="x", expand=True)

        for item in self.items:
            make_item(item)

        self.menu.bind("<FocusOut>", lambda e: self.hide())

        x = event.x_root
        y = event.y_root

        self.menu.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        menu_width = self.menu.winfo_reqwidth()
        menu_height = self.menu.winfo_reqheight()
        window_x = app.root.winfo_x()
        window_y = app.root.winfo_y()
        left_edge = window_x
        right_edge = window_x + window_width
        top_edge = window_y
        bottom_edge = window_y + window_height
        x = event.x_root - (menu_width // 2)
        y = event.y_root + 20

        if x < left_edge:
            x = left_edge
        elif x + menu_width > right_edge:
            x = right_edge - menu_width

        if y < top_edge:
            y = top_edge
        elif y + menu_height > bottom_edge:
            y = event.y_root - menu_height

        self.menu.geometry("+%d+%d" % (x, y))

    def show(self, event: Any) -> None:
        Menu.hide_all()

        def do_show() -> None:
            if self.menu:
                self.menu.update_idletasks()
                self.menu.deiconify()
                self.menu.transient(app.root)
                self.menu.update()
                self.menu.wait_window()

        if not self.items:
            return

        self.make(event)
        Menu.current_menu = self
        app.root.after(100, do_show)

    def hide(self) -> None:
        if self.menu:
            self.menu.destroy()
            Menu.current_menu = None
