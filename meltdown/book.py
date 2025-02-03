from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any
from collections.abc import Callable
from dataclasses import dataclass

# Modules
from .app import app
from .args import args
from .utils import utils
from .tooltips import ToolTip
from .widgetutils import widgetutils
from .tips import tips


@dataclass
class TabWidget:
    def __init__(
        self,
        frame: tk.Frame,
        inner: tk.Frame,
        label: tk.Label,
        tooltip_1: ToolTip,
        tooltip_2: ToolTip,
    ):
        self.frame = frame
        self.inner = inner
        self.label = label
        self.tooltip_1 = tooltip_1
        self.tooltip_2 = tooltip_2


class Page:
    notebox_id = 0

    def __init__(
        self, parent: Book, name: str, mode: str, tooltip: str, pin: bool
    ) -> None:
        self.parent = parent
        self.name = name
        self.mode = mode
        self.tooltip = tooltip
        self.picked = False
        self.tab = self.make_tab_widget()
        self.content = self.make_content_widget()
        self.pin = pin
        self.id_ = f"page_{Page.notebox_id}"
        Page.notebox_id += 1

    def make_tab_widget(self) -> TabWidget:
        frame = tk.Frame(self.parent.tabs_container)
        frame.configure(background=app.theme.tab_border)
        frame.configure(cursor="hand2")
        inner = tk.Frame(frame)
        inner.configure(cursor="hand2")
        inner.configure(background=app.theme.tab_normal_background)

        inner.pack(
            expand=True,
            fill="both",
            padx=app.theme.tab_border_width,
            pady=app.theme.tab_border_width,
        )

        if self.mode == "ignore":
            font = app.theme.font("tab_alt")
        else:
            font = app.theme.font("tab")

        label = tk.Label(inner, text=self.name, font=font)
        label.configure(background=app.theme.tab_normal_background)
        label.configure(foreground=app.theme.tab_normal_foreground)

        label.pack(
            expand=True, fill="both", padx=app.theme.tab_padx, pady=app.theme.tab_pady
        )

        label.configure(cursor="hand2")
        tooltip_1 = ToolTip(inner, text=self.tooltip)
        tooltip_2 = ToolTip(label, text=self.tooltip)
        return TabWidget(frame, inner, label, tooltip_1, tooltip_2)

    def make_content_widget(self) -> tk.Frame:
        frame = tk.Frame(self.parent.content_container)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame

    def update_tooltip(self) -> None:
        text = self.tooltip if self.tooltip else "Empty Tab"
        self.tab.tooltip_1.set_text(text)
        self.tab.tooltip_2.set_text(text)

    def get_index(self) -> int:
        for i, page in enumerate(self.parent.pages):
            if page == self:
                return i

        return -1

    def set_tab_text(self, index: int | None = None) -> None:
        text = self.name

        if args.max_tab_width:
            text = text[: args.max_tab_width]

        if args.tab_numbers:
            if index is None:
                index = self.get_index()

            if index >= 0:
                text = f"{index + 1}. {text}"

        if len(text) < 4:
            space = "  "
            text = f"{space}{text}{space}"

        if self.pin:
            icon = args.pin_icon
            text = f"{icon} {text}"

        self.tab.label.configure(text=text)


