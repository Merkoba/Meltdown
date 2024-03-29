# Modules
from .app import app
from .widgets import widgets
from .inputcontrol import inputcontrol
from .display import display
from .model import model
from .commands import commands
from .entrybox import EntryBox
from .tooltips import ToolTip
from .args import args
from .config import config
from . import filemanager
from . import logs
from . import timeutils

# Standard
import tkinter as tk
from typing import Any, Callable, Optional, Dict, List


KbCmd = Optional[Callable[..., Any]]
KbHelp = Optional[str]


class KbItem:
    def __init__(self, command: KbCmd, on_ctrl: KbCmd,
                 on_shift: KbCmd, on_ctrl_shift: KbCmd,
                 widget: Optional[tk.Widget], return_break: bool,
                 help: KbHelp, shift_help: KbHelp,
                 ctrl_help: KbHelp, ctrl_shift_help: KbHelp) -> None:
        self.command = command
        self.on_ctrl = on_ctrl
        self.on_shift = on_shift
        self.on_ctrl_shift = on_ctrl_shift
        self.help = help
        self.shift_help = shift_help
        self.ctrl_help = ctrl_help
        self.ctrl_shift_help = ctrl_shift_help
        self.widget = widget
        self.return_break = return_break


class Keyboard:
    def __init__(self) -> None:
        self.block_date = 0.0
        self.ctrl = False
        self.shift = False
        self.commands: Dict[str, List[KbItem]] = {}

    def block(self) -> None:
        self.block_date = timeutils.now()

    def blocked(self) -> bool:
        from .menus import Menu
        from .dialogs import Dialog

        if Menu.current_menu:
            return True

        if Dialog.current_dialog:
            return True

        if (timeutils.now() - self.block_date) < 0.35:
            return True

        return False

    def on_key_press(self, event: Any) -> None:
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl = True
        elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift = True

        if self.blocked():
            return

        ToolTip.hide_all()

        if (event.widget != inputcontrol.input) and (not isinstance(event.widget, EntryBox)):
            chars = ["/", "\\", "!", "?", "¿", "!", "¡", ":", ";", ",", ".", "'", "\"", " "]
            syms = ["Return", "Up", "Down", "Left", "Right", "BackSpace", "Delete"]

            # Focus the input and insert char
            if (len(event.keysym.strip()) == 1) or (event.char in chars):
                inputcontrol.focus()
                inputcontrol.input.insert_text(event.char)
            elif event.keysym in syms:
                inputcontrol.focus()
        else:
            if event.keysym != "Tab":
                commands.reset()

    def on_key_release(self, event: Any) -> None:
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl = False
        elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift = False

    def no_modifiers(self) -> bool:
        return (not self.ctrl) and (not self.shift)

    def action(self, item: KbItem) -> bool:
        if self.blocked():
            return False

        ok = True

        if self.ctrl and self.shift:
            if item.on_ctrl_shift:
                item.on_ctrl_shift()
        elif self.ctrl:
            if item.on_ctrl:
                item.on_ctrl()
        elif self.shift:
            if item.on_shift:
                item.on_shift()
        elif item.command:
            item.command()
        else:
            ok = False

        return ok

    def setup(self) -> None:
        self.setup_input()

        if args.keyboard:
            self.setup_globals()

        self.bind_commands()

    def bind_commands(self) -> None:
        app.root.bind("<KeyPress>", lambda e: self.on_key_press(e))
        app.root.bind("<KeyRelease>", lambda e: self.on_key_release(e))

        def run_command(event: Any, key: str) -> str:
            items = self.commands[key]

            for item in items:
                if not item.widget:
                    if self.action(item):
                        if item.return_break:
                            return "break"
                        else:
                            return ""

            for item in items:
                if item.widget:
                    if item.widget == event.widget:
                        if self.action(item):
                            if item.return_break:
                                return "break"
                            else:
                                return ""

            self.on_key_press(event)
            return ""

        for key in self.commands:
            command: Callable[..., Any] = lambda e, key=key: run_command(e, key)
            app.root.bind(key, command)

    def register(self, key: str,
                 command: Optional[Callable[..., Any]] = None,
                 on_ctrl: Optional[Callable[..., Any]] = None,
                 on_shift: Optional[Callable[..., Any]] = None,
                 on_ctrl_shift: Optional[Callable[..., Any]] = None,
                 help: Optional[str] = None,
                 shift_help: Optional[str] = None,
                 ctrl_help: Optional[str] = None,
                 ctrl_shift_help: Optional[str] = None,
                 return_break: bool = False,
                 widget: Optional[tk.Widget] = None) -> None:

        def add(key: str) -> None:
            if not self.commands.get(key):
                self.commands[key] = []

            item = KbItem(command, on_ctrl, on_shift, on_ctrl_shift,
                          widget, return_break, help=help, shift_help=shift_help,
                          ctrl_help=ctrl_help, ctrl_shift_help=ctrl_shift_help)

            self.commands[key].append(item)

        add(key)

        # Add uppercase key since it changes with shift
        if (len(key) == 1) and key.isalpha() and (on_shift or on_ctrl_shift):
            add(key.upper())

    def setup_input(self) -> None:
        self.register("<Tab>",
                      lambda: commands.check_autocomplete(),
                      widget=inputcontrol.input, return_break=True,
                      help="Autocomplete commands")

    def setup_globals(self) -> None:
        def on_enter() -> None:
            if widgets.find_focused():
                display.find_next()
            else:
                inputcontrol.focus()
                inputcontrol.submit()

        def on_shift_enter() -> None:
            if widgets.find_focused():
                display.find_next(False)

        self.register("<Return>",
                      lambda: on_enter(),
                      on_shift=lambda: on_shift_enter(),
                      on_ctrl=lambda: model.load(),
                      help="Submit prompt",
                      ctrl_help="Load model")

        self.register("<Escape>",
                      lambda: widgets.esckey(),
                      on_ctrl=lambda: model.unload(True),
                      help="Clear input, stop model stream, or go to bottom",
                      ctrl_help="Unload model")

        self.register("<Page_Up>",
                      lambda: display.scroll_up(),
                      help="Scroll up")

        self.register("<Page_Down>",
                      lambda: display.scroll_down(),
                      help="Scroll down")

        self.register("<BackSpace>",
                      on_ctrl=lambda: display.clear(),
                      ctrl_help="Clear output")

        self.register("<Up>",
                      lambda: inputcontrol.history_up(),
                      on_ctrl=lambda: display.to_top(),
                      on_shift=lambda: widgets.show_context(),
                      help="History up",
                      shift_help="Show context",
                      ctrl_help="Scroll to top")

        self.register("<Down>",
                      lambda: inputcontrol.history_down(),
                      on_ctrl=lambda: display.to_bottom(),
                      help="History down",
                      ctrl_help="Scroll to bottom")

        self.register("<Left>",
                      on_ctrl=lambda: display.tab_left(),
                      ctrl_help="Tab left")

        self.register("<Right>",
                      on_ctrl=lambda: display.tab_right(),
                      ctrl_help="Tab right")

        self.register("<space>",
                      on_ctrl=lambda: widgets.show_main_menu(),
                      ctrl_help="Show main menu")

        self.register("<F1>",
                      lambda: commands.help_command(),
                      help="Show help")

        self.register("<F2>",
                      lambda: inputcontrol.input.focus(),
                      help="Focus input")

        self.register("<F3>",
                      lambda: display.find_next(),
                      help="Find next string")

        self.register("<F5>",
                      lambda: config.reset(),
                      help="Reset config")

        self.register("<F12>",
                      lambda: display.show_tab_list(True),
                      help="Show tab list")

        self.register("<F8>",
                      lambda: app.toggle_compact(),
                      help="Toggle compact")

        self.register("<F11>",
                      lambda: app.toggle_fullscreen(),
                      help="Toggle fullscreen")

        self.register("f",
                      on_ctrl=lambda: display.find(),
                      ctrl_help="Find text")

        self.register("t",
                      on_ctrl=lambda: display.make_tab(),
                      ctrl_help="Make tab")

        self.register("w",
                      on_ctrl=lambda: display.close_current_tab(),
                      ctrl_help="Close tab")

        self.register("s",
                      on_ctrl=lambda: logs.log_menu(),
                      ctrl_help="Save log")

        self.register("y",
                      on_ctrl=lambda: display.copy_output(),
                      ctrl_help="Copy conversation")

        self.register("p",
                      on_ctrl=lambda: app.toggle_compact(),
                      ctrl_help="Toggle compact")

        self.register("r",
                      on_ctrl=lambda: app.resize(),
                      ctrl_help="Resize window")

        self.register("m",
                      on_ctrl=lambda: model.browse_models(),
                      ctrl_help="Browse models")

        self.register("l",
                      on_ctrl=lambda: logs.log_menu(),
                      on_ctrl_shift=lambda: filemanager.open_logs_dir(),
                      ctrl_help="Save log",
                      ctrl_shift_help="Open logs directory")

    def reset(self) -> None:
        self.ctrl = False
        self.shift = False

    def show_help(self, tab_id: str = "") -> None:
        from .display import display

        separator = "--------------------------------"
        lines = ["Keyboard Shortcuts:"]
        keys = []

        for key in self.commands:
            values = self.commands[key]
            upkey = key.upper()

            if upkey in keys:
                continue

            keys.append(upkey)
            upkey = upkey.replace("<", "< ").replace(">", " >")
            upkey.replace("_", " ")
            items = [separator]
            items.append(f"{upkey}")

            for value in values:
                if value.help:
                    items.append(f"{value.help}")

                if value.ctrl_help:
                    items.append(f" Ctrl: {value.ctrl_help}")

                if value.shift_help:
                    items.append(f" Shift: {value.shift_help}")

                if value.ctrl_shift_help:
                    items.append(f" Ctrl+Shift: {value.ctrl_shift_help}")

                lines.append("\n\n".join(items))

        text = "\n\n".join(lines)
        display.print(text, tab_id=tab_id)


keyboard = Keyboard()
