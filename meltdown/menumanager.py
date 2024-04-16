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
            text="System Prompt", command=lambda: widgets.write_system_prompt()
        )
        self.menu.separator()
        self.menu.add(text="Configs", command=lambda: config.menu())
        self.menu.add(text="Sessions", command=lambda: session.menu())
        self.menu.add(text="Logs", command=lambda: logs.menu())
        self.menu.separator()
        self.menu.add(text="Commands", command=lambda: commands.show_palette())
        self.menu.separator()
        self.menu.add(text="Compact", command=lambda: app.toggle_compact())
        self.menu.add(text="Resize", command=lambda: app.resize())
        self.menu.add(text="Theme", command=lambda: app.toggle_theme())
        self.menu.add(text="About", command=lambda: app.show_about())
        self.menu.separator()
        self.menu.add(text="Exit", command=lambda: app.exit())

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
            text="Recent Models", command=lambda: widgets.show_recent_models()
        )
        self.menu.add(text="Browse Models", command=lambda: model.browse_models())
        self.menu.add(text="Use GPT Model", command=lambda: gpt_menu.show())
        self.menu.add(text="Set API Key", command=lambda: model.set_api_key())

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
            self.menu.add(text=gpt[1], command=lambda gpt=gpt: widgets.use_gpt(gpt[0]))

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
        self.menu.add(text="Find", command=lambda: display.find())
        self.menu.add(text="Find All", command=lambda: display.find_all())
        self.menu.separator()
        self.menu.add(text="Copy All", command=lambda: display.copy_output())
        self.menu.add(text="Select All", command=lambda: display.select_output())
        self.menu.separator()
        self.menu.add(text="View Text", command=lambda: display.view_text())
        self.menu.add(text="View JSON", command=lambda: display.view_json())
        self.menu.separator()
        self.menu.add(text="Tabs", command=lambda: tab_menu.show())
        self.menu.separator()
        self.menu.add(text="Bigger Font", command=lambda: display.increase_font())
        self.menu.add(text="Smaller Font", command=lambda: display.decrease_font())
        self.menu.add(text="Reset Font", command=lambda: display.reset_font())

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

        self.menu = Menu()
        self.menu.add(text="Tab List", command=lambda: display.show_tab_list())
        self.menu.add(text="First Tab", command=lambda: display.select_first_tab())
        self.menu.add(text="Last Tab", command=lambda: display.select_last_tab())
        self.menu.add(text="Active Tab", command=lambda: display.select_active_tab())

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
