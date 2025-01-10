from __future__ import annotations

# Standard
import sys
from pathlib import Path
from typing import Any

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
        self.system_colors = True
        self.system_cpu = True
        self.system_gpu = True
        self.system_gpu_ram = True
        self.system_gpu_temp = True
        self.system_ram = True
        self.system_temp = True
        self.system_threshold = 70
        self.system_delay = 2
        self.system_suspend = 1
        self.system_auto_hide = True
        self.keyboard = True
        self.taps = True
        self.taps_command = ""
        self.wrap = True
        self.stream = True
        self.maximize = False
        self.show_tabs = True
        self.allow_empty = True
        self.bottom = True
        self.bottom_autohide = True
        self.reorder = True
        self.tab_numbers = False
        self.test = False
        self.test2 = False
        self.alt_palette = False
        self.width = 0
        self.height = 0
        self.max_tabs = 100
        self.config = ""
        self.session = ""
        self.on_log = ""
        self.on_log_text = ""
        self.on_log_json = ""
        self.on_log_markdown = ""
        self.on_copy = ""
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
        self.shift_f1 = ""
        self.shift_f2 = ""
        self.shift_f3 = ""
        self.shift_f4 = ""
        self.shift_f5 = ""
        self.shift_f6 = ""
        self.shift_f7 = ""
        self.shift_f8 = ""
        self.shift_f9 = ""
        self.shift_f10 = ""
        self.shift_f11 = ""
        self.shift_f12 = ""
        self.input = ""
        self.aliases: list[str] = []
        self.tasks: list[str] = []
        self.max_tab_width = 0
        self.old_tabs_minutes = 30
        self.max_list_items = 10
        self.list_item_width = 100
        self.drag_threshold = 90
        self.tab_highlight = True
        self.quiet = False
        self.delay = 0.1
        self.prefix = "/"
        self.andchar = "&"
        self.commands = True
        self.compact = False
        self.compact_system = False
        self.compact_model = False
        self.compact_details_1 = False
        self.compact_details_2 = False
        self.compact_file = False
        self.compact_buttons = False
        self.compact_input = False
        self.show_intro = True
        self.show_header = True
        self.autorun = ""
        self.console = False
        self.console_height = 3
        self.console_vi = False
        self.input_memory = True
        self.input_memory_min = 5
        self.input_memory_max = 30
        self.input_memory_max_items = 1000
        self.listener = False
        self.listener_delay = 1
        self.listener_path = ""
        self.sticky = False
        self.commandoc = ""
        self.argumentdoc = ""
        self.keyboardoc = ""
        self.after_stream = ""
        self.clean_slate = True
        self.tabs_always = False
        self.model_icon = True
        self.model_feedback = True
        self.time = True
        self.verbose = False
        self.emojis = True
        self.write_button = True
        self.log_feedback = True
        self.avatars_in_logs = False
        self.avatars_in_uploads = False
        self.files_in_logs = True
        self.files_in_uploads = True
        self.generic_names_logs = False
        self.generic_names_uploads = False
        self.browser = ""
        self.file_manager = ""
        self.wrap_textbox = True
        self.font_diff = 0
        self.task_manager = "auto"
        self.task_manager_gpu = "auto"
        self.terminal = "auto"
        self.tabs_wheel = True
        self.display_wheel = True
        self.ordered_char = "."
        self.unordered_char = "•"
        self.ordered_spacing = "auto"
        self.unordered_spacing = "auto"

        self.markdown = "both"
        self.markdown_snippets = "ai"
        self.markdown_ordered = "ai"
        self.markdown_unordered = "ai"
        self.markdown_italic_asterisk = "ai"
        self.markdown_italic_underscore = "ai"
        self.markdown_bold = "ai"
        self.markdown_highlight = "ai"
        self.markdown_quote = "both"
        self.markdown_url = "both"
        self.markdown_path = "both"
        self.markdown_header = "ai"
        self.markdown_separator = "ai"

        self.bold_effects = "bold"
        self.italic_effects = "italic_color"
        self.highlight_effects = "color"
        self.uselink_effects = "color"
        self.quote_effects = "color"
        self.list_effects = "color"
        self.url_effects = "underline"
        self.path_effects = "underline"
        self.header_1_effects = "bold"
        self.header_2_effects = "bold"
        self.header_3_effects = "bold"

        self.errors = False
        self.log_errors = True
        self.program_text = ""
        self.program_json = ""
        self.program_markdown = ""
        self.program = ""

        self.gestures = True
        self.gestures_threshold = 33
        self.gestures_left = ""
        self.gestures_right = ""
        self.gestures_up = ""
        self.gestures_down = ""

        self.increment_logs = True
        self.confirm_close = True
        self.confirm_clear = True
        self.confirm_delete = True
        self.confirm_exit = False
        self.fill_prompt = True
        self.scroll_lines = 1
        self.auto_bottom = True
        self.user_color = "auto"
        self.ai_color = "auto"
        self.use_keywords = True
        self.snippets_font = "monospace"
        self.short_labels = False
        self.show_labels = True
        self.short_buttons = False
        self.short_system = False
        self.syntax_highlighting = True
        self.emoji_unloaded = "👻"
        self.emoji_local = "✅"
        self.emoji_remote = "🌐"
        self.emoji_loading = "⏰"
        self.emoji_storage = "💾"
        self.name_mode = "random"
        self.auto_name = True
        self.auto_name_length = 30
        self.tab_double_click = True
        self.arrow_mode = "history"
        self.display_mode = False
        self.no_exit = False
        self.disable_buttons = True
        self.scroll_percentage = False
        self.scroll_percentage_reverse = False
        self.item_numbers = False
        self.name_menu = True
        self.word_menu = True
        self.url_menu = True
        self.path_menu = True
        self.list_menu = True
        self.file = ""
        self.image_prompt = "Describe this image"
        self.durations = False
        self.separators = False
        self.help_prompt = "I need help!"
        self.explain_prompt = "What is ((words))?"
        self.new_prompt = "Tell me about ((words))"
        self.summarize_prompt = "Summarize this, without addressing me"
        self.custom_prompts: list[str] = []
        self.on_shift_middle_click = ""
        self.on_ctrl_middle_click = ""
        self.on_ctrl_shift_middle_click = ""
        self.temporary = False
        self.clean = False
        self.profile = "main"
        self.limit_tokens = True
        self.clean_names = True
        self.border_color = ""
        self.border_size = 5
        self.title = ""
        self.icon = ""
        self.auto_scroll_delay = 720
        self.show_auto_scroll = True
        self.scroller_buttons = True
        self.portrait = ""
        self.command_history = True
        self.shorten_paths = True
        self.separate_logs = True
        self.separate_uploads = True
        self.ascii_logs = False
        self.quote_used_words = True
        self.open_on_log = False
        self.list_item_max_length = 200
        self.response_file = ""
        self.response_program = ""
        self.use_program = ""
        self.use_both = False
        self.theme = ""
        self.auto_unload = 0
        self.tab_tooltip_length = 235
        self.uselinks: list[str] = []
        self.concat_logs = False
        self.mouse_scroll = False
        self.thinking_text = "Thinking..."
        self.logs_dir = ""
        self.upload_password = ""
        self.log_name_user = ""
        self.log_name_ai = ""
        self.upload_name_user = ""
        self.upload_name_ai = ""
        self.signals = ""
        self.config_dir = ""
        self.data_dir = ""
        self.border_effect = False
        self.border_effect_color = ""
        self.argfile = ""
        self.max_items = 100

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], argspec.arguments, self)

        self.fill_functions()
        self.fill_gestures()

        for attr_name, attr_value in vars(self).items():
            argspec.defaults[attr_name] = attr_value

        other_name = [
            ("alias", "aliases"),
            ("task", "tasks"),
            ("custom_prompt", "custom_prompts"),
            ("uselink", "uselinks"),
            ("no_tooltips", "tooltips"),
            ("no_scrollbars", "scrollbars"),
            ("no_colors", "colors"),
            ("no_avatars", "avatars"),
            ("no_system_colors", "system_colors"),
            ("no_cpu", "system_cpu"),
            ("no_ram", "system_ram"),
            ("no_temp", "system_temp"),
            ("no_keyboard", "keyboard"),
            ("no_wrap", "wrap"),
            ("no_tabs", "show_tabs"),
            ("no_stream", "stream"),
            ("no_taps", "taps"),
            ("no_empty", "allow_empty"),
            ("no_bottom_autohide", "bottom_autohide"),
            ("no_bottom", "bottom"),
            ("no_reorder", "reorder"),
            ("no_tab_highlight", "tab_highlight"),
            ("no_commands", "commands"),
            ("no_intro", "show_intro"),
            ("no_header", "show_header"),
            ("no_clean_slate", "clean_slate"),
            ("no_emojis", "emojis"),
            ("no_model_icon", "model_icon"),
            ("no_model_feedback", "model_feedback"),
            ("no_input_memory", "input_memory"),
            ("no_write_button", "write_button"),
            ("no_log_feedback", "log_feedback"),
            ("no_wrap_textbox", "wrap_textbox"),
            ("no_gpu", "system_gpu"),
            ("no_gpu_ram", "system_gpu"),
            ("no_gpu_temp", "system_gpu"),
            ("no_log_errors", "log_errors"),
            ("no_time", "time"),
            ("no_gestures", "gestures"),
            ("no_increment_logs", "increment_logs"),
            ("no_confirm_close", "confirm_close"),
            ("no_confirm_clear", "confirm_clear"),
            ("no_confirm_delete", "confirm_delete"),
            ("no_fill_prompt", "fill_prompt"),
            ("no_keywords", "use_keywords"),
            ("no_labels", "show_labels"),
            ("no_syntax_highlighting", "syntax_highlighting"),
            ("no_auto_name", "auto_name"),
            ("no_tab_double_click", "tab_double_click"),
            ("no_disable_buttons", "disable_buttons"),
            ("no_auto_bottom", "auto_bottom"),
            ("no_name_menu", "name_menu"),
            ("no_word_menu", "word_menu"),
            ("no_url_menu", "url_menu"),
            ("no_path_menu", "path_menu"),
            ("no_list_menu", "list_menu"),
            ("no_files_in_logs", "files_in_logs"),
            ("no_files_in_uploads", "files_in_uploads"),
            ("no_tabs_wheel", "tabs_wheel"),
            ("no_display_wheel", "display_wheel"),
            ("no_limit_tokens", "limit_tokens"),
            ("no_clean_names", "clean_names"),
            ("no_auto_scroll", "show_auto_scroll"),
            ("no_scroller_buttons", "scroller_buttons"),
            ("no_command_history", "command_history"),
            ("no_shorten_paths", "shorten_paths"),
            ("no_separate_logs", "separate_logs"),
            ("no_separate_uploads", "separate_uploads"),
            ("no_quote_used_words", "quote_used_words"),
            ("no_system_auto_hide", "system_auto_hide"),
        ]

        for r_item in other_name:
            ap.get_value(*r_item)

        normals = [
            "maximize",
            "width",
            "height",
            "test",
            "test2",
            "config",
            "session",
            "tab_numbers",
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
            "shift_f1",
            "shift_f2",
            "shift_f3",
            "shift_f4",
            "shift_f5",
            "shift_f6",
            "shift_f7",
            "shift_f8",
            "shift_f9",
            "shift_f10",
            "shift_f11",
            "shift_f12",
            "alt_palette",
            "max_tab_width",
            "old_tabs_minutes",
            "max_list_items",
            "list_item_width",
            "system_threshold",
            "drag_threshold",
            "system_delay",
            "system_suspend",
            "quiet",
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
            "autorun",
            "console_height",
            "console_vi",
            "verbose",
            "markdown",
            "listener",
            "listener_delay",
            "listener_path",
            "sticky",
            "commandoc",
            "argumentdoc",
            "keyboardoc",
            "after_stream",
            "tabs_always",
            "input_memory_min",
            "input_memory_max",
            "input_memory_max_items",
            "browser",
            "file_manager",
            "font_diff",
            "task_manager",
            "task_manager_gpu",
            "terminal",
            "on_log",
            "on_log_text",
            "on_log_json",
            "on_log_markdown",
            "on_copy",
            "errors",
            "program_text",
            "program_json",
            "program_markdown",
            "program",
            "gestures_threshold",
            "gestures_left",
            "gestures_right",
            "gestures_up",
            "gestures_down",
            "scroll_lines",
            "user_color",
            "ai_color",
            "confirm_exit",
            "snippets_font",
            "short_labels",
            "short_buttons",
            "short_system",
            "emoji_unloaded",
            "emoji_local",
            "emoji_remote",
            "emoji_loading",
            "emoji_storage",
            "name_mode",
            "auto_name_length",
            "arrow_mode",
            "display_mode",
            "compact",
            "no_exit",
            "summarize_prompt",
            "scroll_percentage",
            "scroll_percentage_reverse",
            "item_numbers",
            "file",
            "image_prompt",
            "avatars_in_logs",
            "avatars_in_uploads",
            "durations",
            "separators",
            "markdown_snippets",
            "markdown_ordered",
            "markdown_unordered",
            "markdown_italic_asterisk",
            "markdown_italic_underscore",
            "markdown_bold",
            "markdown_highlight",
            "markdown_quote",
            "markdown_url",
            "markdown_path",
            "markdown_header",
            "markdown_separator",
            "help_prompt",
            "explain_prompt",
            "new_prompt",
            "on_shift_middle_click",
            "on_ctrl_middle_click",
            "on_ctrl_shift_middle_click",
            "temporary",
            "clean",
            "profile",
            "console",
            "border_color",
            "border_size",
            "title",
            "icon",
            "auto_scroll_delay",
            "portrait",
            "open_on_log",
            "ordered_spacing",
            "unordered_spacing",
            "list_item_max_length",
            "response_file",
            "response_program",
            "use_program",
            "use_both",
            "taps_command",
            "theme",
            "bold_effects",
            "italic_effects",
            "highlight_effects",
            "uselink_effects",
            "quote_effects",
            "list_effects",
            "url_effects",
            "path_effects",
            "header_1_effects",
            "header_2_effects",
            "header_3_effects",
            "auto_unload",
            "tab_tooltip_length",
            "ascii_logs",
            "concat_logs",
            "mouse_scroll",
            "thinking_text",
            "logs_dir",
            "upload_password",
            "log_name_user",
            "log_name_ai",
            "upload_name_user",
            "upload_name_ai",
            "generic_names_logs",
            "generic_names_uploads",
            "signals",
            "config_dir",
            "data_dir",
            "border_effect",
            "border_effect_color",
            "argfile",
            "max_items",
        ]

        for n_item in normals:
            ap.get_value(n_item)

        no_strip = [
            "ordered_char",
            "unordered_char",
        ]

        for ns_item in no_strip:
            ap.get_value(ns_item, no_strip=True)

        # Read self.args_file and override arguments, based on the arguments defined in that json
        if self.argfile:
            self.load_argfile()

        if not sys.stdin.isatty():
            self.input = sys.stdin.read()
        else:
            string_arg = ap.string_arg()

            if string_arg:
                self.input = string_arg[:2000]

        if self.display_mode:
            self.compact = True
            self.compact_model = True
            self.compact_details_1 = True
            self.compact_details_2 = True
            self.compact_system = True
            self.compact_buttons = True
            self.compact_file = True
            self.compact_input = True
            self.show_tabs = False
            self.show_intro = False
            self.show_header = False

        self.parser = ap.parser

    def fill_functions(self) -> None:
        def add(num: int, func: str, shift: bool = False) -> None:
            if shift:
                if not getattr(self, f"shift_f{num}"):
                    setattr(self, f"shift_f{num}", self.prefix + func)
            elif not getattr(self, f"f{num}"):
                setattr(self, f"f{num}", self.prefix + func)

        add(1, "help")
        add(2, "findprev")
        add(3, "findnext")
        add(4, "close")
        add(5, "reset")
        add(6, "delete")
        add(7, "clear")
        add(8, "compact")
        add(9, "autoscroll")
        add(10, "logtext")
        add(11, "fullscreen")
        add(12, "list")

        # With Shift
        add(1, "commands", True)
        add(3, "findprev", True)
        add(5, "upload", True)
        add(9, "autoscrollup", True)
        add(10, "logjson", True)
        add(12, "last", True)

    def fill_gestures(self) -> None:
        if not self.gestures_left:
            self.gestures_left = f"{self.prefix}left"

        if not self.gestures_right:
            self.gestures_right = f"{self.prefix}right"

        if not self.gestures_up:
            self.gestures_up = f"{self.prefix}top"

        if not self.gestures_down:
            self.gestures_down = f"{self.prefix}bottom"

        if not self.taps_command:
            self.taps_command = f"{self.prefix}palette"

    def show_help(
        self, tab_id: str | None = None, filter_text: str | None = None
    ) -> None:
        from .display import display

        text = self.get_argtext(filter_text)
        display.print(text, tab_id=tab_id)
        display.format_text(tab_id=tab_id, mode="all")

    def get_argtext(self, filter_text: str | None = None) -> str:
        from .utils import utils

        sep = "\n\n---\n\n"
        text = ""
        filter_lower = ""

        if not filter_text:
            text = "# Arguments\n\n"
            text += "Here are all the available command line arguments:"
        else:
            filter_lower = filter_text.lower()

        for key in argspec.arguments:
            if key == "string_arg":
                continue

            arg = argspec.arguments[key]
            info = arg.get("help", "")

            if filter_text:
                if filter_lower not in key.lower():
                    if filter_lower not in info.lower():
                        continue

            text += sep
            name = key.replace("_", "-")
            text += f"### {name}"

            if info:
                text += "\n\n"
                text += info

            defvalue = argspec.defaults.get(key)

            if defvalue is not None:
                if isinstance(defvalue, str):
                    if defvalue == "":
                        defvalue = "[Empty string]"
                    elif defvalue.strip() == "":
                        spaces = defvalue.count(" ")
                        ds = utils.singular_or_plural(spaces, "space", "spaces")
                        defvalue = f"[{spaces} {ds}]"
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

        text += "\n"
        return text.lstrip()

    def make_argumentdoc(self, pathstr: str) -> None:
        from .utils import utils
        from .display import display
        from .files import files

        path = Path(pathstr)

        if (not path.parent.exists()) or (not path.parent.is_dir()):
            utils.msg(f"Invalid path: {pathstr}")
            return

        text = self.get_argtext()
        files.write(path, text)
        msg = f"Saved to {path}"
        display.print(msg)
        utils.msg(msg)

    def show_used_args(self) -> None:
        from .dialogs import Dialog

        text = []

        for attr_name, attr_value in vars(self).items():
            if attr_name not in argspec.defaults:
                continue

            if argspec.defaults[attr_name] != attr_value:
                value = attr_value

                if isinstance(attr_value, str):
                    if attr_value == "":
                        value = "[Empty string]"
                    else:
                        value = f'"{attr_value}"'

                text.append(f"{attr_name} = {value}")

        if not text:
            Dialog.show_message("No arguments were used")
            return

        Dialog.show_msgbox("Arguments", "\n".join(text))

    def set_command(self, cmd: str) -> None:
        from .utils import utils
        from .display import display

        if not cmd:
            display.print("Format: [name] [value]")
            return

        if " " in cmd:
            name, value = cmd.split(" ", 1)
        else:
            name = cmd
            value = ""

        value = utils.empty_string(value)
        arg = getattr(self, name)

        if arg is None:
            display.print("Invalid argument.")
            return

        vtype = arg.__class__
        new_value: Any = None

        if vtype is str:
            new_value = str(value)
        elif vtype is int:
            try:
                new_value = int(value)
            except BaseException:
                pass
        elif vtype is float:
            try:
                new_value = float(value)
            except BaseException:
                pass
        elif vtype is bool:
            if utils.is_bool_true(value):
                new_value = True
            elif utils.is_bool_false(value):
                new_value = False
        elif vtype is list:
            new_value = utils.get_list(value)

        if new_value is None:
            display.print("Invalid value.")
            return

        if arg == new_value:
            display.print("Already set to that.")
            return

        setattr(self, name, new_value)
        svalue = new_value

        if svalue == "":
            svalue = "[Empty]"

        display.print(f"Arg: `{name}` set to `{svalue}`", do_format=True)

    def load_argfile(self) -> None:
        from .files import files

        path = Path(self.argfile)

        if not path.exists():
            return

        obj = files.load(path)

        for key, value in obj.items():
            nkey = key.replace("-", "_")

            if hasattr(self, nkey):
                arg = getattr(self, nkey)
                vtype = arg.__class__

                if isinstance(value, vtype):
                    setattr(self, nkey, value)


args = Args()
