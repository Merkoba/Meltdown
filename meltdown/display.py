from __future__ import annotations

# Standard
import tkinter as tk
import sys
from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

# Modules
from .app import app
from .config import config
from .menus import Menu
from .dialogs import Dialog, Commands
from .output import Output
from .bottom import Bottom
from .book import Book, Page
from .find import Find
from .args import args
from .utils import utils
from .autoscroll import autoscroll
from .itemops import itemops

if TYPE_CHECKING:
    from .session import Conversation


class Tab:
    def __init__(
        self,
        page: Page,
        conversation_id: str,
        tab_id: str,
        mode: str,
        no_intro: bool,
        output: Output | None = None,
        find: Find | None = None,
        bottom: Bottom | None = None,
        created: bool = False,
    ) -> None:
        self.page = page
        self.conversation_id = conversation_id
        self.tab_id = tab_id
        self.modified = False
        self.mode = mode
        self.loaded = False
        self.streaming = False
        self.num_user_prompts = 0
        self.no_intro = no_intro
        self.output = output
        self.find = find
        self.bottom = bottom
        self.created = created

    def create(self) -> None:
        if self.created:
            return

        pcontent = self.page.content
        find = Find(pcontent, self.tab_id)
        output_frame = tk.Frame(pcontent)
        output_frame.grid(row=1, column=0, sticky="nsew")
        output = Output(output_frame, self.tab_id)
        bottom = Bottom(pcontent, self.tab_id)

        self.output = output
        self.find = find
        self.bottom = bottom
        self.created = True

    def get_output(self) -> Output:
        self.create()
        return self.output  # type: ignore

    def get_find(self) -> Find:
        self.create()
        return self.find  # type: ignore

    def get_bottom(self) -> Bottom:
        self.create()
        return self.bottom  # type: ignore

    def is_pin(self) -> bool:
        return self.page.pin


