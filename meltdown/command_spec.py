# Standard
from typing import Any, List, Callable, Dict

# Modules
from .app import app
from .config import config
from .args import args
from .display import display
from .model import model
from .session import session
from .logs import logs
from .widgets import widgets
from .inputcontrol import inputcontrol
from .commands import commands
from . import summarize
from . import menumanager
from . import findmanager


class CommandSpec:
    def __init__(self) -> None:
        self.force = "Use 'force' to force"
        self.file_name = "You can provide the file name"
        self.sortfilter = "Use 'sort' or a word to filter"
        self.infos: List[str] = []
        self.commands: Dict[str, Any] = {}

        self.add_commands()

    def add_cmd(
        self, key: str, info: str, action: Callable[..., Any], **kwargs: Any
    ) -> None:
        if key in self.commands:
            raise Exception(f"Duplicate command: {key}")

        if not info:
            raise Exception(f"Missing info for command: {key}")

        if info in self.infos:
            raise Exception(f"Duplicate info for command: {key}")

        self.commands[key] = {
            "info": info,
            "action": action,
            **kwargs,
        }

        self.infos.append(info)

    def add_commands(self) -> None:
        self.add_cmd(
            "clear",
            "Clear the conversation",
            lambda a=None: display.clear(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "exit",
            "Exit the application. Optional seconds delay",
            lambda a=None: app.exit(a),
            type=int,
        )

        self.add_cmd(
            "cancelexit",
            "Cancel the exit if you had set a delay",
            lambda a=None: app.cancel_exit(True),
        )

        self.add_cmd(
            "compact", "Toggle compact mode", lambda a=None: app.toggle_compact()
        )

        self.add_cmd("log", "Show the log menu", lambda a=None: logs.menu())

        self.add_cmd(
            "logtext",
            "Save conversation to a text file",
            lambda a=None: logs.to_text(name=a),
            type=str,
        )

        self.add_cmd(
            "logjson",
            "Save conversation to a JSON file",
            lambda a=None: logs.to_json(name=a),
            type=str,
        )

        self.add_cmd(
            "logtextall",
            "Save all conversations to text files",
            lambda a=None: logs.to_text(True),
        )

        self.add_cmd(
            "logjsonall",
            "Save all conversations to JSON files",
            lambda a=None: logs.to_json(True),
        )

        self.add_cmd(
            "openlog",
            "Open a log file by name",
            lambda a=None: logs.open(a),
            type=str,
        )

        self.add_cmd("resize", "Resize the window", lambda a=None: app.resize())

        self.add_cmd(
            "stop", "Stop the current stream", lambda a=None: model.stop_stream()
        )

        self.add_cmd(
            "taskmanager",
            "Open the system task manager",
            lambda a=None: app.open_task_manager(),
        )

        self.add_cmd("top", "Scroll to the top", lambda a=None: display.to_top())

        self.add_cmd(
            "bottom", "Scroll to the bottom", lambda a=None: display.to_bottom()
        )

        self.add_cmd(
            "maximize", "Maximize the window", lambda a=None: app.toggle_maximize()
        )

        self.add_cmd(
            "close",
            "Close current tab",
            lambda a=None: display.close_tab(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeothers",
            "Close other tabs",
            lambda a=None: display.close_other_tabs(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeall",
            "Close all tabs",
            lambda a=None: display.close_all_tabs(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeold",
            "Close old tabs",
            lambda a=None: display.close_old_tabs(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeleft",
            "Close tabs to the left",
            lambda a=None: display.close_tabs_left(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeright",
            "Close tabs to the right",
            lambda a=None: display.close_tabs_right(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd("new", "Make a new tab", lambda a=None: display.make_tab())

        self.add_cmd("about", "Show the about window", lambda a=None: app.show_about())

        self.add_cmd(
            "help", "Show help information", lambda a=None: commands.help_command()
        )

        self.add_cmd(
            "commands",
            "Show the commands help",
            lambda a=None: app.show_help("commands", mode=a),
            extra=self.sortfilter,
            type=str,
        )

        self.add_cmd(
            "arguments",
            "Show the arguments help",
            lambda a=None: app.show_help("arguments", mode=a),
            extra=self.sortfilter,
            type=str,
        )

        self.add_cmd(
            "keyboard",
            "Show the keyboard help",
            lambda a=None: app.show_help("keyboard", mode=a),
            extra=self.sortfilter,
            type=str,
        )

        self.add_cmd(
            "list",
            "Show the tab list to pick a tab",
            lambda a=None: display.show_tab_list(),
        )

        self.add_cmd(
            "find",
            "Find a text string",
            lambda a=None: findmanager.find(query=a),
            type=str,
        )

        self.add_cmd(
            "findall",
            "Find a text string among all tabs",
            lambda a=None: findmanager.find_all(a),
            type=str,
        )

        self.add_cmd(
            "first",
            "Go to the first tab",
            lambda a=None: display.select_first_tab(),
        )

        self.add_cmd(
            "last", "Go to the last tab", lambda a=None: display.select_last_tab()
        )

        self.add_cmd(
            "config",
            "Config menu or view, set, reset a config",
            lambda a=None: config.command(a),
            type=str,
        )

        self.add_cmd("session", "Show the session menu", lambda a=None: session.menu())

        self.add_cmd(
            "reset",
            "Reset all configs",
            lambda a=None: config.reset(force=a),
            type="force",
        )

        self.add_cmd("viewtext", "View raw text", lambda a=None: display.view_text())

        self.add_cmd("viewjson", "View raw JSON", lambda a=None: display.view_json())

        self.add_cmd(
            "move",
            "Move tab to the start or end",
            lambda a=None: display.move_tab(),
        )

        self.add_cmd(
            "tab",
            "Go to a tab by its number or by its name",
            lambda a=None: display.select_tab_by_string(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "fullscreen",
            "Toggle fullscreen",
            lambda a=None: app.toggle_fullscreen(),
        )

        self.add_cmd(
            "next", "Find next text match", lambda a=None: findmanager.find_next()
        )

        self.add_cmd("scrollup", "Scroll up", lambda a=None: display.scroll_up())

        self.add_cmd("scrolldown", "Scroll down", lambda a=None: display.scroll_down())

        self.add_cmd("load", "Load the model", lambda a=None: model.load())

        self.add_cmd("unload", "Unload the model", lambda a=None: model.unload(True))

        self.add_cmd(
            "context",
            "Show the context list",
            lambda a=None: widgets.show_context(),
        )

        self.add_cmd(
            "left", "Go to the tab on the left", lambda a=None: display.tab_left()
        )

        self.add_cmd(
            "right",
            "Go to the tab on the right",
            lambda a=None: display.tab_right(),
        )

        self.add_cmd(
            "moveleft",
            "Move the tab to the left",
            lambda a=None: display.move_tab_left(),
        )

        self.add_cmd(
            "moveright",
            "Move the tab to the right",
            lambda a=None: display.move_tab_right(),
        )

        self.add_cmd(
            "movefirst",
            "Move the tab to the start",
            lambda a=None: display.move_tab_to_start(),
        )

        self.add_cmd(
            "movelast",
            "Move the tab to the end",
            lambda a=None: display.move_tab_to_end(),
        )

        self.add_cmd(
            "main", "Show the main menu", lambda a=None: widgets.show_main_menu()
        )

        self.add_cmd(
            "savesession",
            "Save the current session",
            lambda a=None: session.save_state(name=a),
            type=str,
        )

        self.add_cmd(
            "loadsession",
            "Load a session",
            lambda a=None: session.load_state(name=a),
            extra=self.file_name,
            type=str,
        )

        self.add_cmd(
            "saveconfig",
            "Save the current config",
            lambda a=None: config.save_state(name=a),
            type=str,
        )

        self.add_cmd(
            "loadconfig",
            "Load a config",
            lambda a=None: config.load_state(name=a),
            extra=self.file_name,
            type=str,
        )

        self.add_cmd("copy", "Copy all the text", lambda a=None: display.copy_output())

        self.add_cmd(
            "select", "Select all text", lambda a=None: display.select_output()
        )

        self.add_cmd(
            "deselect",
            "Deselect all text",
            lambda a=None: display.deselect_output(),
        )

        self.add_cmd(
            "model", "Show the model menu", lambda a=None: widgets.show_model_menu()
        )

        self.add_cmd(
            "recent",
            "Show the recent models",
            lambda a=None: widgets.show_recent_models(),
        )

        self.add_cmd(
            "browse", "Browse the models", lambda a=None: widgets.browse_models()
        )

        self.add_cmd("file", "Browse for a file", lambda a=None: widgets.browse_file())

        self.add_cmd(
            "palette",
            "Show the command palette",
            lambda a=None: commands.show_palette(),
        )

        self.add_cmd(
            "rename",
            "Rename the tab",
            lambda a=None: display.rename_tab(name=a),
            type=str,
        )

        self.add_cmd(
            "input",
            "Prompt the AI with this input",
            lambda a=None: inputcontrol.input_command(a),
            type=str,
        )

        self.add_cmd(
            "write",
            "Write the input prompt",
            lambda a=None: inputcontrol.set(text=a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "sleep",
            "Wait x seconds before the next command",
            lambda a=None: None,
            type=int,
            arg_req=True,
            skip_palette=True,
        )

        self.add_cmd("hide", "Close dialogs and menus", lambda a=None: app.hide_all())

        self.add_cmd(
            "printconfig",
            "Print all the config settings",
            lambda a=None: config.print_config(),
        )

        self.add_cmd(
            "bigger",
            "Increase the font size",
            lambda a=None: display.increase_font(),
        )

        self.add_cmd(
            "smaller",
            "Decrease the font size",
            lambda a=None: display.decrease_font(),
        )

        self.add_cmd(
            "font",
            "Set the font size",
            lambda a=None: display.set_font_size(a),
            type=str,
        )

        self.add_cmd(
            "fontfamily",
            "Set the font family",
            lambda a=None: display.set_font_family(a),
            type=str,
        )

        self.add_cmd("resetfont", "Reset the font", lambda a=None: display.reset_font())

        self.add_cmd(
            "togglescroll",
            "Scroll to the bottom or to the top",
            lambda a=None: display.toggle_scroll(),
        )

        self.add_cmd(
            "stats", "Show some internal information", lambda a=None: app.stats()
        )

        self.add_cmd(
            "sticky",
            "Make the window stay at the top",
            lambda a=None: app.toggle_sticky(),
        )

        self.add_cmd(
            "commandoc",
            "Make a file with all the commands",
            lambda a=None: commands.make_commandoc(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "argumentdoc",
            "Make a file with all the arguments",
            lambda a=None: args.make_argumentdoc(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "active",
            "Go to the tab that is currently streaming",
            lambda a=None: display.select_active_tab(),
        )

        self.add_cmd(
            "apikey", "Set the OpenAI API key", lambda a=None: model.set_api_key()
        )

        self.add_cmd(
            "system",
            "Write the system prompt",
            lambda a=None: widgets.write_system_prompt(a),
            type=str,
        )

        self.add_cmd(
            "more",
            "Show the more menu",
            lambda a=None: menumanager.more_menu.show(),
        )

        self.add_cmd(
            "tabmenu",
            "Show the tab menu",
            lambda a=None: menumanager.tab_menu.show(),
        )

        self.add_cmd(
            "fontmenu",
            "Show the font menu",
            lambda a=None: menumanager.font_menu.show(),
        )

        self.add_cmd(
            "gpt", "Show the GPT menu", lambda a=None: menumanager.gpt_menu.show()
        )

        self.add_cmd(
            "progtext",
            "Open a program using the text",
            lambda a=None: app.program(mode="text", cmd=a),
            type=str,
        )

        self.add_cmd(
            "progjson",
            "Open a program using the JSON",
            lambda a=None: app.program(mode="json", cmd=a),
            type=str,
        )

        self.add_cmd("submit", "Submit the input", lambda a=None: inputcontrol.submit())

        self.add_cmd(
            "change",
            "Set a model by its name",
            lambda a=None: widgets.change_model(a),
            type=str,
        )

        self.add_cmd(
            "mode",
            "Change the model mode",
            lambda a=None: widgets.change_mode(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "toggletabs",
            "Toggle tabs visibility",
            lambda a=None: display.toggle_tabs(),
        )

        self.add_cmd(
            "summarize",
            "Summarize the conversation",
            lambda a=None: summarize.summarize(),
        )


command_spec = CommandSpec()
