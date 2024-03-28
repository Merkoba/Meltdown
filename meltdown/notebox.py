# Modules
from .app import app

# Standard
import tkinter as tk
from typing import List, Optional, Any, Callable

class TabWidget:
    def __init__(self, frame: tk.Frame, inner: tk.Frame, label: tk.Label):
        self.frame = frame
        self.inner = inner
        self.label = label


class NoteboxItem():
    notebox_id = 0

    def __init__(self, parent: "Notebox", name: str):
        self.parent = parent
        self.name = name
        self.tab = self.make_tab_widget(name)
        self.content = self.make_content_widget()
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.id = f"notebox_item_{NoteboxItem.notebox_id}"
        NoteboxItem.notebox_id += 1 # Lock 2

    def make_tab_widget(self, text: str) -> TabWidget:
        frame = tk.Frame(self.parent.tabs_container)
        frame.configure(background=app.theme.tab_border)
        frame.configure(cursor="hand2")
        inner = tk.Frame(frame)
        inner.configure(cursor="hand2")
        inner.configure(background=app.theme.tab_normal_background)
        inner.pack(expand=True, fill="both", padx=app.theme.tab_border_with, pady=app.theme.tab_border_with)
        label = tk.Label(inner, text=text, font=app.theme.font_tab)
        label.configure(background=app.theme.tab_normal_background)
        label.configure(foreground=app.theme.tab_normal_foreground)
        label.pack(expand=True, fill="both", padx=app.theme.tab_padx, pady=app.theme.tab_pady)
        label.configure(cursor="hand2")
        return TabWidget(frame, inner, label)

    def make_content_widget(self) -> tk.Frame:
        frame = tk.Frame(self.parent.content_container)
        return frame

    def change_name(self, name: str):
        self.name = name
        self.tab.label.configure(text=name)


class Notebox(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.parent = parent
        self.items: List[NoteboxItem] = []
        self.tabs_container = tk.Frame(self)
        self.tabs_container.configure(background=app.theme.tabs_container_color)
        self.content_container = tk.Frame(self)
        self.tabs_container.grid(row=0, column=0, sticky="ew")
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.current_item: Optional[NoteboxItem] = None
        self.drag_item: Optional[NoteboxItem] = None
        self.dragging = False

        padx = ((app.theme.padx, app.theme.right_padding))
        self.grid(row=0, column=0, sticky="nsew", padx=padx, pady=(app.theme.pady, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.bind_tab_mousewheel(self.tabs_container)

        self.tabs_container.bind("<Double-Button-1>", lambda e: self.tab_double_click())

    def tab_right_click(self, event: Any):
        if self.on_tab_right_click:
            self.on_tab_right_click(event, self.current_item.id)

    def tab_double_click(self):
        if self.on_tab_double_click:
            self.on_tab_double_click()

    def bind_tab_click(self, item: NoteboxItem):
        self.bind_recursive("<ButtonRelease-1>", lambda e: self.select(item.id), item.tab.frame)

    def bind_tab_mousewheel(self, widget):
        widget.bind("<Button-4>", lambda e: self.select_left())
        widget.bind("<Button-5>", lambda e: self.select_right())

    def bind_tab_right_click(self, widget):
        widget.bind("<Button-3>", lambda e: self.tab_right_click(e))

    def bind_tab_drag(self, item: NoteboxItem):
        self.bind_recursive("<B1-Motion>", lambda e: self.do_tab_drag(e, item), item.tab.frame)
        self.bind_recursive("<Leave>", lambda e: self.end_tab_drag(), item.tab.frame)

    def add(self, name: str):
        item = NoteboxItem(self, name)
        self.items.append(item)
        self.current_item = item.id
        self.add_tab(item)
        self.add_content(item.content)
        return item

    def select(self, id: Optional[int] = None):
        if len(self.items) == 0:
            return

        if id is None:
            return self.current_item.id
        else:
            item = self.get_item_by_id(id)

            if item:
                self.hide_all_except(item.id)
                self.current_item = item

                if self.on_change:
                    self.on_change()

        self.update_tab_colors()

    def update_tab_colors(self) -> None:
        for item in self.items:
            if item.id == self.current_item.id:
                item.tab.inner.configure(background=app.theme.tab_selected_background)
                item.tab.label.configure(background=app.theme.tab_selected_background)
                item.tab.label.configure(foreground=app.theme.tab_selected_foreground)
            else:
                item.tab.inner.configure(background=app.theme.tab_normal_background)
                item.tab.label.configure(background=app.theme.tab_normal_background)
                item.tab.label.configure(foreground=app.theme.tab_normal_foreground)

    def hide_all_except(self, id: int) -> None:
        for item in self.items:
            if item.id != id:
                item.content.grid_remove()
            else:
                item.content.grid()

    def get_item_by_id(self, id: int) -> NoteboxItem:
        for item in self.items:
            if item.id == id:
                return item

    def ids(self) -> List[int]:
        return [item.id for item in self.items]

    def add_tab(self, item: NoteboxItem):
        self.bind_tab_click(item)
        self.bind_tab_mousewheel(item.tab.label)
        self.bind_tab_right_click(item.tab.label)
        self.bind_tab_drag(item)
        item.tab.frame.grid(row=0, column=len(self.items), sticky="ew")

    def add_content(self, content: tk.Frame):
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_forget()

    def index(self, id: int) -> int:
        for i, item in enumerate(self.items):
            if item.id == id:
                return i

    def select_left(self) -> None:
        if len(self.items) == 0:
            return

        index = self.index(self.current_item.id)

        if index == 0:
            return

        self.select(self.items[index - 1].id)

    def select_right(self) -> None:
        if len(self.items) == 0:
            return

        index = self.index(self.current_item.id)

        if index == len(self.items) - 1:
            return

        self.select(self.items[index + 1].id)

    def get_name(self, id: int) -> str:
        for item in self.items:
            if item.id == id:
                return item.name

    def change_name(self, id: int, name: str):
        for item in self.items:
            if item.id == id:
                item.change_name(name)
                return

    def close(self, id: int):
        index = self.index(id)
        self.items[index].tab.frame.grid_forget()
        self.items[index].content.grid_forget()
        self.items.pop(index)

        if len(self.items) == 0:
            self.current_item = None
        else:
            if index == len(self.items):
                self.select(self.items[index - 1].id)
            else:
                self.select(self.items[index].id)

    def do_tab_drag(self, event: Any, item: NoteboxItem) -> None:
        if not self.dragging:
            self.dragging = True
            self.drag_item = item
            self.select(item.id)
            return

        new_item = self.get_tab_at_x(event.x_root)

        if new_item and (new_item != self.drag_item):
            old_index = self.items.index(self.drag_item)
            new_index = self.items.index(new_item)
            self.items.insert(new_index, self.items.pop(old_index))

            for i, item in enumerate(self.items):
                item.tab.frame.grid(row=0, column=i)

    def get_tab_at_x(self, x: int) -> Optional[NoteboxItem]:
        for item in self.items:
            tab_x = item.tab.frame.winfo_rootx()
            tab_width = item.tab.frame.winfo_width()

            if tab_x <= x <= tab_x + tab_width:
                return item

    def end_tab_drag(self) -> None:
        self.dragging = False
        self.drag_item = None

    def bind_recursive(self, what: str, action: Callable[..., Any], widget: tk.Widget):
        widget.bind(what, action)

        for child in widget.winfo_children():
            self.bind_recursive(what, action, child)