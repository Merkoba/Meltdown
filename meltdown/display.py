# Modules
from .config import config
from .app import app
from . import widgetutils
from .enums import Fill
from .menus import Menu
from . import dialogs

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
        self.output_menu = Menu()
        self.tab_menu = Menu()
        self.tab_menu.add(text="Rename", command=lambda: self.tab_menu_rename())
        self.tab_menu.add(text="Close", command=lambda: self.tab_menu_close())
        self.output_menu.add(text="Copy All", command=lambda: self.copy_output())
        self.output_menu.add(text="Select All", command=lambda: self.select_output())
        self.output_menu.add(text="Smaller Font", command=lambda: self.decrease_font())
        self.output_menu.add(text="Bigger Font", command=lambda: self.increase_font())
        self.output_menu.add(text="Reset Font", command=lambda: self.reset_font())
        self.current_tab = "none"
        self.drag_start_index = 0
        self.tab_number = 1

        self.root.bind("<Button-1>", lambda e: self.on_click(e))
        self.root.bind("<ButtonRelease-2>", lambda e: self.on_middle_click(e))
        self.root.bind("<Button-3>", lambda e: self.on_right_click(e))
        self.root.bind("<Double-Button-1>", lambda e: self.on_double_click(e))
        self.root.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_change(e))
        self.root.bind("<B1-Motion>", self.on_tab_drag)

        def on_mousewheel(direction: str) -> None:
            if direction == "left":
                self.tab_left()
            elif direction == "right":
                self.tab_right()

        self.root.bind("<Button-4>", lambda e: on_mousewheel("left"))
        self.root.bind("<Button-5>", lambda e: on_mousewheel("right"))

    def make_tab(self, name: Optional[str] = None,
                 document_id: Optional[str] = None, select_tab: bool = True) -> None:
        from .widgets import widgets
        from .session import session
        frame = widgetutils.make_frame(self.root)

        if not name:
            name = self.random_tab_name()

        self.root.add(frame, text=name)
        output = widgetutils.make_text(frame, state="disabled", fill=Fill.BOTH)

        if not document_id:
            document = session.add(name)
            document_id = document.id

        tab_id = self.tab_ids()[-1]
        output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        output.bind("<Button-4>", lambda e: self.on_output_scroll(tab_id, "up"))
        output.bind("<Button-5>", lambda e: self.on_output_scroll(tab_id, "down"))
        output.tag_config("name_user", foreground="#87CEEB")
        output.tag_config("name_ai", foreground="#98FB98")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        tab = Tab(document_id, tab_id, output)
        self.tabs[tab_id] = tab

        if select_tab:
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
                  force: bool = False, make_empty: bool = True, show_close_all: bool = False) -> None:
        if (not tab_id) and event:
            tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            tab_id = self.root.select()

        if not tab_id:
            return

        def action() -> None:
            self.root.forget(tab_id)
            self.update_current_tab()
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

            dialogs.show_confirm("Close tab?", lambda: action(), cmd_list=cmd_list)

    def select_tab(self, tab_id: str) -> None:
        self.root.select(tab_id)
        self.current_tab = tab_id
        app.update()
        self.check_scroll_buttons(tab_id)

    def update_current_tab(self) -> None:
        tab_id = self.root.select()
        self.current_tab = tab_id

    def update_tab_index(self) -> None:
        self.drag_start_index = self.root.index(self.root.select())  # type: ignore

    def on_tab_change(self, event: Any) -> None:
        from .widgets import widgets
        from .session import session
        self.update_current_tab()
        tab = self.get_current_tab()

        if tab:
            document = session.get_document(tab.document_id)

            if document and (not document.loaded):
                document.print()
                document.loaded = True

        widgets.focus_input()

    def get_current_tab(self) -> Optional[Tab]:
        return self.get_tab(self.current_tab)

    def get_current_output(self) -> Optional[tk.Text]:
        return self.get_output(self.current_tab)

    def get_tab(self, id: str) -> Optional[Tab]:
        return self.tabs.get(id)

    def get_tab_by_document_id(self, document_id: str) -> Optional[Tab]:
        for tab in self.tabs.values():
            if tab.document_id == document_id:
                return tab

        return None

    def get_output(self, id: str) -> Optional[tk.Text]:
        tab = self.get_tab(id)

        if tab:
            return tab.output
        else:
            return None

    def on_click(self, event: Any) -> None:
        dialogs.Dialog.hide_all()
        self.on_tab_start_drag(event)
        tab_id = self.tab_on_coords(event.x, event.y)

        if tab_id:
            self.check_scroll_buttons(tab_id)

    def on_right_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if tab_id:
            self.tab_menu_id = tab_id
            self.tab_menu.show(event)

    def on_middle_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if tab_id:
            self.close_tab(event)

    def on_double_click(self, event: Any) -> None:
        tab_id = self.tab_on_coords(event.x, event.y)

        if not tab_id:
            self.make_tab()

    def tab_menu_rename(self) -> None:
        tab_id = self.tab_menu_id
        name = self.get_tab_name(tab_id)
        dialogs.show_input("Pick a name", lambda s: self.rename_tab(tab_id, s), value=name)

    def rename_tab(self, tab_id: str, name: str) -> None:
        from .session import session

        if name:
            tab = self.get_tab(tab_id)

            if not tab:
                return

            o_name = self.get_tab_name(tab_id)

            if name == o_name:
                return

            self.root.tab(tab_id, text=name)
            session.change_name(tab.document_id, name)

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

    def close_all_tabs(self, force: bool = False, make_empty: bool = True) -> None:
        def action() -> None:
            for tab_id in self.tab_ids():
                self.close_tab(tab_id=tab_id, force=True, make_empty=make_empty)

        if force:
            action()
        else:
            dialogs.show_confirm("Close all tabs?", lambda: action())

    def tab_ids(self) -> List[str]:
        return self.root.tabs()  # type: ignore

    def index(self, tab_id: str) -> int:
        return self.root.index(tab_id)  # type: ignore

    def on_output_scroll(self, tab_id: str, direction: str) -> None:
        tab = self.get_tab(tab_id)

        if not tab:
            return

        if direction == "up":
            tab.auto_scroll = False
        elif direction == "down":
            if tab.output.yview()[1] >= 1.0:
                tab.auto_scroll = True

    def show_output_menu(self, event: Any) -> None:
        self.output_menu.show(event)

    def output_top(self) -> None:
        output = self.get_current_output()

        if output:
            widgetutils.to_top(output)
            self.check_scroll_buttons()

    def output_bottom(self) -> None:
        tab = self.get_current_tab()

        if not tab:
            return

        tab.auto_scroll = True
        widgetutils.to_bottom(tab.output)
        self.check_scroll_buttons()

    def copy_output(self) -> None:
        text = self.get_output_text()
        widgetutils.copy(text)

    def get_output_text(self, tab_id: str = "") -> str:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return ""

        text = widgetutils.get_text(output)
        text = "\n".join(text.split("\n")[len(config.intro):]).strip()
        return text

    def clear_output(self, tab_id: str = "") -> None:
        from .widgets import widgets

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        if not self.get_output_text(tab_id):
            return

        def action() -> None:
            from .session import session
            tab = self.get_tab(tab_id)

            if (not tab) or (not output):
                return

            widgetutils.clear_text(output, True)
            session.clear(tab.document_id)
            widgets.show_intro(tab_id)
            self.check_scroll_buttons(tab_id)

        dialogs.show_confirm("Clear output?", lambda: action())

    def select_output(self) -> None:
        output = self.get_current_output()

        if output:
            widgetutils.select_all(output)

    def print(self, text: str, linebreak: bool = True, tab_id: str = "") -> None:
        if not app.exists():
            return

        left = ""
        right = ""

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

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

        if not tab:
            return

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

        if not tab:
            return

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

    def check_scroll_buttons(self, tab_id: str = "") -> None:
        from .widgets import widgets

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        output = tab.output

        if not output:
            return

        yview = output.yview()

        if yview[1] == 1.0:
            widgets.disable_bottom_button()
        else:
            widgets.enable_bottom_button()

        if yview[0] == 0:
            widgets.disable_top_button()
        else:
            widgets.enable_top_button()

    def tab_left(self) -> None:
        index = self.index(self.current_tab) - 1

        if index < 0:
            return

        self.select_tab(self.tab_ids()[index])

    def tab_right(self) -> None:
        index = self.index(self.current_tab) + 1

        if index >= self.num_tabs():
            return

        self.select_tab(self.tab_ids()[index])

    def close_current_tab(self) -> None:
        self.close_tab(tab_id=self.current_tab)

    def decrease_font(self) -> None:
        from . import state
        new_size = config.output_font_size - 1

        if new_size < 6:
            return

        state.set_config("output_font_size", new_size)

    def increase_font(self) -> None:
        from . import state
        new_size = config.output_font_size + 1

        if new_size > 60:
            return

        state.set_config("output_font_size", new_size)

    def reset_font(self) -> None:
        from . import state
        state.reset_one_config("output_font_size")

    def update_font(self) -> None:
        for tab in self.tabs.values():
            tab.output.configure(font=config.get_output_font())
