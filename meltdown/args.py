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
        self.taps = True
        self.wrap = True
        self.stream = True
        self.maximized = False
        self.compact = False
        self.tabs = True
        self.allow_empty = True
        self.numbers = False
        self.full = False
        self.test = False
        self.width = -1
        self.height = -1
        self.max_tabs = 0
        self.theme = ""
        self.config = ""
        self.session = ""
        self.on_log = ""
        self.f1 = "help"
        self.f2 = ""
        self.f3 = "next"
        self.f4 = ""
        self.f5 = "reset"
        self.f6 = ""
        self.f7 = ""
        self.f8 = "compact"
        self.f9 = ""
        self.f10 = ""
        self.f11 = "fullscreen"
        self.f12 = "list"
        self.input = ""

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
            "no-taps": {"action": "store_false", "help": "Disable double ctrl taps"},
            "no-wrap": {"action": "store_false", "help": "Disable wrapping when selecting items"},
            "no-tabs": {"action": "store_false", "help": "Don't show the tab bar"},
            "no-stream": {"action": "store_false", "help": "Don't stream responses"},
            "no-empty": {"action": "store_false", "help": "Don't save empty conversations"},
            "maximized": {"action": "store_true", "help": "Start in maximized mode"},
            "compact": {"action": "store_true", "help": "Start in compact mode"},
            "full": {"action": "store_true", "help": "Start in full mode"},
            "numbers": {"action": "store_true", "help": "Show numbers in the tab bar"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "max-tabs": {"type": int, "help": "Max number fo tabs to keep open"},
            "theme": {"type": str, "help": "The color theme to use, either dark or light", "choices": ["dark", "light"]},
            "config": {"type": str, "help": "Name or path of a config file to use"},
            "session": {"type": str, "help": "Name or path of a session file to use"},
            "on-log": {"type": str, "help": "Command to execute when saving a log file"},
            "f1": {"type": str, "help": "Command to assign to the F1 key"},
            "f2": {"type": str, "help": "Command to assign to the F2 key"},
            "f3": {"type": str, "help": "Command to assign to the F3 key"},
            "f4": {"type": str, "help": "Command to assign to the F4 key"},
            "f5": {"type": str, "help": "Command to assign to the F5 key"},
            "f6": {"type": str, "help": "Command to assign to the F6 key"},
            "f7": {"type": str, "help": "Command to assign to the F7 key"},
            "f8": {"type": str, "help": "Command to assign to the F8 key"},
            "f9": {"type": str, "help": "Command to assign to the F9 key"},
            "f10": {"type": str, "help": "Command to assign to the F10 key"},
            "f11": {"type": str, "help": "Command to assign to the F11 key"},
            "f12": {"type": str, "help": "Command to assign to the F12 key"},
            "input": {"type": str, "help": "Prompt the AI automatically with this input when starting the program"},
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
            ("no_wrap", "wrap"), ("no_tabs", "tabs"),
            ("no_stream", "stream"), ("no_taps", "taps"),
            ("no_empty", "allow_empty"),
        ]

        for r_item in reversed:
            ap.normal(*r_item)

        normals = [
            "maximized", "compact", "full", "width", "height",
            "theme", "test", "config", "session", "on_log",
            "numbers", "max_tabs", "f1", "f2", "f3", "f4",
            "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
            "input",
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