class Book(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self.parent = parent
        self.pages: list[Page] = []
        self.tabs_enabled = True
        self.tabs_manual = False
        self.panel = tk.Frame(self)
        self.left_icon = "<"
        self.right_icon = ">"

        self.button_left = widgetutils.get_button(
            self.panel, self.left_icon, self.button_left_click, style="alt"
        )

        self.button_right = widgetutils.get_button(
            self.panel, self.right_icon, self.button_right_click, style="alt"
        )

        ToolTip(self.button_left, text=tips["tabs_left"])
        self.button_left.set_bind("<Button-2>", lambda e: self.select_first())
        self.button_left.set_bind("<Button-3>", lambda e: self.btn_right_click(e))
        self.bind_tab_mousewheel(self.button_left)

        ToolTip(self.button_right, text=tips["tabs_right"])
        self.button_right.set_bind("<Button-2>", lambda e: self.select_last())
        self.button_right.set_bind("<Button-3>", lambda e: self.btn_right_click(e))
        self.bind_tab_mousewheel(self.button_right)

        self.tabs_frame = tk.Frame(self.panel)

        self.tabs_canvas = tk.Canvas(
            self.tabs_frame, borderwidth=0, highlightthickness=0
        )

        self.tabs_canvas.configure(background=app.theme.tabs_container_color)
        self.bind_tab_mousewheel(self.tabs_canvas)

        tabs_scrollbar = tk.Scrollbar(self.tabs_frame, orient="horizontal")
        self.tabs_canvas.configure(xscrollcommand=tabs_scrollbar.set)
        tabs_scrollbar.configure(command=self.tabs_canvas.xview)

        self.tabs_container = tk.Frame(
            self.tabs_canvas, background=app.theme.background_color
        )

        self.tabs_container_id = self.tabs_canvas.create_window(
            (0, 0), window=self.tabs_container, anchor="nw"
        )

        self.tabs_container.bind("<Configure>", lambda e: self.update_tabs())
        self.tabs_container.configure(background=app.theme.tabs_container_color)
        self.panel.configure(background=app.theme.tabs_container_color)

        if args.show_tabs:
            self.tabs_canvas.grid(row=0, column=0, sticky="ew")

        self.panel.grid(row=0, column=0, sticky="ew")
        self.panel.grid_columnconfigure(0, weight=0)
        self.panel.grid_columnconfigure(1, weight=1)
        self.panel.grid_columnconfigure(2, weight=0)

        self.button_left.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.button_right.grid(row=0, column=2, sticky="ew", padx=(10, 0))

        self.tabs_frame.grid(row=0, column=1, sticky="ew")
        self.tabs_frame.grid_propagate(True)

        self.tabs_frame.configure(background=app.theme.tabs_container_color)
        self.tabs_frame.grid_rowconfigure(0, weight=0)
        self.tabs_frame.grid_columnconfigure(0, weight=1)
        self.tabs_frame.bind("<Configure>", lambda e: self.on_tabs_configure())

        self.content_container = tk.Frame(self)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.current_page: Page | None = None
        self.drag_page: Page | None = None
        self.dragging = False

        padx = app.theme.padx
        pady = app.theme.pady

        self.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.bind_tab_mousewheel(self.tabs_container)
        self.tabs_canvas.bind("<ButtonRelease-1>", lambda e: self.tabs_click())

        if args.tab_double_click:
            self.tabs_canvas.bind(
                "<Double-Button-1>", lambda e: self.tabs_double_click()
            )

        self.on_tab_right_click: Callable[..., Any] | None = None
        self.on_tab_middle_click: Callable[..., Any] | None = None
        self.on_tabs_click: Callable[..., Any] | None = None
        self.on_tabs_double_click: Callable[..., Any] | None = None
        self.on_change: Callable[..., Any] | None = None
        self.on_reorder: Callable[..., Any] | None = None
        self.on_num_tabs_change: Callable[..., Any] | None = None
        self.on_button_right_click: Callable[..., Any] | None = None

        self.discover_debouncer = ""
        self.discover_delay = 250
        self.num_tabs_after = ""

    def tab_click(self, id_: str) -> None:
        from .keyboard import keyboard

        if keyboard.shift:
            self.pick_range(id_)
            return

        if keyboard.ctrl:
            self.pick_one(id_)
            return

        if keyboard.alt:
            self.move_to_end(id_)
            return

        self.unpick()
        self.end_tab_drag()
        self.select(id_)

    def tab_right_click(self, event: Any, id_: str) -> None:
        if self.on_tab_right_click:
            self.on_tab_right_click(event, id_)

    def tabs_click(self) -> None:
        if self.on_tabs_click:
            self.on_tabs_click()

    def tabs_double_click(self) -> None:
        if self.on_tabs_double_click:
            self.on_tabs_double_click()

    def tab_middle_click(self, page: Page) -> None:
        if self.on_tab_middle_click:
            self.on_tab_middle_click(page.id_)

    def bind_tab_click(self, page: Page) -> None:
        self.bind_recursive(
            "<ButtonRelease-1>", lambda e: self.tab_click(page.id_), page.tab.frame
        )

    def mousewheel_up(self, ctrl: bool = False, shift: bool = False) -> None:
        if not args.tabs_wheel:
            return

        if ctrl:
            self.move_left()
        elif shift:
            self.scroll_left()
        else:
            self.select_left()

    def mousewheel_down(self, ctrl: bool = False, shift: bool = False) -> None:
        if not args.tabs_wheel:
            return

        if ctrl:
            self.move_right()
        elif shift:
            self.scroll_right()
        else:
            self.select_right()

    def bind_tab_mousewheel(self, widget: tk.Widget) -> None:
        self.bind_recursive("<Button-4>", lambda e: self.mousewheel_up(), widget)

        self.bind_recursive(
            "<Control-Button-4>", lambda e: self.mousewheel_up(True, False), widget
        )

        self.bind_recursive(
            "<Shift-Button-4>", lambda e: self.mousewheel_up(False, True), widget
        )

        self.bind_recursive("<Button-5>", lambda e: self.mousewheel_down(), widget)

        self.bind_recursive(
            "<Control-Button-5>", lambda e: self.mousewheel_down(True, False), widget
        )

        self.bind_recursive(
            "<Shift-Button-5>", lambda e: self.mousewheel_down(False, True), widget
        )

    def bind_tab_right_click(self, page: Page) -> None:
        self.bind_recursive(
            "<Button-3>", lambda e: self.tab_right_click(e, page.id_), page.tab.frame
        )

    def bind_tab_middle_click(self, page: Page) -> None:
        self.bind_recursive(
            "<Button-2>", lambda e: self.tab_middle_click(page), page.tab.frame
        )

    def bind_tab_drag(self, page: Page) -> None:
        self.bind_recursive(
            "<B1-Motion>", lambda e: self.do_tab_drag(e, page), page.tab.frame
        )

    def add(
        self,
        name: str,
        mode: str,
        tooltip: str,
        position: str = "end",
        pin: bool = False,
    ) -> Page:
        tooltip = self.clean_tooltip(tooltip)
        page = Page(self, name, mode=mode, tooltip=tooltip, pin=pin)

        if position == "start":
            self.pages.insert(0, page)
        else:
            self.pages.append(page)

        self.current_page = page
        self.add_tab(page)
        self.add_content(page.content)
        self.check_max_tabs()
        self.check_num_tabs_change()
        page.update_tooltip()
        return page

    def check_max_tabs(self) -> None:
        if args.max_tabs <= 0:
            return

        ids = self.ids()

        if len(ids) <= args.max_tabs:
            return

        for id_ in ids[: -args.max_tabs]:
            self.close(id_)

    def current(self) -> str:
        if not self.current_page:
            return ""

        return self.current_page.id_

    def select(self, id_: str, unpick: bool = True) -> bool:
        if not self.pages:
            return False

        page = self.get_page_by_id(id_)

        if not page:
            return False

        self.hide_all_except(page.id_)
        self.current_page = page
        self.scroll_to_page(page)

        if unpick:
            self.unpick()

        if self.on_change:
            self.on_change()

        self.update_tab_colors()
        self.check_buttons()
        return True

    def select_first(self) -> None:
        if not self.pages:
            return

        self.select(self.pages[0].id_)

    def select_last(self) -> None:
        if not self.pages:
            return

        self.select(self.pages[-1].id_)

    def get_first(self) -> Page | None:
        if not self.pages:
            return None

        return self.pages[0]

    def get_last(self) -> Page | None:
        if not self.pages:
            return None

        return self.pages[-1]

    def select_by_index(self, index: int) -> None:
        if not self.pages:
            return

        if index < 0:
            index = 0
        elif index >= len(self.pages):
            index = len(self.pages) - 1

        self.select(self.pages[index].id_)

    def select_by_name(self, name: str) -> None:
        closest = ""
        name = name.lower()

        for page in self.pages:
            page_name = page.name.lower()

            if page_name == name:
                closest = page.id_
                break

            if page_name.startswith(name):
                closest = page.id_

        if closest:
            self.select(closest)

    def update_tab_colors(self) -> None:
        if not self.current_page:
            return

        for page in self.pages:
            if page.id_ == self.current_page.id_:
                page.tab.inner.configure(background=app.theme.tab_selected_background)
                page.tab.label.configure(background=app.theme.tab_selected_background)
                page.tab.label.configure(foreground=app.theme.tab_selected_foreground)
            else:
                page.tab.inner.configure(background=app.theme.tab_normal_background)
                page.tab.label.configure(background=app.theme.tab_normal_background)
                page.tab.label.configure(foreground=app.theme.tab_normal_foreground)

    def hide_all_except(self, id_: str) -> None:
        for page in self.pages:
            if page.id_ != id_:
                page.content.grid_remove()
            else:
                page.content.grid()

    def get_page_by_id(self, id_: str) -> Page | None:
        for page in self.pages:
            if page.id_ == id_:
                return page

        return None

    def get_page_by_index(self, index: int) -> Page | None:
        if index < 0 or index >= len(self.pages):
            return None

        return self.pages[index]

    def ids(self) -> list[str]:
        return [page.id_ for page in self.pages]

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

    def index(self, id_: str) -> int:
        for i, page in enumerate(self.pages):
            if page.id_ == id_:
                return i

        return -1

    def select_left(self) -> None:
        if not self.pages:
            return

        if not self.current_page:
            return

        index = self.index(self.current_page.id_)
        length = len(self.pages)

        if index == 0:
            if args.wrap_tabs and (length >= 2):
                index = length - 1
            else:
                return
        else:
            index -= 1

        ToolTip.hide_all()
        page = self.pages[index]
        self.select(page.id_)

    def select_right(self) -> None:
        if not self.pages:
            return

        if not self.current_page:
            return

        index = self.index(self.current_page.id_)
        length = len(self.pages)

        if index == length - 1:
            if args.wrap_tabs and (length >= 2):
                index = 0
            else:
                return
        else:
            index += 1

        ToolTip.hide_all()
        page = self.pages[index]
        self.select(page.id_)

    def get_name(self, id_: str) -> str:
        page = self.get_page_by_id(id_)

        if not page:
            return ""

        return page.name

    def set_name(self, id_: str, name: str) -> None:
        page = self.get_page_by_id(id_)

        if not page:
            return

        page.name = name
        page.set_tab_text()
        self.update_tabs()
        self.discover()

    def set_pin(self, id_: str, pin: bool) -> None:
        page = self.get_page_by_id(id_)

        if not page:
            return

        page.pin = pin
        page.set_tab_text()
        self.update_tabs()
        self.discover()

    def close(self, id_: str) -> None:
        page = self.get_page_by_id(id_)

        if not page:
            return

        index = self.index(id_)
        was_current = self.current_page == self.pages[index]
        page.tab.frame.grid_forget()
        page.content.grid_forget()
        self.pages.pop(index)

        if not self.pages:
            self.current_page = None
        elif was_current:
            if index == len(self.pages):
                self.select(self.pages[index - 1].id_)
            else:
                self.select(self.pages[index].id_)

        self.update_tab_columns()
        self.discover()
        self.check_hide_tabs()
        self.check_num_tabs_change()

    def do_tab_drag(self, event: Any, page: Page) -> None:
        from .keyboard import keyboard

        if keyboard.ctrl or keyboard.shift:
            return

        if not args.reorder:
            return

        if not self.dragging:
            self.dragging = True
            self.drag_page = page
            self.drag_index = self.pages.index(page)
            self.drag_x = event.x_root
            self.select(page.id_, False)
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

        picked = self.get_picked()
        old_index = self.pages.index(self.drag_page)
        new_index = self.pages.index(new_page)
        difference = abs(new_index - old_index)
        direction = ""

        if new_index < old_index:
            direction = "left"
        elif new_index > old_index:
            direction = "right"

        if not direction:
            return

        if picked:
            if direction == "left":
                if self.pages.index(picked[0]) == 0:
                    return
            elif direction == "right":
                if self.pages.index(picked[-1]) == len(self.pages) - 1:
                    return

        self.drag_index = new_index
        self.drag_x = event.x_root

        if self.drag_page.picked:
            if direction == "right":
                picked.reverse()

            leader = self.pages.index(picked[0])

            if direction == "left":
                leader -= difference
            elif direction == "right":
                leader += difference

            for i, p_page in enumerate(picked):
                if direction == "left":
                    old_index = self.pages.index(p_page)
                    self.pages.insert(leader + i, self.pages.pop(old_index))
                elif direction == "right":
                    old_index = self.pages.index(p_page)
                    self.pages.insert(leader - i, self.pages.pop(old_index))
        else:
            self.pages.insert(new_index, self.pages.pop(old_index))

        self.scroll_to_page(new_page)
        self.update_tab_columns()

    def get_center_x(self, page: Page) -> int:
        return page.tab.frame.winfo_rootx() + page.tab.frame.winfo_width() // 2

    def get_page_at_x(self, x: int) -> Page | None:
        for page in self.pages:
            tab_x = page.tab.frame.winfo_rootx()
            tab_width = page.tab.frame.winfo_width()

            if tab_x <= x <= (tab_x + tab_width):
                return page

        return None

    def end_tab_drag(self) -> None:
        self.dragging = False
        self.drag_page = None

        if self.on_reorder:
            self.on_reorder()

    def bind_recursive(
        self, what: str, action: Callable[..., Any], widget: tk.Widget
    ) -> None:
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

        self.discover_debouncer = app.root.after(
            self.discover_delay, lambda: self.discover()
        )

    def discover(self) -> None:
        if not self.current_page:
            return

        self.scroll_to_page(self.current_page)

    def move_to_start(self, id_: str) -> None:
        pages = self.picked_or_page(id_)

        if not pages:
            return

        i = 0

        for page in pages:
            self.pages.insert(i, self.pages.pop(self.pages.index(page)))
            i += 1

        self.update_tab_columns()
        self.select(id_)

        if self.on_reorder:
            self.on_reorder()

    def move_to_end(self, id_: str) -> None:
        pages = self.picked_or_page(id_)

        if not pages:
            return

        i = len(self.pages) - 1
        pages.reverse()

        for page in pages:
            self.pages.insert(i, self.pages.pop(self.pages.index(page)))
            i -= 1

        self.update_tab_columns()
        self.select(id_)

        if self.on_reorder:
            self.on_reorder()

    def move_left(self, page: Page | None = None) -> None:
        if not page:
            page = self.current_page

        if not page:
            return

        index = self.pages.index(page)

        if index == 0:
            return

        self.pages.insert(index - 1, self.pages.pop(index))
        self.update_tab_columns()
        self.select(page.id_)

        if self.on_reorder:
            self.on_reorder()

    def move_right(self, page: Page | None = None) -> None:
        if not page:
            page = self.current_page

        if not page:
            return

        index = self.pages.index(page)

        if index == len(self.pages) - 1:
            return

        self.pages.insert(index + 1, self.pages.pop(index))
        self.update_tab_columns()
        self.select(page.id_)

        if self.on_reorder:
            self.on_reorder()

    def highlight(self, id_: str) -> None:
        for page in self.pages:
            if page.id_ == id_:
                page.tab.label.configure(font=app.theme.font("tab_highlight"))
            else:
                page.tab.label.configure(font=app.theme.font("tab"))

    def remove_highlights(self) -> None:
        for page in self.pages:
            page.tab.label.configure(font=app.theme.font("tab"))

    def check_hide_tabs(self) -> None:
        if self.tabs_manual:
            return

        if args.tabs_always:
            return

        if len(self.pages) <= 1:
            self.hide_tabs()
        else:
            self.show_tabs()

    def hide_tabs(self) -> None:
        self.tabs_enabled = False
        self.panel.grid_remove()

    def show_tabs(self) -> None:
        self.tabs_enabled = True
        self.panel.grid()

    def toggle_tabs(self) -> None:
        self.tabs_manual = True

        if self.tabs_enabled:
            self.hide_tabs()
        else:
            self.show_tabs()

    def check_num_tabs_change(self) -> int | None:
        if self.on_num_tabs_change:
            if self.num_tabs_after:
                app.root.after_cancel(self.num_tabs_after)

            self.num_tabs_after = app.root.after(100, lambda: self.do_num_tabs_change())

        return None

    def do_num_tabs_change(self) -> None:
        if self.on_num_tabs_change:
            self.on_num_tabs_change(len(self.pages))

    def pick_range(self, id_: str) -> None:
        if not self.current_page:
            return

        self.unpick()
        ids = self.ids()
        index = ids.index(id_)
        start = ids.index(self.current_page.id_)
        end = index

        if start > end:
            start, end = end, start

        for i, page in enumerate(self.pages):
            if start <= i <= end:
                self.do_pick(page)

    def pick_one(self, id_: str) -> None:
        page = self.get_page_by_id(id_)

        if not page:
            return

        self.pick(page)

    def pick(self, page: Page) -> None:
        if not self.current_page:
            return

        pick_value = not page.picked

        if pick_value:
            if not self.get_picked():
                self.do_pick(self.current_page)

            self.do_pick(page)
        else:
            self.do_unpick(page)

    def unpick(self) -> None:
        picked = self.get_picked()

        if not picked:
            return

        for page in picked:
            self.do_unpick(page)

    def do_pick(self, page: Page) -> None:
        color = app.theme.tab_picked_border
        page.tab.frame.configure(background=color)
        page.picked = True

    def do_unpick(self, page: Page) -> None:
        color = app.theme.tab_border
        page.tab.frame.configure(background=color)
        page.picked = False

    def get_picked(self) -> list[Page]:
        return [page for page in self.pages if page.picked]

    def update_tooltip(self, id_: str, tooltip: str) -> None:
        page = self.get_page_by_id(id_)

        if not page:
            return

        page.tooltip = self.clean_tooltip(tooltip)
        page.update_tooltip()

    def clean_tooltip(self, tooltip: str) -> str:
        return utils.compact_text(tooltip, args.tab_tooltip_length)

    def picked_or_page(self, id_: str) -> list[Page]:
        pages = self.get_picked()

        if not pages:
            page = self.get_page_by_id(id_)

            if page:
                pages.append(page)

        return pages

    def disable_button(self, side: str) -> None:
        button = getattr(self, f"button_{side}")
        button.set_style("disabled")

    def enable_button(self, side: str) -> None:
        button = getattr(self, f"button_{side}")
        button.set_style("alt")

    def check_buttons(self) -> None:
        if not self.pages:
            self.disable_button("left")
            self.disable_button("right")
            return

        if len(self.pages) == 1:
            self.disable_button("left")
            self.disable_button("right")
            return

        if not args.wrap_tabs:
            if not self.current_page:
                return

            index = self.index(self.current_page.id_)

            if index == 0:
                self.disable_button("left")
            else:
                self.enable_button("left")

            if index == len(self.pages) - 1:
                self.disable_button("right")
            else:
                self.enable_button("right")
        else:
            self.enable_button("left")
            self.enable_button("right")

    def btn_right_click(self, event: Any) -> None:
        if self.on_button_right_click:
            self.on_button_right_click(event)

    def has_overflow(self) -> bool:
        return self.tabs_canvas.bbox("all")[2] > self.tabs_canvas.winfo_width()

    def scroll_left(self) -> None:
        if self.has_overflow():
            self.tabs_canvas.xview_scroll(-1, "units")

    def scroll_right(self) -> None:
        if self.has_overflow():
            self.tabs_canvas.xview_scroll(1, "units")

    def button_left_click(self) -> None:
        from .keyboard import keyboard

        if keyboard.shift:
            self.scroll_left()
        elif keyboard.ctrl:
            self.move_left()
        else:
            self.select_left()

    def button_right_click(self) -> None:
        from .keyboard import keyboard

        if keyboard.shift:
            self.scroll_right()
        elif keyboard.ctrl:
            self.move_right()
        else:
            self.select_right()

    def sort_pins(self, mode: str = "start") -> None:
        pins = []
        normal = []

        for page in self.pages:
            if page.pin:
                pins.append(page)
            else:
                normal.append(page)

        if mode == "start":
            self.pages = pins + normal
        else:
            self.pages = normal + pins

        self.update_tab_columns()
        self.reselect()

    def reselect(self) -> None:
        if self.current_page:
            self.select(self.current_page.id_)
