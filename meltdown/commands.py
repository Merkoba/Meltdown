# Modules
from .app import app
from .config import config
from .menus import Menu

# Standard
from typing import Any, Dict, List
from difflib import SequenceMatcher


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.prefix = "/"
        self.autocomplete_index = 0
        self.autocomplete_matches: List[str] = []
        self.palette = Menu()

    def setup(self) -> None:
        from .display import display
        from .model import model
        from .session import session
        from .logs import logs
        from .widgets import widgets

        self.commands = {
            "clear": {
                "aliases": ["clean", "cls"],
                "help": "Clear conversation",
                "action": lambda a=None: display.clear(),
            },
            "config": {
                "aliases": ["configuration"],
                "help": "Show the current configuration",
                "action": lambda a=None: config.show_config(),
            },
            "exit": {
                "aliases": ["quit"],
                "help": "Exit the application",
                "action": lambda a=None: app.exit(),
            },
            "compact": {
                "aliases": [],
                "help": "Toggle compact mode",
                "action": lambda a=None: app.toggle_compact(),
            },
            "log": {
                "aliases": ["logs"],
                "help": "Save conversation to a file",
                "action": lambda a=None: logs.menu(),
            },
            "logsdir": {
                "aliases": ["openlogs"],
                "help": "Open the logs directory",
                "action": lambda a=None: logs.open(),
            },
            "resize": {
                "aliases": ["restore"],
                "help": "Resize the window",
                "action": lambda a=None: app.resize(),
            },
            "stop": {
                "aliases": [],
                "help": "Stop the current stream",
                "action": lambda a=None: model.stop_stream(),
            },
            "sys": {
                "aliases": ["monitor", "system"],
                "help": "Open the system task manager",
                "action": lambda a=None: app.open_task_manager(),
            },
            "top": {
                "aliases": ["up"],
                "help": "Scroll to the top",
                "action": lambda a=None: display.to_top(),
            },
            "bottom": {
                "aliases": ["down"],
                "help": "Scroll to the bottom",
                "action": lambda a=None: display.to_bottom(),
            },
            "maximize": {
                "aliases": ["max"],
                "help": "Maximize the window",
                "action": lambda a=None: app.toggle_maximize(),
            },
            "close": {
                "aliases": [],
                "help": "Close the current tab",
                "action": lambda a=None: display.close_tab(),
            },
            "closeall": {
                "aliases": [],
                "help": "Close all tabs",
                "action": lambda a=None: display.close_all_tabs(),
            },
            "closeold": {
                "aliases": ["old", "trim"],
                "help": "Close old tabs",
                "action": lambda a=None: display.close_old_tabs(),
            },
            "tab": {
                "aliases": ["new"],
                "help": "Make a new tab",
                "action": lambda a=None: display.make_tab(),
            },
            "theme": {
                "aliases": [],
                "help": "Change the color theme",
                "action": lambda a=None: app.toggle_theme(),
            },
            "about": {
                "aliases": [],
                "help": "Show the about window",
                "action": lambda a=None: app.show_about(),
            },
            "help": {
                "aliases": ["info", "information"],
                "help": "Show help information",
                "action": lambda a=None: self.help_command(),
            },
            "commands": {
                "aliases": ["cmds"],
                "help": "Show the command line arguments",
                "action": lambda a=None: app.show_help("commands"),
            },
            "arguments": {
                "aliases": ["args"],
                "help": "Show the command line arguments",
                "action": lambda a=None: app.show_help("arguments"),
            },
            "keyboard": {
                "aliases": ["shortcuts"],
                "help": "Show the tab list to pick a tab",
                "action": lambda a=None: app.show_help("keyboard"),
            },
            "list": {
                "aliases": ["tabs", "tablist"],
                "help": "Show the tab list to pick a tab",
                "action": lambda a=None: display.show_tab_list(),
            },
            "find": {
                "aliases": ["search"],
                "help": "Find a text string",
                "action": lambda a=None: display.find(),
            },
            "findall": {
                "aliases": ["searchall"],
                "help": "Find a text string among all tabs",
                "action": lambda a=None: display.find_all(a),
            },
            "first": {
                "aliases": [],
                "help": "Go to the first tab",
                "action": lambda a=None: display.select_first_tab(),
            },
            "last": {
                "aliases": [],
                "help": "Go to the last tab",
                "action": lambda a=None: display.select_last_tab(),
            },
            "config": {
                "aliases": ["configuration"],
                "help": "Show the config menu",
                "action": lambda a=None: config.menu(),
            },
            "session": {
                "aliases": [],
                "help": "Show the config menu",
                "action": lambda a=None: session.menu(),
            },
            "reset": {
                "aliases": ["restart"],
                "help": "Reset the config",
                "action": lambda a=None: config.reset(),
            },
            "viewtext": {
                "aliases": ["text"],
                "help": "View raw text",
                "action": lambda a=None: display.view_text(),
            },
            "viewjson": {
                "aliases": ["json"],
                "help": "View raw JSON",
                "action": lambda a=None: display.view_json(),
            },
            "move": {
                "aliases": [],
                "help": "Move tab to start or end",
                "action": lambda a=None: display.move_tab(True),
            },
            "num": {
                "aliases": ["number", "tabnum", "tabnumber"],
                "help": "Go to a tab by its number",
                "action": lambda a=None: display.select_tab_by_number(a),
                "type": int,
            },
            "fullscreen": {
                "aliases": ["full"],
                "help": "Toggle fullscreen",
                "action": lambda a=None: app.toggle_fullscreen(),
            },
            "next": {
                "aliases": ["findnext", "match"],
                "help": "Find next text match",
                "action": lambda a=None: display.find_next(),
            },
            "scrollup": {
                "aliases": ["moveup"],
                "help": "Scroll up",
                "action": lambda a=None: display.scroll_up(),
            },
            "scrolldown": {
                "aliases": ["movedown"],
                "help": "Scroll down",
                "action": lambda a=None: display.scroll_down(),
            },
            "load": {
                "aliases": ["loadmodel"],
                "help": "Load the model",
                "action": lambda a=None: model.load(),
            },
            "unload": {
                "aliases": ["unloadmodel"],
                "help": "Unload the model",
                "action": lambda a=None: model.unload(True),
            },
            "context": {
                "aliases": ["widgetlist", "rightclick"],
                "help": "Show context list of a widget",
                "action": lambda a=None: widgets.show_context(),
            },
            "left": {
                "aliases": ["tableft"],
                "help": "Go to the tab on the left",
                "action": lambda a=None: display.tab_left(),
            },
            "right": {
                "aliases": ["tabright"],
                "help": "Go to the tab on the right",
                "action": lambda a=None: display.tab_right(),
            },
            "menu": {
                "aliases": ["mainmenu"],
                "help": "Show the main menu",
                "action": lambda a=None: widgets.show_main_menu(),
            },
            "savesession": {
                "aliases": [],
                "help": "Save the current session",
                "action": lambda a=None: session.save_state(),
            },
            "loadsession": {
                "aliases": ["open"],
                "help": "Load a session",
                "action": lambda a=None: session.load_state(),
            },
            "copy": {
                "aliases": [],
                "help": "Copy all the text",
                "action": lambda a=None: display.copy_output(),
            },
            "browse": {
                "aliases": [],
                "help": "Browse the models",
                "action": lambda a=None: model.browse_models(),
            },
            "palette": {
                "aliases": [],
                "help": "Show the command palette",
                "action": lambda a=None: self.show_palette(),
            },
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
        if len(text) < 2:
            return False

        with_prefix = text.startswith(self.prefix)
        second_char = text[1:2]
        return with_prefix and second_char.isalpha()

    def run(self, key: str, argument: str) -> None:
        item = self.commands[key]
        action = item["action"]
        argtype = item.get("type")

        if argtype:
            argument = argtype(argument)

        action(argument)

    def check(self, text: str, direct: bool = False) -> bool:
        text = text.strip()

        if not direct:
            if not self.command_format(text):
                return False

        split = text.split(" ")
        cmd = split[0]

        if not direct:
            cmd = cmd[1:]

        argument = " ".join(split[1:])

        # Check normal
        for key, value in self.commands.items():
            if cmd == key or (value.get("aliases") and cmd in value["aliases"]):
                self.run(key, argument)
                return True

        # Similarity on keys
        for key, value in self.commands.items():
            if self.check_match(cmd, key):
                self.run(key, argument)
                return True

        # Similarity on aliases
        for key, value in self.commands.items():
            aliases = value.get("aliases")

            if aliases:
                for alias in aliases:
                    if self.check_match(cmd, alias):
                        self.run(key, argument)
                        return True

        return True

    def check_match(self, a: str, b: str) -> bool:
        if a == b:
            return True

        if self.similarity(a, b) >= 0.8:
            return True

        return False

    def help_command(self) -> None:
        from .display import display

        items = []
        items.append("Use /commands to see commands")
        items.append("Use /arguments to see command line arguments")
        items.append("Use /keyboard to see keyboard shortcuts")

        text = "\n".join(items)
        display.print(text)

    def show_help(self, tab_id: str = "") -> None:
        from .display import display
        display.print("Commands:", tab_id=tab_id)
        text = []

        for cmd, data in self.commands.items():
            text.append(f"{self.prefix}{cmd} = {data['help']}")

        display.print("\n".join(text), tab_id=tab_id)

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

    def show_palette(self) -> None:
        from .widgets import widgets
        self.palette.clear()

        def add_item(key: str) -> None:
            cmd = self.commands[key]

            def command() -> None:
                cmd["action"]()

            help = cmd["help"]
            self.palette.add(text=key, command=command, tooltip=help)

        for key in self.commands:
            add_item(key)

        self.palette.show(widget=widgets.main_menu_button)


commands = Commands()
