# Modules
from .app import app
from .argparser import ArgParser

# Standard
from typing import Any, Dict, List


class Args:
    def __init__(self) -> None:
        self.tooltips = True
        self.scrollbars = True
        self.colors = True
        self.avatars = True
        self.monitors = True
        self.monitor_colors = True
        self.monitor_cpu = True
        self.monitor_ram = True
        self.monitor_temp = True
        self.keyboard = True
        self.wrap = True
        self.maximized = False
        self.compact = False
        self.full = False
        self.test = False
        self.width = -1
        self.height = -1
        self.theme = ""
        self.config = ""
        self.session = ""
        self.on_log = ""

    class Internal:
        title = app.manifest["title"]
        version = app.manifest["version"]
        vinfo = f"{title} {version}"

        arguments: Dict[str, Any] = {
            "test": {"action": "store_true", "help": "Make a test tab for debugging"},
            "version": {"action": "version", "help": "Check the version of the program", "version": vinfo},
            "no-tooltips": {"action": "store_false", "help": "Don't show tooltips"},
            "no-scrollbars": {"action": "store_false", "help": "Don't show scrollbars"},
            "no-colors": {"action": "store_false", "help": "Don't show user colors"},
            "no-avatars": {"action": "store_false", "help": "Don't show user avatars"},
            "no-monitors": {"action": "store_false", "help": "Don't show system monitors"},
            "no-monitor-colors": {"action": "store_false", "help": "Disable system monitor colors"},
            "no-cpu": {"action": "store_false", "help": "Don't show the CPU monitor"},
            "no-ram": {"action": "store_false", "help": "Don't show the RAM monitor"},
            "no-temp": {"action": "store_false", "help": "Don't show the temperature monitor"},
            "no-keyboard": {"action": "store_false", "help": "Disable keyboard shortcuts"},
            "no-wrap": {"action": "store_false", "help": "Disable tab and menu wrapping"},
            "maximized": {"action": "store_true", "help": "Start in maximized mode"},
            "compact": {"action": "store_true", "help": "Start in compact mode"},
            "full": {"action": "store_true", "help": "Start in full mode"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "theme": {"type": str, "help": "The color theme to use, either dark or light", "choices": ["dark", "light"]},
            "config": {"type": str, "help": "Name or path of a config file to use"},
            "session": {"type": str, "help": "Name or path of a session file to use"},
            "on-log": {"type": str, "help": "Command to execute when saving a log file"},
        }

        aliases: Dict[str, List[str]] = {
            "maximized": ["--maximize", "-maximize", "--max", "-max"],
        }

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self.Internal.aliases, self)

        reversed = [
            ("no_tooltips", "tooltips"), ("no_scrollbars", "scrollbars"),
            ("no_colors", "colors"), ("no_avatars", "avatars"),
            ("no_monitors", "monitors"), ("no_monitor_colors", "monitor_colors"),
            ("no_cpu", "monitor_cpu"), ("no_ram", "monitor_ram"),
            ("no_temp", "monitor_temp"), ("no_keyboard", "keyboard"),
            ("no_wrap", "wrap"),
        ]

        for r_item in reversed:
            ap.normal(*r_item)

        normals = [
            "maximized", "compact", "full", "width", "height",
            "theme", "test", "config", "session", "on_log",
        ]

        for n_item in normals:
            ap.normal(n_item)

        self.parser = ap.parser

    def show_help(self, tab_id: str = "") -> None:
        from .display import display
        text = self.parser.format_help().strip()
        display.print("Command Line Arguments:", tab_id=tab_id)
        display.print(text, tab_id=tab_id)


args = Args()
