# Modules
from .app import app
from .menus import Menu
from .dialogs import Dialog
from .output import Output
from .bottom import Bottom
from .book import Book, Page
from .find import Find
from .args import args
from . import timeutils
from . import widgetutils

# Standard
import random
import string
from typing import List, Dict, Any
from typing import Optional
import tkinter as tk


class Tab:
    def __init__(self, conversation_id: str, tab_id: str,
                 output: Output, find: Find, bottom: Bottom,
                 mode: str) -> None:
        self.conversation_id = conversation_id
        self.tab_id = tab_id
        self.output = output
        self.find = find
        self.bottom = bottom
        self.modified = False
        self.mode = mode
        self.loaded = False


class Display:
    def __init__(self) -> None:
        self.current_tab: str = "none"

    def make(self) -> None:
        from .widgets import widgets

        self.book = Book(widgets.display_frame)
        self.book.on_change = lambda: self.on_tab_change()

        self.tabs: Dict[str, Tab] = {}

        self.tab_menu = Menu()
        self.tab_menu.add(text="Rename", command=lambda: self.rename_tab())
        self.tab_menu.add(text="Move", command=lambda: self.move_tab())
        self.tab_menu.add(text="Close", command=lambda: self.tab_menu_close())
        self.tab_list_menu = Menu()

        self.output_menu = Menu()
        self.output_menu.add(text="Find", command=lambda: self.find())
        self.output_menu.add(text="Find All", command=lambda: self.find_all())
        self.output_menu.add(text="Copy All", command=lambda: self.copy_output())
        self.output_menu.add(text="Select All", command=lambda: self.select_output())
        self.output_menu.add(text="View Text", command=lambda: self.view_text())
        self.output_menu.add(text="View JSON", command=lambda: self.view_json())
        self.output_menu.add(text="Tab List", command=lambda: self.show_tab_list())
        self.output_menu.add(text="First Tab", command=lambda: self.select_first_tab())
        self.output_menu.add(text="Last Tab", command=lambda: self.select_last_tab())
        self.output_menu.add(text="Bigger Font", command=lambda: self.increase_font())
        self.output_menu.add(text="Smaller Font", command=lambda: self.decrease_font())
        self.output_menu.add(text="Reset Font", command=lambda: self.reset_font())

        self.tab_number = 1
        self.max_old_tabs = 5

        self.book.on_tab_right_click = lambda e, id: self.on_tab_right_click(e, id)
        self.book.on_tabs_click = lambda: self.on_tabs_click()
        self.book.on_tabs_double_click = lambda: self.on_tabs_double_click()
        self.book.on_tab_middle_click = lambda id: self.on_tab_middle_click(id)
        self.book.on_reorder = lambda: self.update_session()

    def make_tab(self, name: Optional[str] = None,
                 conversation_id: Optional[str] = None,
                 select_tab: bool = True, mode: str = "normal",
                 save: bool = True) -> str:
        from .session import session

        if not name:
            name = self.random_tab_name()

        if not conversation_id:
            conv_id = "ignore" if mode == "ignore" else ""
            conversation = session.add(name, conv_id=conv_id)
            conversation_id = conversation.id

        if not conversation_id:
            return ""

        page = self.book.add(name)
        tab_id = page.id
        find = Find(page.content, tab_id)
        output_frame = widgetutils.make_frame(page.content)
        output_frame.grid(row=1, column=0, sticky="nsew")
        output = Output(output_frame, tab_id)
        bottom = Bottom(page.content, tab_id)
        tab = Tab(conversation_id, tab_id, output, find, bottom, mode=mode)
        self.tabs[tab_id] = tab

        if select_tab:
            self.select_tab(tab_id)

        page.content.grid_rowconfigure(0, weight=0)
        page.content.grid_rowconfigure(1, weight=1)
        page.content.grid_rowconfigure(2, weight=0)

        self.tab_number += 1
        app.show_intro(tab_id)
        tab.modified = False

        if save:
            session.save()

        return tab_id

    def close_tab(self, tab_id: str = "",
                  force: bool = False,
                  make_empty: bool = True, method: str = "normal") -> None:
        if not tab_id:
            tab_id = self.book.current()

        if not tab_id:
            return

        tab = self.get_tab(tab_id)

        if not tab:
            return

        if method == "middle_click":
            if tab.mode == "ignore":
                force = True

            if self.tab_is_empty(tab_id):
                force = True

        def action() -> None:
            self.book.close(tab_id)
            self.update_current_tab()
            self.remove_tab(tab_id)

            if self.num_tabs() == 0:
                if make_empty:
                    self.make_tab()

        if force:
            action()
            return

        cmds = []
        num_tabs = self.num_tabs()

        if num_tabs > 1:
            if num_tabs > 5:
                cmds.append(("Old", lambda: self.close_old_tabs()))

            cmds.append(("Others", lambda: self.close_other_tabs()))
            cmds.append(("Left", lambda: self.close_tabs_left()))
            cmds.append(("Right", lambda: self.close_tabs_right()))
            cmds.append(("All", lambda: self.close_all_tabs()))

        cmds.append(("Ok", lambda: action()))
        Dialog.show_commands("Close tab?", cmds)

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
            return
        except BaseException:
            pass

        self.book.select_by_name(what)

    def update_current_tab(self) -> None:
        tab_id = self.book.current()
        self.current_tab = tab_id

    def on_tab_change(self) -> None:
        from .inputcontrol import inputcontrol
        from .session import session
        self.update_current_tab()
        tab = self.get_current_tab()

        if tab and not tab.loaded:
            conversation = session.get_conversation(tab.conversation_id)

            if conversation:
                conversation.print()
                tab.loaded = True

        inputcontrol.focus()
        self.check_scroll_buttons()

    def get_current_tab(self) -> Optional[Tab]:
        return self.get_tab(self.current_tab)

    def get_current_output(self) -> Optional[Output]:
        return self.get_output(self.current_tab)

    def get_current_bottom(self) -> Optional[Bottom]:
        return self.get_bottom(self.current_tab)

    def get_tab(self, tab_id: str) -> Optional[Tab]:
        return self.tabs.get(tab_id)

    def get_tab_by_conversation_id(self, conversation_id: str) -> Optional[Tab]:
        for tab in self.tabs.values():
            if tab.conversation_id == conversation_id:
                return tab

        return None

    def get_output(self, tab_id: str) -> Optional[Output]:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.output
        else:
            return None

    def get_bottom(self, tab_id: str) -> Optional[Bottom]:
        tab = self.get_tab(tab_id)

        if tab:
            return tab.bottom
        else:
            return None

    def on_tab_right_click(self, event: Any, tab_id: str) -> None:
        self.tab_menu_id = tab_id
        self.tab_menu.show(event)

    def on_tab_middle_click(self, tab_id: str) -> None:
        self.close_tab(tab_id=tab_id, method="middle_click")

    def on_tabs_click(self) -> None:
        app.hide_all()

    def on_tabs_double_click(self) -> None:
        self.make_tab()

    def show_tab_list(self) -> None:
        from .widgets import widgets
        widget = widgets.output_menu

        if not widget:
            return

        self.tab_list_menu.clear()

        def add_item(page: Page, num: int) -> None:
            def command() -> None:
                return self.select_tab(page.id)

            name = f"{num}. {page.name}"
            self.tab_list_menu.add(text=name, command=command)

        for i, page in enumerate(self.book.pages):
            add_item(page, i + 1)

        self.tab_list_menu.show(widget=widget)

    def rename_tab(self, current: bool = False) -> None:
        if current:
            tab_id = self.current_tab
        else:
            tab_id = self.tab_menu_id

        name = self.get_tab_name(tab_id)
        Dialog.show_input("Pick a name", lambda s: self.do_rename_tab(tab_id, s), value=name)

    def do_rename_tab(self, tab_id: str, name: str) -> None:
        from .session import session
        name = name.strip()

        if not name:
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
        self.close_tab(tab_id=self.tab_menu_id)

    def close_all_tabs(self, force: bool = False, make_empty: bool = True) -> None:
        def action() -> None:
            for tab_id in self.tab_ids():
                self.close_tab(tab_id=tab_id, force=True, make_empty=make_empty)

        if force:
            action()
            return

        Dialog.show_confirm("Close all tabs?", lambda: action())

    def close_old_tabs(self, force: bool = False) -> None:
        from .session import session
        ids = self.tab_ids()

        if len(ids) <= 1:
            return

        max_minutes = args.old_tabs_minutes
        max_date = timeutils.now() - (60 * max_minutes)

        def action() -> None:
            for tab_id in ids:
                tab = self.get_tab(tab_id)

                if not tab:
                    continue

                conversation = session.get_conversation(tab.conversation_id)

                if not conversation:
                    continue

                if conversation.last_modified < max_date:
                    self.close_tab(tab_id=tab_id, force=True, make_empty=True)

        if force:
            action()
            return

        Dialog.show_confirm("Close old tabs?", lambda: action())

    def close_other_tabs(self, force: bool = False) -> None:
        ids = self.tab_ids()

        if len(ids) <= 1:
            return

        current = self.current_tab

        def action() -> None:
            for tab_id in ids:
                if tab_id != current:
                    self.close_tab(tab_id=tab_id, force=True)

        if force:
            action()
            return

        Dialog.show_confirm("Close other tabs?", lambda: action())

    def close_tabs_left(self, force: bool = False) -> None:
        tab_ids = self.tab_ids()

        if len(tab_ids) <= 1:
            return

        index = self.index(self.current_tab)
        tabs = tab_ids[:index]

        def action() -> None:
            for tab_id in tabs:
                self.close_tab(tab_id=tab_id, force=True)

        if force:
            action()
            return

        Dialog.show_confirm("Close tabs to the left?", lambda: action())

    def close_tabs_right(self, force: bool = False) -> None:
        tab_ids = self.tab_ids()

        if len(tab_ids) <= 1:
            return

        index = self.index(self.current_tab)
        tabs = tab_ids[index + 1:]

        def action() -> None:
            for tab_id in tabs:
                self.close_tab(tab_id=tab_id, force=True)

        if force:
            action()
            return

        Dialog.show_confirm("Close tabs to the right?", lambda: action())

    def tab_ids(self) -> List[str]:
        return self.book.ids()

    def index(self, tab_id: str) -> int:
        return self.book.index(tab_id)

    def show_output_menu(self, event: Any) -> None:
        self.output_menu.show(event)

    def to_top(self, tab_id: str = "") -> None:
        if tab_id:
            tab = self.get_tab(tab_id)
        else:
            tab = self.get_current_tab()

        if not tab:
            return

        tab.output.to_top()

    def to_bottom(self, tab_id: str = "") -> None:
        if tab_id:
            tab = self.get_tab(tab_id)
        else:
            tab = self.get_current_tab()

        if not tab:
            return

        tab.output.to_bottom()
        tab.bottom.hide()

    def copy_output(self) -> None:
        output = self.get_current_output()

        if not output:
            return

        output.copy_all()

    def clear(self, tab_id: str = "", force: bool = False) -> None:
        from .session import session

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        if not tab.modified:
            return

        def action() -> None:
            if (not tab) or (not tab.output):
                return

            tab.output.clear_text()
            session.clear(tab.conversation_id)
            app.show_intro(tab_id)
            tab.modified = False

        if force:
            action()
            return

        Dialog.show_confirm("Clear conversation?", lambda: action())

    def select_output(self) -> None:
        output = self.get_current_output()

        if output:
            output.select_all()

    def print(self, text: str, tab_id: str = "") -> None:
        if not app.exists():
            return

        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.print(text)
        tab.modified = True

    def insert(self, text: str, tab_id: str = "") -> None:
        if not app.exists():
            return

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.insert_text(text)
        tab.modified = True

    def get_tab_name(self, tab_id: str) -> str:
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

        if yview[1] >= 0.9999:
            tab.bottom.hide()
        else:
            tab.bottom.show()

        if yview[0] <= 0.0001:
            widgets.disable_top_button()
        else:
            widgets.enable_top_button()

    def tab_left(self) -> None:
        self.book.select_left()

    def tab_right(self) -> None:
        self.book.select_right()

    def close_current_tab(self) -> None:
        self.close_tab(tab_id=self.current_tab)

    def decrease_font(self) -> None:
        from .config import config
        new_size = config.output_font_size - 1

        if new_size < 6:
            return

        config.set("output_font_size", new_size)

    def increase_font(self) -> None:
        from .config import config
        new_size = config.output_font_size + 1

        if new_size > 48:
            return

        config.set("output_font_size", new_size)

    def reset_font(self) -> None:
        from .config import config
        config.reset_one("output_font_size")

    def update_font(self) -> None:
        for tab in self.tabs.values():
            tab.output.update_font()

    def scroll_up(self, tab_id: str = "") -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if output:
            output.scroll_up()

    def scroll_down(self, tab_id: str = "") -> None:
        if not tab_id:
            tab_id = self.current_tab

        output = self.get_output(tab_id)

        if output:
            output.scroll_down()

    def update_session(self) -> None:
        from .session import session
        session.update()

    def hide_bottom(self, tab_id: str = "") -> None:
        if tab_id:
            tab_id = self.current_tab

        bottom = self.get_bottom(tab_id)

        if not bottom:
            return

        bottom.hide()

    def prompt(self, who: str, text: str = "", tab_id: str = "", to_bottom: bool = True) -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        if who == "user":
            if to_bottom:
                self.to_bottom(tab_id)

        tab.output.prompt(who)

        if text:
            tab.output.insert_text(text)

        tab.modified = True

    def format_text(self, tab_id: str = "") -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.output.format_text()
        tab.modified = True

    def select_first_tab(self) -> None:
        self.book.select_first()

    def select_last_tab(self) -> None:
        self.book.select_last()

    def find(self, tab_id: str = "", widget: Optional[tk.Text] = None, query: str = "") -> None:
        if not tab_id:
            tab_id = self.current_tab

        tab = self.get_tab(tab_id)

        if not tab:
            return

        tab.find.show(widget=widget, query=query)

        if query:
            tab.find.find_next()

    def find_next(self, case_insensitive: bool = True) -> None:
        tab = self.get_current_tab()

        if not tab:
            return

        if not tab.find.visible:
            tab.find.show()
            return

        tab.find.find_next(case_insensitive)

    def hide_find(self) -> None:
        tab = self.get_current_tab()

        if not tab:
            return

        tab.find.hide()

    def view_text(self) -> None:
        from .session import session
        from .logs import logs
        tab = self.get_current_tab()

        if not tab:
            return

        if tab.mode == "ignore":
            return

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return

        text = logs.get_text(conversation)
        name = self.get_tab_name(tab.tab_id)

        if text:
            new_tab = self.make_tab(name=f"{name} Text", mode="ignore")
            self.print(text, tab_id=new_tab)
            self.to_top(tab_id=new_tab)

    def view_json(self) -> None:
        from .session import session
        from .logs import logs
        tab = self.get_current_tab()

        if not tab:
            return

        if tab.mode == "ignore":
            return

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return

        text = logs.get_json(conversation)
        name = self.get_tab_name(tab.tab_id)

        if text:
            new_tab = self.make_tab(name=f"{name} JSON", mode="ignore")
            self.print(text, tab_id=new_tab)
            self.to_top(tab_id=new_tab)

    def move_tab(self, current: bool = False) -> None:
        if len(self.tab_ids()) <= 1:
            return

        if current:
            tab_id = self.current_tab
        else:
            tab_id = self.tab_menu_id

        cmds = []
        cmds.append(("To Start", lambda: self.move_tab_to_start(tab_id)))
        cmds.append(("To End", lambda: self.move_tab_to_end(tab_id)))
        Dialog.show_commands("Move tab?", cmds)

    def move_tab_to_start(self, tab_id: str) -> None:
        self.book.move_to_start(tab_id)
        self.update_session()

    def move_tab_to_end(self, tab_id: str) -> None:
        self.book.move_to_end(tab_id)
        self.update_session()

    def find_all(self, query: str = "") -> None:
        if query:
            self.find_all_text(query)
        else:
            Dialog.show_input("Find text in all tabs", lambda s: self.find_all_text(s))

    def find_all_text(self, query: str) -> None:
        from .session import session

        if not query:
            return

        for tab in self.tabs.values():
            conversation = session.get_conversation(tab.conversation_id)

            if not conversation:
                continue

            if conversation.id == "ignore":
                continue

            tab.output.auto_scroll = False

            if not tab.loaded:
                conversation.print()
                tab.loaded = True
                app.update()

            start_index = tab.output.find_text(query)

            if start_index:
                self.select_tab(tab.tab_id)
                tab.find.show(query=query)
                break

    def tab_is_empty(self, tab_id: str) -> bool:
        from .session import session
        tab = self.get_tab(tab_id)

        if not tab:
            return True

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return False

        if conversation.items:
            return False

        return True

    def stream_started(self, tab_id: str) -> None:
        if not args.tab_highlight:
            return

        self.book.highlight(tab_id)

    def stream_stopped(self) -> None:
        if not args.tab_highlight:
            return

        self.book.remove_highlights()


display = Display()
