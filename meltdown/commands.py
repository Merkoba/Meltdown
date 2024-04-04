# Modules
from .app import app
from .config import config
from .dialogs import Dialog
from .menus import Menu
from .args import args
from .paths import paths
from . import utils
from . import timeutils
from . import filemanager

# Standard
import re
import json
from typing import Any, Dict, List, Optional
import tkinter as tk


class QueueItem:
    def __init__(self, cmd: str, argument: str) -> None:
        self.cmd = cmd
        self.argument = argument


class Queue:
    def __init__(self, items: List[QueueItem], wait: float = 0.0) -> None:
        self.items = items
        self.wait = wait


class Commands:
    def __init__(self) -> None:
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.prefix = "/"
        self.autocomplete_index = 0
        self.autocomplete_matches: List[str] = []
        self.autocomplete_match = ""
        self.autocomplete_word = ""
        self.autocomplete_pos = 0
        self.autocomplete_missing = ""
        self.loop_delay = 25
        self.queues: List[Queue] = []

        prefix = utils.escape_regex(self.prefix)
        self.cmd_pattern = fr"&(?= {prefix}\w+)"

    def setup(self) -> None:
        self.make_commands()
        self.make_aliases()
        self.check_commands()
        self.load_file()
        self.start_loop()

    def start_loop(self) -> None:
        def loop() -> None:
            for queue in self.queues:
                if queue.wait > 0.0:
                    queue.wait -= self.loop_delay

                    if queue.wait <= 0.0:
                        queue.wait = 0.0

                    continue

                if queue.items:
                    item = queue.items.pop(0)

                    if item.cmd == "sleep":
                        if item.argument and queue.items:
                            queue.wait = float(item.argument) * 1000.0
                    else:
                        if self.aliases.get(item.cmd):
                            self.exec(self.aliases[item.cmd], queue)
                        else:
                            self.try_to_run(item.cmd, item.argument)

                    if not queue.items:
                        self.queues.remove(queue)

            app.root.after(self.loop_delay, lambda: loop())

        loop()

    def make_commands(self) -> None:
        from .display import display
        from .model import model
        from .session import session
        from .logs import logs
        from .widgets import widgets
        from .inputcontrol import inputcontrol
        force = "Use 'force' to force"
        file_name = "You can provide the file name"

        self.commands = {
            "clear": {
                "aliases": ["clean", "cls"],
                "help": "Clear conversation",
                "extra": force,
                "action": lambda a=None: display.clear(force=a),
                "type": "force",
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
                "help": "Show the log menu",
                "action": lambda a=None: logs.menu(),
            },
            "logtext": {
                "aliases": [],
                "help": "Save conversation to a text file",
                "action": lambda a=None: logs.to_text(),
            },
            "logjson": {
                "aliases": [],
                "help": "Save conversation to a JSON file",
                "action": lambda a=None: logs.to_json(),
            },
            "logtextall": {
                "aliases": [],
                "help": "Save all conversations to text files",
                "action": lambda a=None: logs.to_text(True),
            },
            "logjsonall": {
                "aliases": [],
                "help": "Save all conversations to JSON files",
                "action": lambda a=None: logs.to_json(True),
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
            "system": {
                "aliases": ["sys", "monitor"],
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
                "help": "Close current tab",
                "extra": force,
                "action": lambda a=None: display.close_tab(force=a),
                "type": "force",
            },
            "closeothers": {
                "aliases": ["others"],
                "help": "Close other tabs",
                "extra": force,
                "action": lambda a=None: display.close_other_tabs(force=a),
                "type": "force",
            },
            "closeall": {
                "aliases": [],
                "help": "Close all tabs",
                "extra": force,
                "action": lambda a=None: display.close_all_tabs(force=a),
                "type": "force",
            },
            "closeold": {
                "aliases": ["old", "trim"],
                "help": "Close old tabs",
                "extra": force,
                "action": lambda a=None: display.close_old_tabs(force=a),
                "type": "force",
            },
            "closeleft": {
                "aliases": [],
                "help": "Close tabs to the left",
                "extra": force,
                "action": lambda a=None: display.close_tabs_left(force=a),
                "type": "force",
            },
            "closeright": {
                "aliases": [],
                "help": "Close tabs to the right",
                "extra": force,
                "action": lambda a=None: display.close_tabs_right(force=a),
                "type": "force",
            },
            "new": {
                "aliases": ["make", "maketab", "newtab"],
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
                "help": "Show the commands help",
                "action": lambda a=None: app.show_help("commands"),
            },
            "arguments": {
                "aliases": ["args"],
                "help": "Show the arguments help",
                "action": lambda a=None: app.show_help("arguments"),
            },
            "keyboard": {
                "aliases": ["shortcuts"],
                "help": "Show the keyboard help",
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
                "action": lambda a=None: display.find(query=a),
                "type": str,
            },
            "findall": {
                "aliases": ["searchall"],
                "help": "Find a text string among all tabs",
                "action": lambda a=None: display.find_all(a),
                "type": str,
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
                "help": "Show the session menu",
                "action": lambda a=None: session.menu(),
            },
            "reset": {
                "aliases": ["restart"],
                "help": "Reset the config",
                "extra": force,
                "action": lambda a=None: config.reset(force=a),
                "type": "force",
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
            "tab": {
                "aliases": ["num", "number", "tabnum", "tabnumber"],
                "help": "Go to a tab by its number or by its name",
                "action": lambda a=None: display.select_tab_by_string(a),
                "type": str,
                "arg_req": True,
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
                "help": "Show the context list",
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
                "aliases": ["open", "sessionload"],
                "help": "Load a session",
                "extra": file_name,
                "action": lambda a=None: session.load_state(name=a),
                "type": str,
            },
            "loadconfig": {
                "aliases": ["configload"],
                "help": "Load a session",
                "extra": file_name,
                "action": lambda a=None: config.load_state(name=a),
                "type": str,
            },
            "copy": {
                "aliases": [],
                "help": "Copy all the text",
                "action": lambda a=None: display.copy_output(),
            },
            "select": {
                "aliases": [],
                "help": "Select all text",
                "action": lambda a=None: display.select_output(),
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
            "rename": {
                "aliases": ["name"],
                "help": "Rename the tab",
                "action": lambda a=None: display.rename_tab(True),
            },
            "input": {
                "aliases": ["prompt", "ask"],
                "help": "Prompt the AI with this input",
                "action": lambda a=None: inputcontrol.submit(text=a),
                "type": str,
                "arg_req": True,
            },
            "write": {
                "aliases": ["fill"],
                "help": "Set the input without submitting",
                "action": lambda a=None: inputcontrol.set(text=a),
                "type": str,
                "arg_req": True,
            },
            "sleep": {
                "aliases": ["wait"],
                "help": "Wait X seconds before running the next command",
                "action": lambda a=None: None,
                "type": int,
                "arg_req": True,
            },
            "hide": {
                "aliases": [],
                "help": "Close dialogs and menus",
                "action": lambda a=None: self.hide_cmd(),
            },
            "printconfig": {
                "aliases": ["showconfig"],
                "help": "Print all the config settings",
                "action": lambda a=None: config.print_config(),
            },
            "bigger": {
                "aliases": ["biggerfont"],
                "help": "Increase the font size",
                "action": lambda a=None: display.increase_font(),
            },
            "smaller": {
                "aliases": ["smallerfont"],
                "help": "Decrease the font size",
                "action": lambda a=None: display.decrease_font(),
            },
            "resetfont": {
                "aliases": [],
                "help": "Reset the font size",
                "action": lambda a=None: display.reset_font(),
            },
        }

        for key in self.commands:
            self.commands[key]["date"] = 0.0

    def make_aliases(self) -> None:
        self.aliases = {}

        for alias in args.aliases:
            split = alias.split("=")
            key = split[0].strip()
            value = "=".join(split[1:]).strip()

            if not key or not value:
                continue

            self.aliases[key] = value

    def check_commands(self) -> None:
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

    def is_command(self, text: str) -> bool:
        if len(text) < 2:
            return False

        with_prefix = text.startswith(self.prefix)
        second_char = text[1:2]
        return with_prefix and second_char.isalpha()

    def exec(self, text: str, queue: Optional[Queue] = None) -> bool:
        text = text.strip()

        if not self.is_command(text):
            return False

        cmds = re.split(self.cmd_pattern, text)
        items = []

        for item in cmds:
            split = item.strip().split(" ")
            cmd = split[0][1:]
            argument = " ".join(split[1:])
            queue_item = QueueItem(cmd, argument)
            items.append(queue_item)

        if items:
            if queue:
                queue.items = items + queue.items
            else:
                queue = Queue(items)
                self.queues.append(queue)

        return True

    def run(self, cmd: str, argument: str = "") -> None:
        item = self.commands.get(cmd)

        if not item:
            return

        arg_req = item.get("arg_req")

        if (not argument) and arg_req:
            return

        argtype = item.get("type")
        new_argument: Any = None

        if argtype and argument:
            if argtype == "force":
                new_argument = True if argument.lower() == "force" else False
            else:
                new_argument = argtype(argument)

        item = self.commands[cmd]
        item["action"](new_argument)
        item["date"] = timeutils.now()
        self.save_commands()

    def save_commands(self) -> None:
        cmds = {}

        for key in self.commands:
            cmds[key] = {"date": self.commands[key]["date"]}

        filemanager.save(paths.commands, cmds)

    def try_to_run(self, cmd: str, argument: str) -> None:
        # Check normal
        for key, value in self.commands.items():
            if cmd == key or (value.get("aliases") and cmd in value["aliases"]):
                self.run(key, argument)
                return

        # Similarity on keys
        for key, value in self.commands.items():
            if utils.check_match(cmd, key):
                self.run(key, argument)
                return

        # Similarity on aliases
        for key, value in self.commands.items():
            aliases = value.get("aliases")

            if aliases:
                for alias in aliases:
                    if utils.check_match(cmd, alias):
                        self.run(key, argument)
                        return

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
            msg = data['help']

            if data.get("extra"):
                msg += f" ({data['extra']})"

            text.append(f"{self.prefix}{cmd} = {msg}")

        display.print("\n".join(text), tab_id=tab_id)

    def check_autocomplete(self) -> None:
        from .inputcontrol import inputcontrol
        text = inputcontrol.input.get()

        if not self.is_command(text):
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

            missing = match[len(self.clean(self.autocomplete_word)):]

            if self.autocomplete_match:
                inputcontrol.input.delete_text(self.autocomplete_pos, len(self.autocomplete_missing))

            inputcontrol.input.insert_text(missing, index=str(self.autocomplete_pos))
            self.autocomplete_index += 1
            self.autocomplete_match = match
            self.autocomplete_missing = missing

        if self.autocomplete_matches:
            check()

    def reset(self) -> None:
        self.autocomplete_matches = []
        self.autocomplete_match = ""
        self.autocomplete_missing = ""
        self.autocomplete_index = 0
        self.autocomplete_pos = 0

    def get_matches(self, text: str) -> None:
        from .inputcontrol import inputcontrol

        if not text:
            return

        self.reset()
        caret_pos = inputcontrol.input.index(tk.INSERT)
        text_to_caret = text[:caret_pos]
        last_space_pos = text_to_caret.rfind(" ")
        word = text_to_caret[last_space_pos + 1:caret_pos]

        if not word:
            return

        if not self.is_command(word):
            return

        self.autocomplete_word = word
        self.autocomplete_pos = inputcontrol.input.index(caret_pos)
        word = self.clean(word)

        for cmd, data in self.commands.items():
            if cmd.startswith(word):
                self.autocomplete_matches.append(cmd)

            for alias in data["aliases"]:
                if alias.startswith(word):
                    self.autocomplete_matches.append(alias)

        for cmd, value in self.aliases.items():
            if cmd.startswith(word):
                self.autocomplete_matches.append(cmd)

    def make_palette(self) -> None:
        self.palette = Menu()

        def add_item(key: str) -> None:
            cmd = self.commands[key]

            def command() -> None:
                if cmd.get("arg_req"):
                    Dialog.show_input("Argument", lambda a: self.run(key, a))
                else:
                    self.run(key)

            if args.alt_palette:
                text = key
                aliases = []
                tooltip = cmd["help"]
            else:
                text = cmd["help"]
                aliases = [key]
                tooltip = ", ".join(aliases)

            aliases.extend(cmd["aliases"])
            self.palette.add(text=text, command=command, tooltip=tooltip, aliases=aliases)

        keys = sorted(self.commands, key=lambda x: self.commands[x]["date"], reverse=True)

        for key in keys:
            add_item(key)

    def show_palette(self) -> None:
        from .widgets import widgets
        self.make_palette()
        self.palette.show(widget=widgets.main_menu_button)

    def clean(self, text: str) -> str:
        if text.startswith(self.prefix):
            return text[1:]

        return text

    def cmd(self, text: str) -> str:
        return self.prefix + text

    def hide_cmd(self) -> None:
        Dialog.hide_all()
        Menu.hide_all()

    def load_file(self) -> None:
        if (not paths.commands.exists()) or (not paths.commands.is_file()):
            return

        with open(paths.commands, "r") as file:
            try:
                cmds = json.load(file)
            except BaseException:
                cmds = {}

        for key in cmds:
            if key in self.commands:
                self.commands[key]["date"] = cmds[key].get("date", 0.0)


commands = Commands()
