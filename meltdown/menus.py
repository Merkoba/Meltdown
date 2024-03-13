# Modules
from .app import app
from .config import config

# Standard
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Any, Optional, Dict


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

    def on_mousewheel(self, direction: str) -> None:
        if not self.container:
            return

        y_top = self.container.winfo_y()
        y_bottom = y_top + self.container.winfo_height()
        height = self.root.winfo_height()
        distance = height - y_bottom

        if direction == "up":
            if y_top >= 0:
                return

            self.root.yview_scroll(-1, "units")
        elif direction == "down":
            if distance >= 0:
                return

            self.root.yview_scroll(1, "units")

    def make(self, event: Any) -> None:
        self.root = tk.Canvas(app.root, bg="white", borderwidth=0, highlightthickness=0)
        self.container = tk.Frame(self.root, bg="white", borderwidth=0)
        self.root.create_window((0, 0), window=self.container, anchor="nw")
        self.current_widget = None

        def exec() -> None:
            if self.selected_index is not None:
                item = self.items[self.selected_index]

                if item.command:
                    item.command()

        def cmd() -> None:
            self.hide()

            if self.selected_index is not None:
                app.root.after(10, lambda: exec())

        def on_motion(event: Any) -> None:
            widget = event.widget.winfo_containing(event.x_root, event.y_root)

            if not widget:
                return

            if isinstance(widget, ttk.Separator):
                return

            if isinstance(widget, tk.Frame):
                return

            if self.current_widget != widget:
                if self.current_widget:
                    self.current_widget.event_generate("<<Custom-Leave>>")

                self.current_widget = widget

                if self.current_widget:
                    self.current_widget.event_generate("<<Custom-Enter>>")

        self.container.bind("<Button-4>", lambda e: self.on_mousewheel("up"))
        self.container.bind("<Button-5>", lambda e: self.on_mousewheel("down"))
        self.root.bind("<Escape>", lambda e: self.hide())
        self.root.bind("<Return>", lambda e: cmd())
        self.root.bind("<Up>", lambda e: self.arrow_up())
        self.root.bind("<Down>", lambda e: self.arrow_down())
        self.elements: Dict[int, Dict[str, Any]] = {}

        def make_item(item: MenuItem, i: int) -> None:
            if item.separator:
                separator = ttk.Separator(self.container, orient="horizontal")
                separator.pack(expand=True, fill="x", padx=6, pady=2)
                separator.bind("<Motion>", lambda e: on_motion(e))
                separator.bind("<Button-4>", lambda e: self.on_mousewheel("up"))
                separator.bind("<Button-5>", lambda e: self.on_mousewheel("down"))
            else:
                colors = self.get_colors(item)
                frame = tk.Frame(self.container, background=colors["background"], borderwidth=0)
                label = tk.Label(frame, text=item.text, background=colors["background"], foreground=colors["foreground"],
                                 wraplength=600, justify=tk.LEFT, anchor="w", font=config.font, borderwidth=0)

                self.elements[i] = {"item": item, "index": i, "frame": frame, "label": label}
                frame.bind("<ButtonRelease-1>", lambda e: cmd())
                label.bind("<ButtonRelease-1>", lambda e: cmd())
                frame.bind("<Motion>", lambda e: on_motion(e))
                label.bind("<Motion>", lambda e: on_motion(e))
                frame.bind("<<Custom-Enter>>", lambda e: self.on_enter(i))
                label.bind("<<Custom-Enter>>", lambda e: self.on_enter(i))
                frame.bind("<<Custom-Leave>>", lambda e: self.on_leave(i))
                label.bind("<<Custom-Leave>>", lambda e: self.on_leave(i))
                label.bind("<Button-4>", lambda e: self.on_mousewheel("up"))
                label.bind("<Button-5>", lambda e: self.on_mousewheel("down"))
                label.pack(expand=True, fill="x", padx=6, pady=0)
                frame.pack(fill="x", expand=True)

        for i, item in enumerate(self.items):
            make_item(item, i)

        self.selected_index = 0
        self.select_item(self.selected_index)

        self.root.bind("<FocusOut>", lambda e: self.hide())

        self.root.update_idletasks()
        self.container.update_idletasks()

        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()

        # Limit width to fit the container
        self.root.configure(width=self.container.winfo_reqwidth())

        # Limit height to 500 or window height if smaller
        h = min(window_height, min(500, self.container.winfo_reqheight()))
        self.root.configure(height=h)

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

    def arrow_up(self, n: int = -1) -> None:
        if n == -1:
            n = self.selected_index

        n -= 1

        if n >= 0:
            if not self.select_item(n):
                self.arrow_up(n)

    def arrow_down(self, n: int = -1) -> None:
        if n == -1:
            n = self.selected_index

        n += 1

        if n <= len(self.items) - 1:
            if not self.select_item(n):
                self.arrow_down(n)

    def select_item(self, index: int) -> bool:
        if index in self.elements:
            self.on_enter(index)
            return True

        return False

    def on_enter(self, index: int) -> None:
        if index not in self.elements:
            return

        if self.selected_index is not None:
            self.on_leave(self.selected_index)

        els = self.elements[index]
        colors = self.get_colors(els["item"])
        els["frame"]["background"] = colors["hover_background"]
        els["label"]["background"] = colors["hover_background"]
        diff = self.selected_index - index
        self.selected_index = index
        self.scroll_to_item()

    def on_leave(self, index: int) -> None:
        if index not in self.elements:
            return

        els = self.elements[index]
        colors = self.get_colors(els["item"])
        els["frame"]["background"] = colors["background"]
        els["label"]["background"] = colors["background"]

    def get_colors(self, item: MenuItem) -> Any:
        background = "white"

        if item.disabled:
            foreground = "#3D4555"
            hover_background = "white"
        else:
            foreground = "black"
            hover_background = "lightgray"

        return {"background": background, "foreground": foreground,
                "hover_background": hover_background}

    def scroll_to_item(self) -> None:
        els = self.elements[self.selected_index]
        tries = 0

        while tries < 10:
            widget_y = els["frame"].winfo_rooty() - app.root.winfo_rooty()
            widget_height = els["frame"].winfo_height()
            window_height = app.root.winfo_height()

            if widget_y + widget_height > window_height or widget_y < 0:
                outside_top = abs(min(0, widget_y))
                outside_bottom = max(0, (widget_y + widget_height) - window_height)
                print(outside_top, outside_bottom)

                if outside_top > 0:
                    self.root.yview_scroll(-1, "units")
                elif outside_bottom > 0:
                    self.root.yview_scroll(1, "units")
                else:
                    break
            else:
                break

            tries += 1
