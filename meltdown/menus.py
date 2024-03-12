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
        self.container: Optional[tk.Frame] = None
        self.items: List[MenuItem] = []

    def add(self, text: str, command: Optional[Callable[..., Any]] = None, disabled: bool = False) -> None:
        self.items.append(MenuItem(text, command, disabled=disabled))

    def separator(self) -> None:
        self.items.append(MenuItem("", lambda: None, separator=True))

    def clear(self) -> None:
        self.items = []

    def make(self, event: Any) -> None:
        self.root = tk.Canvas(app.root, bg="white", borderwidth=0, highlightthickness=0)
        self.container = tk.Frame(self.root, bg="white", borderwidth=0)
        self.root.create_window((0, 0), window=self.container, anchor="nw")

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

        def on_mousewheel(event: Any) -> None:
            if not self.container:
                return

            y_top = self.container.winfo_y()
            y_bottom = y_top + self.container.winfo_height()
            height = self.root.winfo_height()
            distance = height - y_bottom

            if event.num == 4:
                if y_top >= 0:
                    return

                self.root.yview_scroll(-1, "units")  # Scroll up
            elif event.num == 5:
                if distance >= 0:
                    return

                self.root.yview_scroll(1, "units")  # Scroll down

        self.container.bind("<Button-4>", on_mousewheel)
        self.container.bind("<Button-5>", on_mousewheel)

        def make_item(item: MenuItem) -> None:
            if item.separator:
                separator = ttk.Separator(self.container, orient="horizontal")
                separator.pack(expand=True, fill="x", padx=6, pady=2)
                separator.bind("<Motion>", lambda e: on_motion(e))
                separator.bind("<Button-4>", on_mousewheel)
                separator.bind("<Button-5>", on_mousewheel)
            else:
                frame = tk.Frame(self.container, background="white", borderwidth=0)

                if item.disabled:
                    foreground = "#3D4555"
                    hover_background = "white"
                else:
                    foreground = "black"
                    hover_background = "lightgray"

                label = tk.Label(frame, text=item.text, background="white", foreground=foreground,
                                 wraplength=600, justify=tk.LEFT, anchor="w", font=config.font, borderwidth=0)

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
                label.bind("<Button-4>", on_mousewheel)
                label.bind("<Button-5>", on_mousewheel)
                label.pack(expand=True, fill="x", padx=6, pady=0)
                frame.pack(fill="x", expand=True)

        for item in self.items:
            make_item(item)

        self.root.bind("<FocusOut>", lambda e: self.hide())

        self.root.update_idletasks()
        self.container.update_idletasks()

        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()

        # Limit width to fit the container
        self.root.config(width=self.container.winfo_reqwidth())

        # Limit height to 500 or window height if smaller
        h = min(window_height, min(500, self.container.winfo_reqheight()))
        self.root.config(height=h)

        menu_width = self.root.winfo_reqwidth()
        menu_height = self.root.winfo_reqheight()
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

        self.root.place(x=x, y=y)

    def show(self, event: Any) -> None:
        Menu.hide_all()

        if not self.items:
            return

        self.make(event)

        if self.root:
            self.root.update_idletasks()
            self.root.focus_set()
            Menu.current_menu = self

    def hide(self) -> None:
        if self.root:
            self.root.place_forget()
            self.root.destroy()
            Menu.current_menu = None
