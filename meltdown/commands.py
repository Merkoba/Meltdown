# Modules
from .app import app
from .config import config

# Standard
from typing import Any, Dict, List
from difflib import SequenceMatcher


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.prefix = "/"
        self.autocomplete_index = 0
        self.autocomplete_matches: List[str] = []

    def setup(self) -> None:
        from .display import display
        from .model import model
        from . import state
        from . import logs

        self.commands = {
            "clear": {"aliases": ["clean", "cls"], "help": "Clear conversation", "action": lambda: display.clear()},
            "config": {"aliases": ["configuration"], "help": "Show the current configuration", "action": lambda: config.show_config()},
            "exit": {"aliases": ["quit"], "help": "Exit the application", "action": lambda: app.exit()},
            "compact": {"aliases": [], "help": "Toggle compact mode", "action": lambda: app.toggle_compact()},
            "log": {"aliases": ["save"], "help": "Save conversation to a file", "action": lambda: logs.save_log()},
            "logs": {"aliases": [], "help": "Open the logs directory", "action": lambda: state.open_logs_dir()},
            "resize": {"aliases": ["restore"], "help": "Resize the window", "action": lambda: app.resize()},
            "stop": {"aliases": [], "help": "Stop the current stream", "action": lambda: model.stop_stream()},
            "sys": {"aliases": ["monitor", "system"], "help": "Open the system task manager", "action": lambda: app.open_task_manager()},
            "top": {"aliases": ["up"], "help": "Scroll to the top", "action": lambda: display.to_top()},
            "bottom": {"aliases": ["down"], "help": "Scroll to the bottom", "action": lambda: display.to_bottom()},
            "maximize": {"aliases": ["max"], "help": "Maximize the window", "action": lambda: app.toggle_maximize()},
            "unmaximize": {"aliases": ["unmax"], "help": "Unmaximize the window", "action": lambda: app.unmaximize()},
            "close": {"aliases": [], "help": "Close the current tab", "action": lambda: display.close_tab()},
            "closeall": {"aliases": [], "help": "Close all tabs", "action": lambda: display.close_all_tabs()},
            "closeold": {"aliases": ["old", "trim"], "help": "Close old tabs", "action": lambda: display.close_old_tabs()},
            "tab": {"aliases": ["new"], "help": "Make a new tab", "action": lambda: display.make_tab()},
            "theme": {"aliases": [], "help": "Change the color theme", "action": lambda: app.toggle_theme()},
            "about": {"aliases": [], "help": "Show the about window", "action": lambda: app.show_about()},
            "help": {"aliases": ["info", "commands", "cmds"], "help": "Show help information", "action": lambda: self.show_help()},
            "args": {"aliases": ["arguments"], "help": "Show the command line arguments", "action": lambda: self.show_arguments()},
        }

        cmds = []

        # Check for duplicate commands
        for key, value in self.commands.items():
            if key in cmds:
                raise ValueError(f"Command duplicate: {key}")
            else:
                cmds.append(key)

            for alias in value["aliases"]:
                if alias in cmds:
                    raise ValueError(f"Command duplicate: {key} {alias}")
                else:
                    cmds.append(alias)

    def command_format(self, text: str) -> bool:
        with_prefix = text.startswith(self.prefix)
        single_word = len(text.split()) == 1
        return (with_prefix and single_word)

    def check(self, text: str) -> bool:
        if not self.command_format(text):
            return False

        cmd = text[1:]

        # Check normal
        for key, value in self.commands.items():
            if cmd == key or (value.get("aliases") and cmd in value["aliases"]):
                value["action"]()
                return True

        # Similarity on keys
        for key, value in self.commands.items():
            if self.check_match(cmd, key):
                value["action"]()
                return True

        # Similarity on aliases
        for key, value in self.commands.items():
            aliases = value.get("aliases")

            if aliases:
                for alias in aliases:
                    if self.check_match(cmd, alias):
                        value["action"]()
                        return True

        return True

    def check_match(self, a: str, b: str) -> bool:
        if a == b:
            return True

        if self.similarity(a, b) >= 0.8:
            return True

        return False

    def show_help(self, tab_id: str = "") -> None:
        from .display import display
        display.print("Commands:", tab_id=tab_id)
        text = []

        for cmd, data in self.commands.items():
            text.append(f"{self.prefix}{cmd} = {data['help']}")

        display.print("\n".join(text), tab_id=tab_id)

    def show_arguments(self, tab_id: str = "") -> None:
        from .args import args
        from .display import display
        text = args.parser.format_help().strip()
        display.print("Arguments:", tab_id=tab_id)
        display.print(text, tab_id=tab_id)

    def check_autocomplete(self) -> None:
        from .inputcontrol import inputcontrol
        text = inputcontrol.input.get()

        if not self.command_format(text):
            return

        if not self.autocomplete_matches:
            self.get_matches(text)

        def check() -> None:
            if self.autocomplete_index >= len(self.autocomplete_matches):
                self.autocomplete_index = 0

            match = self.autocomplete_matches[self.autocomplete_index]
            input_text = inputcontrol.input.get()[1:]

            if match == input_text:
                if len(self.autocomplete_matches) == 1:
                    return

                self.autocomplete_index += 1
                check()
                return

            inputcontrol.input.set_text(self.prefix + match)
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

    def similarity(self, a: str, b: str) -> float:
        matcher = SequenceMatcher(None, a, b)
        return matcher.ratio()


commands = Commands()
