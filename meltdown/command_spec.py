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
from .files import files
from .output import Output
from .keyboard import keyboard
from .utils import utils
from .autoscroll import autoscroll
from . import itemops
from . import summarize
from . import menumanager
from . import findmanager
from . import delete
from . import close


class CommandSpec:
    def __init__(self) -> None:
        self.force = "Use 'force' to force"
        self.file_name = "You can provide the file name"
        self.delcmd = "You can use a specific number, or words like 'first' and 'last'"
        self.optdelay = "Optional delay in seconds"
        self.autoscroll = "Optional up or down argument"
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
            "Exit the application",
            lambda a=None: app.exit(a),
            extra=self.optdelay,
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
            lambda a=None: close.close(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeothers",
            "Close other tabs",
            lambda a=None: close.close_other(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeall",
            "Close all tabs",
            lambda a=None: close.close_all(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeold",
            "Close old tabs",
            lambda a=None: close.close_old(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeempty",
            "Close empty tabs",
            lambda a=None: close.close_empty(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeleft",
            "Close tabs to the left",
            lambda a=None: close.close_left(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closeright",
            "Close tabs to the right",
            lambda a=None: close.close_right(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "refresh",
            "Refresh the conversation",
            lambda a=None: display.refresh(),
        )

        self.add_cmd(
            "new", "Make a new tab", lambda a=None: display.make_tab(a), type=str
        )

        self.add_cmd("about", "Show the about window", lambda a=None: app.show_about())

        self.add_cmd("help", "Ask for help", lambda a=None: commands.help())

        self.add_cmd(
            "commands",
            "Show the commands help",
            lambda a=None: app.show_help("commands"),
        )

        self.add_cmd(
            "arguments",
            "Show the arguments help",
            lambda a=None: app.show_help("arguments"),
        )

        self.add_cmd(
            "keyboard",
            "Show the keyboard help",
            lambda a=None: app.show_help("keyboard"),
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
            "findallprev",
            "Find a text string among all tabs (backwards)",
            lambda a=None: findmanager.find_all(a, reverse=True),
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
            "findprev",
            "Find previous text match",
            lambda a=None: findmanager.find_prev(),
        )

        self.add_cmd(
            "findnext", "Find next text match", lambda a=None: findmanager.find_next()
        )

        self.add_cmd("scrollup", "Scroll up", lambda a=None: display.scroll_up())

        self.add_cmd(
            "scrollupmore",
            "Scroll up more",
            lambda a=None: display.scroll_up(more=True),
        )

        self.add_cmd("scrolldown", "Scroll down", lambda a=None: display.scroll_down())

        self.add_cmd(
            "scrolldownmore",
            "Scroll down more",
            lambda a=None: display.scroll_down(more=True),
        )

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

        self.add_cmd(
            "copyall", "Copy all the text", lambda a=None: display.copy_output()
        )

        self.add_cmd(
            "selectall", "Select all text", lambda a=None: display.select_output()
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
            "write",
            "Write an input prompt",
            lambda a=None: inputcontrol.input_command(a),
            type=str,
        )

        self.add_cmd(
            "writemax",
            "Write an input prompt and maximize",
            lambda a=None: inputcontrol.input_command(a, maxed=True),
            type=str,
        )

        self.add_cmd(
            "setinput",
            "Set the input to this text",
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
            "memory",
            "Show how much memory the program is using",
            lambda a=None: app.show_memory(),
        )

        self.add_cmd(
            "started",
            "How long ago the program started",
            lambda a=None: app.show_started(),
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
            "keyboardoc",
            "Make a file with all the keyboard shortcuts",
            lambda a=None: keyboard.make_keyboardoc(a),
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
            "cleansubmit",
            "Submit the input without using history",
            lambda a=None: inputcontrol.submit(no_history=True),
        )

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

        self.add_cmd(
            "delete",
            "Remove a specific item of a conversation",
            lambda a=None: delete.delete_items(number=a),
            extra=self.delcmd,
            type=str,
        )

        self.add_cmd(
            "deleteabove",
            "Delete items above this item",
            lambda a=None: delete.delete_items(number=a, mode="above"),
            extra=self.delcmd,
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "deletebelow",
            "Delete items below this item",
            lambda a=None: delete.delete_items(number=a, mode="below"),
            extra=self.delcmd,
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "deleteothers",
            "Delete the other items",
            lambda a=None: delete.delete_items(number=a, mode="others"),
            extra=self.delcmd,
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "openfile",
            "Open the last file used",
            lambda a=None: files.open_last_file(),
        )

        self.add_cmd(
            "date",
            "Show the current date and time",
            lambda a=None: app.show_date(),
        )

        self.add_cmd(
            "explain",
            "Explain selected words",
            lambda a=None: Output.explain_selected(),
        )

        self.add_cmd(
            "newexplain",
            "Open a new tab and explain something",
            lambda a=None: Output.new_selected(),
        )

        self.add_cmd(
            "search",
            "Search using the selected text",
            lambda a=None: Output.search_selected(),
        )

        self.add_cmd(
            "copy",
            "Copy the selected text",
            lambda a=None: Output.copy_selected(),
        )

        self.add_cmd(
            "args",
            "Show the arguments used",
            lambda a=None: args.show_used_args(),
        )

        self.add_cmd(
            "prevtab",
            "Go to the previous tab",
            lambda a=None: display.goto_prev_tab(),
        )

        self.add_cmd(
            "nothing",
            "Do nothing",
            lambda a=None: None,
        )

        self.add_cmd(
            "random",
            "Make up a random prompt",
            lambda a=None: utils.random_prompt(),
        )

        self.add_cmd(
            "toggleframe",
            "Toggle a specific frame",
            lambda a=None: app.toggle_frame(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "lastlog",
            "Open the last log",
            lambda a=None: logs.open_last_log(),
        )

        self.add_cmd(
            "autoscroll",
            "Toggle automatic scrolling",
            lambda a=None: autoscroll.toggle(),
        )

        self.add_cmd(
            "enableautoscroll",
            "Enable automatic scrolling",
            lambda a=None: autoscroll.enable(a),
            extra=self.autoscroll,
            type=str,
        )

        self.add_cmd(
            "disableautoscroll",
            "Disable automatic scrolling",
            lambda a=None: autoscroll.disable(),
        )

        self.add_cmd(
            "repeat",
            "Repeat the specified prompt",
            lambda a=None: itemops.repeat(number=a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "repeatclean",
            "Repeat the specified prompt (without history)",
            lambda a=None: itemops.repeat(number=a, no_history=True),
            type=str,
        )

        self.add_cmd(
            "copyitem",
            "Copy the specified item",
            lambda a=None: itemops.copy(number=a),
            type=str,
        )

        self.add_cmd(
            "selectitem",
            "Select the specified item",
            lambda a=None: itemops.select(number=a),
            type=str,
        )

        self.add_cmd(
            "profile",
            "Show the current profile",
            lambda a=None: app.open_profile(),
        )

        self.add_cmd(
            "portrait",
            "Show the assistant's portrait",
            lambda a=None: app.show_portrait(),
        )

        self.add_cmd(
            "theme",
            "Show the theme menu",
            lambda a=None: menumanager.theme_menu.show(),
        )

        self.add_cmd(
            "modelname",
            "Show the model name",
            lambda a=None: model.show_name(),
        )

        self.add_cmd(
            "size",
            "Show the number of lines and characters",
            lambda a=None: display.show_size(),
        )


command_spec = CommandSpec()
