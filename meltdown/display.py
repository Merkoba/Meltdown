from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any, TYPE_CHECKING

# Modules
from .app import app
from .config import config
from .menus import Menu
from .dialogs import Dialog
from .output import Output
from .bottom import Bottom
from .book import Book, Page
from .find import Find
from .args import args
from .utils import utils
from .autoscroll import autoscroll

if TYPE_CHECKING:
    from .session import Conversation


class Tab:
    def __init__(
        self,
        conversation_id: str,
        tab_id: str,
        output: Output,
        find: Find,
        bottom: Bottom,
        mode: str,
        no_intro: bool,
    ) -> None:
        self.conversation_id = conversation_id
        self.tab_id = tab_id
        self.output = output
        self.find = find
        self.bottom = bottom
        self.modified = False
        self.mode = mode
        self.loaded = False
        self.streaming = False
        self.num_user_prompts = 0
        self.no_intro = no_intro


class TabConvo:
    def __init__(self, tab: Tab, convo: Conversation) -> None:
        self.tab = tab
        self.convo = convo


class Display:
    def __init__(self) -> None:
        self.prev_tab = "none"
        self.current_tab = "none"
        self.tab_streaming = "none"
        self.book: Book
        self.min_font_size = 6
        self.max_font_size = 36
        self.num_tabs_open = 0
        self.tab_number = 1
        self.max_old_tabs = 5

    def make(self) -> None:
        from .widgets import widgets

        self.book = Book(widgets.display_frame)
        self.book.on_change = lambda: self.on_tab_change()

        self.tabs: dict[str, Tab] = {}
        self.tab_list_menu = Menu()

        self.book.on_tab_right_click = lambda e, id: self.on_tab_right_click(e, id)
        self.book.on_tabs_click = lambda: self.on_tabs_click()
        self.book.on_tabs_double_click = lambda: self.on_tabs_double_click()
        self.book.on_tab_middle_click = lambda id: self.on_tab_middle_click(id)
        self.book.on_reorder = lambda: self.update_session()
        self.book.on_num_tabs_change = lambda n: self.on_num_tabs_change(n)

    def make_tab(
        self,
        name: str | None = None,
        conversation_id: str | None = None,
        select_tab: bool = True,
        mode: str = "normal",
        save: bool = True,
        no_intro: bool = False,
        position: str = "end",
    ) -> str:
        from .session import session
        from . import close

        if args.max_tabs > 0:
            if self.num_tabs() >= args.max_tabs:
                max_cmds = []
                max_cmds.append(("Close", lambda a: close.close(force=False)))
                max_cmds.append(("Ok", lambda a: None))
                Dialog.show_dialog(f"Max tabs reached ({args.max_tabs})", max_cmds)
                return ""

        if not name:
            if args.name_mode == "random":
                name = utils.random_word()
            elif args.name_mode == "noun":
                name = utils.random_noun()
            else:
                name = "tab"

            name = name.capitalize()

        name = self.prepare_name(name)

        if not conversation_id:
            conv_id = "ignore" if mode == "ignore" else ""
            conversation = session.add(name, conv_id=conv_id, position=position)
            conversation_id = conversation.id

        if not conversation_id:
            return ""

        convo = session.get_conversation(conversation_id)
        tooltip = ""

        if convo and convo.items:
            tooltip = convo.items[0].ai

        page = self.book.add(name, mode=mode, tooltip=tooltip, position=position)
        tab_id = page.id_
        find = Find(page.content, tab_id)
        output_frame = tk.Frame(page.content)
        output_frame.grid(row=1, column=0, sticky="nsew")
        output = Output(output_frame, tab_id)
        bottom = Bottom(page.content, tab_id)

        tab = Tab(
            conversation_id, tab_id, output, find, bottom, mode=mode, no_intro=no_intro
        )

        self.tabs[tab_id] = tab

        if select_tab:
            self.select_tab(tab_id)

        page.content.grid_rowconfigure(0, weight=0)
        page.content.grid_rowconfigure(1, weight=1)
        page.content.grid_rowconfigure(2, weight=0)
        self.tab_number += 1

        if save:
            session.save()

        return tab_id

    def select_tab(self, tab_id: str) -> None:
        if self.book.select(tab_id):
            app.update()

    def select_tab_by_number(self, num: int) -> None:
        if num < 1 or num > 9:
            return

        if num == 9:
            self.book.select_last()
        else:
            self.book.select_by_index(num - 1)

    def select_tab_by_string(self, what: str) -> None:
        try:
            num = int(what)
            self.select_tab_by_number(num)
        except BaseException as e:
            self.book.select_by_name(what)
            utils.error(e)

    def update_current_tab(self) -> None:
        tab_id = self.book.current()
        self.prev_tab = self.current_tab
        self.current_tab = tab_id
        self.current_tab_object = self.get_tab(tab_id)

    def on_tab_change(self) -> None:
        from .inputcontrol import inputcontrol

        self.update_current_tab()
        tab = self.get_current_tab()

        if not tab:
            return

        if not tab.loaded:
            self.load_tab(tab.tab_id)

        autoscroll.stop()
        tab.output.reset_drag()
        inputcontrol.focus()
        self.check_scroll_buttons()

    def show_intro(self, tab_id: str) -> None:
        if not args.show_intro:
            return

        text = "\n".join(app.intro)
        display.print(text, tab_id=tab_id, modified=False)
        self.format_text(tab_id, mode="all", force=True)

    def load_tab(self, tab_id: str) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not args.auto_bottom:
            self.disable_auto_bottom(tab_id)

        self.show_header(tab_id)

        if tabconvo.convo.id != "ignore":
            if not tabconvo.convo.items:
                if not tabconvo.tab.no_intro:
                    self.show_intro(tab_id)

        if not args.auto_bottom:
            self.enable_auto_bottom(tab_id)

        if tabconvo.convo.items:
            tabconvo.convo.print()

        tabconvo.tab.loaded = True

    def show_header(self, tab_id: str) -> None:
        if not args.show_header:
            return

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        nice_date = utils.to_date(tabconvo.convo.created)
        self.print(nice_date, tab_id=tab_id, modified=False)

    def get_current_tab(self) -> Tab | None:
        if hasattr(self, "current_tab_object"):
            return self.current_tab_object

        return None

    def get_current_output(self) -> Output | None:
        return self.get_output(self.current_tab)

    def get_current_bottom(self) -> Bottom | None:
        return self.get_bottom(self.current_tab)

    def get_tab(self, tab_id: str) -> Tab | None:
        return self.tabs.get(tab_id)

    def get_tab_by_conversation_id(self, conversation_id: str) -> Tab | None:
        for tab in self.tabs.values():
            if tab.conversation_id == conversation_id:
                return tab

        return None

    def get_output(self, tab_id: str) -> Output | None:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.output

        return None

    def get_bottom(self, tab_id: str) -> Bottom | None:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.bottom

        return None

    def on_tab_right_click(self, event: Any, tab_id: str) -> None:
        from .menumanager import tab_menu

        self.tab_menu_id = tab_id
        self.tab_menu_event = event
        tab_menu.show(event, "tab_right_click")

    def on_tab_middle_click(self, tab_id: str) -> None:
        from . import close
        from .keyboard import keyboard

        if keyboard.shift:
            close.close_others(tab_id=tab_id)
        elif keyboard.ctrl:
            close.close(tab_id=tab_id, force=True)
        else:
            close.close(tab_id=tab_id, force_empty=True, full=False)

    def on_tabs_click(self) -> None:
        app.hide_all()

    def on_tabs_double_click(self) -> None:
        self.make_tab()

    def show_tab_list(self, event: Any = None) -> None:
        from .widgets import widgets
        from . import close

        widget = widgets.stop_button

        if not widget:
            return

        self.tab_list_menu.clear()

        def add_item(page: Page, num: int) -> None:
            def command() -> None:
                return self.select_tab(page.id_)

            def alt_cmd() -> None:
                close.close(tab_id=page.id_, force=True)
                self.show_tab_list(event)

            tab = self.get_tab(page.id_)

            if not tab:
                return

            underline = tab.streaming

            self.tab_list_menu.add(
                text=page.name,
                command=lambda e: command(),
                alt_command=lambda e: alt_cmd(),
                underline=underline,
            )

        selected = 0

        for i, page in enumerate(self.book.pages):
            add_item(page, i + 1)

            if page.id_ == self.current_tab:
                selected = i

        self.tab_list_menu.show(event, widget=widget, selected=selected)

    def rename_tab(self, tab_id: str | None = None, name: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        if name:
            self.do_rename_tab(tab_id, name)
            return

        name = self.get_tab_name(tab_id)

        Dialog.show_input(
            "Pick a name", lambda s: self.do_rename_tab(tab_id, s), value=name
        )

    def do_rename_tab(self, tab_id: str, name: str) -> None:
        from .session import session

        name = self.prepare_name(name)

        if not name:
            self.redo_auto_name_tab(tab_id)
            return

        tab = self.get_tab(tab_id)

        if not tab:
            return

        o_name = self.get_tab_name(tab_id)

        if name == o_name:
            return

        self.book.change_name(tab_id, name)
        session.change_name(tab.conversation_id, name)

    def tab_menu_close(self) -> None:
        from . import close

        close.close(tab_id=self.tab_menu_id, full=False)

    def tab_ids(self) -> list[str]:
        return self.book.ids()

    def index(self, tab_id: str) -> int:
        return self.book.index(tab_id)

    def to_top(self, tab_id: str | None = None) -> None:
        if tab_id:
            tab = self.get_tab(tab_id)
        else:
            tab = self.get_current_tab()

        if not tab:
            return

        autoscroll.stop()
        tab.output.to_top()

    def to_bottom(self, tab_id: str | None = None) -> None:
        if tab_id:
            tab = self.get_tab(tab_id)
        else:
            tab = self.get_current_tab()

        if not tab:
            return

        autoscroll.stop()
        tab.output.to_bottom()
        tab.bottom.hide()

    def copy_output(self) -> None:
        output = self.get_current_output()

        if not output:
            return

        output.copy_all()

    def copy_items_or_all(self) -> None:
        output = self.get_current_output()

        if not output:
            return

        output.copy_items_or_all()

    def clear(self, tab_id: str | None = None, force: bool = False) -> None:
        from .session import session

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if tabconvo.convo.id == "ignore":
            return

        if not tabconvo.convo.items:
            if not tabconvo.tab.modified:
                return

        def action() -> None:
            if not tabconvo:
                return

            session.clear(tabconvo.tab.conversation_id)
            self.reset_tab(tabconvo.tab)

            if args.auto_name:
                name = utils.random_word()
                name = name.capitalize()
                self.do_rename_tab(tabconvo.tab.tab_id, name)

        if force or (not args.confirm_clear):
            action()
            return

        Dialog.show_confirm("Clear conversation ?", lambda: action())

    def reset_tab(self, tab: Tab) -> None:
        tab.output.reset()
        tab.modified = False
        tab.num_user_prompts = 0
        self.show_header(tab.tab_id)
        self.show_intro(tab.tab_id)

    def select_output(self) -> None:
        output = self.get_current_output()

        if output:
            output.select_all()

    def deselect_output(self) -> None:
        output = self.get_current_output()

        if output:
            output.deselect_all()

    def print(
        self, text: str, tab_id: str | None = None, modified: bool = True
    ) -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.print(text)

        if modified:
            tab.modified = True

    def insert(self, text: str, tab_id: str | None = None) -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.insert_text(text)
        tab.modified = True

    def get_tab_name(self, tab_id: str | None = None) -> str:
        if not tab_id:
            tab_id = self.current_tab

        return self.book.get_name(tab_id)

    def get_current_tab_name(self) -> str:
        return self.get_tab_name(self.current_tab)

    def num_tabs(self) -> int:
        return len(self.tab_ids())

    def remove_tab(self, tab_id: str) -> None:
        from .session import session

        tab = self.get_tab(tab_id)

        if not tab:
            return

        session.remove(tab.conversation_id)
        del self.tabs[tab_id]

    def check_scroll_buttons(self, tab_id: str | None = None) -> None:
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

        if yview[1] >= 0.9999:
            if autoscroll.direction == "down":
                autoscroll.stop()

            tab.bottom.hide()
        else:
            if yview[0] <= 0.0001:
                if autoscroll.direction == "up":
                    autoscroll.stop()

            tab.bottom.show()

            if args.scroll_percentage:
                visible_range = yview[1] - yview[0]
                total_range = 1.0 - visible_range
                perc = int((yview[0] / total_range) * 100)
                tab.bottom.set_text(f"{perc}%")
            elif args.scroll_percentage_reverse:
                visible_range = yview[1] - yview[0]
                total_range = 1.0 - visible_range
                perc = int((1.0 - yview[1]) / total_range * 100)
                tab.bottom.set_text(f"{perc}%")

        if args.disable_buttons:
            if yview[0] <= 0.0001:
                widgets.disable_top_button()
            else:
                widgets.enable_top_button()

    def tab_left(self) -> None:
        self.book.select_left()

    def tab_right(self) -> None:
        self.book.select_right()

    def apply_font_size(self, size: int) -> None:
        config.set("font_size", size)

    def set_font_size(self, text: str | None = None) -> None:
        from .menumanager import font_menu

        if not text:
            font_menu.show()
            return

        if text in ["default", "reset"]:
            display.reset_font()
            return

        try:
            size = int(text)
        except BaseException:
            return

        if size < self.min_font_size:
            size = self.min_font_size

        if size > self.max_font_size:
            size = self.max_font_size

        self.apply_font_size(size)

    def decrease_font(self) -> None:
        new_size = config.font_size - 1

        if new_size < self.min_font_size:
            return

        self.apply_font_size(new_size)

    def increase_font(self) -> None:
        new_size = config.font_size + 1

        if new_size > self.max_font_size:
            return

        self.apply_font_size(new_size)

    def pick_font_family(self, name: str | None = None) -> None:
        def action(name: str) -> None:
            self.set_font_family(name)

        if name:
            action(name)
            return

        cmds = []
        cmds.append(("Mono", lambda a: action("monospace")))
        cmds.append(("Serif", lambda a: action("serif")))
        cmds.append(("Sans", lambda a: action("sans-serif")))

        Dialog.show_dialog("Font Family", cmds)

    def set_font_family(self, name: str | None = None) -> None:
        if name not in ["sans-serif", "sans", "monospace", "mono", "serif"]:
            return

        if name == "sans":
            name = "sans-serif"
        elif name == "mono":
            name = "monospace"

        config.set("font_family", name)

    def reset_font(self) -> None:
        config.reset_one("font_size", False)
        config.reset_one("font_family")

    def update_font(self, key: str) -> None:
        for tab in self.tabs.values():
            tab.output.update_font()

            if key == "font_family":
                if tab.modified:
                    self.refresh(tab.tab_id)

    def scroll_up(
        self,
        tab_id: str | None = None,
        more: bool = False,
        disable_auto_scroll: bool = False,
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        if disable_auto_scroll:
            autoscroll.stop()

        output.scroll_up(more=more)

    def scroll_down(
        self,
        tab_id: str | None = None,
        more: bool = False,
        disable_auto_scroll: bool = False,
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        if disable_auto_scroll:
            autoscroll.stop()

        output.scroll_down(more=more)

    def update_session(self) -> None:
        from .session import session

        session.update()

    def hide_bottom(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        bottom = self.get_bottom(tab_id)

        if not bottom:
            return

        bottom.hide()

    def prompt(
        self,
        who: str,
        text: str | None = None,
        tab_id: str | None = None,
        to_bottom: bool = True,
        original: str | None = None,
        file: str | None = None,
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        if (who == "user") and to_bottom:
            self.to_bottom(tab_id)

        if args.separators and (who == "user"):
            if tab.modified:
                tab.output.separate()

        tab.output.prompt(who)

        if text:
            tab.output.insert_text(text)

        if file:
            file_text = f"File:\u00a0{file}"
            tab.output.print(file_text)

        if args.auto_name and (who == "user") and original:
            if not self.has_messages(tab_id):
                self.auto_name_tab(tab_id, original)

        if who == "ai":
            tab.num_user_prompts += 1

        tab.modified = True

    def auto_name_tab(self, tab_id: str, text: str) -> None:
        tab = self.get_tab(tab_id)

        if not tab:
            return

        if tab.mode == "ignore":
            return

        text = utils.compact_text(text, args.auto_name_length)
        self.do_rename_tab(tab_id, text)

    def redo_auto_name_tab(self, tab_id: str) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if len(tabconvo.convo.items) >= 1:
            item = tabconvo.convo.items[0]
            self.auto_name_tab(tab_id, item.user)

    def has_messages(self, tab_id: str | None = None) -> bool:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return False

        return bool(tabconvo.convo.items)

    def tab_is_empty(self, tab_id: str) -> bool:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return True

        return not bool(tabconvo.convo.items)

    def format_text(
        self, tab_id: str | None = None, mode: str = "normal", force: bool = False
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.format_text(mode=mode, force=force)

    def select_first_tab(self) -> None:
        self.book.select_first()

    def select_last_tab(self) -> None:
        self.book.select_last()

    def move_tab(self, tab_id: str | None = None) -> None:
        if len(self.tab_ids()) <= 1:
            return

        if not tab_id:
            tab_id = self.current_tab

        cmds = []
        cmds.append(("To Start", lambda a: self.move_tab_to_start(tab_id)))
        cmds.append(("To End", lambda a: self.move_tab_to_end(tab_id)))

        picked = self.get_picked()

        if picked:
            n = len(picked)
            Dialog.show_dialog(f"Move tabs? ({n})", cmds)
        else:
            Dialog.show_dialog("Move tab?", cmds)

    def move_tab_to_start(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        self.book.move_to_start(tab_id)
        self.update_session()

    def move_tab_to_end(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        self.book.move_to_end(tab_id)
        self.update_session()

    def stream_started(self, tab_id: str) -> None:
        if not args.tab_highlight:
            return

        self.book.highlight(tab_id)
        self.set_tab_streaming(tab_id)
        self.tab_streaming = tab_id

    def stream_stopped(self) -> None:
        if not args.tab_highlight:
            return

        self.book.remove_highlights()
        self.clear_tab_streaming()
        self.format_text(self.tab_streaming)
        self.update_tooltip(self.tab_streaming)

    def set_tab_streaming(self, tab_id: str) -> None:
        for key, values in self.tabs.items():
            if values.tab_id == tab_id:
                self.tabs[key].streaming = True
            else:
                self.tabs[key].streaming = False

    def clear_tab_streaming(self) -> None:
        for key in self.tabs:
            self.tabs[key].streaming = False

    def toggle_scroll(self) -> None:
        tab = self.get_current_tab()

        if not tab:
            return

        yview = tab.output.yview()

        if yview[1] >= 0.9999:
            tab.output.to_top()
        else:
            tab.output.to_bottom()

    def select_active_tab(self) -> bool:
        for key, value in self.tabs.items():
            if value.streaming:
                if key != self.current_tab:
                    self.select_tab(key)
                    return True

        return False

    def output_is_selected(self) -> bool:
        tab = self.get_current_tab()

        if not tab:
            return False

        return bool(tab.output.get_selected_text())

    def move_tab_left(self) -> None:
        self.book.move_left()

    def move_tab_right(self) -> None:
        self.book.move_right()

    def toggle_tabs(self) -> None:
        self.book.toggle_tabs()

    def on_num_tabs_change(self, num: int) -> None:
        self.num_tabs_open = num

    def is_modified(self, tab_id: str | None = None) -> bool:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return False

        return tab.modified

    def is_ignored(self, tab_id: str | None = None) -> bool:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return False

        return tabconvo.convo.id == "ignore"

    def enable_auto_bottom(self, tab_id: str) -> None:
        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.auto_bottom = True

    def disable_auto_bottom(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.auto_bottom = False

    def num_user_prompts(self, tab_id: str | None = None) -> int:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return 0

        return tab.num_user_prompts

    def refresh(self, tab_id: str | None = None) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        self.reset_tab(tabconvo.tab)
        tabconvo.convo.print()

    def get_tab_convo(self, tab_id: str | None = None) -> TabConvo | None:
        from .session import session

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return None

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return None

        return TabConvo(tab, conversation)

    def get_num_items(self, tab_id: str | None = None) -> int:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return 0

        return len(tabconvo.convo.items)

    def get_text(self, tab_id: str | None = None) -> str:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return ""

        num_lines = 0

        if args.show_header:
            num_lines += 1

        if num_lines:
            num_lines += 1

        if args.show_intro:
            num_lines += len(app.intro)

        if num_lines:
            num_lines += 1

        text = tabconvo.tab.output.get_text()

        if num_lines:
            text = text.split("\n", num_lines)[-1]

        return text.strip()

    def goto_prev_tab(self) -> None:
        if self.prev_tab == "none":
            return

        tabconvo = self.get_tab_convo(self.prev_tab)

        if not tabconvo:
            return

        self.select_tab(self.prev_tab)

    def prepare_name(self, name: str) -> str:
        return name[: config.max_name_length].strip()

    def update_scroll(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.update_scroll()

    def get_picked(self) -> list[Tab]:
        picked = self.book.get_picked()
        tabs = []

        for page in picked:
            tab = self.get_tab(page.id_)

            if tab:
                tabs.append(tab)

        return tabs

    def unpick(self) -> None:
        self.book.unpick()

    def update_tooltip(self, tab_id: str) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        item = tabconvo.convo.items[0]
        self.book.update_tooltip(tab_id, item.ai)

    def clear_last_ai(self, tab_id: str) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        tabconvo.convo.items[0].ai = ""

    def remove_last_ai(self, tab_id: str | None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        output.remove_last_ai()

    def count_tabs(self) -> None:
        from .session import session

        texts = []
        num_tabs = len(self.book.pages)
        num_convs = session.count()
        texts.append(f"Tabs: {num_tabs}")
        texts.append(f"Items: {num_convs}")
        Dialog.show_message("\n".join(texts))


display = Display()
