# Modules
from .app import app
from .config import config

# Standard
from typing import Any, Dict


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.prefix = "/"

    def setup(self) -> None:
        from .widgets import widgets
        from .model import model
        from . import state

        self.commands = {
            "clear": {"help": "Clear the output", "action": lambda: widgets.display.clear_output()},
            "config": {"help": "Show the current configuration", "action": lambda: config.show_config()},
            "exit": {"aliases": ["quit"], "help": "Exit the application", "action": lambda: app.exit()},
            "compact": {"help": "Toggle compact mode", "action": lambda: app.toggle_compact()},
            "log": {"help": "Save the current log", "action": lambda: state.save_log()},
            "logs": {"help": "Open the logs directory", "action": lambda: state.open_logs_dir()},
            "resize": {"help": "Resize the window", "action": lambda: app.resize()},
            "stop": {"help": "Stop the current stream", "action": lambda: model.stop_stream()},
            "sys": {"help": "Open the system task manager", "action": lambda: app.open_task_manager()},
            "top": {"help": "Scroll to the top", "action": lambda: widgets.display.to_top()},
            "bottom": {"help": "Scroll to the bottom", "action": lambda: widgets.display.to_bottom()},
            "maximize": {"aliases": ["max"], "help": "Maximize the window", "action": lambda: app.toggle_maximize()},
            "unmaximize": {"aliases": ["unmax"], "help": "Unmaximize the window", "action": lambda: app.unmaximize()},
            "close": {"help": "Close the current tab", "action": lambda: widgets.display.close_tab()},
            "closeall": {"help": "Close all tabs", "action": lambda: widgets.display.close_all_tabs()},
            "closeold": {"aliases": ["old", "trim"], "help": "Close old tabs", "action": lambda: widgets.display.close_old_tabs()},
            "tab": {"aliases": ["new"], "help": "Make a new tab", "action": lambda: widgets.display.make_tab()},
            "help": {"help": "Show help information", "action": lambda: self.show_help()},
        }

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

    def check_autocomplete(self) -> None:
        from .widgets import widgets
        from .model import model
        from . import state

        text = widgets.input.get()

        if not self.command_format(text):
            return

        for cmd in self.commands:
            if cmd.startswith(text[1:]):
                widgets.input.set_text(f"{self.prefix}{cmd} ")
                return


commands = Commands()
