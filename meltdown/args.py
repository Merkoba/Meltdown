# Modules
from .app import app
from .argparser import ArgParser

# Standard
import sys
from typing import Any, Dict, List


class Args:
    def __init__(self) -> None:
        self.force = False
        self.tooltips = True
        self.scrollbars = True
        self.colors = True
        self.avatars = True
        self.system = True
        self.system_colors = True
        self.system_cpu = True
        self.system_ram = True
        self.system_temp = True
        self.system_threshold = 70
        self.system_delay = 3
        self.keyboard = True
        self.taps = True
        self.wrap = True
        self.stream = True
        self.maximize = False
        self.compact = False
        self.tabs = True
        self.allow_empty = True
        self.bottom = True
        self.bottom_autohide = True
        self.reorder = True
        self.numbers = False
        self.full = False
        self.test = False
        self.alt_palette = False
        self.width = -1
        self.height = -1
        self.max_tabs = 0
        self.theme = ""
        self.config = ""
        self.session = ""
        self.on_log = ""
        self.f1 = ""
        self.f2 = ""
        self.f3 = ""
        self.f4 = ""
        self.f5 = ""
        self.f6 = ""
        self.f7 = ""
        self.f8 = ""
        self.f9 = ""
        self.f10 = ""
        self.f11 = ""
        self.f12 = ""
        self.input = ""
        self.aliases: List[str] = []
        self.tasks: List[str] = []
        self.max_tab_width = 0
        self.old_tabs_minutes = 30
        self.max_list_items = 10
        self.list_item_width = 100
        self.drag_threshold = 88
        self.tab_highlight = True
        self.quiet = False
        self.debug = False
        self.delay = 0.15
        self.prefix = "/"
        self.andchar = "&"
        self.keychar = "@"
        self.commands = True
        self.compact_model = False
        self.compact_system = False
        self.compact_details = False
        self.compact_addons = False
        self.compact_buttons = False
        self.compact_input = False
        self.display = False

    class Internal:
        title = app.manifest["title"]
        version = app.manifest["version"]
        vinfo = f"{title} {version}"

        arguments: Dict[str, Any] = {
            "test": {"action": "store_true", "help": "Make a test tab for debugging"},
            "force": {"action": "store_true", "help": "Allow opening multiple instances"},
            "version": {"action": "version", "help": "Check the version of the program", "version": vinfo},
            "no-tooltips": {"action": "store_false", "help": "Don't show tooltips"},
            "no-scrollbars": {"action": "store_false", "help": "Don't show scrollbars"},
            "no-colors": {"action": "store_false", "help": "Don't show user colors"},
            "no-avatars": {"action": "store_false", "help": "Don't show user avatars"},
            "no-system": {"action": "store_false", "help": "Don't show system monitors"},
            "no-system-colors": {"action": "store_false", "help": "Disable system monitor colors"},
            "no-cpu": {"action": "store_false", "help": "Don't show the CPU monitor"},
            "no-ram": {"action": "store_false", "help": "Don't show the RAM monitor"},
            "no-temp": {"action": "store_false", "help": "Don't show the temperature monitor"},
            "system-threshold": {"type": int, "help": "Show system monitors as critical after this percentage threshold"},
            "system-delay": {"type": int, "help": "Delay in seconds for system monitor updates"},
            "no-keyboard": {"action": "store_false", "help": "Disable keyboard shortcuts"},
            "no-taps": {"action": "store_false", "help": "Disable double ctrl taps"},
            "no-wrap": {"action": "store_false", "help": "Disable wrapping when selecting items"},
            "no-tabs": {"action": "store_false", "help": "Don't show the tab bar"},
            "no-stream": {"action": "store_false", "help": "Don't stream responses"},
            "no-empty": {"action": "store_false", "help": "Don't save empty conversations"},
            "no-bottom": {"action": "store_false", "help": "Don't show the Bottom button"},
            "no-bottom-autohide": {"action": "store_false", "help": "Don't autohide the Bottom button"},
            "no-reorder": {"action": "store_false", "help": "Disable tab reordering by dragging"},
            "no-tab-highlight": {"action": "store_false", "help": "Don't highlight the tab when streaming"},
            "no-commands": {"action": "store_false", "help": "Disable commands when typing on the input"},
            "compact-model": {"action": "store_true", "help": "Hide the model frame in compact mode"},
            "compact-system": {"action": "store_true", "help": "Hide the system frame in compactm ode"},
            "compact-details": {"action": "store_true", "help": "Hide the details frame in compact mode"},
            "compact-buttons": {"action": "store_true", "help": "Hide the buttons frame in compact mode"},
            "compact-addons": {"action": "store_true", "help": "Hide the addons frame in compact mode"},
            "compact-input": {"action": "store_true", "help": "Hide the input frame in compact mode"},
            "maximize": {"action": "store_true", "help": "Maximize the window on start"},
            "compact": {"action": "store_true", "help": "Start in compact mode"},
            "full": {"action": "store_true", "help": "Start in full mode"},
            "numbers": {"action": "store_true", "help": "Show numbers in the tab bar"},
            "alt-palette": {"action": "store_true", "help": "Show commands instead of descriptions in the palette"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "max-tabs": {"type": int, "help": "Max number fo tabs to keep open"},
            "max-tab-width": {"type": int, "help": "Max number of characters to show in a tab name"},
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
            "alias": {"type": str, "action": "append", "help": "Define an alias to run commands"},
            "task": {"type": str, "action": "append", "help": "Define a task to run periodically"},
            "old-tabs-minutes": {"type": int, "help": "Consider a tab old after these minutes (using last modified date)"},
            "max-list-items": {"type": int, "help": "Max number of items in context menu lists"},
            "list-item-width": {"type": int, "help": "Max characters for the text of list items"},
            "drag-threshold": {"type": int, "help": "The higher the number the less sensitive the tab dragging will be"},
            "quiet": {"action": "store_true", "help": "Don't show some messages"},
            "debug": {"action": "store_true", "help": "Show some information for debugging"},
            "delay": {"type": float, "help": "Delay in seconds between each print when streaming"},
            "prefix": {"type": str, "help": "Character used to prefix commands like /"},
            "andchar": {"type": str, "help": "Character used to join commands like &"},
            "keychar": {"type": str, "help": "Character used for keywords like @"},
            "display": {"action": "store_true", "help": "Only show the output and tabs"},
        }

        aliases: Dict[str, List[str]] = {
            "maximize": ["--max", "-max"],
        }

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self.Internal.aliases, self)

        other_name = [
            ("no_tooltips", "tooltips"), ("no_scrollbars", "scrollbars"),
            ("no_colors", "colors"), ("no_avatars", "avatars"),
            ("no_system", "system"), ("no_system_colors", "system_colors"),
            ("no_cpu", "system_cpu"), ("no_ram", "system_ram"),
            ("no_temp", "system_temp"), ("no_keyboard", "keyboard"),
            ("no_wrap", "wrap"), ("no_tabs", "tabs"),
            ("no_stream", "stream"), ("no_taps", "taps"),
            ("no_empty", "allow_empty"), ("alias", "aliases"),
            ("task", "tasks"), ("no_bottom_autohide", "bottom_autohide"),
            ("no_bottom", "bottom"), ("no_reorder", "reorder"),
            ("no_tab_highlight", "tab_highlight"), ("no_commands", "commands"),
        ]

        for r_item in other_name:
            ap.normal(*r_item)

        normals = [
            "maximize", "compact", "full", "width", "height",
            "theme", "test", "config", "session", "on_log",
            "numbers", "max_tabs", "input", "force",

            "f1", "f2", "f3", "f4", "f5", "f6", "f7",
            "f8", "f9", "f10", "f11", "f12",

            "alt_palette", "max_tab_width", "old_tabs_minutes",
            "max_list_items", "list_item_width", "system_threshold",
            "drag_threshold", "system_delay", "quiet", "debug",
            "delay", "prefix", "keychar", "andchar",

            "compact_system", "compact_details", "compact_addons",
            "compact_buttons", "compact_model", "compact_input",

            "display",
        ]

        for n_item in normals:
            ap.normal(n_item)

        if not sys.stdin.isatty():
            self.input = sys.stdin.read()
        else:
            string_arg = ap.string_arg()

            if string_arg:
                self.input = string_arg

        self.fill_functions()
        self.parser = ap.parser

    def fill_functions(self) -> None:
        if not self.f1:
            self.f1 = f"{self.prefix}help"

        if not self.f3:
            self.f3 = f"{self.prefix}next"

        if not self.f5:
            self.f5 = f"{self.prefix}reset"

        if not self.f8:
            self.f8 = f"{self.prefix}compact"

        if not self.f11:
            self.f11 = f"{self.prefix}fullscreen"

        if not self.f12:
            self.f12 = f"{self.prefix}list"

    def show_help(self, tab_id: str = "", mode: str = "") -> None:
        from .display import display
        keys = list(self.Internal.arguments.keys())

        if mode:
            if mode == "sort":
                keys = list(sorted(keys))
            else:
                keys = [key for key in keys if mode in key]

        text = []

        for key in keys:
            data = self.Internal.arguments[key]
            msg = data.get("help")

            if not msg:
                continue

            argtype = data.get("type", "")
            action = data.get("action", "")

            if argtype:
                extra = f" ({str(argtype.__name__)})"
            elif action:
                extra = " (flag)"
            else:
                extra = ""

            text.append(f"{key}{extra} = {msg}")

        display.print("\n".join(text), tab_id=tab_id)


args = Args()
