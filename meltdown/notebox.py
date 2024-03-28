# Modules
from .app import app
from .args import args

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

    def __init__(self, parent: "Notebox", name: str) -> None:
        self.parent = parent
        self.name = name
        self.tab = self.make_tab_widget(name)
        self.content = self.make_content_widget()
        self.id = f"notebox_item_{NoteboxItem.notebox_id}"
        NoteboxItem.notebox_id += 1

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
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame

    def change_name(self, name: str) -> None:
        self.name = name
        self.tab.label.configure(text=name)


class Notebox(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self.parent = parent
        self.items: List[NoteboxItem] = []

        tabs_frame = tk.Frame(self)
        self.tabs_canvas = tk.Canvas(tabs_frame, borderwidth=0, highlightthickness=0)
        self.tabs_canvas.configure(background=app.theme.tabs_container_color)

        tabs_scrollbar = tk.Scrollbar(tabs_frame, orient="horizontal")
        self.tabs_canvas.configure(xscrollcommand=tabs_scrollbar.set)
        tabs_scrollbar.configure(command=self.tabs_canvas.xview)

        self.tabs_container = tk.Frame(self.tabs_canvas, background=app.theme.background_color)
        self.tabs_container_id = self.tabs_canvas.create_window((0, 0), window=self.tabs_container, anchor="nw")
        self.tabs_container.bind("<Configure>", lambda e: self.update_tabs())
        self.tabs_container.configure(background=app.theme.tabs_container_color)

        self.tabs_canvas.grid(row=0, column=0, sticky="ew")
        # tabs_scrollbar.grid(row=1, column=0, sticky="ew")
        tabs_frame.grid(row=0, column=0, sticky="ew")

        tabs_frame.configure(background=app.theme.tabs_container_color)
        tabs_frame.grid_rowconfigure(0, weight=0)
        tabs_frame.grid_columnconfigure(0, weight=1)

        self.content_container = tk.Frame(self)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.current_item: Optional[NoteboxItem] = None
        self.drag_item: Optional[NoteboxItem] = None
        self.dragging = False

        padx = ((app.theme.padx, app.theme.right_padding))
        self.grid(row=0, column=0, sticky="nsew", padx=padx, pady=(app.theme.pady, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.bind_tab_mousewheel(self.tabs_container)

        self.tabs_canvas.bind("<ButtonRelease-1>", lambda e: self.tabs_click())
        self.tabs_canvas.bind("<Double-Button-1>", lambda e: self.tabs_double_click())

        self.on_tab_right_click: Optional[Callable[..., Any]] = None
        self.on_tab_middle_click: Optional[Callable[..., Any]] = None
        self.on_tabs_click: Optional[Callable[..., Any]] = None
        self.on_tabs_double_click: Optional[Callable[..., Any]] = None
        self.on_change: Optional[Callable[..., Any]] = None
        self.on_reorder: Optional[Callable[..., Any]] = None

    def tab_right_click(self, event: Any, id: str) -> None:
        if self.on_tab_right_click:
            self.on_tab_right_click(event, id)

    def tabs_click(self) -> None:
        if self.on_tabs_click:
            self.on_tabs_click()

    def tabs_double_click(self) -> None:
        if self.on_tabs_double_click:
            self.on_tabs_double_click()

    def tab_middle_click(self, item: NoteboxItem) -> None:
        if self.on_tab_middle_click:
            self.on_tab_middle_click(item.id)

    def bind_tab_click(self, item: NoteboxItem) -> None:
        self.bind_recursive("<ButtonRelease-1>", lambda e: self.select(item.id), item.tab.frame)

    def bind_tab_mousewheel(self, widget: tk.Widget) -> None:
        self.bind_recursive("<Button-4>", lambda e: self.select_left(), widget)
        self.bind_recursive("<Button-5>", lambda e: self.select_right(), widget)

    def bind_tab_right_click(self, item: NoteboxItem) -> None:
        self.bind_recursive("<Button-3>", lambda e: self.tab_right_click(e, item.id), item.tab.frame)

    def bind_tab_middle_click(self, item: NoteboxItem) -> None:
        self.bind_recursive("<Button-2>", lambda e: self.tab_middle_click(item), item.tab.frame)

    def bind_tab_drag(self, item: NoteboxItem) -> None:
        self.bind_recursive("<B1-Motion>", lambda e: self.do_tab_drag(e, item), item.tab.frame)
        self.bind_recursive("<Leave>", lambda e: self.end_tab_drag(), item.tab.frame)

    def add(self, name: str) -> NoteboxItem:
        item = NoteboxItem(self, name)
        self.items.append(item)
        self.current_item = item
        self.add_tab(item)
        self.add_content(item.content)
        return item

    def current(self) -> str:
        if not self.current_item:
            return ""

        return self.current_item.id

    def select(self, id: str) -> None:
        if len(self.items) == 0:
            return

        item = self.get_item_by_id(id)

        if item:
            self.hide_all_except(item.id)
            self.current_item = item
            self.scroll_to_item(item)

            if self.on_change:
                self.on_change()

            self.update_tab_colors()

    def update_tab_colors(self) -> None:
        if not self.current_item:
            return

        for item in self.items:
            if item.id == self.current_item.id:
                item.tab.inner.configure(background=app.theme.tab_selected_background)
                item.tab.label.configure(background=app.theme.tab_selected_background)
                item.tab.label.configure(foreground=app.theme.tab_selected_foreground)
            else:
                item.tab.inner.configure(background=app.theme.tab_normal_background)
                item.tab.label.configure(background=app.theme.tab_normal_background)
                item.tab.label.configure(foreground=app.theme.tab_normal_foreground)

    def hide_all_except(self, id: str) -> None:
        for item in self.items:
            if item.id != id:
                item.content.grid_remove()
            else:
                item.content.grid()

        return None

    def get_item_by_id(self, id: str) -> Optional[NoteboxItem]:
        for item in self.items:
            if item.id == id:
                return item

        return None

    def ids(self) -> List[str]:
        return [item.id for item in self.items]

    def add_tab(self, item: NoteboxItem) -> None:
        self.bind_tab_click(item)
        self.bind_tab_mousewheel(item.tab.frame)
        self.bind_tab_right_click(item)
        self.bind_tab_middle_click(item)
        self.bind_tab_drag(item)
        self.update_tab_columns()

    def add_content(self, content: tk.Frame) -> None:
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_remove()

    def index(self, id: str) -> int:
        for i, item in enumerate(self.items):
            if item.id == id:
                return i

        return -1

    def select_left(self) -> None:
        if len(self.items) == 0:
            return

        if not self.current_item:
            return

        index = self.index(self.current_item.id)

        if index == 0:
            if args.wrap and (len(self.items) >= 2):
                index = len(self.items) - 1
            else:
                return
        else:
            index -= 1

        self.select(self.items[index].id)

    def select_right(self) -> None:
        if len(self.items) == 0:
            return

        if not self.current_item:
            return

        index = self.index(self.current_item.id)
        length = len(self.items)

        if index == length - 1:
            if args.wrap and (length >= 2):
                index = 0
            else:
                return
        else:
            index += 1

        self.select(self.items[index].id)

    def get_name(self, id: str) -> str:
        for item in self.items:
            if item.id == id:
                return item.name

        return ""

    def change_name(self, id: str, name: str) -> None:
        for item in self.items:
            if item.id == id:
                item.change_name(name)
                return

    def close(self, id: str) -> None:
        item = self.get_item_by_id(id)

        if not item:
            return

        index = self.index(id)
        was_current = self.current_item == self.items[index]
        item.tab.frame.grid_forget()
        item.content.grid_forget()
        self.items.pop(index)

        if len(self.items) == 0:
            self.current_item = None
        elif was_current:
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

        if new_item and self.drag_item and (new_item != self.drag_item):
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

        return None

    def end_tab_drag(self) -> None:
        self.dragging = False
        self.drag_item = None

        if self.on_reorder:
            self.on_reorder()

    def bind_recursive(self, what: str, action: Callable[..., Any], widget: tk.Widget) -> None:
        widget.bind(what, action)

        for child in widget.winfo_children():
            self.bind_recursive(what, action, child)

    def update_tabs(self) -> None:
        self.tabs_canvas.after_idle(self.do_update_tabs)

    def do_update_tabs(self) -> None:
        bbox = self.tabs_container.bbox()

        if bbox:
            self.tabs_canvas.configure(scrollregion=bbox)
            self.tabs_canvas.configure(width=bbox[2], height=bbox[3])

    def scroll_to_item(self, item: NoteboxItem) -> None:
        app.update()
        x_left = item.tab.frame.winfo_x()
        x_right = x_left + item.tab.frame.winfo_width()
        width = self.tabs_container.winfo_width()
        xview_left, xview_right = self.tabs_canvas.xview()

        # Calculate the current position of the item in the view fraction
        item_pos_left = x_left / width
        item_pos_right = x_right / width

        # Check if the item is not visible
        if not (xview_left <= item_pos_left <= xview_right):
            # Scroll the canvas to make the left side of the item visible
            self.tabs_canvas.xview_moveto(item_pos_left)
        elif not (xview_left <= item_pos_right <= xview_right):
            # Scroll the canvas to make the right side of the item visible
            self.tabs_canvas.xview_moveto(item_pos_right - (xview_right - xview_left))

    def update_tab_columns(self) -> None:
        for i, item in enumerate(self.items):
            item.tab.frame.grid(row=0, column=i, sticky="ew")
