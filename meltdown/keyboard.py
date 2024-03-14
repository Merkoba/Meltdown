# Modules
from .app import app
from .widgets import widgets
from . import widgetutils

# Standard
from tkinter import ttk
import tkinter as tk
from typing import Any


def on_key(event: Any) -> None:
    # Shift = 1
    # Ctrl = 4

    if event.state & 4:
        if event.keysym == "Up":
            widgets.display.output_top()
        elif event.keysym == "Down":
            widgets.display.output_bottom()
        elif event.keysym == "Left":
            widgets.display.tab_left()
        elif event.keysym == "Right":
            widgets.display.tab_right()
        elif event.keysym == "Return":
            widgets.show_main_menu()

        return

    if event.keysym == "Escape":
        widgets.esckey()
        return

    # Focus the input and insert char
    ftypes = [ttk.Combobox, ttk.Notebook, ttk.Button, tk.Text]

    if type(event.widget) in ftypes:
        chars = ["/", "\\", "!", "?", "¿", "!", "¡", ":", ";", ",", "."]

        if (len(event.keysym.strip()) == 1) or (event.char in chars):
            widgets.focus_input()
            widgetutils.set_text(widgets.input, event.char)
        elif event.keysym == "Return":
            widgets.focus_input()
    elif event.widget == widgets.input:
        if event.keysym == "Up":
            if event.state & 1:
                widgets.show_input_menu()
            else:
                widgets.input_history_up()
        elif event.keysym == "Down":
            widgets.input_history_down()


def setup() -> None:
    app.root.bind("<KeyPress>", on_key)
