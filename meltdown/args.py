# Standard
import sys
from typing import Any, Dict, List, Optional, ClassVar

# Modules
from .app import app
from .argparser import ArgParser


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
        self.system_gpu = True
        self.system_gpu_ram = True
        self.system_gpu_temp = True
        self.system_ram = True
        self.system_temp = True
        self.system_threshold = 70
        self.system_delay = 3
        self.keyboard = True
        self.taps = True
        self.wrap = True
        self.stream = True
        self.maximize = False
        self.tabs = True
        self.allow_empty = True
        self.bottom = True
        self.bottom_autohide = True
        self.reorder = True
        self.numbers = False
        self.test = False
        self.alt_palette = False
        self.width = -1
        self.height = -1
        self.max_tabs = 0
        self.config = ""
        self.session = ""
        self.on_log = ""
        self.on_log_text = ""
        self.on_log_json = ""
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
        self.delay = 0.1
        self.prefix = "/"
        self.andchar = "&"
        self.commands = True
        self.compact_model = False
        self.compact_system = False
        self.compact_details_1 = False
        self.compact_details_2 = False
        self.compact_file = False
        self.compact_buttons = False
        self.compact_input = False
        self.display = False
        self.intro = True
        self.autorun = ""
        self.show_terminal = True
        self.terminal_height = 3
        self.terminal_vi = False
        self.input_memory = True
        self.input_memory_min = 4
        self.listener = False
        self.listener_delay = 0.5
        self.sticky = False
        self.commandoc = ""
        self.argumentdoc = ""
        self.after_stream = ""
        self.clean_slate = True
        self.tabs_always = False
        self.more_button = True
        self.model_icon = True
        self.model_feedback = True
        self.time = True
        self.verbose = False
        self.emojis = True
        self.write_button = True
        self.log_feedback = True
        self.avatars_in_logs = False
        self.browser = ""
        self.wrap_textbox = True
        self.font_diff = 0
        self.task_manager = "auto"
        self.task_manager_gpu = "auto"
        self.terminal = "auto"
        self.markdown = "ai"
        self.markdown_snippets = True
        self.markdown_italic = True
        self.markdown_bold = True
        self.markdown_highlights = True
        self.markdown_urls = True
        self.errors = False
        self.log_errors = True
        self.progtext = ""
        self.progjson = ""
        self.program = ""
        self.gestures = True
        self.gesture_threshold = 33
        self.increment_logs = True
        self.confirm_urls = True
        self.confirm_search = True
        self.confirm_close = True
        self.confirm_clear = True
        self.fill_prompt = True
        self.scroll_lines = 1
        self.user_color = "auto"
        self.ai_color = "auto"
        self.drag_and_drop = True
        self.confirm_exit = False
        self.use_keywords = True
        self.snippets_font = "monospace"
        self.show_prevnext = False
        self.short_labels = False
        self.show_labels = True
        self.short_buttons = False
        self.syntax_highlighting = True
        self.emoji_unloaded = "👻"
        self.emoji_local = "✅"
        self.emoji_remote = "🌐"
        self.emoji_loading = "⏰"
        self.emoji_storage = "💾"
        self.name_mode = "random"
        self.auto_name = True
        self.auto_name_length = 35
        self.tab_double_click = True

    class Internal:
        title: ClassVar[str] = app.manifest["title"]
        version: ClassVar[str] = app.manifest["version"]
        vinfo: ClassVar[str] = f"{title} {version}"
        defaults: ClassVar[Dict[str, Any]] = {}

        arguments: ClassVar[Dict[str, Any]] = {
            "version": {
                "action": "version",
                "help": "Check the version of the program",
                "version": vinfo,
            },
            "no_tooltips": {"action": "store_false", "help": "Don't show tooltips"},
            "no_scrollbars": {"action": "store_false", "help": "Don't show scrollbars"},
            "no_colors": {"action": "store_false", "help": "Don't show user colors"},
            "no_avatars": {"action": "store_false", "help": "Don't show user avatars"},
            "no_system": {
                "action": "store_false",
                "help": "Don't show system monitors",
            },
            "no_system_colors": {
                "action": "store_false",
                "help": "Disable system monitor colors",
            },
            "no_cpu": {"action": "store_false", "help": "Don't show the CPU monitor"},
            "no_gpu": {"action": "store_false", "help": "Don't show the GPU monitor"},
            "no_gpu_ram": {
                "action": "store_false",
                "help": "Don't show the GPU memory monitor",
            },
            "no_gpu_temp": {
                "action": "store_false",
                "help": "Don't show the GPU temperature monitor",
            },
            "no_ram": {"action": "store_false", "help": "Don't show the RAM monitor"},
            "no_temp": {
                "action": "store_false",
                "help": "Don't show the temperature monitor",
            },
            "no_keyboard": {
                "action": "store_false",
                "help": "Disable keyboard shortcuts",
            },
            "no_taps": {"action": "store_false", "help": "Disable double ctrl taps"},
            "no_wrap": {
                "action": "store_false",
                "help": "Disable wrapping when selecting items",
            },
            "no_tabs": {"action": "store_false", "help": "Don't show the tab bar"},
            "no_stream": {"action": "store_false", "help": "Don't stream responses"},
            "no_empty": {
                "action": "store_false",
                "help": "Don't save empty conversations",
            },
            "no_bottom": {
                "action": "store_false",
                "help": "Don't show the Bottom button",
            },
            "no_bottom_autohide": {
                "action": "store_false",
                "help": "Don't autohide the Bottom button",
            },
            "no_reorder": {
                "action": "store_false",
                "help": "Disable tab reordering by dragging",
            },
            "no_tab_highlight": {
                "action": "store_false",
                "help": "Don't highlight the tab when streaming",
            },
            "no_commands": {
                "action": "store_false",
                "help": "Disable commands when typing on the input",
            },
            "no_intro": {
                "action": "store_false",
                "help": "Don't print the intro in conversations",
            },
            "no_terminal": {
                "action": "store_false",
                "help": "Don't enable the interactive terminal",
            },
            "no_clean_slate": {
                "action": "store_false",
                "help": "Don't make a new tab when starting with an input",
            },
            "no_more_button": {
                "action": "store_false",
                "help": "Don't show the More button",
            },
            "no_model_icon": {
                "action": "store_false",
                "help": "Don't show the model icon",
            },
            "no_model_feedback": {
                "action": "store_false",
                "help": "Don't show model feedback when loading",
            },
            "no_log_feedback": {
                "action": "store_false",
                "help": "Don't show feedback when saving logs",
            },
            "no_emojis": {"action": "store_false", "help": "Don't use emojis"},
            "no_input_memory": {
                "action": "store_false",
                "help": "Don't remember input words",
            },
            "no_write_button": {
                "action": "store_false",
                "help": "Don't show the textbox button",
            },
            "no_wrap_textbox": {
                "action": "store_false",
                "help": "Don't wrap the textbox text",
            },
            "no_markdown_snippets": {
                "action": "store_false",
                "help": "Don't do snippet markdown",
            },
            "no_markdown_italic": {
                "action": "store_false",
                "help": "Don't do italic markdown",
            },
            "no_markdown_bold": {
                "action": "store_false",
                "help": "Don't do bold markdown",
            },
            "no_markdown_highlights": {
                "action": "store_false",
                "help": "Don't do highlight markdown",
            },
            "no_markdown_urls": {
                "action": "store_false",
                "help": "Don't do URL markdown",
            },
            "no_log_errors": {
                "action": "store_false",
                "help": "Don't log error messages to a file",
            },
            "no_time": {
                "action": "store_false",
                "help": "Don't show the loading time at startup",
            },
            "no_gestures": {
                "action": "store_false",
                "help": "Don't enable mouse gestures",
            },
            "no_increment_logs": {
                "action": "store_false",
                "help": "Always use the file name, don't increment with numbers",
            },
            "no_confirm_urls": {
                "action": "store_false",
                "help": "No need to confirm when opening URLs",
            },
            "no_confirm_search": {
                "action": "store_false",
                "help": "No need to confirm when searching",
            },
            "no_confirm_close": {
                "action": "store_false",
                "help": "No need to confirm closing tabs",
            },
            "no_confirm_clear": {
                "action": "store_false",
                "help": "No need to confirm clearing conversations",
            },
            "no_fill_prompt": {
                "action": "store_false",
                "help": "Don't fill the text input prompt in some cases when empty",
            },
            "no_drag_and_drop": {
                "action": "store_false",
                "help": "Don't enable drag and drop",
            },
            "no_keywords": {
                "action": "store_false",
                "help": "Don't do keyword replacements like ((now))",
            },
            "no_prevnext": {
                "action": "store_false",
                "help": "Don't show the Prev and Next buttons",
            },
            "no_auto_name": {
                "action": "store_false",
                "help": "Don't auto-name tabs based on input",
            },
            "no_tab_double_click": {
                "action": "store_false",
                "help": "Open new tabs on double click",
            },
            "no_labels": {
                "action": "store_false",
                "help": "Don't show the labels",
            },
            "no_syntax_highlighting": {
                "action": "store_false",
                "help": "Don't apply syntax highlighting to snippets",
            },
            "test": {"action": "store_true", "help": "Make a test tab for debugging"},
            "force": {
                "action": "store_true",
                "help": "Allow opening multiple instances",
            },
            "confirm_exit": {
                "action": "store_true",
                "help": "Show confirm exit dialog",
            },
            "compact_model": {
                "action": "store_true",
                "help": "Hide the model frame in compact mode",
            },
            "compact_system": {
                "action": "store_true",
                "help": "Hide the system frame in compactm ode",
            },
            "compact_details_1": {
                "action": "store_true",
                "help": "Hide the first details frame in compact mode",
            },
            "compact_details_2": {
                "action": "store_true",
                "help": "Hide the second details frame in compact mode",
            },
            "compact_buttons": {
                "action": "store_true",
                "help": "Hide the buttons frame in compact mode",
            },
            "compact_file": {
                "action": "store_true",
                "help": "Hide the URL frame in compact mode",
            },
            "compact_input": {
                "action": "store_true",
                "help": "Hide the input frame in compact mode",
            },
            "maximize": {
                "action": "store_true",
                "help": "Maximize the window on start",
            },
            "numbers": {"action": "store_true", "help": "Show numbers in the tab bar"},
            "alt_palette": {
                "action": "store_true",
                "help": "Show commands instead of descriptions in the palette",
            },
            "terminal_vi": {
                "action": "store_true",
                "help": "Use vi mode in the terminal",
            },
            "tabs_always": {
                "action": "store_true",
                "help": "Always show the tab bar even if only one tab",
            },
            "verbose": {
                "action": "store_true",
                "help": "Make the model verbose when streaming",
            },
            "quiet": {"action": "store_true", "help": "Don't show some messages"},
            "debug": {
                "action": "store_true",
                "help": "Show some information for debugging",
            },
            "display": {
                "action": "store_true",
                "help": "Only show the output and tabs",
            },
            "listener": {
                "action": "store_true",
                "help": "Listen for changes to the stdin file",
            },
            "sticky": {"action": "store_true", "help": "Make the window always on top"},
            "avatars_in_logs": {
                "action": "store_true",
                "help": "Show avatars in text logs",
            },
            "short_labels": {
                "action": "store_true",
                "help": "Use the short version of labels",
            },
            "short_buttons": {
                "action": "store_true",
                "help": "Use the short version of buttons",
            },
            "errors": {
                "action": "store_true",
                "help": "Show error messages",
            },
            "terminal_height": {
                "type": int,
                "help": "Reserve these number of rows for the terminal",
            },
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "max_tabs": {"type": int, "help": "Max number fo tabs to keep open"},
            "max_tab_width": {
                "type": int,
                "help": "Max number of characters to show in a tab name",
            },
            "config": {"type": str, "help": "Name or path of a config file to use"},
            "session": {"type": str, "help": "Name or path of a session file to use"},
            "on_log": {
                "type": str,
                "help": "Command to execute when saving any log file",
            },
            "on_log_text": {
                "type": str,
                "help": "Command to execute when saving a text log file",
            },
            "on_log_json": {
                "type": str,
                "help": "Command to execute when saving a JSON log file",
            },
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
            "input": {
                "type": str,
                "help": "Prompt the AI automatically with this input when starting the program",
            },
            "alias": {
                "type": str,
                "action": "append",
                "help": "Define an alias to run commands",
            },
            "task": {
                "type": str,
                "action": "append",
                "help": "Define a task to run periodically",
            },
            "gesture_threshold": {
                "type": str,
                "help": "Threshold in pixels for mouse gestures",
            },
            "scroll_lines": {
                "type": int,
                "help": "How many lines to scroll the output",
            },
            "auto_name_length": {
                "type": int,
                "help": "Max char length for auto tab names",
            },
            "old_tabs_minutes": {
                "type": int,
                "help": "Consider a tab old after these minutes (using last modified date)",
            },
            "max_list_items": {
                "type": int,
                "help": "Max number of items in context menu lists",
            },
            "list_item_width": {
                "type": int,
                "help": "Max characters for the text of list items",
            },
            "drag_threshold": {
                "type": int,
                "help": "The higher the number the less sensitive the tab dragging will be",
            },
            "delay": {
                "type": float,
                "help": "Delay in seconds between each print when streaming",
            },
            "prefix": {"type": str, "help": "Character used to prefix commands like /"},
            "andchar": {"type": str, "help": "Character used to join commands like &"},
            "system_threshold": {
                "type": int,
                "help": "Show system monitors as critical after this percentage threshold",
            },
            "system_delay": {
                "type": int,
                "help": "Delay in seconds for system monitor updates",
            },
            "autorun": {"type": str, "help": "Run this command at startup"},
            "input_memory_min": {
                "type": int,
                "help": "Minimum number of characters for input words to be remembered",
            },
            "listener_delay": {"type": float, "help": "Delay for the listener checks"},
            "commandoc": {
                "type": str,
                "help": "Make the commandoc and save it on this path",
            },
            "argumentdoc": {
                "type": str,
                "help": "Make the argument and save it on this path",
            },
            "after_stream": {
                "type": str,
                "help": "Execute this command after streaming a response",
            },
            "markdown": {
                "type": str,
                "choices": ["user", "ai", "all", "none"],
                "help": "Define where to apply markdown formatting",
            },
            "browser": {"type": str, "help": "Open links with this browser"},
            "font_diff": {"type": int, "help": "Add or subtract this from font sizes"},
            "task_manager": {"type": str, "help": "Which task manager to use"},
            "task_manager_gpu": {
                "type": str,
                "help": "Which task manager to use on the gpu monitors",
            },
            "terminal": {"type": str, "help": "Which terminal to use"},
            "progtext": {
                "type": str,
                "help": "Use this program as default for the progtext command",
            },
            "progjson": {
                "type": str,
                "help": "Use this program as default for the progjson command",
            },
            "program": {
                "type": str,
                "help": "Use this program as default for the progtext and progjson commands",
            },
            "user_color": {
                "type": str,
                "help": "The color of the text for the name of the user",
            },
            "ai_color": {
                "type": str,
                "help": "The color of the text for the name of the AI",
            },
            "snippets_font": {
                "type": str,
                "help": "The font to use in snippets",
            },
            "emoji_unloaded": {
                "type": str,
                "help": "Emoji to show when a model is not loaded",
            },
            "emoji_local": {
                "type": str,
                "help": "Emoji to show when a model is loaded locally",
            },
            "emoji_remote": {
                "type": str,
                "help": "Emoji to show when a model is loaded remotely",
            },
            "emoji_loading": {
                "type": str,
                "help": "Emoji to show when loading a model",
            },
            "emoji_storage": {
                "type": str,
                "help": "Emoji to show when saving a log",
            },
            "name_mode": {
                "type": str,
                "choices": ["random", "noun", "empty"],
                "help": "What mode to use when naming new tabs",
            },
        }

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self)

        self.fill_functions()

        for attr_name, attr_value in vars(self).items():
            self.Internal.defaults[attr_name] = attr_value

        other_name = [
            ("alias", "aliases"),
            ("task", "tasks"),
            ("no_tooltips", "tooltips"),
            ("no_scrollbars", "scrollbars"),
            ("no_colors", "colors"),
            ("no_avatars", "avatars"),
            ("no_system", "system"),
            ("no_system_colors", "system_colors"),
            ("no_cpu", "system_cpu"),
            ("no_ram", "system_ram"),
            ("no_temp", "system_temp"),
            ("no_keyboard", "keyboard"),
            ("no_wrap", "wrap"),
            ("no_tabs", "tabs"),
            ("no_stream", "stream"),
            ("no_taps", "taps"),
            ("no_empty", "allow_empty"),
            ("no_bottom_autohide", "bottom_autohide"),
            ("no_bottom", "bottom"),
            ("no_reorder", "reorder"),
            ("no_tab_highlight", "tab_highlight"),
            ("no_commands", "commands"),
            ("no_intro", "intro"),
            ("no_terminal", "show_terminal"),
            ("no_clean_slate", "clean_slate"),
            ("no_emojis", "emojis"),
            ("no_more_button", "more_button"),
            ("no_model_icon", "model_icon"),
            ("no_model_feedback", "model_feedback"),
            ("no_input_memory", "input_memory"),
            ("no_write_button", "write_button"),
            ("no_log_feedback", "log_feedback"),
            ("no_wrap_textbox", "wrap_textbox"),
            ("no_gpu", "system_gpu"),
            ("no_gpu_ram", "system_gpu"),
            ("no_gpu_temp", "system_gpu"),
            ("no_markdown_snippets", "markdown_snippets"),
            ("no_markdown_italic", "markdown_italic"),
            ("no_markdown_bold", "markdown_bold"),
            ("no_markdown_highlights", "markdown_highlights"),
            ("no_markdown_urls", "markdown_urls"),
            ("no_log_errors", "log_errors"),
            ("no_time", "time"),
            ("no_gestures", "gestures"),
            ("no_increment_logs", "increment_logs"),
            ("no_confirm_urls", "confirm_urls"),
            ("no_confirm_search", "confirm_search"),
            ("no_confirm_close", "confirm_close"),
            ("no_confirm_clear", "confirm_clear"),
            ("no_fill_prompt", "fill_prompt"),
            ("no_drag_and_drop", "drag_and_drop"),
            ("no_keywords", "use_keywords"),
            ("no_prevnext", "show_prevnext"),
            ("no_labels", "show_labels"),
            ("no_syntax_highlighting", "syntax_highlighting"),
            ("no_auto_name", "auto_name"),
            ("no_tab_double_click", "tab_double_click"),
        ]

        for r_item in other_name:
            ap.get_value(*r_item)

        normals = [
            "maximize",
            "width",
            "height",
            "test",
            "config",
            "session",
            "numbers",
            "max_tabs",
            "input",
            "force",
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f7",
            "f8",
            "f9",
            "f10",
            "f11",
            "f12",
            "alt_palette",
            "max_tab_width",
            "old_tabs_minutes",
            "max_list_items",
            "list_item_width",
            "system_threshold",
            "drag_threshold",
            "system_delay",
            "quiet",
            "debug",
            "delay",
            "prefix",
            "andchar",
            "compact_system",
            "compact_details_1",
            "compact_details_2",
            "compact_file",
            "compact_buttons",
            "compact_model",
            "compact_input",
            "display",
            "autorun",
            "terminal_height",
            "terminal_vi",
            "verbose",
            "markdown",
            "listener",
            "listener_delay",
            "sticky",
            "commandoc",
            "argumentdoc",
            "after_stream",
            "tabs_always",
            "input_memory_min",
            "avatars_in_logs",
            "browser",
            "font_diff",
            "task_manager",
            "task_manager_gpu",
            "terminal",
            "on_log",
            "on_log_text",
            "on_log_json",
            "errors",
            "progtext",
            "progjson",
            "program",
            "gesture_threshold",
            "scroll_lines",
            "user_color",
            "ai_color",
            "confirm_exit",
            "snippets_font",
            "short_labels",
            "short_buttons",
            "emoji_unloaded",
            "emoji_local",
            "emoji_remote",
            "emoji_loading",
            "emoji_storage",
            "name_mode",
            "auto_name_length",
        ]

        for n_item in normals:
            ap.get_value(n_item)

        if not sys.stdin.isatty():
            self.input = sys.stdin.read()
        else:
            string_arg = ap.string_arg()

            if string_arg:
                self.input = string_arg

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

    def show_help(
        self, tab_id: Optional[str] = None, mode: Optional[str] = None
    ) -> None:
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
                extra = f" ({argtype.__name__})"
            elif action:
                extra = " (bool)"
            else:
                extra = ""

            text.append(f"{key}{extra} = {msg}")

        display.print("\n".join(text), tab_id=tab_id)

    def make_argumentdoc(self, pathstr: str) -> None:
        from .utils import utils
        from .display import display
        from pathlib import Path

        path = Path(pathstr)

        if (not path.parent.exists()) or (not path.parent.is_dir()):
            utils.msg(f"Invalid path: {pathstr}")
            return

        sep = "\n\n---\n\n"

        text = "## Arguments\n\n"

        text += "Here are all the available command line arguments:"

        for key in self.Internal.arguments:
            if key == "string_arg":
                continue

            arg = self.Internal.arguments[key]
            text += sep
            name = key.replace("_", "-")
            text += f"### {name}"

            info = arg.get("help")

            if info:
                text += "\n\n"
                text += info

            defvalue = self.Internal.defaults.get(key)

            if defvalue is not None:
                if type(defvalue) == str:
                    if defvalue == "":
                        defvalue = "[Empty string]"
                    else:
                        defvalue = f'"{defvalue}"'

                text += "\n\n"
                text += f"Default: {defvalue}"

            choices = arg.get("choices", [])

            if choices:
                text += "\n\n"
                text += "Choices: "

                choicestr = [
                    f'"{choice}"' if isinstance(choice, str) else choice
                    for choice in choices
                ]

                text += ", ".join(choicestr)

            action = arg.get("action", "")

            if action:
                text += "\n\n"
                text += f"Action: {action}"

            argtype = arg.get("type", "")

            if argtype:
                text += "\n\n"
                text += f"Type: {argtype.__name__}"

        with path.open("w", encoding="utf-8") as file:
            file.write(text)

        msg = f"Saved to {path}"
        display.print(msg)
        utils.msg(msg)


args = Args()
