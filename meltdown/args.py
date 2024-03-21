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
        self.maximized = False
        self.compact = False
        self.full = False
        self.test = False
        self.width = -1
        self.height = -1
        self.theme = ""

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
            "maximized": {"action": "store_true", "help": "Start in maximized mode"},
            "compact": {"action": "store_true", "help": "Start in compact mode"},
            "full": {"action": "store_true", "help": "Start in full mode"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "theme": {"type": str, "help": "The color theme to use, either dark or light", "choices": ["dark", "light"]},
        }

        aliases: Dict[str, List[str]] = {
            "maximized": ["--maximize", "-maximize", "--max", "-max"],
        }

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self.Internal.aliases, self)
        ap.normal("no_tooltips", "tooltips")
        ap.normal("no_scrollbars", "scrollbars")
        ap.normal("no_colors", "colors")
        ap.normal("no_avatars", "avatars")
        ap.normal("no_monitors", "monitors")
        ap.normal("no_monitor_colors", "monitor_colors")
        ap.normal("no_cpu", "monitor_cpu")
        ap.normal("no_ram", "monitor_ram")
        ap.normal("no_temp", "monitor_temp")
        ap.normal("no_keyboard", "keyboard")
        ap.normal("maximized")
        ap.normal("compact")
        ap.normal("full")
        ap.normal("width")
        ap.normal("height")
        ap.normal("theme")
        ap.normal("test")

        self.parser = ap.parser


args = Args()
