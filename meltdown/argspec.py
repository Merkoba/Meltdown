# Standard
from typing import Any

# Modules
from .app import app


class DuplicateArgumentError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate argument: {key}"

    def __str__(self) -> str:
        return self.message


class MissingInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Missing info for argument: {key}"

    def __str__(self) -> str:
        return self.message


class DuplicateInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate info for argument: {key}"

    def __str__(self) -> str:
        return self.message


class ArgSpec:
    def __init__(self) -> None:
        self.title = app.manifest["title"]
        self.version = app.manifest["version"]
        self.vinfo = f"{self.title} {self.version}"
        self.defaults: dict[str, Any] = {}
        self.arguments: dict[str, Any] = {}
        self.infos: list[str] = []
        self.markdown_choices = ["user", "ai", "both", "none"]
        self.list_choices = ["auto", "never", "always"]
        self.effects_info = 'bold, italic, color, underline, monospace. Separated by _, for example: "bold_color"'
        self.zero = "0 to disable"
        self.add_arguments()

    def add_argument(self, key: str, info: str, **kwargs: Any) -> None:
        if key in self.arguments:
            raise DuplicateArgumentError(key)

        if not info:
            raise MissingInfoError(key)

        if info in self.infos:
            raise DuplicateInfoError(key)

        self.arguments[key] = {
            "help": info,
            **kwargs,
        }

        self.infos.append(info)

    def add_arguments(self) -> None:
        self.add_argument(
            "version",
            action="version",
            info="Check the version of the program",
            version=self.vinfo,
        )

        self.add_argument(
            "no_color_italic",
            action="store_false",
            info="Don't apply color to italic text",
        )

        self.add_argument(
            "no_color_quotes",
            action="store_false",
            info="Don't apply color to quotes",
        )

        self.add_argument(
            "no_separate_logs",
            action="store_false",
            info="Don't use separator in logs",
        )

        self.add_argument(
            "no_separate_uploads",
            action="store_false",
            info="Don't use separator in uploads",
        )

        self.add_argument(
            "no_command_history",
            action="store_false",
            info="Don't include commands when cycling input history",
        )

        self.add_argument(
            "no_scroller_buttons",
            action="store_false",
            info="Don't show left and right scroller buttons",
        )

        self.add_argument(
            "no_clean_names",
            action="store_false",
            info="Don't change names when saving files",
        )

        self.add_argument(
            "no_files_in_logs",
            action="store_false",
            info="Don't show files in logs",
        )

        self.add_argument(
            "no_files_in_uploads",
            action="store_false",
            info="Don't show files in uploads",
        )

        self.add_argument(
            "no_quote_used_words",
            action="store_false",
            info="Don't add quotes to used words",
        )

        self.add_argument(
            "no_tabs_wheel",
            action="store_false",
            info="Don't enable mousewheel events on the tabs bar",
        )

        self.add_argument(
            "no_shorten_paths",
            action="store_false",
            info="Don't shorten paths like model file names",
        )

        self.add_argument(
            "no_display_wheel",
            action="store_false",
            info="Don't enable mousewheel events on the display",
        )

        self.add_argument(
            "no_tooltips",
            action="store_false",
            info="Don't show tooltips",
        )

        self.add_argument(
            "no_name_menu",
            action="store_false",
            info="Don't show a menu when clicking the user names",
        )

        self.add_argument(
            "no_word_menu",
            action="store_false",
            info="Don't show a menu when clicking special words",
        )

        self.add_argument(
            "no_url_menu",
            action="store_false",
            info="Don't show a menu when clicking URLs",
        )

        self.add_argument(
            "no_link_menu",
            action="store_false",
            info="Don't show a menu when clicking links",
        )

        self.add_argument(
            "no_path_menu",
            action="store_false",
            info="Don't show a menu when clicking paths",
        )

        self.add_argument(
            "no_list_menu",
            action="store_false",
            info="Don't show a menu when clicking list chars",
        )

        self.add_argument(
            "no_scrollbars",
            action="store_false",
            info="Don't show scrollbars",
        )

        self.add_argument(
            "no_colors",
            action="store_false",
            info="Don't show user colors",
        )

        self.add_argument(
            "no_avatars",
            action="store_false",
            info="Don't show user avatars",
        )

        self.add_argument(
            "no_system_colors",
            action="store_false",
            info="Disable system monitor colors",
        )

        self.add_argument(
            "no_cpu",
            action="store_false",
            info="Don't show the CPU monitor",
        )

        self.add_argument(
            "no_gpu",
            action="store_false",
            info="Don't show the GPU monitor",
        )

        self.add_argument(
            "no_gpu_ram",
            action="store_false",
            info="Don't show the GPU memory monitor",
        )

        self.add_argument(
            "no_gpu_temp",
            action="store_false",
            info="Don't show the GPU temperature monitor",
        )

        self.add_argument(
            "no_ram",
            action="store_false",
            info="Don't show the RAM monitor",
        )

        self.add_argument(
            "no_temp",
            action="store_false",
            info="Don't show the temperature monitor",
        )

        self.add_argument(
            "no_keyboard",
            action="store_false",
            info="Disable keyboard shortcuts",
        )

        self.add_argument(
            "no_taps",
            action="store_false",
            info="Disable double ctrl taps",
        )

        self.add_argument(
            "wrap_tabs",
            action="store_true",
            info="Enable tab wrapping",
        )

        self.add_argument(
            "no_wrap_menus",
            action="store_false",
            info="Disable menu wrapping",
        )

        self.add_argument(
            "no_tabs",
            action="store_false",
            info="Don't show the tab bar",
        )

        self.add_argument(
            "no_stream",
            action="store_false",
            info="Don't stream responses",
        )

        self.add_argument(
            "no_empty",
            action="store_false",
            info="Don't save empty conversations",
        )

        self.add_argument(
            "no_bottom",
            action="store_false",
            info="Don't show the Bottom button",
        )

        self.add_argument(
            "no_bottom_autohide",
            action="store_false",
            info="Don't autohide the Bottom button",
        )

        self.add_argument(
            "no_reorder",
            action="store_false",
            info="Disable tab reordering by dragging",
        )

        self.add_argument(
            "no_tab_highlight",
            action="store_false",
            info="Don't highlight the tab when streaming",
        )

        self.add_argument(
            "no_limit_tokens",
            action="store_false",
            info="Don't limit the tokens in the prompt",
        )

        self.add_argument(
            "no_commands",
            action="store_false",
            info="Disable commands when typing on the input",
        )

        self.add_argument(
            "no_intro",
            action="store_false",
            info="Don't print the intro in conversations",
        )

        self.add_argument(
            "no_header",
            action="store_false",
            info="Don't print the header in conversations",
        )

        self.add_argument(
            "no_disable_buttons",
            action="store_false",
            info="Don't disable buttons based on state",
        )

        self.add_argument(
            "no_clean_slate",
            action="store_false",
            info="Don't make a new tab when starting with an input",
        )

        self.add_argument(
            "no_model_icon",
            action="store_false",
            info="Don't show the model icon",
        )

        self.add_argument(
            "no_model_feedback",
            action="store_false",
            info="Don't show model feedback when loading",
        )

        self.add_argument(
            "no_log_feedback",
            action="store_false",
            info="Don't show feedback when saving logs",
        )

        self.add_argument(
            "no_emojis",
            action="store_false",
            info="Don't use emojis",
        )

        self.add_argument(
            "no_input_memory",
            action="store_false",
            info="Don't remember input words",
        )

        self.add_argument(
            "no_write_button",
            action="store_false",
            info="Don't show the textbox button",
        )

        self.add_argument(
            "no_wrap_textbox",
            action="store_false",
            info="Don't wrap the textbox text",
        )

        self.add_argument(
            "no_log_errors",
            action="store_false",
            info="Don't log error messages to a file",
        )

        self.add_argument(
            "no_time",
            action="store_false",
            info="Don't show the loading time at startup",
        )

        self.add_argument(
            "no_gestures",
            action="store_false",
            info="Don't enable mouse gestures",
        )

        self.add_argument(
            "no_increment_logs",
            action="store_false",
            info="Always use the file name, don't increment with numbers",
        )

        self.add_argument(
            "no_confirm_close",
            action="store_false",
            info="No need to confirm closing tabs",
        )

        self.add_argument(
            "no_confirm_clear",
            action="store_false",
            info="No need to confirm clearing conversations",
        )

        self.add_argument(
            "no_confirm_delete",
            action="store_false",
            info="No need to confirm deleting items",
        )

        self.add_argument(
            "no_auto_bottom",
            action="store_false",
            info="Don't scroll to the bottom when loading tabs",
        )

        self.add_argument(
            "no_fill_prompt",
            action="store_false",
            info="Don't fill the text input prompt in some cases when empty",
        )

        self.add_argument(
            "no_keywords",
            action="store_false",
            info="Don't do keyword replacements like ((now))",
        )

        self.add_argument(
            "no_auto_name",
            action="store_false",
            info="Don't auto-name tabs based on input",
        )

        self.add_argument(
            "no_tab_double_click",
            action="store_false",
            info="Open new tabs on double click",
        )

        self.add_argument(
            "no_labels",
            action="store_false",
            info="Don't show the labels",
        )

        self.add_argument(
            "no_syntax_highlighting",
            action="store_false",
            info="Don't apply syntax highlighting to snippets",
        )

        self.add_argument(
            "no_autoscroll",
            action="store_false",
            info="Don't show the auto-scroll button",
        )

        self.add_argument(
            "no_names_in_logs",
            action="store_false",
            info="Don't use the user names in logs",
        )

        self.add_argument(
            "no_color_list",
            action="store_false",
            info="Don't color the list characters",
        )

        self.add_argument(
            "concat_logs",
            action="store_true",
            info="Concat logs when saving multiple conversations",
        )

        self.add_argument(
            "ascii_logs",
            action="store_true",
            info="Escape non-ascii chars in json logs",
        )

        self.add_argument(
            "use_both",
            action="store_true",
            info="Use user and AI text when using items",
        )

        self.add_argument(
            "open_on_log",
            action="store_true",
            info="Open program automatically on log",
        )

        self.add_argument(
            "separators",
            action="store_true",
            info="Show separators between items",
        )

        self.add_argument(
            "console",
            action="store_true",
            info="Enable the interactive console",
        )

        self.add_argument(
            "temporary",
            action="store_true",
            info="Don't save the session",
        )

        self.add_argument(
            "clean",
            action="store_true",
            info="Don't load the session at startup",
        )

        self.add_argument(
            "avatars_in_logs",
            action="store_true",
            info="Show avatars in logs",
        )

        self.add_argument(
            "avatars_in_uploads",
            action="store_true",
            info="Show avatars in uploads",
        )

        self.add_argument(
            "durations",
            action="store_true",
            info="Show the amount of seconds that took to produce a response",
        )

        self.add_argument(
            "item_numbers",
            action="store_true",
            info="Add numbers to each message",
        )

        self.add_argument(
            "scroll_percentage",
            action="store_true",
            info="Show scroll percentage on the Go To Bottom button",
        )

        self.add_argument(
            "scroll_percentage_reverse",
            action="store_true",
            info="Show scroll percentage on the Go To Bottom button (reversed)",
        )

        self.add_argument(
            "display_mode",
            action="store_true",
            info="Only show the display. This is a preset that sets other arguments",
        )

        self.add_argument(
            "compact",
            action="store_true",
            info="Start in compact mode",
        )

        self.add_argument(
            "no_exit",
            action="store_true",
            info="Disable exit commands",
        )

        self.add_argument(
            "force",
            action="store_true",
            info="Allow opening multiple instances",
        )

        self.add_argument(
            "confirm_exit",
            action="store_true",
            info="Show confirm exit dialog",
        )

        self.add_argument(
            "compact_model",
            action="store_true",
            info="Hide the model frame in compact mode",
        )

        self.add_argument(
            "compact_system",
            action="store_true",
            info="Hide the system frame in compact mode",
        )

        self.add_argument(
            "compact_details_1",
            action="store_true",
            info="Hide the first details frame in compact mode",
        )

        self.add_argument(
            "compact_details_2",
            action="store_true",
            info="Hide the second details frame in compact mode",
        )

        self.add_argument(
            "compact_buttons",
            action="store_true",
            info="Hide the buttons frame in compact mode",
        )

        self.add_argument(
            "compact_input",
            action="store_true",
            info="Hide the input frame in compact mode",
        )

        self.add_argument(
            "maximize",
            action="store_true",
            info="Maximize the window on start",
        )

        self.add_argument(
            "tab_numbers",
            action="store_true",
            info="Show numbers in the tab bar",
        )

        self.add_argument(
            "alt_palette",
            action="store_true",
            info="Show commands instead of descriptions in the palette",
        )

        self.add_argument(
            "console_vi",
            action="store_true",
            info="Use vi mode in the console",
        )

        self.add_argument(
            "tabs_always",
            action="store_true",
            info="Always show the tab bar even if only one tab",
        )

        self.add_argument(
            "verbose",
            action="store_true",
            info="Make the model verbose when streaming",
        )

        self.add_argument(
            "quiet",
            action="store_true",
            info="Don't show some messages",
        )

        self.add_argument(
            "listen",
            action="store_true",
            info="Listen for changes to the stdin file",
        )

        self.add_argument(
            "sticky",
            action="store_true",
            info="Make the window always on top",
        )

        self.add_argument(
            "short_labels",
            action="store_true",
            info="Use the short version of labels",
        )

        self.add_argument(
            "short_buttons",
            action="store_true",
            info="Use the short version of buttons",
        )

        self.add_argument(
            "short_system",
            action="store_true",
            info="Use the short version of system monitors",
        )

        self.add_argument(
            "errors",
            action="store_true",
            info="Show error messages",
        )

        self.add_argument(
            "tab_tooltip_length",
            type=int,
            info="Max length for tab tooltips",
        )

        self.add_argument(
            "auto_unload",
            type=int,
            info=f"Auto-unload the model after this number of minutes after last use. {self.zero}",
        )

        self.add_argument(
            "border_size",
            type=int,
            info="The size of the border",
        )

        self.add_argument(
            "autoscroll_delay",
            type=int,
            info="The delay in ms for each auto scroll tick",
        )

        self.add_argument(
            "console_height",
            type=int,
            info="Reserve these number of rows for the console",
        )

        self.add_argument(
            "width",
            type=int,
            info="Width of the window",
        )

        self.add_argument(
            "height",
            type=int,
            info="Height of the window",
        )

        self.add_argument(
            "max_tabs",
            type=int,
            info=f"Max number of tabs to keep open. {self.zero}",
        )

        self.add_argument(
            "max_tab_width",
            type=int,
            info="Max number of characters to show in a tab name",
        )

        self.add_argument(
            "ordered_char",
            type=str,
            info="Character to use on ordered lists",
        )

        self.add_argument(
            "unordered_char",
            type=str,
            info="Character to use on unordered lists",
        )

        self.add_argument(
            "config",
            type=str,
            info="Name or path of a config file to use",
        )

        self.add_argument(
            "session",
            type=str,
            info="Name or path of a session file to use",
        )

        self.add_argument(
            "on_log",
            type=str,
            info="Command to execute when saving any log file",
        )

        self.add_argument(
            "on_log_text",
            type=str,
            info="Command to execute when saving a text log file",
        )

        self.add_argument(
            "on_log_json",
            type=str,
            info="Command to execute when saving a JSON log file",
        )

        self.add_argument(
            "on_log_markdown",
            type=str,
            info="Command to execute when saving a markdown log file",
        )

        self.add_argument(
            "on_copy",
            type=str,
            info="Command to execute when copying text",
        )

        self.add_argument(
            "file",
            type=str,
            info="Path to a file to use at startup",
        )

        self.add_argument(
            "image_prompt",
            type=str,
            info="Text to use when using an image without a text prompt",
        )

        self.add_argument(
            "f1",
            type=str,
            info="Command to assign to the F1 key",
        )

        self.add_argument(
            "f2",
            type=str,
            info="Command to assign to the F2 key",
        )

        self.add_argument(
            "f3",
            type=str,
            info="Command to assign to the F3 key",
        )

        self.add_argument(
            "f4",
            type=str,
            info="Command to assign to the F4 key",
        )

        self.add_argument(
            "f5",
            type=str,
            info="Command to assign to the F5 key",
        )

        self.add_argument(
            "f6",
            type=str,
            info="Command to assign to the F6 key",
        )

        self.add_argument(
            "f7",
            type=str,
            info="Command to assign to the F7 key",
        )

        self.add_argument(
            "f8",
            type=str,
            info="Command to assign to the F8 key",
        )

        self.add_argument(
            "f9",
            type=str,
            info="Command to assign to the F9 key",
        )

        self.add_argument(
            "f10",
            type=str,
            info="Command to assign to the F10 key",
        )

        self.add_argument(
            "f11",
            type=str,
            info="Command to assign to the F11 key",
        )

        self.add_argument(
            "f12",
            type=str,
            info="Command to assign to the F12 key",
        )

        self.add_argument(
            "shift_f1",
            type=str,
            info="Command to assign to the Shift + F1 key",
        )

        self.add_argument(
            "shift_f2",
            type=str,
            info="Command to assign to the Shift + F2 key",
        )

        self.add_argument(
            "shift_f3",
            type=str,
            info="Command to assign to the Shift + F3 key",
        )

        self.add_argument(
            "shift_f4",
            type=str,
            info="Command to assign to the Shift + F4 key",
        )

        self.add_argument(
            "shift_f5",
            type=str,
            info="Command to assign to the Shift + F5 key",
        )

        self.add_argument(
            "shift_f6",
            type=str,
            info="Command to assign to the Shift + F6 key",
        )

        self.add_argument(
            "shift_f7",
            type=str,
            info="Command to assign to the Shift + F7 key",
        )

        self.add_argument(
            "shift_f8",
            type=str,
            info="Command to assign to the Shift + F8 key",
        )

        self.add_argument(
            "shift_f9",
            type=str,
            info="Command to assign to the Shift + F9 key",
        )

        self.add_argument(
            "shift_f10",
            type=str,
            info="Command to assign to the Shift + F10 key",
        )

        self.add_argument(
            "shift_f11",
            type=str,
            info="Command to assign to the Shift + F11 key",
        )

        self.add_argument(
            "shift_f12",
            type=str,
            info="Command to assign to the Shift + F12 key",
        )

        self.add_argument(
            "input",
            type=str,
            info="Prompt the AI automatically with this input when starting the program",
        )

        self.add_argument(
            "uselink",
            type=str,
            action="append",
            info="Add a custom uselink to the intro",
        )

        self.add_argument(
            "alias",
            type=str,
            action="append",
            info='Define an alias to run commands. Format is "[name] [commands]"',
        )

        self.add_argument(
            "task",
            type=str,
            action="append",
            info='Define a task to run periodically. Format is "[seconds] [commands] [/now (optional)]',
        )

        self.add_argument(
            "custom_prompt",
            type=str,
            action="append",
            info='Custom prompts to use in the word menu. Format is "[word] = what is ((words))?"',
        )

        self.add_argument(
            "gestures_threshold",
            type=str,
            info="Threshold in pixels for mouse gestures",
        )

        self.add_argument(
            "gestures_left",
            type=str,
            info="Command to execute on left gesture",
        )

        self.add_argument(
            "gestures_right",
            type=str,
            info="Command to execute on right gesture",
        )

        self.add_argument(
            "gestures_up",
            type=str,
            info="Command to execute on up gesture",
        )

        self.add_argument(
            "gestures_down",
            type=str,
            info="Command to execute on down gesture",
        )

        self.add_argument(
            "scroll_pixels",
            type=int,
            info="How many pixels to scroll the display up or down",
        )

        self.add_argument(
            "auto_name_length",
            type=int,
            info="Max char length for auto tab names",
        )

        self.add_argument(
            "old_tabs_minutes",
            type=int,
            info="Consider a tab old after these minutes (using last modified date)",
        )

        self.add_argument(
            "max_list_items",
            type=int,
            info="Max number of items in context menu lists",
        )

        self.add_argument(
            "list_item_width",
            type=int,
            info="Max characters for the text of list items",
        )

        self.add_argument(
            "drag_threshold",
            type=int,
            info="The higher the number the less sensitive the tab dragging will be",
        )

        self.add_argument(
            "delay",
            type=float,
            info="Delay in seconds between each print when streaming",
        )

        self.add_argument(
            "command_prefix",
            type=str,
            info="Character used to prefix commands like /",
        )

        self.add_argument(
            "andchar",
            type=str,
            info="Character used to join commands like &",
        )

        self.add_argument(
            "system_threshold",
            type=int,
            info="Show system monitors as critical after this percentage threshold",
        )

        self.add_argument(
            "system_delay",
            type=int,
            info="Delay in seconds for system monitor updates",
        )

        self.add_argument(
            "system_suspend",
            type=int,
            info=f"Stop updating the system these minutes after the last stream. {self.zero}",
        )

        self.add_argument(
            "no_system_auto_hide",
            action="store_false",
            info="Auto-hide the system panel automatically when it gets suspended",
        )

        self.add_argument(
            "autorun",
            type=str,
            info="Run this command at startup",
        )

        self.add_argument(
            "help_prompt",
            type=str,
            info="What text to use for the help prompt",
        )

        self.add_argument(
            "explain_prompt",
            type=str,
            info="What text to use for the explain prompt",
        )

        self.add_argument(
            "new_prompt",
            type=str,
            info="What text to use for the new prompt",
        )

        self.add_argument(
            "input_memory_min",
            type=int,
            info="Minimum number of characters for input words to be remembered",
        )

        self.add_argument(
            "input_memory_max",
            type=int,
            info="Maximum number of characters for input words to be remembered",
        )

        self.add_argument(
            "input_memory_max_items",
            type=int,
            info="Maximum number of input memory items to remember",
        )

        self.add_argument(
            "list_item_max_length",
            type=int,
            info="Maximum length of the text of list items",
        )

        self.add_argument(
            "listen_file",
            type=str,
            info="Path to the file for the listener. By default it uses /tmp/mlt_[program].input",
        )

        self.add_argument(
            "commandoc",
            type=str,
            info="Make the commandoc and save it on this path",
        )

        self.add_argument(
            "argumentdoc",
            type=str,
            info="Make the argumentdoc and save it on this path",
        )

        self.add_argument(
            "keyboardoc",
            type=str,
            info="Make the keyboardoc and save it on this path",
        )

        self.add_argument(
            "after_stream",
            type=str,
            info="Execute this command after streaming a response",
        )

        self.add_argument(
            "markdown",
            type=str,
            choices=["user", "ai", "both", "none"],
            info="Define where to apply markdown formatting",
        )

        self.add_argument(
            "browser",
            type=str,
            info="Open links with this browser",
        )

        self.add_argument(
            "file_manager",
            type=str,
            info="Open files with this file manager",
        )

        self.add_argument(
            "font_diff",
            type=int,
            info="Add or subtract this from font sizes",
        )

        self.add_argument(
            "snippets_font",
            type=str,
            info="The font to use in snippets",
        )

        self.add_argument(
            "task_manager",
            type=str,
            info="Which task manager to use",
        )

        self.add_argument(
            "task_manager_gpu",
            type=str,
            info="Which task manager to use on the gpu monitors",
        )

        self.add_argument(
            "terminal",
            type=str,
            info="Which terminal to use when opening programs",
        )

        self.add_argument(
            "program_text",
            type=str,
            info="Use this program as default for the prog text command",
        )

        self.add_argument(
            "program_json",
            type=str,
            info="Use this program as default for the prog json command",
        )

        self.add_argument(
            "program_markdown",
            type=str,
            info="Use this program as default for the prog markdown command",
        )

        self.add_argument(
            "program",
            type=str,
            info="Use this program as default for the progtext and progjson commands",
        )

        self.add_argument(
            "user_color",
            type=str,
            info="The color of the text for the name of the user",
        )

        self.add_argument(
            "ai_color",
            type=str,
            info="The color of the text for the name of the AI",
        )

        self.add_argument(
            "emoji_unloaded",
            type=str,
            info="Emoji to show when a model is not loaded",
        )

        self.add_argument(
            "emoji_local",
            type=str,
            info="Emoji to show when a model is loaded locally",
        )

        self.add_argument(
            "emoji_remote",
            type=str,
            info="Emoji to show when a model is loaded remotely",
        )

        self.add_argument(
            "emoji_loading",
            type=str,
            info="Emoji to show when loading a model",
        )

        self.add_argument(
            "emoji_storage",
            type=str,
            info="Emoji to show when saving a log",
        )

        self.add_argument(
            "name_mode",
            type=str,
            choices=["random", "noun", "empty"],
            info="What mode to use when naming new tabs",
        )

        self.add_argument(
            "arrow_mode",
            type=str,
            choices=["history", "scroll"],
            info="What to do on up and down arrows",
        )

        self.add_argument(
            "summarize_prompt",
            type=str,
            info="The instruction to tell the AI to summarize a conversation",
        )

        self.add_argument(
            "markdown_snippets",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for snippets",
        )

        self.add_argument(
            "markdown_ordered",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for ordered lists",
        )

        self.add_argument(
            "markdown_unordered",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for unordered lists",
        )

        self.add_argument(
            "markdown_italic_asterisk",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for italic with one asterisk",
        )

        self.add_argument(
            "markdown_italic_underscore",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for italic with one underscore",
        )

        self.add_argument(
            "markdown_bold_asterisk",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for bold with asterisk",
        )

        self.add_argument(
            "markdown_bold_underscore",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for bold with underscores",
        )

        self.add_argument(
            "markdown_highlight",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for highlights",
        )

        self.add_argument(
            "markdown_quote",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for quotes",
        )

        self.add_argument(
            "markdown_url",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for URLs",
        )

        self.add_argument(
            "markdown_link",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for links like [Click here](https://example.com)",
        )

        self.add_argument(
            "markdown_path",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for paths",
        )

        self.add_argument(
            "markdown_header",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for headers",
        )

        self.add_argument(
            "markdown_separator",
            type=str,
            choices=self.markdown_choices,
            info="Markdown mode for separators",
        )

        self.add_argument(
            "markdown_join",
            type=str,
            info="Join multiple lines into a single line separated by a char",
        )

        self.add_argument(
            "markdown_clean",
            type=str,
            info="Collapse multiple empty lines into one",
        )

        self.add_argument(
            "on_shift_middle_click",
            type=str,
            info="Commands to run when shift middle clicking the display",
        )

        self.add_argument(
            "on_ctrl_middle_click",
            type=str,
            info="Commands to run when ctrl middle clicking the display",
        )

        self.add_argument(
            "on_ctrl_shift_middle_click",
            type=str,
            info="Commands to run when ctrl shift middle clicking the display",
        )

        self.add_argument(
            "profile",
            type=str,
            info="The profile to save the files",
        )

        self.add_argument(
            "border_color",
            type=str,
            info="The color of the border around the window",
        )

        self.add_argument(
            "title",
            type=str,
            info="Use a specific title for the window",
        )

        self.add_argument(
            "icon",
            type=str,
            info="Use a specific icon for the window. png or gif",
        )

        self.add_argument(
            "portrait",
            type=str,
            info="Path to an image for the portrait of the AI",
        )

        self.add_argument(
            "ordered_spacing",
            type=str,
            choices=self.list_choices,
            info="How to space between ordered list items",
        )

        self.add_argument(
            "unordered_spacing",
            type=str,
            choices=self.list_choices,
            info="How to space between unordered list items",
        )

        self.add_argument(
            "response_file",
            type=str,
            info="Save the latest response to this file",
        )

        self.add_argument(
            "response_program",
            type=str,
            info="Run a program with the latest response as the argument",
        )

        self.add_argument(
            "use_program",
            type=str,
            info="Run a program with the selected item's response as the argument",
        )

        self.add_argument(
            "taps_command",
            type=str,
            info="What command to run on double taps",
        )

        self.add_argument(
            "theme",
            type=str,
            choices=["dark", "light", "contrast"],
            info="What color theme to use",
        )

        self.add_argument(
            "bold_effects",
            type=str,
            info=f"Effects to apply to bold text. {self.effects_info}",
        )

        self.add_argument(
            "italic_effects",
            type=str,
            info=f"Effects to apply to italic text. {self.effects_info}",
        )

        self.add_argument(
            "uselink_effects",
            type=str,
            info=f"Effects to apply to uselinks. {self.effects_info}",
        )

        self.add_argument(
            "highlight_effects",
            type=str,
            info=f"Effects to apply to highlight text. {self.effects_info}",
        )

        self.add_argument(
            "quote_effects",
            type=str,
            info=f"Effects to apply to quote text. {self.effects_info}",
        )

        self.add_argument(
            "list_effects",
            type=str,
            info=f"Effects to apply to list characters on the left. {self.effects_info}",
        )

        self.add_argument(
            "url_effects",
            type=str,
            info=f"Effects to apply to URL text. {self.effects_info}",
        )

        self.add_argument(
            "link_effects",
            type=str,
            info=f"Effects to apply to links. {self.effects_info}",
        )

        self.add_argument(
            "path_effects",
            type=str,
            info=f"Effects to apply to path text. {self.effects_info}",
        )

        self.add_argument(
            "header_1_effects",
            type=str,
            info=f"Effects to apply to headers (Level 1). {self.effects_info}",
        )

        self.add_argument(
            "header_2_effects",
            type=str,
            info=f"Effects to apply to headers (Level 2). {self.effects_info}",
        )

        self.add_argument(
            "header_3_effects",
            type=str,
            info=f"Effects to apply to headers (Level 3). {self.effects_info}",
        )

        self.add_argument(
            "mouse_scroll",
            action="store_true",
            info="Scroll lists by simply focusing items with the mouse",
        )

        self.add_argument(
            "thinking_text",
            type=str,
            info="Text to show temporarily while the AI is thinking",
        )

        self.add_argument(
            "generating_text",
            type=str,
            info="Text to show temporarily while the AI is generating",
        )

        self.add_argument(
            "logs_dir",
            type=str,
            info="Use a different directory for the logs",
        )

        self.add_argument(
            "upload_password",
            type=str,
            info="The password to be able to edit an upload. Else it will use a random word",
        )

        self.add_argument(
            "log_name_user",
            type=str,
            info="Name to use for the user name in logs",
        )

        self.add_argument(
            "log_name_ai",
            type=str,
            info="Name to use for the AI name in logs",
        )

        self.add_argument(
            "upload_name_user",
            type=str,
            info="Name to use for the user name on uploads",
        )

        self.add_argument(
            "upload_name_ai",
            type=str,
            info="Name to use for the AI name on uploads",
        )

        self.add_argument(
            "generic_names_logs",
            action="store_true",
            info="Show generic names in logs, like User and AI",
        )

        self.add_argument(
            "generic_names_uploads",
            action="store_true",
            info="Show generic names in uploads, like User and AI",
        )

        self.add_argument(
            "signals",
            type=str,
            info="Path to a file that defines the available signals",
        )

        self.add_argument(
            "config_dir",
            type=str,
            info="Path for the config files",
        )

        self.add_argument(
            "data_dir",
            type=str,
            info="Path for the data files",
        )

        self.add_argument(
            "border_effect",
            action="store_true",
            info="Change the border color when streaming responses",
        )

        self.add_argument(
            "border_effect_color",
            type=str,
            info="The color of the border effect",
        )

        self.add_argument(
            "argfile",
            type=str,
            info="Path to a file that overrides the arguments",
        )

        self.add_argument(
            "max_items",
            type=int,
            info="Max number of items a conversation can have",
        )

        self.add_argument(
            "var",
            type=str,
            action="append",
            info='Add an input variable. Like "x = the world"',
        )

        self.add_argument(
            "variable_prefix",
            type=str,
            info="The prefix used for variables. For example $ in $name",
        )

        self.add_argument(
            "no_keep_empty_tab",
            action="store_false",
            info="Allow new tabs to be opened when the last one is empty",
        )

        self.add_argument(
            "join_lines_char",
            type=str,
            info="The symbol used to join the lines",
        )

        self.add_argument(
            "delimiter",
            type=str,
            info="The separator between the names and the message",
        )

        self.add_argument(
            "no_autoscroll_interrupt",
            action="store_false",
            info="Don't stop auto scroll on manual scrolling",
        )

        self.add_argument(
            "test",
            type=str,
            info="Run a specific test",
        )

        self.add_argument(
            "pin_icon",
            type=str,
            info="The icon to use on pinned tabs",
        )

        self.add_argument(
            "auto_sort_pins",
            action="store_true",
            info="Sort the pins to the start automatically",
        )

        self.add_argument(
            "image_size",
            type=str,
            info="The size to use for images. 1024x1024 might be the minimum",
        )

        self.add_argument(
            "image_prompt_max",
            type=int,
            info="Maximum text length for the image prompt",
        )

        self.add_argument(
            "image_model",
            type=str,
            info="The model used for image generation",
        )

        self.add_argument(
            "auto_program",
            action="store_true",
            info="Run a program automatically after a response",
        )

        self.add_argument(
            "symbol_continue",
            type=str,
            info="The symbol to use for the continue prompt",
        )

        self.add_argument(
            "symbol_explain",
            type=str,
            info="The symbol to use for the explain prompt",
        )

        self.add_argument(
            "symbol_expand",
            type=str,
            info="The symbol to use for the expand prompt",
        )

        self.add_argument(
            "symbol_continue_text",
            type=str,
            info="The text to use for the continue prompt",
        )

        self.add_argument(
            "symbol_explain_text",
            type=str,
            info="The text to use for the explain prompt",
        )

        self.add_argument(
            "symbol_expand_text",
            type=str,
            info="The text to use for the expand prompt",
        )

        self.add_argument(
            "symbol_fresh",
            type=int,
            info="When this is used as the first character of a prompt, the context will not be used on the prompt. This a shortcut to quickly do fresh prompts",
        )

        self.add_argument(
            "crop_user",
            type=int,
            info=f"Crop long user prompts to these characters. {self.zero}",
        )

        self.add_argument(
            "explain_sample",
            type=int,
            info="When using the 'Explain' button on snippets, how much of the snippet should be used in the prompt",
        )

        self.add_argument(
            "show_file",
            action="store_true",
            info="Show the file frame at startup",
        )

        self.add_argument(
            "input_icon",
            type=str,
            info="The icon on the left of the input field",
        )


argspec = ArgSpec()
