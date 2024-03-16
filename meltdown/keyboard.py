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
from typing import Any, Callable


block_date = 0.0


def block() -> None:
    global block_date
    block_date = timeutils.now()


def blocked() -> bool:
    from .menus import Menu
    from .dialogs import Dialog

    if Menu.current_menu:
        return True

    if Dialog.current_dialog:
        return True

    if (timeutils.now() - block_date) < 0.5:
        return True

    return False


def is_entrybox(widget: tk.Misc) -> bool:
    if isinstance(widget, EntryBox):
        return True
    elif widget.master is not None:
        return is_entrybox(widget.master)
    else:
        return False


def on_key(event: Any) -> None:
    if blocked():
        return

    if event.widget and (not is_entrybox(event.widget)):
        chars = ["/", "\\", "!", "?", "¿", "!", "¡", ":", ";", ",", ".", "'", "\"", " "]
        syms = ["Return", "BackSpace", "Up", "Down", "Left", "Right"]

        # Focus the input and insert char
        if (len(event.keysym.strip()) == 1) or (event.char in chars):
            widgets.focus_input()
            widgets.input.insert_text(event.char)
        elif event.keysym in syms:
            widgets.focus_input()


def setup() -> None:
    setup_input()

    app.root.bind("<KeyPress>", on_key)

    def register(when: str, command: Callable[..., Any]) -> None:
        def cmd() -> None:
            if blocked():
                return

            command()

        app.root.bind(when, lambda e: cmd())

    def on_enter() -> None:
        widgets.focus_input()
        widgets.submit()

    register("<KeyPress-Return>", lambda: on_enter())
    register("<KeyPress-Escape>", lambda: widgets.esckey())
    register("<KeyPress-Page_Up>", lambda: widgets.display.scroll_up())
    register("<KeyPress-Page_Down>", lambda: widgets.display.scroll_down())
    register("<Shift-KeyPress-Up>", lambda: widgets.show_context())
    register("<Control-KeyPress-Up>", lambda: widgets.display.to_top())
    register("<Control-KeyPress-Down>", lambda: widgets.display.to_bottom())
    register("<Control-KeyPress-Left>", lambda: widgets.display.tab_left())
    register("<Control-KeyPress-Right>", lambda: widgets.display.tab_right())
    register("<Control-KeyPress-Return>", lambda: model.load())
    register("<Control-KeyPress-Escape>", lambda: model.unload(True))
    register("<Control-KeyPress-BackSpace>", lambda: widgets.display.clear_output())
    register("<Control-KeyPress-t>", lambda: widgets.display.make_tab())
    register("<Control-KeyPress-w>", lambda: widgets.display.close_current_tab())
    register("<Control-KeyPress-l>", lambda: state.save_log())
    register("<Control-KeyPress-s>", lambda: state.save_log())
    register("<Control-KeyPress-y>", lambda: widgets.display.copy_output())
    register("<Control-KeyPress-p>", lambda: app.toggle_compact())
    register("<Control-KeyPress-r>", lambda: app.resize())
    register("<Control-KeyPress-m>", lambda: model.browse_models())
    register("<Control-KeyPress-space>", lambda: widgets.show_main_menu())
    register("<Control-Shift-KeyPress-L>", lambda: state.open_logs_dir())


def setup_input() -> None:
    def on_tab() -> str:
        commands.check_autocomplete()
        return "break"

    widgets.input.bind("<KeyPress-Tab>", lambda e: on_tab())
    widgets.input.bind("<KeyPress-Up>", lambda e: widgets.input_history_up())
    widgets.input.bind("<KeyPress-Down>", lambda e: widgets.input_history_down())
