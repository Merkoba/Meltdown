# Standard
from typing import Any
from collections.abc import Callable

# Modules
from .app import app
from .config import config
from .args import args
from .display import display
from .model import model
from .session import session
from .logs import logs
from .widgets import widgets
from .modelcontrol import modelcontrol
from .filecontrol import filecontrol
from .inputcontrol import inputcontrol
from .commands import commands
from .files import files
from .output import Output
from .keyboard import keyboard
from .utils import utils
from .autoscroll import autoscroll
from .itemops import itemops
from .upload import upload
from .signals import signals
from .close import close
from .delete import delete
from .summarize import summarize
from .system_prompt import system_prompt
from .findmanager import findmanager
from .formats import formats
from .menumanager import menumanager
from .variables import variables
from .run import run
from .tasks import tasks


class DuplicateCommandError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate command: {key}"

    def __str__(self) -> str:
        return self.message


class MissingInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Missing info for command: {key}"

    def __str__(self) -> str:
        return self.message


class DuplicateInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate info for command: {key}"

    def __str__(self) -> str:
        return self.message


class CommandSpec:
    def __init__(self) -> None:
        self.force = "Use 'force' to force"
        self.delcmd = "You can use a specific number, or words like 'first' and 'last'"
        self.optdelay = "Optional delay in seconds"
        self.autoscroll = "Optional up or down argument"
        self.helpcmd = "You can filter by text"
        self.state_info = "You can provide a file name. You can use 'last'"
        self.upload_info = "Optional 'all' or 'last' argument"
        self.infos: list[str] = []
        self.commands: dict[str, Any] = {}

        self.add_commands()

    def add_cmd(
        self, key: str, info: str, action: Callable[..., Any], **kwargs: Any
    ) -> None:
        if key in self.commands:
            raise DuplicateCommandError(key)

        if not info:
            raise MissingInfoError(key)

        if info in self.infos:
            raise DuplicateInfoError(key)

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
            "logmarkdown",
            "Save conversation to a markdown file",
            lambda a=None: logs.to_markdown(name=a),
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
            "logmarkdownall",
            "Save all conversations to markdown files",
            lambda a=None: logs.to_markdown(True),
        )

        self.add_cmd(
            "resize",
            "Resize the window. You can provide dimensions like 800x600",
            lambda a=None: app.resize(a),
            type=str,
        )

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
            lambda a=None: close.close_others(force=a),
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
            "closeoldest",
            "Close oldest tab",
            lambda a=None: close.close_oldest(force=a),
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
            "closepins",
            "Close all pinned tabs",
            lambda a=None: close.close_pins(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closenormal",
            "Close all normal tabs",
            lambda a=None: close.close_normal(force=a),
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
            "closepicked",
            "Close picked tabs",
            lambda a=None: close.close_picked(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "closehalf",
            "Close the first half of the tabs",
            lambda a=None: close.close_half(force=a),
            extra=self.force,
            type="force",
        )

        self.add_cmd(
            "refresh",
            "Refresh the conversation",
            lambda a=None: display.refresh(),
        )

        self.add_cmd(
            "replay",
            "Replay the conversation, one message at a time, mainly to debug",
            lambda a=None: display.replay(),
        )

        self.add_cmd(
            "new",
            "Make a new tab. Optional argument for the name",
            lambda a=None: display.new_tab(name=a),
            type=str,
        )

        self.add_cmd(
            "newstart",
            "Make a new tab at the start. Optional argument for the name",
            lambda a=None: display.new_tab(name=a, position="start"),
            type=str,
        )

        self.add_cmd("about", "Show the about window", lambda a=None: app.show_about())

        self.add_cmd(
            "help",
            "Show the help overview",
            lambda a=None: app.show_help("overview", a),
            extra=self.helpcmd,
            type=str,
        )

        self.add_cmd(
            "commands",
            "Show the commands help",
            lambda a=None: app.show_help("commands", a),
            extra=self.helpcmd,
            type=str,
        )

        self.add_cmd(
            "arguments",
            "Show the arguments help",
            lambda a=None: app.show_help("arguments", a),
            extra=self.helpcmd,
            type=str,
        )

        self.add_cmd(
            "keyboard",
            "Show the keyboard help",
            lambda a=None: app.show_help("keyboard", a),
            extra=self.helpcmd,
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
            "middle",
            "Go to the middle of tabs",
            lambda a=None: display.select_middle_tab(),
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

        self.add_cmd("copytext", "Copy raw text", lambda a=None: formats.copy_text())

        self.add_cmd("copyjson", "Copy raw JSON", lambda a=None: formats.copy_json())

        self.add_cmd(
            "copymarkdown", "Copy raw Markdown", lambda a=None: formats.copy_markdown()
        )

        self.add_cmd("viewtext", "View raw text", lambda a=None: formats.view_text())

        self.add_cmd("viewjson", "View raw JSON", lambda a=None: formats.view_json())

        self.add_cmd(
            "viewmarkdown", "View raw Markdown", lambda a=None: formats.view_markdown()
        )

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

        self.add_cmd(
            "scrollup",
            "Scroll up",
            lambda a=None: display.scroll_up(disable_autoscroll=True),
        )

        self.add_cmd(
            "scrollupmore",
            "Scroll up more",
            lambda a=None: display.scroll_up(more=True, disable_autoscroll=True),
        )

        self.add_cmd(
            "scrolldown",
            "Scroll down",
            lambda a=None: display.scroll_down(disable_autoscroll=True),
        )

        self.add_cmd(
            "scrolldownmore",
            "Scroll down more",
            lambda a=None: display.scroll_down(more=True, disable_autoscroll=True),
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
            "movestart",
            "Move the tab to the start",
            lambda a=None: display.move_tab_to_start(),
        )

        self.add_cmd(
            "moveend",
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
            extra=self.state_info,
            type=str,
        )

        self.add_cmd(
            "loadsession",
            "Load a session",
            lambda a=None: session.load_state(name=a),
            extra=self.state_info,
            type=str,
        )

        self.add_cmd(
            "saveconfig",
            "Save the current config",
            lambda a=None: config.save_state(name=a),
            extra=self.state_info,
            type=str,
        )

        self.add_cmd(
            "loadconfig",
            "Load a config",
            lambda a=None: config.load_state(name=a),
            extra=self.state_info,
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
            lambda a=None: modelcontrol.show_recent(),
        )

        self.add_cmd(
            "browse", "Browse the models", lambda a=None: modelcontrol.browse()
        )

        self.add_cmd("file", "Browse for a file", lambda a=None: filecontrol.browse())

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
            "prompt",
            "Make a new tab and use this prompt",
            lambda a=None: inputcontrol.prompt_command(a),
            type=str,
        )

        self.add_cmd(
            "promptforce",
            "Force a new tab and use this prompt",
            lambda a=None: inputcontrol.prompt_command(a, True),
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
            "type",
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
            lambda a=None: display.pick_font_family(a),
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
            "system",
            "Write the system prompt",
            lambda a=None: system_prompt.write(a),
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
            "openai",
            "Show the OpenAI menu",
            lambda a=None: menumanager.openai_menu.show(),
        )

        self.add_cmd(
            "google",
            "Show the Google menu",
            lambda a=None: menumanager.google_menu.show(),
        )

        self.add_cmd(
            "anthropic",
            "Show the Anthropic menu",
            lambda a=None: menumanager.anthropic_menu.show(),
        )

        self.add_cmd(
            "openaikey",
            "Set the OpenAI API key",
            lambda a=None: model.set_openai_key(),
        )

        self.add_cmd(
            "googlekey",
            "Set the Google API key",
            lambda a=None: model.set_google_key(),
        )

        self.add_cmd(
            "anthropickey",
            "Set the Anthropic API key",
            lambda a=None: model.set_anthropic_key(),
        )

        self.add_cmd(
            "opentext",
            "Open a program using the text",
            lambda a=None: formats.do_open(mode="text", cmd=a),
            type=str,
        )

        self.add_cmd(
            "openjson",
            "Open a program using the JSON",
            lambda a=None: formats.do_open(mode="json", cmd=a),
            type=str,
        )

        self.add_cmd(
            "openmarkdown",
            "Open a program using the markdown",
            lambda a=None: formats.do_open(mode="markdown", cmd=a),
            type=str,
        )

        self.add_cmd(
            "usetext",
            "Use the current text (text)",
            lambda a=None: formats.do_use("text"),
        )

        self.add_cmd(
            "usejson",
            "Use the current text (JSON)",
            lambda a=None: formats.do_use("json"),
        )

        self.add_cmd(
            "usemarkdown",
            "Use the current text (markdown)",
            lambda a=None: formats.do_use("markdown"),
        )

        self.add_cmd("submit", "Submit the input", lambda a=None: inputcontrol.submit())

        self.add_cmd(
            "fresh",
            "Do a prompt without using the history",
            lambda a=None: inputcontrol.submit(text=a, no_history=True, mode="fresh"),
            type=str,
        )

        self.add_cmd(
            "change",
            "Set a model by its name",
            lambda a=None: modelcontrol.change(a),
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
            "copymenu",
            "Copy the last item",
            lambda a=None: menumanager.copy_menu.last_item(),
        )

        self.add_cmd(
            "copy",
            "Copy the last user and AI text",
            lambda a=None: Output.copy_item(last=True),
        )

        self.add_cmd(
            "copyuser",
            "Copy the last user text",
            lambda a=None: Output.copy_item("user", last=True),
        )

        self.add_cmd(
            "copyai",
            "Copy the last AI text",
            lambda a=None: Output.copy_item("ai", last=True),
        )

        self.add_cmd(
            "args",
            "Show the arguments used",
            lambda a=None: args.show_used_args(),
        )

        self.add_cmd(
            "prev",
            "Go to the previous tab",
            lambda a=None: display.goto_prev_tab(),
        )

        self.add_cmd(
            "nothing",
            "Do nothing",
            lambda a=None: None,
            skip_palette=True,
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
            "showframe",
            "Show a specific frame",
            lambda a=None: app.show_frame_cmd(a),
            type=str,
            arg_req=True,
        )

        self.add_cmd(
            "hideframe",
            "Hide a specific frame",
            lambda a=None: app.hide_frame_cmd(a),
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
            lambda a=None: autoscroll.toggle(a),
            extra=self.autoscroll,
            type=str,
        )

        self.add_cmd(
            "autoscrollup",
            "Toggle automatic scrolling (Up)",
            lambda a=None: autoscroll.toggle("up"),
        )

        self.add_cmd(
            "startautoscroll",
            "Start automatic scrolling",
            lambda a=None: autoscroll.start(a),
            extra=self.autoscroll,
            type=str,
        )

        self.add_cmd(
            "autoscrollstop",
            "Stop automatic scrolling",
            lambda a=None: autoscroll.stop(),
        )

        self.add_cmd(
            "faster",
            "Make auto-scroll faster",
            lambda a=None: autoscroll.faster(),
        )

        self.add_cmd(
            "slower",
            "Make auto-scroll slower",
            lambda a=None: autoscroll.slower(),
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
            "use",
            "Use the specified item",
            lambda a=None: itemops.use_item(number=a),
            type=str,
        )

        self.add_cmd(
            "info",
            "Show information about the specified item",
            lambda a=None: itemops.show_info(number=a),
            type=str,
        )

        self.add_cmd(
            "profile",
            "Show the current profile",
            lambda a=None: app.open_profile(),
        )

        self.add_cmd(
            "portrait",
            "Show the AI's portrait",
            lambda a=None: app.show_portrait(),
        )

        self.add_cmd(
            "describe",
            "The describe prompt",
            lambda a=None: app.describe(),
        )

        self.add_cmd(
            "theme",
            "Show the theme menu",
            lambda a=None: app.pick_theme(),
        )

        self.add_cmd(
            "modelname",
            "Show the model name",
            lambda a=None: model.show_name(),
        )

        self.add_cmd(
            "size",
            "Show size and length information",
            lambda a=None: display.show_size(),
        )

        self.add_cmd(
            "information",
            "Show the info dialog",
            lambda a=None: app.show_info(),
        )

        self.add_cmd(
            "upload",
            f"Start an upload. {self.upload_info}",
            lambda a=None: upload.service_picker(mode=a),
            type=str,
        )

        self.add_cmd(
            "uploadfull",
            f"Start a full upload process. {self.upload_info}",
            lambda a=None: upload.service_picker(mode=a, full=True),
            type=str,
        )

        self.add_cmd(
            "uploadharambe",
            f"Start a Harambe upload. {self.upload_info}",
            lambda a=None: upload.service_picker(mode=a, service="harambe"),
            type=str,
        )

        self.add_cmd(
            "uploadrentry",
            f"Start a Rentry upload. {self.upload_info}",
            lambda a=None: upload.service_picker(mode=a, service="rentry"),
            type=str,
        )

        self.add_cmd(
            "uploadmarkdown",
            f"Upload markdown to a hosting service. {self.upload_info}",
            lambda a=None: upload.upload(mode=a, format_="markdown"),
            type=str,
        )

        self.add_cmd(
            "uploadraw",
            f"Upload raw to a hosting service. {self.upload_info}",
            lambda a=None: upload.upload(mode=a, format_="raw"),
            type=str,
        )

        self.add_cmd(
            "uploadjson",
            f"Upload json to a hosting service. {self.upload_info}",
            lambda a=None: upload.upload(mode=a, format_="json"),
            type=str,
        )

        self.add_cmd(
            "uploadtext",
            f"Upload text to a hosting service. {self.upload_info}",
            lambda a=None: upload.upload(mode=a, format_="text"),
            type=str,
        )

        self.add_cmd(
            "count",
            "Count the number of open tabs and items",
            lambda a=None: app.count(),
        )

        self.add_cmd(
            "signal",
            "Run a signal by its name",
            lambda a=None: signals.run(a),
            type=str,
        )

        self.add_cmd(
            "arg",
            "Set an argument while the program is running",
            lambda a=None: args.set_command(a),
            type=str,
        )

        self.add_cmd(
            "setvar",
            "Set a variable. For example: /setvar x the world. Then use it with $x",
            lambda a=None: variables.set_variable(a),
            type=str,
        )

        self.add_cmd(
            "unsetvar",
            "Unset a variable",
            lambda a=None: variables.unset_variable(a),
            type=str,
        )

        self.add_cmd(
            "readvar",
            "Read the content of a variable",
            lambda a=None: variables.read_variable(a),
            type=str,
        )

        self.add_cmd(
            "vars",
            "Read all the variables",
            lambda a=None: variables.read_variables(),
        )

        self.add_cmd(
            "print",
            "Print a message",
            lambda a=None: display.print(a),
            type=str,
        )

        self.add_cmd(
            "echo",
            "Print a message and format markdown",
            lambda a=None: display.print(a, do_format=True),
            type=str,
        )

        self.add_cmd(
            "pin",
            "Pin a tab",
            lambda a=None: display.pin(),
        )

        self.add_cmd(
            "unpin",
            "Unpin a tab",
            lambda a=None: display.unpin(),
        )

        self.add_cmd(
            "togglepin",
            "Pin or unpin a tab",
            lambda a=None: display.toggle_pin(),
        )

        self.add_cmd(
            "pins",
            "Show the tab list but only with pins",
            lambda a=None: display.show_tab_list(mode="pins"),
        )

        self.add_cmd(
            "sortpins",
            "Place the pins at the start of the list",
            lambda a=None: display.sort_pins(mode="start"),
        )

        self.add_cmd(
            "sortpinsend",
            "Place the pins at the end of the list",
            lambda a=None: display.sort_pins(mode="end"),
        )

        self.add_cmd(
            "image",
            "Generate an image through a prompt",
            lambda a=None: model.generate_image(prompt=a),
            type=str,
        )

        self.add_cmd(
            "setalias",
            "Set an alias. For example: /setalias pro /loadconfig pro",
            lambda a=None: commands.set_alias(a),
            type=str,
        )

        self.add_cmd(
            "unsetalias",
            "Unset an alias",
            lambda a=None: commands.unset_alias(a),
            type=str,
        )

        self.add_cmd(
            "readalias",
            "Read the content of an alias",
            lambda a=None: commands.read_alias(a),
            type=str,
        )

        self.add_cmd(
            "say",
            "Say something exactly as it is",
            lambda a=None: display.say(a),
            type=str,
        )

        self.add_cmd(
            "program",
            "Use a program with the last AI response",
            lambda a=None: itemops.run_program(),
            type=str,
        )

        self.add_cmd(
            "notify",
            "Show a notification message using notify-send",
            lambda a=None: app.notify(a),
            type=str,
        )

        self.add_cmd(
            "filter",
            "Filter the conversation by a specific text",
            lambda a=None: display.filter_text(None, a),
            type=str,
        )

        self.add_cmd(
            "randomconfig",
            "Randomize some config settings",
            lambda a=None: config.randomize(),
        )

        self.add_cmd(
            "script",
            "Use a registered script using the current conversation",
            lambda a=None: run.run_script(a),
            type=str,
        )

        self.add_cmd(
            "enabletasks",
            "Enable automatic tasks",
            lambda a=None: tasks.enable(),
        )

        self.add_cmd(
            "disabletasks",
            "Disable automatic tasks",
            lambda a=None: tasks.disable(),
        )

        self.add_cmd(
            "snippets",
            "Print the number of snippets",
            lambda a=None: display.count_snippets(),
        )


command_spec = CommandSpec()
