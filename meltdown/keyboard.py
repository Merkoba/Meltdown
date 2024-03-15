# Modules
from .app import app
from .widgets import widgets
from .model import model
from . import widgetutils
from . import state

# Standard
from tkinter import ttk
import tkinter as tk
from typing import Any


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
    app.root.bind("<KeyPress>", on_key)
    app.root.bind("<KeyPress-Escape>", lambda e: widgets.esckey())
    app.root.bind("<Shift-KeyPress-Up>", lambda e: widgets.show_context())
    app.root.bind("<Control-KeyPress-Up>", lambda e: widgets.display.output_top())
    app.root.bind("<Control-KeyPress-Down>", lambda e: widgets.display.output_bottom())
    app.root.bind("<Control-KeyPress-Left>", lambda e: widgets.display.tab_left())
    app.root.bind("<Control-KeyPress-Right>", lambda e: widgets.display.tab_right())
    app.root.bind("<Control-KeyPress-Return>", lambda e: widgets.show_main_menu())
    app.root.bind("<Control-KeyPress-Escape>", lambda e: widgets.show_main_menu())
    app.root.bind("<Control-KeyPress-BackSpace>", lambda e: widgets.display.clear_output())
    app.root.bind("<Control-KeyPress-t>", lambda e: widgets.display.make_tab())
    app.root.bind("<Control-KeyPress-w>", lambda e: widgets.display.close_current_tab())
    app.root.bind("<Control-KeyPress-l>", lambda e: state.save_log())
    app.root.bind("<Control-KeyPress-y>", lambda e: widgets.display.copy_output())
    app.root.bind("<Control-KeyPress-p>", lambda e: app.toggle_compact())
    app.root.bind("<Control-KeyPress-r>", lambda e: app.resize())
    app.root.bind("<Control-KeyPress-m>", lambda e: model.browse_models())
    app.root.bind("<Control-Shift-KeyPress-L>", lambda e: state.open_logs_dir())
