# Modules
from .app import app
from .widgets import widgets
from .model import model
from . import widgetutils
from . import state

# Standard
from tkinter import ttk
import tkinter as tk
from typing import Any, Callable


def on_key(event: Any) -> None:
    # Focus the input and insert char
    ftypes = [ttk.Combobox, ttk.Notebook, ttk.Button, tk.Text]

    if type(event.widget) in ftypes:
        chars = ["/", "\\", "!", "?", "¿", "!", "¡", ":", ";", ",", "."]
        syms = ["Return", "BackSpace", "Up", "Down", "Left", "Right"]

        if (len(event.keysym.strip()) == 1) or (event.char in chars):
            widgets.focus_input()
            widgetutils.set_text(widgets.input, event.char)
        elif event.keysym in syms:
            widgets.focus_input()
    elif event.widget == widgets.input:
        if event.keysym == "Up":
            widgets.input_history_up()
        elif event.keysym == "Down":
            widgets.input_history_down()


def setup() -> None:
    from .menus import Menu
    from .dialogs import Dialog
    app.root.bind("<KeyPress>", on_key)

    def register(when: str, command: Callable[..., Any]) -> None:
        def cmd() -> None:
            if Menu.current_menu:
                return

            if Dialog.current_dialog:
                return

            command()

        app.root.bind(when, lambda e: cmd())

    register("<KeyPress-Escape>", lambda: widgets.esckey())
    register("<Shift-KeyPress-Up>", lambda: widgets.show_context())
    register("<Control-KeyPress-Up>", lambda: widgets.display.output_top())
    register("<Control-KeyPress-Down>", lambda: widgets.display.output_bottom())
    register("<Control-KeyPress-Left>", lambda: widgets.display.tab_left())
    register("<Control-KeyPress-Right>", lambda: widgets.display.tab_right())
    register("<Control-KeyPress-Return>", lambda: widgets.show_main_menu())
    register("<Control-KeyPress-Escape>", lambda: widgets.show_main_menu())
    register("<Control-KeyPress-BackSpace>", lambda: widgets.display.clear_output())
    register("<Control-KeyPress-t>", lambda: widgets.display.make_tab())
    register("<Control-KeyPress-w>", lambda: widgets.display.close_current_tab())
    register("<Control-KeyPress-l>", lambda: state.save_log())
    register("<Control-KeyPress-s>", lambda: state.save_log())
    register("<Control-KeyPress-y>", lambda: widgets.display.copy_output())
    register("<Control-KeyPress-p>", lambda: app.toggle_compact())
    register("<Control-KeyPress-r>", lambda: app.resize())
    register("<Control-KeyPress-m>", lambda: model.browse_models())
    register("<Control-Shift-KeyPress-L>", lambda: state.open_logs_dir())
