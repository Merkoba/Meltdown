# Standard
import tkinter as tk
from typing import List, Optional, Any, Callable

# Modules
from .app import app
from .args import args
from .tooltips import ToolTip


class TabWidget:
    def __init__(self, frame: tk.Frame,
                 inner: tk.Frame, label: tk.Label, tooltip: ToolTip):
        self.frame = frame
        self.inner = inner
        self.label = label
        self.tooltip = tooltip


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
        tooltip = ToolTip(frame, text=text)
        return TabWidget(frame, inner, label, tooltip)

    def make_content_widget(self) -> tk.Frame:
        frame = tk.Frame(self.parent.content_container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame

    def change_name(self, name: str) -> None:
        self.name = name
        self.set_tab_text()
        self.tab.tooltip.set_text(name)
        self.parent.update_tabs()

    def get_index(self) -> int:
        for i, page in enumerate(self.parent.pages):
            if page == self:
                return i

        return -1

    def set_tab_text(self, index: Optional[int] = None) -> None:
        text = self.name

        if args.max_tab_width:
            text = text[:args.max_tab_width]

        if args.numbers:
            if index is None:
                index = self.get_index()

            if index >= 0:
                text = f"{index + 1}. {text}"

        if len(text) < 4:
            space = "  "
            text = f"{space}{text}{space}"

        self.tab.label.configure(text=text)


class Book(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self.parent = parent
        self.pages: List[Page] = []

        self.tabs_frame = tk.Frame(self)
        self.tabs_canvas = tk.Canvas(self.tabs_frame, borderwidth=0, highlightthickness=0)
        self.tabs_canvas.configure(background=app.theme.tabs_container_color)

        tabs_scrollbar = tk.Scrollbar(self.tabs_frame, orient="horizontal")
        self.tabs_canvas.configure(xscrollcommand=tabs_scrollbar.set)
        tabs_scrollbar.configure(command=self.tabs_canvas.xview)

        self.tabs_container = tk.Frame(self.tabs_canvas, background=app.theme.background_color)
        self.tabs_container_id = self.tabs_canvas.create_window((0, 0), window=self.tabs_container, anchor="nw")
        self.tabs_container.bind("<Configure>", lambda e: self.update_tabs())
        self.tabs_container.configure(background=app.theme.tabs_container_color)

        if args.tabs:
            self.tabs_canvas.grid(row=0, column=0, sticky="ew")

        # tabs_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tabs_frame.grid(row=0, column=0, sticky="ew")

        self.tabs_frame.configure(background=app.theme.tabs_container_color)
        self.tabs_frame.grid_rowconfigure(0, weight=0)
        self.tabs_frame.grid_columnconfigure(0, weight=1)
        self.tabs_frame.bind("<Configure>", lambda e: self.on_tabs_configure())

        self.content_container = tk.Frame(self)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.current_page: Optional[Page] = None
        self.drag_page: Optional[Page] = None
        self.dragging = False

        if args.display:
            padx = (0, 0)
            pady = (0, 0)
        else:
            padx = ((app.theme.padx, app.theme.right_padding))
            pady = (app.theme.pady, 0)

        self.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)
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

        self.discover_debouncer = ""
        self.discover_delay = 250

    def tab_click(self, id: str) -> None:
        self.end_tab_drag()
        self.select(id)

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
        self.bind_recursive("<ButtonRelease-1>", lambda e: self.tab_click(page.id), page.tab.frame)

    def bind_tab_mousewheel(self, widget: tk.Widget) -> None:
        self.bind_recursive("<Button-4>", lambda e: self.mousewheel_up(e), widget)
        self.bind_recursive("<Button-5>", lambda e: self.mousewheel_down(e), widget)

    def bind_tab_right_click(self, page: Page) -> None:
        self.bind_recursive("<Button-3>", lambda e: self.tab_right_click(e, page.id), page.tab.frame)

    def bind_tab_middle_click(self, page: Page) -> None:
        self.bind_recursive("<Button-2>", lambda e: self.tab_middle_click(page), page.tab.frame)

    def bind_tab_drag(self, page: Page) -> None:
        self.bind_recursive("<B1-Motion>", lambda e: self.do_tab_drag(e, page), page.tab.frame)

    def add(self, name: str) -> Page:
        page = Page(self, name)
        self.pages.append(page)
        self.current_page = page
        self.add_tab(page)
        self.add_content(page.content)
        self.check_max_tabs()
        return page

    def check_max_tabs(self) -> None:
        if args.max_tabs <= 0:
            return

        ids = self.ids()

        if len(ids) <= args.max_tabs:
            return

        for id in ids[:-args.max_tabs]:
            self.close(id)

    def current(self) -> str:
        if not self.current_page:
            return ""

        return self.current_page.id

    def select(self, id: str) -> bool:
        if len(self.pages) == 0:
            return False

        page = self.get_page_by_id(id)

        if page:
            self.hide_all_except(page.id)
            self.current_page = page
            self.scroll_to_page(page)

            if self.on_change:
                self.on_change()

            self.update_tab_colors()
            return True

        return False

    def select_first(self) -> None:
        if len(self.pages) == 0:
            return

        self.select(self.pages[0].id)

    def select_last(self) -> None:
        if len(self.pages) == 0:
            return

        self.select(self.pages[-1].id)

    def select_by_index(self, index: int) -> None:
        if len(self.pages) == 0:
            return

        if index < 0:
            index = 0
        elif index >= len(self.pages):
            index = len(self.pages) - 1

        self.select(self.pages[index].id)

    def select_by_name(self, name: str) -> None:
        name = name.lower()

        for page in self.pages:
            if page.name.lower() == name:
                self.select(page.id)
                return

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

    def get_page_by_index(self, index: int) -> Optional[Page]:
        if index < 0 or index >= len(self.pages):
            return None

        return self.pages[index]

    def ids(self) -> List[str]:
        return [page.id for page in self.pages]

    def add_tab(self, page: Page) -> None:
        self.bind_tab_click(page)
        self.bind_tab_mousewheel(page.tab.frame)
        self.bind_tab_right_click(page)
        self.bind_tab_middle_click(page)
        self.bind_tab_drag(page)
        self.update_tab_columns()
        self.check_hide_tabs()

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
        length = len(self.pages)

        if index == 0:
            if args.wrap and (length >= 2):
                index = length - 1
            else:
                return
        else:
            index -= 1

        ToolTip.hide_all()
        page = self.pages[index]
        self.select(page.id)

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

        ToolTip.hide_all()
        page = self.pages[index]
        self.select(page.id)

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

        self.update_tab_columns()
        self.discover()
        self.check_hide_tabs()

    def do_tab_drag(self, event: Any, page: Page) -> None:
        if not args.reorder:
            return

        if not self.dragging:
            self.dragging = True
            self.drag_page = page
            self.drag_index = self.pages.index(page)
            self.drag_x = event.x_root
            self.select(page.id)
            return

        if not self.drag_page:
            return

        x = event.x_root - self.drag_x
        new_page = None

        if x >= args.drag_threshold:
            new_page = self.get_page_by_index(self.drag_index + 1)
        elif x <= 0 - args.drag_threshold:
            new_page = self.get_page_by_index(self.drag_index - 1)

        if not new_page:
            return

        old_index = self.pages.index(self.drag_page)
        new_index = self.pages.index(new_page)

        self.drag_index = new_index
        self.drag_x = event.x_root

        self.pages.insert(new_index, self.pages.pop(old_index))
        self.scroll_to_page(new_page)
        self.update_tab_columns()

    def get_center_x(self, page: Page) -> int:
        return page.tab.frame.winfo_rootx() + page.tab.frame.winfo_width() // 2

    def get_page_at_x(self, x: int) -> Optional[Page]:
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
        widget.bind(what, lambda e: action(e))

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
            page.set_tab_text(i)
            page.tab.frame.grid(row=0, column=i, sticky="ew")

    def on_tabs_configure(self) -> None:
        if self.discover_debouncer:
            app.root.after_cancel(self.discover_debouncer)

        self.discover_debouncer = app.root.after(self.discover_delay, lambda: self.discover())

    def discover(self) -> None:
        if not self.current_page:
            return

        self.scroll_to_page(self.current_page)

    def move_to_start(self, id: str) -> None:
        for page in self.pages:
            if page.id == id:
                self.pages.insert(0, self.pages.pop(self.pages.index(page)))
                self.update_tab_columns()
                self.select(id)
                return

    def move_to_end(self, id: str) -> None:
        for page in self.pages:
            if page.id == id:
                self.pages.append(self.pages.pop(self.pages.index(page)))
                self.update_tab_columns()
                self.select(id)
                return

    def move_left(self, page: Optional[Page] = None) -> None:
        if not page:
            page = self.current_page

        if not page:
            return

        index = self.pages.index(page)

        if index == 0:
            return

        self.pages.insert(index - 1, self.pages.pop(index))
        self.update_tab_columns()
        self.select(page.id)

    def move_right(self, page: Optional[Page] = None) -> None:
        if not page:
            page = self.current_page

        if not page:
            return

        index = self.pages.index(page)

        if index == len(self.pages) - 1:
            return

        self.pages.insert(index + 1, self.pages.pop(index))
        self.update_tab_columns()
        self.select(page.id)

    def mousewheel_up(self, event: Any) -> None:
        from .keyboard import keyboard

        if keyboard.ctrl or keyboard.shift:
            self.move_left()
        else:
            self.select_left()

    def mousewheel_down(self, event: Any) -> None:
        from .keyboard import keyboard

        if keyboard.ctrl or keyboard.shift:
            self.move_right()
        else:
            self.select_right()

    def highlight(self, id: str) -> None:
        for page in self.pages:
            if page.id == id:
                page.tab.label.configure(font=app.theme.font_tab_highlight)
            else:
                page.tab.label.configure(font=app.theme.font_tab)

    def remove_highlights(self) -> None:
        for page in self.pages:
            page.tab.label.configure(font=app.theme.font_tab)

    def check_hide_tabs(self) -> None:
        if not args.tabs_always:
            if len(self.pages) <= 1:
                self.tabs_frame.grid_remove()
            else:
                self.tabs_frame.grid()
