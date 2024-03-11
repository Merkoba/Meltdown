# Modules
from .config import config
from .app import app
from . import widgetutils
from .enums import Fill

# Standard
import random
import string
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any
from typing import Optional


class Tab:
    def __init__(self, document_id: str, tab_id: str, output: tk.Text) -> None:
        self.document_id = document_id
        self.tab_id = tab_id
        self.output = output
        self.auto_scroll = True


class Display:
    def __init__(self, widget: ttk.Notebook) -> None:
        self.root = widget
        self.tabs: Dict[str, Tab] = {}
        self.root.bind("<Button-1>", lambda e: self.click(e))
        self.root.bind("<ButtonRelease-2>", lambda e: self.middle_click(e))
        self.root.bind("<Button-3>", lambda e: self.right_click(e))
        self.root.bind("<Double-Button-1>", lambda e: self.double_click(e))
        self.root.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_change(e))
        self.root.bind("<Button-1>", self.on_tab_start_drag)
        self.root.bind("<B1-Motion>", self.on_tab_drag)
        self.output_menu = widgetutils.make_menu()
        self.tab_menu = widgetutils.make_menu()
        self.tab_menu.add_command(label="Rename", command=lambda: self.tab_menu_rename())
        self.tab_menu.add_command(label="Close", command=lambda: self.tab_menu_close())
        self.output_menu.add_command(label="Copy All", command=lambda: self.copy_output())
        self.output_menu.add_command(label="Select All", command=lambda: self.select_output())
        self.current_tab = "none"
        self.drag_start_index = 0
        self.tab_number = 1

    def make_tab(self, name: Optional[str] = None, document_id: Optional[str] = None) -> None:
        from .widgets import widgets
        from . import timeutils
        frame = widgetutils.make_frame(self.root)

        if not name:
            name = self.random_tab_name()

        self.root.add(frame, text=name)
        output = widgetutils.make_text(frame, state="disabled", fill=Fill.BOTH)

        if not document_id:
            document_id = str(timeutils.now())

        tab_id = self.tab_ids()[-1]
        output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        output.bind("<Button-1>", lambda e: widgets.hide_menu())
        output.bind("<Button-4>", lambda e: self.on_output_scroll(tab_id, "up"))
        output.bind("<Button-5>", lambda e: self.on_output_scroll(tab_id, "down"))
        output.tag_config("name_user", foreground="#87CEEB")
        output.tag_config("name_ai", foreground="#98FB98")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        tab = Tab(document_id, tab_id, output)
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

    def close_tab(self, event: Optional[Any] = None, tab_id: str = "",
                  force: bool = False, make_empty: bool = True, show_close_all: bool = True) -> None:
        if (not tab_id) and event:
            tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            tab_id = self.root.select()

        if not tab_id:
            return

        def action() -> None:
            self.root.forget(tab_id)
            self.update_output()
            self.remove_tab(tab_id)

            if self.num_tabs() == 0:
                if make_empty:
                    self.make_tab()

        if force:
            action()
        else:
            cmd_list = []

            if show_close_all and (self.num_tabs() > 1):
                cmd_list.append(("Close All", lambda: self.close_all_tabs()))

            widgetutils.show_confirm("Close tab?", lambda: action(), cmd_list=cmd_list)

    def select_tab(self, tab_id: str) -> None:
        self.root.select(tab_id)
        self.current_tab = tab_id

    def update_output(self) -> None:
        tab_id = self.root.select()
        self.current_tab = tab_id

    def update_tab_index(self) -> None:
        self.drag_start_index = self.root.index(self.root.select())  # type: ignore

    def on_tab_change(self, event: Any) -> None:
        from .widgets import widgets
        self.update_output()
        widgets.focus_input()

    def get_current_tab(self) -> Tab:
        return self.get_tab(self.current_tab)

    def get_current_output(self) -> tk.Text:
        return self.get_output(self.current_tab)

    def get_tab(self, id: str) -> Tab:
        return self.tabs[id]

    def get_tab_by_document_id(self, document_id: str) -> Optional[Tab]:
        for tab in self.tabs.values():
            if tab.document_id == document_id:
                return tab

        return None

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
            self.close_tab(event, show_close_all=False)

    def double_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            self.make_tab()

    def tab_menu_rename(self) -> None:
        tab_id = self.tab_menu_id
        widgetutils.show_input("Pick a name", lambda s: self.rename_tab(tab_id, s))

    def rename_tab(self, tab_id: str, name: str) -> None:
        from .session import session

        if name:
            tab = self.get_tab(tab_id)
            self.root.tab(tab_id, text=name)
            session.change_name(tab.document_id, name)

    def tab_menu_close(self) -> None:
        self.close_tab(tab_id=self.tab_menu_id, show_close_all=False)

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

    def close_all_tabs(self, force: bool = False, make_empty: bool = True) -> None:
        def action() -> None:
            for tab_id in self.tab_ids():
                self.close_tab(tab_id=tab_id, force=True, make_empty=make_empty)

        if force:
            action()
        else:
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

    def copy_output(self) -> None:
        text = self.get_output_text()
        widgetutils.copy(text)

    def get_output_text(self, tab_id: str = "") -> str:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)
        text = widgetutils.get_text(output)
        text = "\n".join(text.split("\n")[len(config.intro):]).strip()
        return text

    def clear_output(self, tab_id: str = "") -> None:
        from .widgets import widgets

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not self.get_output_text(tab_id):
            return

        def action() -> None:
            from .session import session
            tab = self.get_tab(tab_id)
            widgetutils.clear_text(output, True)
            session.clear(tab.document_id)
            widgets.show_intro(tab_id)

        widgetutils.show_confirm("Clear output?", lambda: action())

    def select_output(self) -> None:
        output = self.get_current_output()
        widgetutils.select_all(output)

    def print(self, text: str, linebreak: bool = True, tab_id: str = "") -> None:
        if not app.exists():
            return

        left = ""
        right = ""

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if widgetutils.text_length(output) and \
                (widgetutils.last_character(output) != "\n"):
            left = "\n"

        if linebreak:
            right = "\n"

        text = left + text + right
        widgetutils.insert_text(output, text, True)
        widgetutils.to_bottom(output)

    def insert(self, text: str, tab_id: str = "") -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)
        widgetutils.insert_text(tab.output, text, True)

        if tab.auto_scroll:
            widgetutils.to_bottom(tab.output)

    def save_log(self) -> None:
        from . import state
        state.save_log()

    def get_tab_name(self, tab_id: str) -> str:
        return self.root.tab(tab_id, "text")  # type: ignore

    def get_current_tab_name(self) -> str:
        return self.get_tab_name(self.current_tab)

    def num_tabs(self) -> int:
        return len(self.tab_ids())

    def remove_tab(self, tab_id: str) -> None:
        from .session import session
        tab = self.get_tab(tab_id)
        session.remove(tab.document_id)
        del self.tabs[tab_id]

    def random_tab_name(self) -> str:
        vowels = "aeiou"
        consonants = "".join(set(string.ascii_lowercase) - set(vowels))

        def con() -> str:
            return random.choice(consonants)

        def vow() -> str:
            return random.choice(vowels)

        name = con() + vow() + con() + vow() + con() + vow()
        return name.capitalize()
