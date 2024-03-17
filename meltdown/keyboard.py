# Modules
from .app import app
from .widgets import widgets
from .model import model
from .entrybox import EntryBox
from .commands import commands
from . import timeutils
from . import state

# Standard
import tkinter as tk
from typing import Any, Callable, Optional, Dict, List


class Keyboard:
    def __init__(self) -> None:
        self.block_date = 0.0
        self.ctrl = False
        self.shift = False
        self.commands: Dict[str, List[Dict[str, Any]]] = {}

    def reset(self) -> None:
        self.ctrl = False
        self.shift = False

    def block(self) -> None:
        self.block_date = timeutils.now()

    def blocked(self) -> bool:
        from .menus import Menu
        from .dialogs import Dialog

        if Menu.current_menu:
            return True

        if Dialog.current_dialog:
            return True

        if (timeutils.now() - self.block_date) < 0.5:
            return True

        return False

    def on_key_press(self, event: Any) -> None:
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl = True
        elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift = True

        if self.blocked():
            return

        if event.widget != widgets.input:
            chars = ["/", "\\", "!", "?", "¿", "!", "¡", ":", ";", ",", ".", "'", "\"", " "]
            syms = ["Return", "BackSpace", "Up", "Down", "Left", "Right"]

            # Focus the input and insert char
            if (len(event.keysym.strip()) == 1) or (event.char in chars):
                widgets.focus_input()
                widgets.input.insert_text(event.char)
            elif event.keysym in syms:
                widgets.focus_input()
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

    def action(self, cmd: Dict[str, Any]) -> bool:
        if self.blocked():
            return False

        ok = True

        if self.ctrl and self.shift:
            if cmd["on_ctrl_shift"]:
                cmd["on_ctrl_shift"]()
        elif self.ctrl:
            if cmd["on_ctrl"]:
                cmd["on_ctrl"]()
        elif self.shift:
            if cmd["on_shift"]:
                cmd["on_shift"]()
        elif cmd["command"]:
            cmd["command"]()
        else:
            ok = False

        return ok

    def setup(self) -> None:
        self.setup_input()
        self.setup_globals()
        app.root.bind("<KeyPress>", lambda e: self.on_key_press(e))
        app.root.bind("<KeyRelease>", lambda e: self.on_key_release(e))

        def run_command(event: Any, key: str) -> str:
            cmds = self.commands[key]

            for cmd in cmds:
                if not cmd["widget"]:
                    if self.action(cmd):
                        if cmd["return_break"]:
                            return "break"
                        else:
                            return ""

            for cmd in cmds:
                if cmd["widget"]:
                    if cmd["widget"] == event.widget:
                        if self.action(cmd):
                            if cmd["return_break"]:
                                return "break"
                            else:
                                return ""

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

            self.commands[key].append({"widget": widget, "command": command,
                                       "on_ctrl": on_ctrl, "on_shift": on_shift,
                                       "on_ctrl_shift": on_ctrl_shift,
                                       "return_break": return_break})

        add(key)

        # Add uppercase key since it changes with shift
        if (len(key) == 1) and key.isalpha() and (on_shift or on_ctrl_shift):
            add(key.upper())

    def setup_input(self) -> None:
        self.register("<Tab>", lambda: commands.check_autocomplete(), widget=widgets.input, return_break=True)

    def setup_globals(self) -> None:
        def on_enter() -> None:
            widgets.focus_input()
            widgets.submit()

        self.register("<Return>", lambda: on_enter(), on_ctrl=lambda: model.load())
        self.register("<Escape>", lambda: widgets.esckey(), on_ctrl=lambda: model.unload(True))
        self.register("<Page_Up>", lambda: widgets.display.scroll_up())
        self.register("<Page_Down>", lambda: widgets.display.scroll_down())
        self.register("<BackSpace>", on_ctrl=lambda: widgets.display.clear_output())
        self.register("<Up>", command=lambda: widgets.input_history_up(),
                      on_ctrl=lambda: widgets.display.to_top(), on_shift=lambda: widgets.show_context())
        self.register("<Down>", command=lambda: widgets.input_history_down(),
                      on_ctrl=lambda: widgets.display.to_bottom())
        self.register("<Left>", on_ctrl=lambda: widgets.display.tab_left())
        self.register("<Right>", on_ctrl=lambda: widgets.display.tab_right())
        self.register("space", on_ctrl=lambda: widgets.show_main_menu())
        self.register("t", on_ctrl=lambda: widgets.display.make_tab())
        self.register("w", on_ctrl=lambda: widgets.display.close_current_tab())
        self.register("s", on_ctrl=lambda: state.save_log())
        self.register("y", on_ctrl=lambda: widgets.display.copy_output())
        self.register("p", on_ctrl=lambda: app.toggle_compact())
        self.register("r", on_ctrl=lambda: app.resize())
        self.register("m", on_ctrl=lambda: model.browse_models())
        self.register("l", on_ctrl=lambda: state.save_log(), on_ctrl_shift=lambda: state.open_logs_dir())


keyboard = Keyboard()
