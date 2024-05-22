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
        self.show_tabs = True
        self.allow_empty = True
        self.bottom = True
        self.bottom_autohide = True
        self.reorder = True
        self.tab_numbers = False
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
        self.input = ""
        self.aliases: List[str] = []
        self.tasks: List[str] = []
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
        self.show_terminal = False
        self.terminal_height = 3
        self.terminal_vi = False
        self.input_memory = True
        self.input_memory_min = 4
        self.listener = False
        self.listener_delay = 0.5
        self.sticky = False
        self.commandoc = ""
        self.argumentdoc = ""
        self.keyboardoc = ""
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
        self.files_in_logs = True
        self.browser = ""
        self.file_manager = ""
        self.wrap_textbox = True
        self.font_diff = 0
        self.task_manager = "auto"
        self.task_manager_gpu = "auto"
        self.terminal = "auto"
        self.tabs_wheel = True
        self.display_wheel = True

        self.markdown = "both"
        self.markdown_snippets = "ai"
        self.markdown_italic = "ai"
        self.markdown_bold = "ai"
        self.markdown_highlights = "ai"
        self.markdown_quotes = "both"
        self.markdown_urls = "both"
        self.markdown_paths = "both"
        self.markdown_headers = "ai"
        self.markdown_separators = "ai"

        self.errors = False
        self.log_errors = True
        self.progtext = ""
        self.progjson = ""
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
        self.drag_and_drop = False
        self.use_keywords = True
        self.snippets_font = "monospace"
        self.show_prevnext = True
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
        self.file = ""
        self.image_prompt = "Describe this image"
        self.show_duration = False
        self.separator = ""
        self.help_prompt = "I need help!"
        self.explain_prompt = "What is ((words))?"
        self.new_prompt = "Tell me about ((words))"
        self.summarize_prompt = "Summarize this, without addressing me"
        self.custom_prompts: List[str] = []
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
        self.auto_scroll_delay = 500
        self.show_auto_scroll = True
        self.scroller_buttons = True
        self.portrait = ""
        self.command_history = True

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
            ("no_log_errors", "log_errors"),
            ("no_time", "time"),
            ("no_gestures", "gestures"),
            ("no_increment_logs", "increment_logs"),
            ("no_confirm_close", "confirm_close"),
            ("no_confirm_clear", "confirm_clear"),
            ("no_confirm_delete", "confirm_delete"),
            ("no_fill_prompt", "fill_prompt"),
            ("no_keywords", "use_keywords"),
            ("no_prevnext", "show_prevnext"),
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
            ("no_files_in_logs", "files_in_logs"),
            ("no_tabs_wheel", "tabs_wheel"),
            ("no_display_wheel", "display_wheel"),
            ("no_limit_tokens", "limit_tokens"),
            ("no_clean_names", "clean_names"),
            ("no_auto_scroll", "show_auto_scroll"),
            ("no_scroller_buttons", "scroller_buttons"),
            ("no_command_history", "command_history"),
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
            "alt_palette",
            "max_tab_width",
            "old_tabs_minutes",
            "max_list_items",
            "list_item_width",
            "system_threshold",
            "drag_threshold",
            "system_delay",
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
            "terminal_height",
            "terminal_vi",
            "verbose",
            "markdown",
            "listener",
            "listener_delay",
            "sticky",
            "commandoc",
            "argumentdoc",
            "keyboardoc",
            "after_stream",
            "tabs_always",
            "input_memory_min",
            "browser",
            "file_manager",
            "font_diff",
            "task_manager",
            "task_manager_gpu",
            "terminal",
            "on_log",
            "on_log_text",
            "on_log_json",
            "on_copy",
            "errors",
            "progtext",
            "progjson",
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
            "show_duration",
            "avatars_in_logs",
            "separator",
            "markdown_snippets",
            "markdown_italic",
            "markdown_bold",
            "markdown_highlights",
            "markdown_quotes",
            "markdown_urls",
            "markdown_paths",
            "markdown_headers",
            "markdown_separators",
            "help_prompt",
            "explain_prompt",
            "new_prompt",
            "on_shift_middle_click",
            "on_ctrl_middle_click",
            "on_ctrl_shift_middle_click",
            "temporary",
            "clean",
            "profile",
            "show_terminal",
            "drag_and_drop",
            "border_color",
            "border_size",
            "title",
            "icon",
            "auto_scroll_delay",
            "portrait",
        ]

        for n_item in normals:
            ap.get_value(n_item)

        if not sys.stdin.isatty():
            self.input = sys.stdin.read()
        else:
            string_arg = ap.string_arg()

            if string_arg:
                self.input = string_arg

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
        def add(num: int, func: str) -> None:
            if not getattr(self, f"f{num}"):
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

    def fill_gestures(self) -> None:
        if not self.gestures_left:
            self.gestures_left = f"{self.prefix}left"

        if not self.gestures_right:
            self.gestures_right = f"{self.prefix}right"

        if not self.gestures_up:
            self.gestures_up = f"{self.prefix}top"

        if not self.gestures_down:
            self.gestures_down = f"{self.prefix}bottom"

    def show_help(self, tab_id: Optional[str] = None) -> None:
        from .display import display

        text = self.get_argtext()
        display.print(text, tab_id=tab_id)
        display.format_text(tab_id=tab_id, mode="all")

    def get_argtext(self) -> str:
        sep = "\n\n---\n\n"

        text = "# Arguments\n\n"

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

        text += "\n"
        return text

    def make_argumentdoc(self, pathstr: str) -> None:
        from .utils import utils
        from .display import display
        from pathlib import Path

        path = Path(pathstr)

        if (not path.parent.exists()) or (not path.parent.is_dir()):
            utils.msg(f"Invalid path: {pathstr}")
            return

        text = self.get_argtext()

        with path.open("w", encoding="utf-8") as file:
            file.write(text)

        msg = f"Saved to {path}"
        display.print(msg)
        utils.msg(msg)

    def show_used_args(self) -> None:
        from .display import display

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
            return

        display.make_tab(name="Arguments", mode="ignore")
        display.print("\n".join(text))


args = Args()
