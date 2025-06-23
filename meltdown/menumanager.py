# Standard
import tkinter as tk
from typing import Any

# Modules
from .app import app
from .config import config
from .menus import Menu
from .upload import upload
from .modelcontrol import modelcontrol
from .system_prompt import system_prompt


class MenuManager:
    def __init__(self) -> None:
        self.main_menu: Any = None
        self.model_menu: Any = None
        self.openai_menu: Any = None
        self.google_menu: Any = None
        self.more_menu: Any = None
        self.tab_menu: Any = None
        self.font_menu: Any = None
        self.item_menu: Any = None
        self.word_menu: Any = None
        self.selection_menu: Any = None
        self.url_menu: Any = None
        self.link_menu: Any = None
        self.custom_menu: Any = None
        self.copy_menu: Any = None

    @staticmethod
    def get_main_button() -> tk.Widget:
        from .widgets import widgets

        return widgets.main_menu_button

    @staticmethod
    def get_model_button() -> tk.Widget:
        from .widgets import widgets

        return widgets.model_menu_button

    @staticmethod
    def get_more_button() -> tk.Widget:
        from .widgets import widgets

        return widgets.more_menu_button


class MainMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .session import session
        from .logs import logs
        from .commands import commands

        self.parent = parent
        self.menu = Menu()

        self.menu.add("System", lambda e: system_prompt.write())

        self.menu.separator()

        self.menu.add("Configs", lambda e: config.menu())
        self.menu.add("Sessions", lambda e: session.menu())
        self.menu.add("Logs", lambda e: logs.menu())

        self.menu.separator()

        self.menu.add("Commands", lambda e: commands.show_palette())
        self.menu.add("Profile", lambda e: app.open_profile())
        self.menu.add("Info", lambda e: app.show_info())

        self.menu.separator()

        self.menu.add("Theme", lambda e: app.pick_theme())
        self.menu.add("Font", lambda e: self.parent.font_menu.show(e))

        self.menu.separator()

        self.menu.add("Compact", lambda e: app.toggle_compact())
        self.menu.add("Resize", lambda e: app.resize())
        self.menu.add("About", lambda e: app.show_about())

        self.menu.separator()

        self.menu.add("Exit", lambda e: app.exit())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_main_button()
            self.menu.show(widget=widget)


class ModelMenu:
    def __init__(self, parent: MenuManager) -> None:
        self.parent = parent
        self.menu = Menu()

        self.menu.add(
            "Recent",
            lambda e: modelcontrol.show_recent(target=MenuManager.get_model_button()),
        )

        self.menu.add("Browse", lambda e: modelcontrol.browse())

        self.menu.separator()

        self.menu.add("OpenAI", lambda e: self.parent.openai_menu.show())
        self.menu.add("Google", lambda e: self.parent.google_menu.show())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_model_button()
            self.menu.show(widget=widget)


class OpenAIMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .model import model
        from .widgets import widgets

        self.parent = parent
        self.menu = Menu()

        self.menu.add("API Key", lambda e: model.set_openai_key())
        self.menu.separator()

        for gpt in model.gpts:
            self.menu.add(gpt[1], lambda e, gpt=gpt: widgets.use_gpt(gpt[0]))

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_model_button()
            self.menu.show(widget=widget)


class GoogleMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .model import model
        from .widgets import widgets

        self.parent = parent
        self.menu = Menu()

        self.menu.add("API Key", lambda e: model.set_google_key())
        self.menu.separator()

        for gemini in model.geminis:
            self.menu.add(
                gemini[1], lambda e, gemini=gemini: widgets.use_gemini(gemini[0])
            )

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_model_button()
            self.menu.show(widget=widget)


class MoreMenu:
    def __init__(self, parent: MenuManager) -> None:
        self.parent = parent
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from .findmanager import findmanager
        from .formats import formats

        self.menu.clear()
        num_tabs = display.num_tabs()
        messages = display.has_messages()
        nomsg = not messages
        single = num_tabs == 1

        self.menu.add("Find", lambda e: findmanager.toggle())
        self.menu.add("Find All", lambda e: findmanager.find_all(), disabled=single)

        self.menu.separator()

        self.menu.add("Use Text", lambda e: formats.do_use("text"), disabled=nomsg)
        self.menu.add("Use JSON", lambda e: formats.do_use("json"), disabled=nomsg)
        self.menu.add("Use MrkD", lambda e: formats.do_use("markdown"), disabled=nomsg)

        self.menu.separator()

        self.menu.add("Upload", lambda e: upload.service_picker(), disabled=nomsg)

    def show(self, event: Any = None) -> None:
        self.make()

        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_more_button()
            self.menu.show(widget=widget)


