# Modules
from .app import app
from .config import config

# Standard
from typing import Any, Dict, List


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.prefix = "/"
        self.autocomplete_index = 0
        self.autocomplete_matches: List[str] = []

    def setup(self) -> None:
        from .widgets import widgets
        from .model import model
        from . import state

        self.commands = {
            "clear": {"aliases": ["clean", "cls"], "help": "Clear conversation", "action": lambda: widgets.display.clear_output()},
            "config": {"aliases": ["configuration"], "help": "Show the current configuration", "action": lambda: config.show_config()},
            "exit": {"aliases": ["quit"], "help": "Exit the application", "action": lambda: app.exit()},
            "compact": {"aliases": [], "help": "Toggle compact mode", "action": lambda: app.toggle_compact()},
            "log": {"aliases": ["save"], "help": "Save conversation to a file", "action": lambda: state.save_log()},
            "logs": {"aliases": [], "help": "Open the logs directory", "action": lambda: state.open_logs_dir()},
            "resize": {"aliases": ["restore"], "help": "Resize the window", "action": lambda: app.resize()},
            "stop": {"aliases": [], "help": "Stop the current stream", "action": lambda: model.stop_stream()},
            "sys": {"aliases": ["monitor", "system"], "help": "Open the system task manager", "action": lambda: app.open_task_manager()},
            "top": {"aliases": ["up"], "help": "Scroll to the top", "action": lambda: widgets.display.to_top()},
            "bottom": {"aliases": ["down"], "help": "Scroll to the bottom", "action": lambda: widgets.display.to_bottom()},
            "maximize": {"aliases": ["max"], "help": "Maximize the window", "action": lambda: app.toggle_maximize()},
            "unmaximize": {"aliases": ["unmax"], "help": "Unmaximize the window", "action": lambda: app.unmaximize()},
            "close": {"aliases": [], "help": "Close the current tab", "action": lambda: widgets.display.close_tab()},
            "closeall": {"aliases": [], "help": "Close all tabs", "action": lambda: widgets.display.close_all_tabs()},
            "closeold": {"aliases": ["old", "trim"], "help": "Close old tabs", "action": lambda: widgets.display.close_old_tabs()},
            "tab": {"aliases": ["new"], "help": "Make a new tab", "action": lambda: widgets.display.make_tab()},
            "help": {"aliases": ["info"], "help": "Show help information", "action": lambda: self.show_help()},
            "args": {"aliases": ["arguments"], "help": "Show the command line arguments", "action": lambda: self.show_arguments()},
        }

        aliases = []

        # Check for duplicate aliases
        for cmd, data in self.commands.items():
            if data.get("aliases"):
                for alias in data["aliases"]:
                    if alias in aliases:
                        raise ValueError(f"Command alias '{alias}' is already in use")
                    aliases.append(alias)

    def command_format(self, text: str) -> bool:
        with_prefix = text.startswith(self.prefix)
        single_word = len(text.split()) == 1
        return (with_prefix and single_word)

    def check(self, text: str) -> bool:
        if not self.command_format(text):
            return False

        cmd = text[1:]

        for key, value in self.commands.items():
            if cmd == key or (value.get("aliases") and cmd in value["aliases"]):
                value["action"]()
                return True

        return True

    def show_help(self) -> None:
        from .widgets import widgets
        widgets.display.print("\nCommands:")

        for cmd, data in self.commands.items():
            widgets.display.print(f"{cmd}: {data['help']}")

    def show_arguments(self) -> None:
        from .args import args
        from .widgets import widgets
        text = args.parser.format_help().strip()
        widgets.display.print("\nCommand Line Arguments:\n")
        widgets.display.print(text)

    def check_autocomplete(self) -> None:
        from .widgets import widgets
        text = widgets.input.get()

        if not self.command_format(text):
            return

        if not self.autocomplete_matches:
            self.get_matches(text)

        def check() -> None:
            if self.autocomplete_index >= len(self.autocomplete_matches):
                self.autocomplete_index = 0

            match = self.autocomplete_matches[self.autocomplete_index]
            input_text = widgets.input.get()[1:]

            if match == input_text:
                if len(self.autocomplete_matches) == 1:
                    return

                self.autocomplete_index += 1
                check()
                return

            widgets.input.set_text(self.prefix + match)
            self.autocomplete_index += 1

        if self.autocomplete_matches:
            check()

    def reset(self) -> None:
        self.autocomplete_matches = []
        self.autocomplete_index = 0

    def get_matches(self, text: str) -> None:
        self.reset()

        for cmd, data in self.commands.items():
            if cmd.startswith(text[1:]):
                self.autocomplete_matches.append(cmd)

            for alias in data["aliases"]:
                if alias.startswith(text[1:]):
                    self.autocomplete_matches.append(alias)


commands = Commands()
