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
        self.visible = True
        self.coords = {"x": 0, "y": 0}


class Menu:
    current_menu: Optional["Menu"] = None

    @staticmethod
    def hide_all() -> None:
        if Menu.current_menu:
            Menu.current_menu.hide()

    def __init__(self) -> None:
        self.container: Optional[tk.Frame] = None
        self.items: List[MenuItem] = []
        self.disabled_color = "#E0E0E0"
        self.background_color = "white"
        self.foreground_color = "black"
        self.hover_background = "#6693C3"
        self.hover_foreground = "white"
        self.foreground_disabled = "#3D4555"

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

    def make(self) -> None:
        self.root = tk.Canvas(app.root, bg="white", borderwidth=0, highlightthickness=0)
        self.container = tk.Frame(self.root, bg="white", borderwidth=0)
        self.root.create_window((0, 0), window=self.container, anchor="nw")
        self.root.bind("<FocusOut>", lambda e: self.hide())
        self.root.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.current_widget = None
        self.selected_index = -1
        self.make_items()
        self.select_first_item()
        self.configure_geometry()
        self.setup_keyboard()
        self.filter = ""

    def make_items(self) -> None:
        if not self.container:
            return

        def exec() -> None:
            if self.selected_index not in self.elements:
                return

            item = self.items[self.selected_index]

            if item.command:
                item.command()

        def cmd() -> None:
            self.hide()
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
        self.separators: List[ttk.Separator] = []

        def bind_motion(parent: tk.Widget) -> None:
            for child in parent.winfo_children():
                child.bind("<Motion>", lambda e: on_motion(e))
                child.bind("<B1-Motion>", lambda e: on_motion(e))
                child.bind("<Button-4>", lambda e: self.on_mousewheel("up"))
                child.bind("<Button-5>", lambda e: self.on_mousewheel("down"))
                child.bind("<ButtonRelease-1>", lambda e: cmd())
                child.bind("<ButtonRelease-1>", lambda e: cmd())
                bind_motion(child)

        def make_item(item: MenuItem, i: int) -> None:
            colors = self.get_colors(item)

            if item.separator:
                separator = ttk.Separator(self.container, orient="horizontal", style="Normal.TSeparator")
                separator.grid(row=i, column=0, sticky="ew", padx=6, pady=2)
                self.separators.append(separator)
            else:
                label = ttk.Label(self.container, text=item.text, background=colors["background"], foreground=colors["foreground"],
                                  wraplength=600, justify=tk.LEFT, anchor="w", font=config.font_menu, borderwidth=0, padding=(4, 2, 4, 2))

                self.elements[i] = {"item": item, "index": i, "label": label, "visible": True}
                label.bind("<<Custom-Enter>>", lambda e: self.on_enter(i))
                label.bind("<<Custom-Leave>>", lambda e: self.on_leave(i))
                label.grid(row=i, column=0, sticky="ew", pady=0)

        for i, item in enumerate(self.items):
            make_item(item, i)

        self.no_items = ttk.Label(self.container, text="No Items", background=self.background_color, foreground=self.foreground_color,
                                  wraplength=600, justify=tk.LEFT, anchor="w", font=config.font, borderwidth=0, padding=(4, 2, 4, 2))

        self.no_items.grid(row=len(self.items), column=0, sticky="ew", pady=0)
        self.no_items.grid_remove()

        bind_motion(self.root)

    def all_hidden(self) -> bool:
        return self.num_visible() == 0

    def configure_geometry(self) -> None:
        if not self.root or not self.container:
            return

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
        x = self.coords["x"] - app.root.winfo_rootx()
        y = self.coords["y"] - app.root.winfo_rooty()

        if x < 0:
            x = 0
        elif x + menu_width > window_width:
            x = window_width - menu_width

        if y < 0:
            y = 0
        elif y + menu_height > window_height:
            y = window_height - menu_height

        self.root.place(x=x, y=y)

    def setup_keyboard(self) -> None:
        def on_key(event: Any) -> None:
            if event.keysym == "Escape":
                self.filter = ""
            elif event.keysym == "BackSpace":
                self.filter = self.filter[:-1]
            elif event.char:
                if not self.all_hidden():
                    self.filter += event.char

            self.do_filter()

        self.root.bind("<KeyPress>", on_key)

    def do_filter(self) -> None:
        if not self.filter:
            for els in self.elements.values():
                self.show_item(els["index"])

            for sep in self.separators:
                sep.grid()
        else:
            for els in self.elements.values():
                if els["item"].disabled:
                    self.hide_item(els["index"])
                elif self.filter.lower() in els["item"].text.lower():
                    self.show_item(els["index"])
                else:
                    self.hide_item(els["index"])

            for sep in self.separators:
                sep.grid_remove()

        if self.all_hidden():
            self.no_items.grid()
            self.selected_index = -1
        else:
            self.no_items.grid_remove()
            self.select_first_item()

        self.configure_geometry()

    def show_item(self, index: int) -> None:
        els = self.elements[index]
        els["visible"] = True
        els["label"].grid()

    def hide_item(self, index: int) -> None:
        els = self.elements[index]
        els["visible"] = False
        els["label"].grid_remove()

    def select_first_item(self) -> None:
        for i in range(len(self.items)):
            if i not in self.elements:
                continue

            if self.elements[i]["visible"]:
                self.select_item(i)
                break

    def show(self, event: Optional[Any] = None, widget: Optional[tk.Widget] = None) -> None:
        Menu.hide_all()

        if not self.items:
            return

        if event:
            self.coords = {"x": event.x_root, "y": event.y_root}
        elif widget:
            x = widget.winfo_rootx() + widget.winfo_width() // 2
            y = widget.winfo_rooty() + widget.winfo_height() // 2
            self.coords = {"x": x, "y": y}
        else:
            return

        self.make()

        if self.root:
            self.root.update_idletasks()
            self.root.focus_set()
            Menu.current_menu = self

    def hide(self) -> None:
        from .tooltips import ToolTip
        from . import keyboard

        if self.root:
            self.root.place_forget()
            self.root.destroy()
            ToolTip.block()
            keyboard.block()
            Menu.current_menu = None

    def no_item(self) -> bool:
        return self.selected_index not in self.elements

    def num_visible(self) -> int:
        return len([els for els in self.elements.values() if els["visible"]])

    def arrow_up(self, n: int = -1) -> None:
        if self.no_item():
            return

        if self.num_visible() < 2:
            return

        if n == -1:
            n = self.selected_index

        n -= 1

        if n < 0:
            n = len(self.items) - 1

        if not self.select_item(n):
            self.arrow_up(n)

    def arrow_down(self, n: int = -1) -> None:
        if self.no_item():
            return

        if self.num_visible() < 2:
            return

        if n == -1:
            n = self.selected_index

        n += 1

        if n >= len(self.items):
            n = 0

        if not self.select_item(n):
            self.arrow_down(n)

    def select_item(self, index: int) -> bool:
        if index not in self.elements:
            return False

        if self.elements[index]["item"].disabled:
            return False

        if not self.elements[index]["item"].visible:
            return False

        self.on_enter(index)
        return True

    def on_enter(self, index: int) -> None:
        if index not in self.elements:
            return

        self.on_leave(self.selected_index)
        els = self.elements[index]
        colors = self.get_colors(els["item"])
        els["label"]["background"] = colors["hover_background"]
        els["label"]["foreground"] = colors["hover_foreground"]
        self.selected_index = index
        self.scroll_to_item()

    def on_leave(self, index: int) -> None:
        if index not in self.elements:
            return

        els = self.elements[index]
        colors = self.get_colors(els["item"])
        els["label"]["background"] = colors["background"]
        els["label"]["foreground"] = colors["foreground"]

    def get_colors(self, item: MenuItem) -> Any:
        background = self.background_color

        if item.disabled:
            foreground = self.foreground_disabled
            hover_foreground = self.foreground_disabled
            hover_background = self.background_color
        else:
            foreground = self.foreground_color
            hover_foreground = self.hover_foreground
            hover_background = self.hover_background

        return {"background": background, "foreground": foreground,
                "hover_background": hover_background, "hover_foreground": hover_foreground}

    def scroll_to_item(self) -> None:
        if self.no_item():
            return

        els = self.elements[self.selected_index]
        tries = 0

        while tries < 10:
            widget_y = els["label"].winfo_rooty() - app.root.winfo_rooty()
            widget_height = els["label"].winfo_height()
            window_height = app.root.winfo_height()

            if widget_y + widget_height > window_height or widget_y < 0:
                outside_top = abs(min(0, widget_y))
                outside_bottom = max(0, (widget_y + widget_height) - window_height)

                if outside_top > 0:
                    self.root.yview_scroll(-1, "units")
                elif outside_bottom > 0:
                    self.root.yview_scroll(1, "units")
                else:
                    break
            else:
                break

            tries += 1
