# Standard
import tkinter as tk
from typing import List, Optional, Any

class NoteboxItem():
    notebox_id = 0

    def __init__(self, parent: "Notebox", name: str):
        self.parent = parent
        self.name = name
        self.tab = self.make_tab_widget(name)
        self.tab.bind("<ButtonRelease-1>", lambda e: self.parent.select(self.id))
        self.content = self.make_content_widget()
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.id = f"notebox_item_{NoteboxItem.notebox_id}"
        NoteboxItem.notebox_id += 1

    def make_tab_widget(self, text: str) -> tk.Frame:
        label = tk.Label(self.parent.tabs_container, text=text)
        label.configure(height=1)
        return label

    def make_content_widget(self) -> tk.Frame:
        frame = tk.Frame(self.parent.content_container)
        return frame

    def change_name(self, name: str):
        self.name = name
        self.tab.configure(text=name)

class Notebox(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.parent = parent
        self.items: List[NoteboxItem] = []
        self.tabs_container = tk.Frame(self)
        self.content_container = tk.Frame(self)
        self.tabs_container.grid(row=0, column=0, sticky="ew")
        self.content_container.grid(row=1, column=0, sticky="nsew")

        self.grid(row=0, column=0, sticky="nsew")
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

    def bind_tab_mousewheel(self, widget):
        widget.bind("<Button-4>", lambda e: self.select_left())
        widget.bind("<Button-5>", lambda e: self.select_right())

    def bind_tab_right_click(self, widget):
        widget.bind("<Button-3>", lambda e: self.tab_right_click(e))

    def add(self, name: str):
        item = NoteboxItem(self, name)
        self.items.append(item)
        self.current_item = item.id
        self.add_tab(item.tab)
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

    def hide_all_except(self, id: int):
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

    def add_tab(self, tab: tk.Frame):
        self.bind_tab_mousewheel(tab)
        self.bind_tab_right_click(tab)
        tab.grid(row=0, column=len(self.items), sticky="ew")

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

    # def on_tab_start_drag(self, event: Any) -> None:
    #     tab_id = self.tab_on_coords(event.x, event.y)

    #     if not tab_id:
    #         return

    #     self.drag_start_index = self.index(tab_id)
    #     self.drag_start_x = event.x

    # def on_tab_drag(self, event: Any) -> None:
    #     tab_id = self.tab_on_coords(event.x, event.y)

    #     if not tab_id:
    #         return

    #     if abs(self.drag_start_x - event.x) > 3:
    #         if event.x > self.drag_start_x:
    #             direction = "right"
    #         elif event.x < self.drag_start_x:
    #             direction = "left"
    #     else:
    #         return

    #     if direction == "left":
    #         if self.drag_start_index == 0:
    #             return

    #     index = self.index(tab_id)
    #     width = self.get_tab_width(index)

    #     if direction == "left":
    #         x = 0
    #     elif direction == "right":
    #         x = width - event.x

    #     if direction == "left":
    #         x = index
    #     elif direction == "right":
    #         if abs(x) > width:
    #             x = index if x < 0 else index + 1
    #         else:
    #             x = index

    #     self.root.insert(x, self.drag_start_index)
    #     self.update_tab_index()
    #     self.update_session()
    #     self.drag_start_x = event.x