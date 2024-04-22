# Standard
from typing import Any

# Modules
from .menus import Menu


class MainMenu:
    def __init__(self) -> None:
        from .app import app
        from .config import config
        from .session import session
        from .logs import logs
        from .commands import commands
        from .widgets import widgets

        self.menu = Menu()
        self.menu.add(
            text="System Prompt", command=lambda e: widgets.write_system_prompt()
        )
        self.menu.separator()
        self.menu.add(text="Configs", command=lambda e: config.menu())
        self.menu.add(text="Sessions", command=lambda e: session.menu())
        self.menu.add(text="Logs", command=lambda e: logs.menu())
        self.menu.separator()
        self.menu.add(text="Commands", command=lambda e: commands.show_palette())
        self.menu.separator()
        self.menu.add(text="Compact", command=lambda e: app.toggle_compact())
        self.menu.add(text="Resize", command=lambda e: app.resize())
        self.menu.add(text="Theme", command=lambda e: app.toggle_theme())
        self.menu.add(text="About", command=lambda e: app.show_about())
        self.menu.separator()
        self.menu.add(text="Exit", command=lambda e: app.exit())

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
        self.menu.add(
            text="Recent Models", command=lambda e: widgets.show_recent_models()
        )
        self.menu.add(text="Browse Models", command=lambda e: widgets.browse_models())
        self.menu.add(text="Use GPT Model", command=lambda e: gpt_menu.show())
        self.menu.add(text="Set API Key", command=lambda e: model.set_api_key())

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
            self.menu.add(
                text=gpt[1], command=lambda e, gpt=gpt: widgets.use_gpt(gpt[0])
            )

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "model_menu_button")
            self.menu.show(widget=widget)


class MoreMenu:
    def __init__(self) -> None:
        from .display import display

        self.menu = Menu()
        self.menu.add(text="Find", command=lambda e: display.find())
        self.menu.add(text="Find All", command=lambda e: display.find_all())
        self.menu.separator()
        self.menu.add(text="Copy All", command=lambda e: display.copy_output())
        self.menu.add(text="Select All", command=lambda e: display.select_output())
        self.menu.separator()
        self.menu.add(text="View Text", command=lambda e: display.view_text())
        self.menu.add(text="View JSON", command=lambda e: display.view_json())
        self.menu.separator()
        self.menu.add(text="Font", command=lambda e: font_menu.show())

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "more_menu_button")
            self.menu.show(widget=widget)


class TabMenu:
    def __init__(self) -> None:
        from .display import display

        self.menu_single = Menu()
        self.menu_single.add(text="Rename", command=lambda e: display.rename_tab())
        self.menu_single.add(text="Move", command=lambda e: display.move_tab())
        self.menu_single.add(text="Clear", command=lambda e: display.clear())
        self.menu_single.add(text="Close", command=lambda e: display.tab_menu_close())

        self.menu_multi = Menu()
        self.menu_multi.add(text="Tab List", command=lambda e: display.show_tab_list(e))
        self.menu_multi.separator()
        self.menu_multi.add(text="Tab Left", command=lambda e: display.tab_left())
        self.menu_multi.add(text="Tab Right", command=lambda e: display.tab_right())
        self.menu_multi.separator()
        self.menu_multi.add(
            text="First Tab", command=lambda e: display.select_first_tab()
        )
        self.menu_multi.add(
            text="Last Tab", command=lambda e: display.select_last_tab()
        )
        self.menu_multi.separator()
        self.menu_multi.add(
            text="Active Tab", command=lambda e: display.select_active_tab()
        )
        self.menu_multi.separator()
        self.menu_multi.add(text="Rename", command=lambda e: display.rename_tab())
        self.menu_multi.add(text="Move", command=lambda e: display.move_tab())
        self.menu_multi.add(text="Clear", command=lambda e: display.clear())
        self.menu_multi.add(text="Close", command=lambda e: display.tab_menu_close())

    def show(self, event: Any = None, mode: str = "normal") -> None:
        from .display import display

        if display.num_tabs() > 1:
            menu = self.menu_multi
        else:
            menu = self.menu_single

        if event:
            display.tab_menu_id = display.current_tab
            menu.show(event)
        else:
            page = display.book.current_page

            if not page:
                return

            widget = page.tab.frame

            if widget:
                display.tab_menu_id = page.id
                menu.show(widget=widget)


class FontMenu:
    def __init__(self) -> None:
        from .display import display
        from .dialogs import Dialog

        def action(text: str) -> None:
            display.set_font_size(text)

        def set_font() -> None:
            Dialog.show_input("Set Font Size", lambda a: action(a))

        self.menu = Menu()
        self.menu.add(text="Set Font", command=lambda e: set_font())
        self.menu.add(text="Bigger Font", command=lambda e: display.increase_font())
        self.menu.add(text="Smaller Font", command=lambda e: display.decrease_font())
        self.menu.add(text="Reset Font", command=lambda e: display.reset_font())

    def show(self, event: Any = None) -> None:
        from .widgets import widgets

        if event:
            self.menu.show(event)
        else:
            widget = getattr(widgets, "more_menu_button")
            self.menu.show(widget=widget)


main_menu = MainMenu()
model_menu = ModelMenu()
gpt_menu = GPTMenu()
more_menu = MoreMenu()
tab_menu = TabMenu()
font_menu = FontMenu()
