# Standard
import tkinter as tk
from typing import Any

# Modules
from .args import args
from .menus import Menu


def get_widget() -> tk.Widget:
    from .widgets import widgets

    if args.more_button:
        widget = getattr(widgets, "more_menu_button")
    else:
        widget = getattr(widgets, "stop_button")

    assert isinstance(widget, tk.Widget)
    return widget


class MainMenu:
    def __init__(self) -> None:
        from .app import app
        from .config import config
        from .session import session
        from .logs import logs
        from .commands import commands
        from .widgets import widgets

        self.menu = Menu()

        self.menu.add("System", lambda e: widgets.write_system_prompt())

        self.menu.separator()

        self.menu.add("Configs", lambda e: config.menu())
        self.menu.add("Sessions", lambda e: session.menu())
        self.menu.add("Logs", lambda e: logs.menu())

        self.menu.separator()

        self.menu.add("Commands", lambda e: commands.show_palette())

        self.menu.separator()

        self.menu.add("Compact", lambda e: app.toggle_compact())
        self.menu.add("Resize", lambda e: app.resize())
        self.menu.add("About", lambda e: app.show_about())

        self.menu.separator()

        self.menu.add("Exit", lambda e: app.exit())

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "main_menu_button")
            self.menu.show(widget=widget)


class ModelMenu:
    def __init__(self) -> None:
        from .model import model
        from .widgets import widgets

        self.menu = Menu()

        self.menu.add("Recent Models", lambda e: widgets.show_recent_models())
        self.menu.add("Browse Models", lambda e: widgets.browse_models())
        self.menu.add("Use GPT Model", lambda e: gpt_menu.show())
        self.menu.add("Set API Key", lambda e: model.set_api_key())

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "model_menu_button")
            self.menu.show(widget=widget)


class GPTMenu:
    def __init__(self) -> None:
        from .model import model
        from .widgets import widgets

        self.menu = Menu()

        for gpt in model.gpts:
            self.menu.add(gpt[1], lambda e, gpt=gpt: widgets.use_gpt(gpt[0]))

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "model_menu_button")
            self.menu.show(widget=widget)


class MoreMenu:
    def __init__(self) -> None:
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from . import findmanager

        self.menu.clear()
        num_tabs = display.num_tabs()
        modified = display.is_modified()
        ignored = display.is_ignored()
        single = num_tabs == 1

        self.menu.add("Find", lambda e: findmanager.find())
        self.menu.add("Find All", lambda e: findmanager.find_all(), disabled=single)

        self.menu.separator()

        self.menu.add("Copy All", lambda e: display.copy_output())
        self.menu.add("Select All", lambda e: display.select_output())

        self.menu.separator()

        disable = (not modified) or ignored
        self.menu.add("View Text", lambda e: display.view_text(), disabled=disable)
        self.menu.add("View JSON", lambda e: display.view_json(), disabled=disable)

        self.menu.separator()
        self.menu.add("Font", lambda e: font_menu.show())

    def show(self, event: Any = None) -> None:
        self.make()

        if event:
            self.menu.show(event)
        else:
            widget = get_widget()
            self.menu.show(widget=widget)


class TabMenu:
    def __init__(self) -> None:
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from .logs import logs
        from . import summarize

        self.menu.clear()
        num_tabs = display.num_tabs()
        modified = display.is_modified()
        not_modified = not modified
        single = num_tabs == 1

        self.menu.add("Tab List", lambda e: display.show_tab_list(e), disabled=single)
        self.menu.separator()
        disable = not modified

        self.menu.add(
            "Save Log",
            lambda e: logs.menu(full=False, tab_id=display.tab_menu_id),
            disabled=disable,
        )

        self.menu.add(
            "Summarize",
            lambda e: summarize.summarize(tab_id=display.tab_menu_id),
            disabled=disable,
        )

        self.menu.separator()

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
            disabled=not_modified,
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
                    display.tab_menu_id = page.id

                self.make()
                self.menu.show(widget=widget)


class FontMenu:
    def __init__(self) -> None:
        from .config import config
        from .display import display
        from .dialogs import Dialog

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
        self.menu.add("Font Family", lambda e: font_family_menu.show())
        self.menu.separator()
        self.menu.add("Reset Font", lambda e: display.reset_font())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = get_widget()
            self.menu.show(widget=widget)


class FontFamilyMenu:
    def __init__(self) -> None:
        from .display import display

        self.menu = Menu()

        self.menu.add("Serif", lambda e: display.set_font_family("serif"))
        self.menu.add("Sans-Serif", lambda e: display.set_font_family("sans-serif"))
        self.menu.add("Monospace", lambda e: display.set_font_family("monospace"))

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            widget = get_widget()
            self.menu.show(widget=widget)


class ItemMenu:
    def __init__(self) -> None:
        self.menu = Menu()

    def make(self) -> None:
        from .display import display
        from .output import Output

        self.menu.clear()
        num_items = display.get_num_items()

        self.menu.add(text="Copy", command=lambda e: Output.copy_item())
        self.menu.add(text="Select", command=lambda e: Output.select_item())
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
    def __init__(self) -> None:
        from .args import args
        from .output import Output

        self.menu = Menu()

        self.menu.add(text="Copy", command=lambda e: Output.copy_words())
        self.menu.add(text="Explain", command=lambda e: Output.explain_words())
        self.menu.add(text="Search", command=lambda e: Output.search_words())
        self.menu.add(text="New", command=lambda e: Output.new_tab())

        if args.custom_prompts:
            self.menu.separator()
            self.menu.add(text="Custom", command=lambda e: Output.custom_menu(e))

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class CustomMenu:
    def __init__(self) -> None:
        from .args import args
        from .output import Output

        self.menu = Menu()

        for item in args.custom_prompts:
            split = item.split("=")
            word = split[0].strip()
            prompt = "=".join(split[1:]).strip()

            self.menu.add(text=word, command=lambda e: Output.custom_prompt(prompt))

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class UrlMenu:
    def __init__(self) -> None:
        from .output import Output

        self.menu = Menu()

        self.menu.add(text="Use", command=lambda e: Output.use_path())
        self.menu.add(text="Copy", command=lambda e: Output.copy_words())
        self.menu.add(text="Open", command=lambda e: Output.open_url())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


class PathMenu:
    def __init__(self) -> None:
        from .output import Output

        self.menu = Menu()

        self.menu.add(text="Use", command=lambda e: Output.use_path())
        self.menu.add(text="Copy", command=lambda e: Output.copy_words())
        self.menu.add(text="Open", command=lambda e: Output.open_path())

    def show(self, event: Any = None) -> None:
        if event:
            self.menu.show(event)
        else:
            return


main_menu = MainMenu()
model_menu = ModelMenu()
gpt_menu = GPTMenu()
more_menu = MoreMenu()
tab_menu = TabMenu()
font_menu = FontMenu()
font_family_menu = FontFamilyMenu()
item_menu = ItemMenu()
word_menu = WordMenu()
url_menu = UrlMenu()
path_menu = PathMenu()
custom_menu = CustomMenu()
