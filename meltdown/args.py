# Standard
import sys
from typing import List, Optional

# Modules
from .app import app
from .argparser import ArgParser
from .argspec import argspec


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
        self.drag_threshold = 100
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

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], argspec.arguments, self)

        self.fill_functions()

        for attr_name, attr_value in vars(self).items():
            argspec.defaults[attr_name] = attr_value

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

        keys = list(argspec.arguments.keys())

        if mode:
            if mode == "sort":
                keys = list(sorted(keys))
            else:
                keys = [key for key in keys if mode in key]

        text = []

        for key in keys:
            data = argspec.arguments[key]
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

        for key in argspec.arguments:
            if key == "string_arg":
                continue

            arg = argspec.arguments[key]
            text += sep
            name = key.replace("_", "-")
            text += f"### {name}"

            info = arg.get("help")

            if info:
                text += "\n\n"
                text += info

            defvalue = argspec.defaults.get(key)

            if defvalue is not None:
                if isinstance(defvalue, str):
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
