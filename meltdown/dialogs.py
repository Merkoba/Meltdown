# Modules
from .app import app
from .config import config
from . import widgetutils

# Standard
from typing import Any, Callable, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk


dialog_delay = 100


def make_dialog(text: str) -> Tuple[tk.Frame, tk.Frame, tk.Frame]:
    dialog = tk.Frame(app.root)
    dialog.lift()
    container = tk.Frame(dialog, padx=10, pady=4)
    container.pack()
    tk.Label(container, text=text, font=config.font, wraplength=500).pack(padx=6)
    top_frame = tk.Frame(container)
    top_frame.pack()
    button_frame = tk.Frame(container)
    button_frame.pack()
    dialog.bind("<Escape>", lambda e: hide_dialog(dialog))
    dialog.bind("<FocusOut>", lambda e: hide_dialog(dialog))
    return dialog, top_frame, button_frame


def show_dialog(dialog: tk.Frame, widget: Optional[tk.Widget] = None) -> None:
    def show() -> None:
        dialog.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        dialog_width = dialog.winfo_reqwidth()
        dialog_height = dialog.winfo_reqheight()
        x = (window_width - dialog_width) // 2
        y = (window_height - dialog_height) // 2
        dialog.place(x=x, y=y)
        dialog.focus_set()

        if widget:
            widget.focus_set()

    app.root.after(dialog_delay, show)


def hide_dialog(dialog: tk.Frame) -> None:
    dialog.destroy()
    app.root.focus_set()


def make_dialog_button(parent: tk.Frame, text: str, command: Callable[..., Any]) -> None:
    button = widgetutils.get_button(parent, text)
    button.configure(command=command)
    button.pack(side=tk.LEFT, padx=6, pady=8)


def show_confirm(text: str, cmd_ok: Callable[..., Any],
                 cmd_cancel: Optional[Callable[..., Any]] = None,
                 cmd_list: Optional[List[Tuple[str, Callable[..., Any]]]] = None) -> None:
    def ok() -> None:
        hide_dialog(dialog)
        app.root.after(dialog_delay, lambda: cmd_ok())

    def cancel() -> None:
        hide_dialog(dialog)

        if cmd_cancel:
            app.root.after(dialog_delay, lambda: cmd_cancel())

    def generic(func: Callable[..., Any]) -> None:
        hide_dialog(dialog)
        app.root.after(dialog_delay, lambda: func())

    dialog, top_frame, button_frame = make_dialog(text)
    dialog.bind("<Return>", lambda e: ok())
    make_dialog_button(button_frame, "Cancel", cancel)

    if cmd_list:
        for cmd in cmd_list:
            make_dialog_button(button_frame, cmd[0], lambda: generic(cmd[1]))

    make_dialog_button(button_frame, "Ok", ok)
    show_dialog(dialog)


def show_message(text: str) -> None:
    def ok() -> None:
        hide_dialog(dialog)

    dialog, top_frame, button_frame = make_dialog(text)
    dialog.bind("<Return>", lambda e: ok())
    make_dialog_button(button_frame, "Ok", ok)
    show_dialog(dialog)


def show_input(text: str, cmd_ok: Callable[..., Any], cmd_cancel: Optional[Callable[..., Any]] = None) -> None:
    def ok() -> None:
        text = entry.get()
        hide_dialog(dialog)
        app.root.after(dialog_delay, lambda: cmd_ok(text))

    def cancel() -> None:
        hide_dialog(dialog)

        if cmd_cancel:
            app.root.after(dialog_delay, lambda: cmd_cancel())

    dialog, top_frame, button_frame = make_dialog(text)
    entry = ttk.Entry(top_frame, font=config.font, width=17, style="Input.TEntry", justify="center")
    entry.bind("<Return>", lambda e: ok())
    entry.pack(padx=6, pady=6)
    make_dialog_button(button_frame, "Cancel", cancel)
    make_dialog_button(button_frame, "Ok", ok)
    show_dialog(dialog, entry)
