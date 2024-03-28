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


class Page():
    notebox_id = 0

    def __init__(self, parent: "Book", name: str) -> None:
        self.parent = parent
        self.name = name
        self.tab = self.make_tab_widget(name)
        self.content = self.make_content_widget()
        self.id = f"page_{Page.notebox_id}"
        Page.notebox_id += 1

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


class Book(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self.parent = parent
        self.pages: List[Page] = []

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

        if args.tabs:
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

        self.current_page: Optional[Page] = None
        self.drag_page: Optional[Page] = None
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

    def tab_middle_click(self, page: Page) -> None:
        if self.on_tab_middle_click:
            self.on_tab_middle_click(page.id)

    def bind_tab_click(self, page: Page) -> None:
        self.bind_recursive("<ButtonRelease-1>", lambda e: self.select(page.id), page.tab.frame)

    def bind_tab_mousewheel(self, widget: tk.Widget) -> None:
        self.bind_recursive("<Button-4>", lambda e: self.select_left(), widget)
        self.bind_recursive("<Button-5>", lambda e: self.select_right(), widget)

    def bind_tab_right_click(self, page: Page) -> None:
        self.bind_recursive("<Button-3>", lambda e: self.tab_right_click(e, page.id), page.tab.frame)

    def bind_tab_middle_click(self, page: Page) -> None:
        self.bind_recursive("<Button-2>", lambda e: self.tab_middle_click(page), page.tab.frame)

    def bind_tab_drag(self, page: Page) -> None:
        self.bind_recursive("<B1-Motion>", lambda e: self.do_tab_drag(e, page), page.tab.frame)
        self.bind_recursive("<Leave>", lambda e: self.end_tab_drag(), page.tab.frame)

    def add(self, name: str) -> Page:
        page = Page(self, name)
        self.pages.append(page)
        self.current_page = page
        self.add_tab(page)
        self.add_content(page.content)
        return page

    def current(self) -> str:
        if not self.current_page:
            return ""

        return self.current_page.id

    def select(self, id: str) -> None:
        if len(self.pages) == 0:
            return

        page = self.get_page_by_id(id)

        if page:
            self.hide_all_except(page.id)
            self.current_page = page
            self.scroll_to_page(page)

            if self.on_change:
                self.on_change()

            self.update_tab_colors()

    def update_tab_colors(self) -> None:
        if not self.current_page:
            return

        for page in self.pages:
            if page.id == self.current_page.id:
                page.tab.inner.configure(background=app.theme.tab_selected_background)
                page.tab.label.configure(background=app.theme.tab_selected_background)
                page.tab.label.configure(foreground=app.theme.tab_selected_foreground)
            else:
                page.tab.inner.configure(background=app.theme.tab_normal_background)
                page.tab.label.configure(background=app.theme.tab_normal_background)
                page.tab.label.configure(foreground=app.theme.tab_normal_foreground)

    def hide_all_except(self, id: str) -> None:
        for page in self.pages:
            if page.id != id:
                page.content.grid_remove()
            else:
                page.content.grid()

        return None

    def get_page_by_id(self, id: str) -> Optional[Page]:
        for page in self.pages:
            if page.id == id:
                return page

        return None

    def ids(self) -> List[str]:
        return [page.id for page in self.pages]

    def add_tab(self, page: Page) -> None:
        self.bind_tab_click(page)
        self.bind_tab_mousewheel(page.tab.frame)
        self.bind_tab_right_click(page)
        self.bind_tab_middle_click(page)
        self.bind_tab_drag(page)
        self.update_tab_columns()

    def add_content(self, content: tk.Frame) -> None:
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_remove()

    def index(self, id: str) -> int:
        for i, page in enumerate(self.pages):
            if page.id == id:
                return i

        return -1

    def select_left(self) -> None:
        if len(self.pages) == 0:
            return

        if not self.current_page:
            return

        index = self.index(self.current_page.id)

        if index == 0:
            if args.wrap and (len(self.pages) >= 2):
                index = len(self.pages) - 1
            else:
                return
        else:
            index -= 1

        self.select(self.pages[index].id)

    def select_right(self) -> None:
        if len(self.pages) == 0:
            return

        if not self.current_page:
            return

        index = self.index(self.current_page.id)
        length = len(self.pages)

        if index == length - 1:
            if args.wrap and (length >= 2):
                index = 0
            else:
                return
        else:
            index += 1

        self.select(self.pages[index].id)

    def get_name(self, id: str) -> str:
        for page in self.pages:
            if page.id == id:
                return page.name

        return ""

    def change_name(self, id: str, name: str) -> None:
        for page in self.pages:
            if page.id == id:
                page.change_name(name)
                return

    def close(self, id: str) -> None:
        page = self.get_page_by_id(id)

        if not page:
            return

        index = self.index(id)
        was_current = self.current_page == self.pages[index]
        page.tab.frame.grid_forget()
        page.content.grid_forget()
        self.pages.pop(index)

        if len(self.pages) == 0:
            self.current_page = None
        elif was_current:
            if index == len(self.pages):
                self.select(self.pages[index - 1].id)
            else:
                self.select(self.pages[index].id)

    def do_tab_drag(self, event: Any, page: Page) -> None:
        if not self.dragging:
            self.dragging = True
            self.drag_page = page
            self.select(page.id)
            return

        new_item = self.get_tab_at_x(event.x_root)

        if new_item and self.drag_page and (new_item != self.drag_page):
            old_index = self.pages.index(self.drag_page)
            new_index = self.pages.index(new_item)
            self.pages.insert(new_index, self.pages.pop(old_index))

            for i, page in enumerate(self.pages):
                page.tab.frame.grid(row=0, column=i)

    def get_tab_at_x(self, x: int) -> Optional[Page]:
        for page in self.pages:
            tab_x = page.tab.frame.winfo_rootx()
            tab_width = page.tab.frame.winfo_width()

            if tab_x <= x <= tab_x + tab_width:
                return page

        return None

    def end_tab_drag(self) -> None:
        self.dragging = False
        self.drag_page = None

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

    def scroll_to_page(self, page: Page) -> None:
        app.update()
        x_left = page.tab.frame.winfo_x()
        x_right = x_left + page.tab.frame.winfo_width()
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
        for i, page in enumerate(self.pages):
            page.tab.frame.grid(row=0, column=i, sticky="ew")

    def get_tab(self, id: str) -> Optional[tk.Frame]:
        for page in self.pages:
            if page.id == id:
                return page.tab.frame

        return None