class TabMenu:
    def __init__(self, parent: MenuManager) -> None:
        self.parent = parent
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from .logs import logs
        from .summarize import summarize

        self.menu.clear()
        num_tabs = display.num_tabs()
        messages = display.has_messages(display.tab_menu_id)
        ignored = display.is_ignored(display.tab_menu_id)
        unmod = (not messages) or ignored
        single = num_tabs == 1
        num_pins = display.num_pins()

        self.menu.add("Tab List", lambda e: display.show_tab_list(e), disabled=single)

        if (num_tabs > 1) and (num_pins > 0):
            self.menu.add("Pin List", lambda e: display.show_tab_list(e, mode="pins"))

        self.menu.separator()

        self.menu.add(
            "First Tab", lambda e: display.select_first_tab(), disabled=single
        )

        self.menu.add("Last Tab", lambda e: display.select_last_tab(), disabled=single)

        self.menu.separator()

        self.menu.add(
            "Copy All",
            lambda e: display.copy_items_or_all(),
        )

        self.menu.add(
            "Save Log",
            lambda e: logs.save_menu(full=False, tab_id=display.tab_menu_id),
            disabled=unmod,
        )

        self.menu.add(
            "Summarize",
            lambda e: summarize.summarize(tab_id=display.tab_menu_id),
            disabled=unmod,
        )

        self.menu.separator()

        is_pin = display.is_pin(tab_id=display.tab_menu_id)
        pin_str = "Unpin" if is_pin else "Pin"

        self.menu.add(
            pin_str,
            lambda e: display.toggle_pin(tab_id=display.tab_menu_id),
        )

        self.menu.add(
            "Rename", lambda e: display.rename_tab(tab_id=display.tab_menu_id)
        )

        self.menu.add(
            "Move",
            lambda e: display.move_tab(tab_id=display.tab_menu_id),
            disabled=single,
        )

        self.menu.add(
            "Clear",
            lambda e: display.clear(tab_id=display.tab_menu_id),
            disabled=unmod,
        )

        self.menu.separator()

        self.menu.add("Close", lambda e: display.tab_menu_close(), disabled=single)

    def show(self, event: Any = None, mode: str = "normal") -> None:
        from .display import display

        if event:
            if mode == "normal":
                display.tab_menu_id = display.current_tab

            self.make()
            self.menu.show(event)
        else:
            page = display.book.current_page

            if not page:
                return

            widget = page.tab.frame

            if widget:
                if mode == "normal":
                    display.tab_menu_id = page.id_

                self.make()
                self.menu.show(widget=widget)


class FontMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .display import display
        from .dialogs import Dialog

        self.parent = parent

        def action(text: str) -> None:
            display.set_font_size(text)

        def set_font() -> None:
            Dialog.show_input(
                "Set Font Size", lambda a: action(a), value=str(config.font_size)
            )

        self.menu = Menu()

        self.menu.add("Set Font", lambda e: set_font())
        self.menu.add("Bigger Font", lambda e: display.increase_font())
        self.menu.add("Smaller Font", lambda e: display.decrease_font())
        self.menu.add("Font Family", lambda e: display.pick_font_family())
        self.menu.separator()
        self.menu.add("Reset Font", lambda e: display.reset_font())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_main_button()
            self.menu.show(widget=widget)


class ItemMenu:
    def __init__(self, parent: MenuManager) -> None:
        self.parent = parent
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from .output import Output

        self.menu.clear()
        num_items = display.get_num_items()
        self.menu.add(text="Copy", command=lambda e: self.parent.copy_menu.show(e))
        self.menu.add(text="Select", command=lambda e: Output.select_item())
        self.menu.add(text="Information", command=lambda e: Output.show_info())
        self.menu.add(text="Use", command=lambda e: Output.use_item())
        self.menu.separator()
        self.menu.add(text="Delete", command=lambda e: Output.delete_items())

        if num_items > 1:
            if Output.clicked_number > 1:
                self.menu.add(
                    text="Delete Above", command=lambda e: Output.delete_items("above")
                )

            if Output.clicked_number < num_items:
                self.menu.add(
                    text="Delete Below", command=lambda e: Output.delete_items("below")
                )

            self.menu.add(
                text="Delete Others", command=lambda e: Output.delete_items("others")
            )

        self.menu.separator()
        self.menu.add(text="Repeat Prompt", command=lambda e: Output.repeat_prompt())

        self.menu.add(
            text="Repeat (No History)", command=lambda e: Output.repeat_prompt(True)
        )

    def show(self, event: Any = None) -> None:
        self.make()

        if event:
            self.menu.show(event)
        else:
            return


class WordMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .args import args
        from .output import Output

        self.parent = parent
        self.menu = Menu()

        self.menu.add(text="Copy", command=lambda e: Output.copy_words())
        self.menu.add(text="Explain", command=lambda e: Output.explain_words())
        self.menu.add(text="Elaborate", command=lambda e: Output.elaborate_words())
        self.menu.add(text="Prompt", command=lambda e: Output.prompt_words())
        self.menu.add(text="Search", command=lambda e: Output.search_words())
        self.menu.add(text="New", command=lambda e: Output.new_tab())
        self.menu.add(text="Use", command=lambda e: Output.use_words())

        if args.custom_prompts:
            self.menu.separator()
            self.menu.add(text="Custom", command=lambda e: Output.custom_menu(e))

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class SelectionMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .output import Output

        self.parent = parent
        self.menu = Menu()

        self.menu.add(text="Copy", command=lambda e: Output.copy_selection())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class CustomMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .args import args
        from .utils import utils
        from .output import Output

        self.parent = parent
        self.menu = Menu()

        def add(item: str) -> None:
            word, prompt = utils.cmd_value(item, "=")

            if (not word) or (not prompt):
                return

            self.menu.add(text=word, command=lambda e: Output.custom_prompt(prompt))

        for item in args.custom_prompts:
            add(item)

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class UrlMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .output import Output

        self.parent = parent
        self.menu = Menu()

        self.menu.add(text="Open", command=lambda e: Output.open_url())
        self.menu.add(text="Copy", command=lambda e: Output.copy_url())
        self.menu.add(text="Use", command=lambda e: Output.use_url())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class LinkMenu:
    def __init__(self, parent: MenuManager) -> None:
        from .output import Output

        self.parent = parent
        self.menu = Menu()

        self.menu.add(text="Open", command=lambda e: Output.open_url())
        self.menu.add(text="Copy", command=lambda e: Output.copy_url())
        self.menu.add(text="Use", command=lambda e: Output.use_url())
        self.menu.separator()
        self.menu.add(text="Copy", command=lambda e: Output.copy_words())
        self.menu.add(text="Explain", command=lambda e: Output.explain_words())
        self.menu.add(text="Elaborate", command=lambda e: Output.elaborate_words())
        self.menu.add(text="Prompt", command=lambda e: Output.prompt_words())
        self.menu.add(text="Search", command=lambda e: Output.search_words())
        self.menu.add(text="New", command=lambda e: Output.new_tab())
        self.menu.add(text="Use", command=lambda e: Output.use_words())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class CopyMenu:
    def __init__(self, parent: MenuManager) -> None:
        self.parent = parent
        self.menu = Menu()

    def make(self) -> None:
        from .output import Output
        from .display import display

        self.menu.clear()
        messages = display.has_messages()
        ignored = display.is_ignored()
        unmod = (not messages) or ignored

        self.menu.add(
            text="Copy All", command=lambda e: Output.copy_item(), disabled=unmod
        )

        self.menu.add(
            text="Copy User", command=lambda e: Output.copy_item("user"), disabled=unmod
        )

        self.menu.add(
            text="Copy AI", command=lambda e: Output.copy_item("ai"), disabled=unmod
        )

    def show(self, event: Any = None) -> None:
        self.make()

        if event:
            self.menu.show(event)
        else:
            widget = MenuManager.get_more_button()
            self.menu.show(widget=widget)

    def last_item(self) -> None:
        from .output import Output

        Output.clicked_number = 0
        self.show()


menumanager = MenuManager()
menumanager.main_menu = MainMenu(menumanager)
menumanager.model_menu = ModelMenu(menumanager)
menumanager.openai_menu = OpenAIMenu(menumanager)
menumanager.google_menu = GoogleMenu(menumanager)
menumanager.more_menu = MoreMenu(menumanager)
menumanager.tab_menu = TabMenu(menumanager)
menumanager.font_menu = FontMenu(menumanager)
menumanager.item_menu = ItemMenu(menumanager)
menumanager.word_menu = WordMenu(menumanager)
menumanager.selection_menu = SelectionMenu(menumanager)
menumanager.url_menu = UrlMenu(menumanager)
menumanager.link_menu = LinkMenu(menumanager)
menumanager.custom_menu = CustomMenu(menumanager)
menumanager.copy_menu = CopyMenu(menumanager)
