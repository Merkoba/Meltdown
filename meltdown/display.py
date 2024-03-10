# Modules
from .config import config
from .app import app
from . import widgetutils

# Standard
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any
from typing import Optional


class Tab:
    def __init__(self, id: str, output: tk.Text) -> None:
        self.id = id
        self.output = output
        self.auto_scroll = True


class Display:
    def __init__(self, widget: ttk.Notebook) -> None:
        self.root = widget
        self.tabs: Dict[str, Tab] = {}
        self.root.bind("<Button-1>", lambda e: self.click(e))
        self.root.bind("<Button-2>", lambda e: self.middle_click(e))
        self.root.bind("<Button-3>", lambda e: self.right_click(e))
        self.root.bind("<Double-Button-1>", lambda e: self.double_click(e))
        self.root.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_change(e))
        self.root.bind("<Button-1>", self.on_tab_start_drag)
        self.root.bind("<B1-Motion>", self.on_tab_drag)
        self.output_menu = widgetutils.make_menu()
        self.tab_menu = widgetutils.make_menu()
        self.tab_menu.add_command(label="Rename", command=lambda: self.tab_menu_rename())
        self.tab_menu.add_command(label="Clear", command=lambda: self.tab_menu_clear())
        self.tab_menu.add_command(label="Close", command=lambda: self.tab_menu_close())
        self.output_menu.add_command(label="Select All", command=lambda: self.select_all())
        self.current_tab = "none"
        self.drag_start_index = 0
        self.tab_number = 1

    def make_tab(self) -> None:
        from .widgets import widgets
        frame = widgetutils.make_frame(self.root)
        self.root.add(frame, text=f"Output {self.tab_number}")
        output = widgetutils.make_text(frame, state="disabled", fill="both")
        tab_id = self.tab_ids()[-1]
        output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        output.bind("<Button-1>", lambda e: widgets.hide_menu())
        output.bind("<Button-4>", lambda e: self.on_output_scroll(tab_id, "up"))
        output.bind("<Button-5>", lambda e: self.on_output_scroll(tab_id, "down"))
        output.tag_config("name_user", foreground="#87CEEB")
        output.tag_config("name_ai", foreground="#98FB98")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        tab = Tab(tab_id, output)
        self.tabs[tab_id] = tab
        self.select_tab(tab_id)
        self.tab_number += 1
        widgets.show_intro(tab_id)

    def tab_on_coords(self, x: int, y: int) -> str:
        index = self.root.tk.call(self.root._w, "identify", "tab", x, y)  # type: ignore

        if type(index) == int:
            return self.tab_ids()[index] or ""
        else:
            return ""

    def close_tab(self, event: Optional[Any] = None, tab_id: str = "") -> None:
        if (not tab_id) and event:
            tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            tab_id = self.root.select()

        if not tab_id:
            return

        if len(self.tab_ids()) > 1:
            self.root.forget(tab_id)
            self.update_output()
        else:
            self.clear_output()

    def select_tab(self, tab_id: str) -> None:
        self.root.select(tab_id)
        self.current_tab = tab_id

    def update_output(self) -> None:
        tab_id = self.root.select()
        self.current_tab = tab_id

    def update_tab_index(self) -> None:
        self.drag_start_index = self.root.index(self.root.select())  # type: ignore

    def on_tab_change(self, event: Any) -> None:
        self.update_output()

    def get_current_tab(self) -> Tab:
        return self.get_tab(self.current_tab)

    def get_current_output(self) -> tk.Text:
        return self.get_output(self.current_tab)

    def get_tab(self, id: str) -> Tab:
        return self.tabs[id]

    def get_output(self, id: str) -> tk.Text:
        return self.tabs[id].output

    def click(self, event: Any) -> None:
        from .widgets import widgets
        widgets.hide_menu()

    def right_click(self, event: Any) -> None:
        from .widgets import widgets
        tab_id = self.tab_on_coords(event.x, event.y)

        if tab_id:
            self.tab_menu_id = tab_id
            widgets.show_menu(self.tab_menu, event)

    def middle_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if tab_id:
            self.close_tab(event)

    def double_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            self.make_tab()

    def tab_menu_rename(self) -> None:
        tab_id = self.tab_menu_id
        widgetutils.show_input("Pick a name", lambda s: self.rename_tab(tab_id, s))

    def tab_menu_clear(self) -> None:
        tab_id = self.tab_menu_id
        self.clear_output(tab_id)

    def rename_tab(self, tab_id: str, name: str) -> None:
        if name:
            self.root.tab(tab_id, text=name)

    def tab_menu_close(self) -> None:
        self.close_tab(tab_id=self.tab_menu_id)

    def on_tab_start_drag(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            return

        self.drag_start_index = self.index(tab_id)
        self.drag_start_x = event.x

    def on_tab_drag(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            return

        if abs(self.drag_start_x - event.x) > 3:
            if event.x > self.drag_start_x:
                direction = "right"
            elif event.x < self.drag_start_x:
                direction = "left"
        else:
            return

        if direction == "left":
            if self.drag_start_index == 0:
                return

        index = self.index(tab_id)
        width = self.get_tab_width(index)

        if direction == "left":
            x = 0
        elif direction == "right":
            x = width - event.x

        if direction == "left":
            x = index
        elif direction == "right":
            if abs(x) > width:
                x = index if x < 0 else index + 1
            else:
                x = index

        self.root.insert(x, self.drag_start_index)
        self.update_tab_index()
        self.drag_start_x = event.x

    def get_tab_width(self, index: int) -> int:
        tab_text = self.root.tab(index, "text")
        label = tk.Label(self.root, text=tab_text)
        label.pack()
        width = label.winfo_reqwidth()
        label.pack_forget()
        return width

    def close_all_tabs(self) -> None:
        if len(self.tab_ids()) == 1:
            return

        def action() -> None:
            for tab_id in self.tab_ids():
                self.close_tab(tab_id=tab_id)

        widgetutils.show_confirm("Close all tabs?", lambda: action())

    def tab_ids(self) -> List[str]:
        return self.root.tabs()  # type: ignore

    def index(self, tab_id: str) -> int:
        return self.root.index(tab_id)  # type: ignore

    def on_output_scroll(self, tab_id: str, direction: str) -> None:
        tab = self.get_tab(tab_id)

        if direction == "up":
            tab.auto_scroll = False
        elif direction == "down":
            if tab.output.yview()[1] >= 1.0:
                tab.auto_scroll = True

    def show_output_menu(self, event: Any) -> None:
        from .widgets import widgets
        widgets.show_menu(self.output_menu, event)

    def output_top(self) -> None:
        output = self.get_current_output()
        widgetutils.to_top(output)

    def output_bottom(self) -> None:
        tab = self.get_current_tab()
        tab.auto_scroll = True
        widgetutils.to_bottom(tab.output)

    def output_copy(self) -> None:
        text = self.get_output_text()
        widgetutils.copy(text)

    def get_output_text(self, output_id: str = "") -> str:
        if not output_id:
            output_id = self.current_tab

        output = self.get_output(output_id)
        text = widgetutils.get_text(output)
        text = "\n".join(text.split("\n")[len(config.intro):]).strip()
        return text

    def clear_output(self, output_id: str = "") -> None:
        from .widgets import widgets
        from .model import model

        if not output_id:
            output_id = self.current_tab

        output = self.get_output(output_id)

        if not self.get_output_text(output_id):
            return

        widgetutils.clear_text(output, True)
        model.clear_context(self.current_tab)
        widgets.show_intro(output_id)

    def select_all(self) -> None:
        output = self.get_current_output()
        widgetutils.select_all(output)

    def print(self, text: str, linebreak: bool = True, output_id: str = "") -> None:
        if not app.exists():
            return

        left = ""
        right = ""

        if not output_id:
            output_id = self.current_tab

        output = self.get_output(output_id)

        if widgetutils.text_length(output) and \
                (widgetutils.last_character(output) != "\n"):
            left = "\n"

        if linebreak:
            right = "\n"

        text = left + text + right
        widgetutils.insert_text(output, text, True)
        widgetutils.to_bottom(output)

    def insert(self, text: str, output_id: str = "") -> None:
        if not app.exists():
            return

        if not output_id:
            output_id = self.current_tab

        tab = self.get_tab(output_id)
        widgetutils.insert_text(tab.output, text, True)

        if tab.auto_scroll:
            widgetutils.to_bottom(tab.output)
