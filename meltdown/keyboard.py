from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any
from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass

# Modules
from .app import app
from .args import args
from .config import config
from .modelcontrol import modelcontrol
from .filecontrol import filecontrol
from .inputcontrol import inputcontrol
from .display import display
from .model import model
from .commands import commands
from .tooltips import ToolTip
from .utils import utils
from .files import files


KbCmd = Callable[..., Any] | None
KbHelp = str | None


@dataclass
class KbItem:
    def __init__(
        self,
        command: KbCmd,
        on_ctrl: KbCmd,
        on_shift: KbCmd,
        on_ctrl_shift: KbCmd,
        widget: tk.Widget | None,
        return_break: bool,
        help: KbHelp,
        shift_help: KbHelp,
        ctrl_help: KbHelp,
        ctrl_shift_help: KbHelp,
    ) -> None:
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
        self.alt = False
        self.ctrl_date = 0.0
        self.double_tap_delay = 0.28
        self.commands: dict[str, list[KbItem]] = {}

    def block(self) -> None:
        self.block_date = utils.now()

    def blocked(self) -> bool:
        from .menus import Menu
        from .dialogs import Dialog

        if Menu.current_menu:
            return True

        if Dialog.current_dialog:
            return True

        return (utils.now() - self.block_date) < 0.15

    def on_key_press(self, event: Any) -> None:
        from .entrybox import EntryBox
        from .textbox import TextBox
        from .autocomplete import autocomplete

        is_ctrl = event.keysym == "Control_L" or event.keysym == "Control_R"
        is_shift = event.keysym == "Shift_L" or event.keysym == "Shift_R"
        is_alt = event.keysym == "Alt_L" or event.keysym == "Alt_R"
        is_esc = event.keysym == "Escape"
        is_entrybox = isinstance(event.widget, EntryBox)
        is_textbox = isinstance(event.widget, TextBox)

        if is_entrybox or is_textbox:
            if not self.ctrl:
                event.widget.changes.on_change()

        if not is_ctrl:
            self.ctrl_date = 0.0

        if is_ctrl:
            self.ctrl = True

            if args.taps:
                time_now = utils.now()

                if self.ctrl_date:
                    if (time_now - self.ctrl_date) < self.double_tap_delay:
                        self.on_double_ctrl()

                self.ctrl_date = time_now

        if is_alt:
            self.alt = True

        elif is_shift:
            self.shift = True

        if self.blocked():
            if is_esc:
                app.hide_all()

            return

        if event.keysym != "Tab":
            autocomplete.reset()

        if event.keysym == "Delete":
            if inputcontrol.on_delete():
                return

        ToolTip.hide_all()

        if (event.widget != inputcontrol.input) and (not is_entrybox):
            chars = [
                "/",
                "\\",
                "!",
                "?",
                "¿",
                "!",
                "¡",
                ":",
                ";",
                ",",
                ".",
                "'",
                '"',
                " ",
            ]

            syms = ["Return", "Up", "Down", "Left", "Right", "BackSpace", "Delete"]

            if event.keysym == "c":
                if self.ctrl:
                    if display.output_is_selected():
                        return
            elif event.keysym == "v":
                if self.ctrl:
                    inputcontrol.focus()
                    inputcontrol.paste()
                    return

            # Focus the input and insert char
            if (not self.ctrl) and (
                (len(event.keysym.strip()) == 1) or (event.char in chars)
            ):
                inputcontrol.focus()
                inputcontrol.input.insert_text(event.char)
            elif event.keysym in syms:
                inputcontrol.focus()

    def on_key_release(self, event: Any) -> None:
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl = False
        elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift = False
        elif event.keysym == "Alt_L" or event.keysym == "Alt_R":
            self.alt = False

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

                        return ""

            for item in items:
                if item.widget:
                    if item.widget == event.widget:
                        if self.action(item):
                            if item.return_break:
                                return "break"

                            return ""

            self.on_key_press(event)
            return ""

        def add_cmd(key: str) -> None:
            def action(event: Any) -> str:
                return run_command(event, key)

            app.root.bind(key, lambda e: action(e))

        for key in self.commands:
            add_cmd(key)

    def register(
        self,
        key: str,
        command: Callable[..., Any] | None = None,
        on_ctrl: Callable[..., Any] | None = None,
        on_shift: Callable[..., Any] | None = None,
        on_ctrl_shift: Callable[..., Any] | None = None,
        help: str | None = None,
        shift_help: str | None = None,
        ctrl_help: str | None = None,
        ctrl_shift_help: str | None = None,
        return_break: bool = False,
        widget: tk.Widget | None = None,
    ) -> None:
        def add(key: str) -> None:
            if not self.commands.get(key):
                self.commands[key] = []

            item = KbItem(
                command,
                on_ctrl,
                on_shift,
                on_ctrl_shift,
                widget,
                return_break,
                help=help,
                shift_help=shift_help,
                ctrl_help=ctrl_help,
                ctrl_shift_help=ctrl_shift_help,
            )

            self.commands[key].append(item)

        add(key)

        # Add uppercase key since it changes with shift
        if (len(key) == 1) and key.isalpha() and (on_shift or on_ctrl_shift):
            add(key.upper())

    def setup_input(self) -> None:
        from .autocomplete import autocomplete

        self.register(
            "<Tab>",
            lambda: autocomplete.check(),
            widget=inputcontrol.input,
            return_break=True,
            help="Autocomplete commands",
        )

    def setup_globals(self) -> None:
        from .widgets import widgets
        from .findmanager import findmanager

        def on_enter() -> None:
            if widgets.find_focused():
                findmanager.find_next()
            elif modelcontrol.is_focused():
                config.update("model")
                model.load()
            else:
                inputcontrol.focus()
                inputcontrol.submit()

        def on_shift_enter() -> None:
            if widgets.find_focused():
                findmanager.find_next(reverse=True)
            else:
                inputcontrol.write(add_line=True)

        def on_ctrl_enter() -> None:
            inputcontrol.submit(no_history=True)

        def on_esc() -> None:
            if widgets.find_focused():
                findmanager.hide_find()
            else:
                widgets.esckey()

        def run_command(cmd: str) -> None:
            commands.exec(commands.cmd(cmd))

        def function_key(num: int, shift: bool = False) -> None:
            if shift:
                cmd = getattr(args, f"shift_f{num}")
            else:
                cmd = getattr(args, f"f{num}")

            if cmd:
                commands.exec(cmd)

        def add_function_key(num: int) -> None:
            self.register(
                f"<F{num}>",
                lambda: function_key(num),
                on_shift=lambda: function_key(num, True),
            )

        def register_num(num: int) -> None:
            self.register(str(num), on_ctrl=lambda: run_command(f"tab {num}"))

        self.register(
            "<Return>",
            lambda: on_enter(),
            on_shift=lambda: on_shift_enter(),
            on_ctrl=lambda: on_ctrl_enter(),
            help="Submit prompt",
            shift_help="Show the Write textbox and add a line",
            ctrl_help="Submit without using history",
        )

        self.register(
            "<Escape>",
            lambda: on_esc(),
            on_shift=lambda: run_command("taskmanager"),
            on_ctrl=lambda: run_command("unload"),
            help="Clear input, select active, stop model stream, go to bottom",
            shift_help="Open task manager",
            ctrl_help="Unload model",
        )

        self.register(
            "<Prior>",
            lambda: run_command("scrollup"),
            help="Scroll up",
            on_ctrl=lambda: run_command("scrollupmore"),
            ctrl_help="Scroll up more",
            on_shift=lambda: run_command("scrollupmore"),
            shift_help="Scroll up more",
        )

        self.register(
            "<Next>",
            lambda: run_command("scrolldown"),
            help="Scroll down",
            on_ctrl=lambda: run_command("scrolldownmore"),
            ctrl_help="Scroll down more",
            on_shift=lambda: run_command("scrolldownmore"),
            shift_help="Scroll down more",
        )

        self.register(
            "<Up>",
            lambda: self.up_arrow(),
            on_ctrl=lambda: run_command("top"),
            on_shift=lambda: run_command("context"),
            help="History up",
            shift_help="Show context",
            ctrl_help="Scroll to top",
        )

        self.register(
            "<Down>",
            lambda: self.down_arrow(),
            on_ctrl=lambda: run_command("bottom"),
            help="History down",
            ctrl_help="Scroll to bottom",
        )

        self.register(
            ",",
            on_ctrl=lambda: run_command("left"),
            ctrl_help="Go to the next tab (left)",
        )

        self.register(
            ".",
            on_ctrl=lambda: run_command("right"),
            ctrl_help="Go to the next tab (right)",
        )

        self.register(
            "<less>",
            on_ctrl_shift=lambda: run_command("moveleft"),
            ctrl_shift_help="Move tab to the left",
        )

        self.register(
            "<greater>",
            on_ctrl_shift=lambda: run_command("moveright"),
            ctrl_shift_help="Move tab to the right",
        )

        self.register(
            "<space>",
            on_ctrl=lambda: run_command("write"),
            ctrl_help="Show the Write textbox",
        )

        self.register("f", on_ctrl=lambda: run_command("find"), ctrl_help="Find text")

        self.register("t", on_ctrl=lambda: run_command("new"), ctrl_help="Make tab")

        self.register("n", on_ctrl=lambda: run_command("new"), ctrl_help="Make tab")

        self.register("w", on_ctrl=lambda: run_command("close"), ctrl_help="Close tab")

        self.register(
            "s", on_ctrl=lambda: run_command("savesession"), ctrl_help="Save session"
        )

        self.register(
            "o", on_ctrl=lambda: run_command("loadsession"), ctrl_help="Load session"
        )

        self.register(
            "y",
            on_ctrl_shift=lambda: run_command("copyall"),
            ctrl_shift_help="Copy conversation",
        )

        self.register(
            "p",
            on_ctrl=lambda: run_command("prev"),
            ctrl_help="Go to the previous tab",
        )

        self.register(
            "r", on_ctrl=lambda: run_command("resize"), ctrl_help="Resize window"
        )

        self.register(
            "m", on_ctrl=lambda: run_command("main"), ctrl_help="Show the main menu"
        )

        self.register(
            "l",
            on_ctrl=lambda: run_command("log"),
            on_ctrl_shift=lambda: run_command("lastlog"),
            ctrl_help="Show the log menu",
            ctrl_shift_help="Open the last log",
        )

        self.register(
            "<KP_Add>",
            on_ctrl=lambda: run_command("bigger"),
            on_ctrl_shift=lambda: run_command("resetfont"),
            ctrl_help="Increase the font size",
            ctrl_shift_help="Reset the font size",
        )

        self.register(
            "<KP_Subtract>",
            on_ctrl=lambda: run_command("smaller"),
            on_ctrl_shift=lambda: run_command("resetfont"),
            ctrl_help="Decrease the font size",
            ctrl_shift_help="Reset the font size",
        )

        self.register(
            "<equal>",
            on_ctrl=lambda: run_command("bigger"),
            ctrl_help="Increase the font size",
        )

        self.register(
            "<minus>",
            on_ctrl=lambda: run_command("smaller"),
            ctrl_help="Decrease the font size",
        )

        self.register(
            "0",
            on_ctrl=lambda: run_command("resetfont"),
            ctrl_help="Reset the font size",
        )

        for num in range(1, 13):
            add_function_key(num)

        for num in range(1, 10):
            register_num(num)

    def reset(self) -> None:
        self.ctrl = False
        self.shift = False
        self.alt = False
        self.ctrl_date = 0.0

    def show_help(
        self, tab_id: str | None = None, filter_text: str | None = None
    ) -> None:
        from .display import display

        text = self.get_keyboardtext(filter_text)
        display.print(text, tab_id=tab_id)
        display.format_text(tab_id=tab_id, mode="all")

    def get_keyboardtext(self, filter_text: str | None = None) -> str:
        keys = list(self.commands.keys())
        separator = "---"
        lines = ["# Keyboard Shortcuts"]
        used_keys = []

        for key in keys:
            data = self.commands[key]
            upkey = key.upper()

            if upkey in used_keys:
                continue

            used_keys.append(upkey)

            if all(
                (not value.help)
                and (not value.ctrl_help)
                and (not value.shift_help)
                and (not value.ctrl_shift_help)
                for value in data
            ):
                continue

            upkey = upkey.replace("<", "< ").replace(">", " >")
            upkey.replace("_", " ")
            items = [separator]
            items.append(f"{upkey}")

            for value in data:
                if value.help:
                    items.append(f"{value.help}")

                if value.ctrl_help:
                    items.append(f"Ctrl: {value.ctrl_help}")

                if value.shift_help:
                    items.append(f"Shift: {value.shift_help}")

                if value.ctrl_shift_help:
                    items.append(f"Ctrl+Shift: {value.ctrl_shift_help}")

                lines.append("\n\n".join(items))

        lines.append(separator)
        lines.append("1 to 9 to jump to tabs")
        lines.append(separator)
        lines.append("F1 to F12 to run commands (configurable through arguments)")

        for n in range(1, 13):
            cmd = getattr(args, f"f{n}")
            lines.append(f"F{n} = {cmd}")

        if filter_text:
            lines = [line for line in lines if filter_text.lower() in line.lower()]

        return "\n\n".join(lines) + "\n"

    def on_double_ctrl(self) -> None:
        if not args.taps_command:
            return

        commands.exec(args.taps_command)

    def up_arrow(self) -> None:
        focused = app.focused()

        if args.arrow_mode == "history":
            if focused == modelcontrol.model:
                modelcontrol.history_up()
            elif focused == filecontrol.file:
                filecontrol.history_up()
            else:
                inputcontrol.history_up()
        elif args.arrow_mode == "scroll":
            commands.run("scrollup")

    def down_arrow(self) -> None:
        focused = app.focused()

        if args.arrow_mode == "history":
            if focused == modelcontrol.model:
                modelcontrol.history_down()
            elif focused == filecontrol.file:
                filecontrol.history_down()
            else:
                inputcontrol.history_down()

        elif args.arrow_mode == "scroll":
            commands.run("scrolldown")

    def make_keyboardoc(self, pathstr: str) -> None:
        from .display import display

        path = Path(pathstr)

        if (not path.parent.exists()) or (not path.parent.is_dir()):
            utils.msg(f"Invalid path: {pathstr}")
            return

        text = self.get_keyboardtext()
        files.write(path, text)
        msg = f"Saved to {path}"
        display.print(msg)
        utils.msg(msg)


keyboard = Keyboard()