@dataclass
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

        self.book.on_button_right_click = lambda e: self.on_tab_button_right_click(e)
        self.book.on_tab_right_click = lambda e, id: self.on_tab_right_click(e, id)
        self.book.on_tabs_click = lambda: self.on_tabs_click()
        self.book.on_tabs_double_click = lambda: self.on_tabs_double_click()
        self.book.on_tab_middle_click = lambda id: self.on_tab_middle_click(id)
        self.book.on_reorder = lambda: self.update_session()
        self.book.on_num_tabs_change = lambda n: self.on_num_tabs_change(n)

    def new_tab(
        self,
        name: str | None = None,
        position: str | None = None,
        close_tabs: bool = True,
        force_close: bool = False,
    ) -> bool:
        from .close import close
        from .keyboard import keyboard

        if not position:
            position = "end"

        if args.max_tabs > 0:
            if self.num_tabs() >= args.max_tabs:
                if not close_tabs:
                    return False

                if force_close:
                    close.close_oldest(force=True)
                    return True

                cmds = Commands()
                cmds.add("Close Some Tabs", lambda a: close.close(force=False))
                cmds.add("Do Nothing", lambda a: None)
                Dialog.show_dialog(f"Max tabs reached ({args.max_tabs})", cmds)
                return False

        def check_empty(page: Page | None) -> bool:
            if not page:
                return False

            if self.tab_is_empty(page.id_):
                if self.is_ignored(page.id_):
                    return False

                self.select_tab(page.id_)
                return True

            return False

        if (
            args.keep_empty_tab
            and (not name)
            and (not keyboard.ctrl)
            and (not keyboard.shift)
        ):
            if position == "end":
                if check_empty(self.book.get_last()):
                    return True
            elif position == "start":
                if check_empty(self.book.get_first()):
                    return True

        self.make_tab(name=name, position=position)
        return True

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
            now = int(utils.now())
            n = len(self.tabs)
            conv_id = f"ignore_{now}_{n}" if mode == "ignore" else ""
            conversation = session.add(name, conv_id=conv_id, position=position)
            conversation_id = conversation.id

        if not conversation_id:
            return ""

        convo = session.get_conversation(conversation_id)
        tooltip = ""

        if convo and convo.items:
            tooltip = convo.items[0].ai

        if convo:
            pin = convo.pin
        else:
            pin = False

        page = self.book.add(
            name,
            mode=mode,
            tooltip=tooltip,
            position=position,
            pin=pin,
        )

        tab_id = page.id_

        tab = Tab(
            page=page,
            conversation_id=conversation_id,
            tab_id=tab_id,
            mode=mode,
            no_intro=no_intro,
        )

        self.tabs[tab_id] = tab

        if select_tab:
            self.select_tab(tab_id)

        page.content.grid_rowconfigure(0, weight=0)
        page.content.grid_rowconfigure(1, weight=1)
        page.content.grid_rowconfigure(2, weight=0)

        self.tab_number += 1

        if save and (mode != "ignore"):
            session.save()

        return tab_id

    def select_tab(self, tab_id: str) -> None:
        if self.book.select(tab_id):
            app.update()

    def select_tab_by_number(self, num: int) -> None:
        if num < 1 or (num > len(self.book.pages)):
            return

        if num == 9:
            self.book.select_last()
        else:
            self.book.select_by_index(num - 1)

    def select_middle_tab(self) -> Any:
        num = len(self.book.pages)
        middle = min(num, max(0, num // 2))
        return self.select_tab_by_number(middle)

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
        tab.get_output().reset_drag()
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
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not args.show_header:
            return

        nice_date = utils.to_date(tabconvo.convo.created)
        self.print(nice_date, tab_id=tab_id, modified=False)

    def get_current_tab(self) -> Tab | None:
        if hasattr(self, "current_tab_object"):
            return self.current_tab_object

        return None

    def get_current_output(self) -> Output | None:
        return self.get_output(self.current_tab)

    def get_current_find(self) -> Find | None:
        return self.get_find(self.current_tab)

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
            return tab.get_output()

        return None

    def get_find(self, tab_id: str) -> Find | None:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.get_find()

        return None

    def get_bottom(self, tab_id: str) -> Bottom | None:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.get_bottom()

        return None

    def on_tab_button_right_click(self, event: Any) -> None:
        from .menumanager import menumanager

        menumanager.tab_menu.show(event)

    def on_tab_right_click(self, event: Any, tab_id: str) -> None:
        from .menumanager import menumanager

        self.tab_menu_id = tab_id
        self.tab_menu_event = event
        menumanager.tab_menu.show(event, "tab_right_click")

    def on_tab_middle_click(self, tab_id: str) -> None:
        from .close import close
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

    def show_tab_list(self, event: Any = None, mode: str = "normal") -> None:
        from .widgets import widgets
        from .close import close

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

        items = self.book.pages if args.reverse_tablist else reversed(self.book.pages)

        for i, page in enumerate(items):
            if mode == "pins":
                if not page.pin:
                    continue

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
        name = self.prepare_name(name)

        if not name:
            self.redo_auto_name_tab(tab_id)
            return

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        o_name = self.get_tab_name(tab_id)

        if name == o_name:
            return

        self.book.set_name(tab_id, name)
        tabconvo.convo.set_name(name)

    def tab_menu_close(self) -> None:
        from .close import close

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
        tab.get_output().to_top()

    def to_bottom(self, tab_id: str | None = None) -> None:
        if tab_id:
            tab = self.get_tab(tab_id)
        else:
            tab = self.get_current_tab()

        if not tab:
            return

        autoscroll.stop()
        tab.get_output().to_bottom()
        tab.get_bottom().hide()

    def copy_output(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

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

        if tabconvo.convo.id.startswith("ignore"):
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
        tab.get_output().reset()
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
        self,
        text: str,
        tab_id: str | None = None,
        modified: bool = True,
        do_format: bool = False,
    ) -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.get_output().print(text)

        if modified:
            tab.modified = True

        if do_format:
            self.format_text(tab_id, mode="last")

    def insert(self, text: str, tab_id: str | None = None) -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        text = utils.clean_lines(text)
        tab.get_output().insert_text(text)
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

        if tab.mode != "ignore":
            session.remove(tab.conversation_id)

        del self.tabs[tab_id]

    def check_scroll_buttons(self, tab_id: str | None = None) -> None:
        from .widgets import widgets

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        yview = tab.get_output().yview()

        if yview[1] >= 0.9999:
            if autoscroll.direction == "down":
                autoscroll.stop()

            tab.get_bottom().hide()
        else:
            if yview[0] <= 0.0001:
                if autoscroll.direction == "up":
                    autoscroll.stop()

            tab.get_bottom().show()

            if args.scroll_percentage:
                visible_range = yview[1] - yview[0]
                total_range = 1.0 - visible_range
                perc = int((yview[0] / total_range) * 100)
                tab.get_bottom().set_text(f"{perc}%")
            elif args.scroll_percentage_reverse:
                visible_range = yview[1] - yview[0]
                total_range = 1.0 - visible_range
                perc = int((1.0 - yview[1]) / total_range * 100)
                tab.get_bottom().set_text(f"{perc}%")

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
        from .menumanager import menumanager

        if not text:
            menumanager.font_menu.show()
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

        cmds = Commands()
        cmds.add("Mono", lambda a: action("monospace"))
        cmds.add("Serif", lambda a: action("serif"))
        cmds.add("Sans", lambda a: action("sans-serif"))

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
            if not tab.created:
                continue

            tab.get_output().update_font()

            if key == "font_family":
                if tab.modified:
                    self.refresh(tab.tab_id)

    def scroll_up(
        self,
        tab_id: str | None = None,
        more: bool = False,
        disable_autoscroll: bool = False,
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        if disable_autoscroll:
            autoscroll.stop(check=True)

        output.scroll_up(more=more)

    def scroll_down(
        self,
        tab_id: str | None = None,
        more: bool = False,
        disable_autoscroll: bool = False,
    ) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        if disable_autoscroll:
            autoscroll.stop(check=True)

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
                tab.get_output().separate()

        tab.get_output().prompt(who)

        if text:
            if who == "user":
                if args.crop_user > 0:
                    text = text[: args.crop_user].strip()

            text = utils.clean_lines(text)
            tab.get_output().insert_text(text)

        if file:
            file_text = f"File:\u00a0{file}"
            tab.get_output().print(file_text)

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

        tab.get_output().format_text(mode=mode, force=force)

    def select_first_tab(self) -> None:
        self.book.select_first()

    def select_last_tab(self) -> None:
        self.book.select_last()

    def move_tab(self, tab_id: str | None = None) -> None:
        if len(self.tab_ids()) <= 1:
            return

        if not tab_id:
            tab_id = self.current_tab

        cmds = Commands()
        cmds.add("To Start", lambda a: self.move_tab_to_start(tab_id))
        cmds.add("To End", lambda a: self.move_tab_to_end(tab_id))

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

        app.border_effect_on()
        self.book.highlight(tab_id)
        self.set_tab_streaming(tab_id)
        self.tab_streaming = tab_id

    def stream_ended(self) -> None:
        if not args.tab_highlight:
            return

        app.border_effect_off()
        self.book.remove_highlights()
        self.clear_tab_streaming()
        self.format_text(self.tab_streaming)
        self.update_tooltip(self.tab_streaming)

        if args.auto_program:
            itemops.run_program(auto=True)

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

        yview = tab.get_output().yview()

        if yview[1] >= 0.9999:
            tab.get_output().to_top()
        else:
            tab.get_output().to_bottom()

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

        return bool(tab.get_output().get_selected_text())

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

        return tabconvo.convo.id.startswith("ignore")

    def enable_auto_bottom(self, tab_id: str) -> None:
        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.get_output().auto_bottom = True

    def disable_auto_bottom(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.get_output().auto_bottom = False

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

    def replay(self, tab_id: str | None = None) -> None:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        self.reset_tab(tabconvo.tab)
        tabconvo.convo.print(True)

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

        output = tabconvo.tab.get_output()
        text = output.get_text()

        if num_lines:
            text = text.split("\n", num_lines)[-1]

        return text.strip()

    def get_selected_text(self, tab_id: str | None = None) -> str:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return ""

        output = tabconvo.tab.get_output()
        text = output.get_selected()
        return text.strip()

    def get_all_text(self, tab_id: str | None = None) -> str:
        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return ""

        output = tabconvo.tab.get_output()
        return output.get_text().strip()

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

        tab.get_output().update_scroll()

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

    def show_size(self, tab_id: str | None = None) -> None:
        from .dialogs import Dialog

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        lines = tab.get_output().get_num_lines()
        chars = tab.get_output().get_num_chars()
        kbytes = utils.chars_to_kb(chars)

        Dialog.show_message(f"Lines: {lines}\nChars: {chars}\nKBytes: {kbytes}")

    def set_pin(self, value: bool, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        tabconvo.convo.set_pin(value)
        self.book.set_pin(tab_id, value)

        if args.auto_sort_pins:
            self.sort_pins(mode="start")

    def toggle_pin(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        pin = not tabconvo.convo.pin
        self.set_pin(pin, tab_id)

    def pin(self, tab_id: str | None = None) -> None:
        self.set_pin(True, tab_id)

    def unpin(self, tab_id: str | None = None) -> None:
        self.set_pin(False, tab_id)

    def get_tabs(self) -> list[Tab]:
        return list(self.tabs.values())

    def is_pin(self, tab_id: str | None = None) -> bool:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return False

        return tab.is_pin()

    def get_pins(self) -> list[Tab]:
        tabs = self.get_tabs()
        return [tab for tab in tabs if tab.is_pin()]

    def get_normal(self) -> list[Tab]:
        tabs = self.get_tabs()
        return [tab for tab in tabs if not tab.is_pin()]

    def num_pins(self) -> int:
        return len(self.get_pins())

    def sort_pins(self, mode: str = "start") -> None:
        self.book.sort_pins(mode)
        self.update_session()

    def say(self, text: str, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tabconvo = self.get_tab_convo(tab_id)

        if not tabconvo:
            return

        user_text = args.say_user_message
        ai_text = text[: config.say_limit].strip()

        log_dict: dict[str, Any] = {}
        log_dict["user"] = user_text
        log_dict["ai"] = ai_text
        log_dict["date"] = utils.now()
        log_dict["model"] = "Say"
        tabconvo.convo.add(log_dict)

        self.prompt("user", user_text, tab_id=tab_id)
        self.prompt("ai", ai_text, tab_id=tab_id)
        self.format_text(tab_id)

    def get_prompt(
        self,
        who: str,
        show_avatar: bool = True,
        colon_space: bool = True,
        put_colons: bool = True,
        markers: bool = True,
        generic: bool = False,
        name_user: str = "",
        name_ai: str = "",
    ) -> str:
        name = ""

        if generic:
            if who == "user":
                name = "User"
            elif who == "ai":
                name = "AI"
        else:
            if who == "user":
                if name_user:
                    name = name_user
            elif who == "ai":
                if name_ai:
                    name = name_ai

            if not name:
                name = getattr(config, f"name_{who}")

        avatar = getattr(config, f"avatar_{who}")
        marker = Output.marker_space
        d = utils.delimiter()
        colons = f"{marker}{d}{marker}"
        prompt = ""
        display_space = "\u00a0" if sys.platform == "darwin" else marker

        if args.avatars and show_avatar and avatar:
            prompt = f"{avatar}{display_space}{name}{colons}"
        elif name:
            prompt = f"{name}{colons}"

        prepend = ""

        if args.item_numbers:
            number = self.num_user_prompts()
            prepend = f"({number + 1})"

        if prepend:
            text = f"{prepend} {prompt}"
        else:
            text = prompt

        # Add invisible markers
        umarker = Output.get_marker(who)
        return f"{umarker}{text}"

    def filter_text(self, tab_id: str | None = None, text: str = "") -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        output.filter_text(text)

    def count_snippets(self, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        num = output.count_snippets()
        msg = f"Snippets: {num}"
        Dialog.show_message(msg)

    def react_like(self, tab_id: str | None = None) -> None:
        from .model import model

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        model.prompt(args.like_prompt, tab_id=tab_id)

    def react_dislike(self, tab_id: str | None = None) -> None:
        from .model import model

        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if not output:
            return

        model.prompt(args.dislike_prompt, tab_id=tab_id)


display = Display()
