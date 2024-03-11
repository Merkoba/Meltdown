# Modules
from .app import app
from .config import config
from . import widgetutils

# Standard
from typing import Any, Callable, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk


dialog_delay = 100


def make_dialog(title: str, text: str) -> Tuple[tk.Toplevel, tk.Frame, tk.Frame]:
    dialog = tk.Toplevel(app.root)
    container = tk.Frame(dialog, padx=10, pady=6)
    container.pack()
    dialog.title(title)
    tk.Label(container, text=text, font=config.font, wraplength=500).pack(padx=6)
    top_frame = tk.Frame(container)
    top_frame.pack()
    button_frame = tk.Frame(container)
    button_frame.pack()
    dialog.bind("<Escape>", lambda e: hide_dialog(dialog))
    dialog.withdraw()
    return dialog, top_frame, button_frame


def show_dialog(dialog: tk.Toplevel) -> None:
    def show() -> None:
        dialog.deiconify()
        dialog.transient(app.root)
        dialog.grab_set()
        dialog.update()
        x = app.root.winfo_rootx() + (app.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = app.root.winfo_rooty() + (app.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry("+%d+%d" % (x, y))
        dialog.wait_window()

    app.root.after(dialog_delay, show)


def hide_dialog(dialog: tk.Toplevel) -> None:
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

    dialog, top_frame, button_frame = make_dialog("Confirm", text)
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

    dialog, top_frame, button_frame = make_dialog("Information", text)
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

    dialog, top_frame, button_frame = make_dialog("Input", text)
    entry = ttk.Entry(top_frame, font=config.font, width=17, style="Input.TEntry", justify="center")
    entry.bind("<Return>", lambda e: ok())
    entry.pack(padx=6, pady=6)
    make_dialog_button(button_frame, "Cancel", cancel)
    make_dialog_button(button_frame, "Ok", ok)
    entry.focus()
    show_dialog(dialog)
