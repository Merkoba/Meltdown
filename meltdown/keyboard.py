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
from . import timeutils
from . import state

# Standard
import tkinter as tk
from typing import Any, Callable, Optional, Dict, List


KbCmd = Optional[Callable[..., Any]]


class KbItem:
    def __init__(self, command: KbCmd, on_ctrl: KbCmd,
                 on_shift: KbCmd, on_ctrl_shift: KbCmd,
                 widget: Optional[tk.Widget], return_break: bool) -> None:
        self.command = command
        self.on_ctrl = on_ctrl
        self.on_shift = on_shift
        self.on_ctrl_shift = on_ctrl_shift
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
                 return_break: bool = False,
                 widget: Optional[tk.Widget] = None) -> None:

        def add(key: str) -> None:
            if not self.commands.get(key):
                self.commands[key] = []

            item = KbItem(command, on_ctrl, on_shift, on_ctrl_shift, widget, return_break)
            self.commands[key].append(item)

        add(key)

        # Add uppercase key since it changes with shift
        if (len(key) == 1) and key.isalpha() and (on_shift or on_ctrl_shift):
            add(key.upper())

    def setup_input(self) -> None:
        self.register("<Tab>", lambda: commands.check_autocomplete(), widget=inputcontrol.input, return_break=True)

    def setup_globals(self) -> None:
        def on_enter() -> None:
            inputcontrol.focus()
            inputcontrol.submit()

        self.register("<Return>", lambda: on_enter(), on_ctrl=lambda: model.load())
        self.register("<Escape>", lambda: widgets.esckey(), on_ctrl=lambda: model.unload(True))
        self.register("<Page_Up>", lambda: display.scroll_up())
        self.register("<Page_Down>", lambda: display.scroll_down())
        self.register("<BackSpace>", on_ctrl=lambda: display.clear())
        self.register("<Up>", command=lambda: inputcontrol.history_up(),
                      on_ctrl=lambda: display.to_top(), on_shift=lambda: widgets.show_context())
        self.register("<Down>", command=lambda: inputcontrol.history_down(),
                      on_ctrl=lambda: display.to_bottom())
        self.register("<Left>", on_ctrl=lambda: display.tab_left())
        self.register("<Right>", on_ctrl=lambda: display.tab_right())
        self.register("<space>", on_ctrl=lambda: widgets.show_main_menu())
        self.register("<F1>", lambda: self.show_help())
        self.register("<F2>", lambda: inputcontrol.input.focus())
        self.register("<F3>", lambda: inputcontrol.input.focus())
        self.register("<F8>", lambda: app.toggle_compact())
        self.register("<F11>", lambda: app.toggle_fullscreen())
        self.register("t", on_ctrl=lambda: display.make_tab())
        self.register("w", on_ctrl=lambda: display.close_current_tab())
        self.register("s", on_ctrl=lambda: state.save_log())
        self.register("y", on_ctrl=lambda: display.copy_output())
        self.register("p", on_ctrl=lambda: app.toggle_compact())
        self.register("r", on_ctrl=lambda: app.resize())
        self.register("m", on_ctrl=lambda: model.browse_models())
        self.register("l", on_ctrl=lambda: state.save_log(), on_ctrl_shift=lambda: state.open_logs_dir())

    def reset(self) -> None:
        self.ctrl = False
        self.shift = False

    def show_help(self) -> None:
        tab_id = display.make_tab()
        commands.show_help(tab_id=tab_id)
        commands.show_arguments(tab_id=tab_id)


keyboard = Keyboard()
