# Modules
from .app import app
from .config import config
from .entrybox import EntryBox
from . import widgetutils

# Standard
from typing import Any, Callable, List, Optional, Tuple
import tkinter as tk


class Dialog:
    current_dialog: Optional["Dialog"] = None

    @staticmethod
    def show_confirm(text: str, cmd_ok: Callable[..., Any],
                     cmd_cancel: Optional[Callable[..., Any]] = None,
                     cmd_list: Optional[List[Tuple[str, Callable[..., Any]]]] = None) -> None:
        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()
            cmd_ok()

        def cancel() -> None:
            dialog.hide()

            if cmd_cancel:
                cmd_cancel()

        def generic(func: Callable[..., Any]) -> None:
            dialog.hide()
            func()

        dialog.root.bind("<Return>", lambda e: ok())
        dialog.make_button("Cancel", cancel)

        def make_button(cmd: Tuple[str, Callable[..., Any]]) -> None:
            dialog.make_button(cmd[0], lambda: generic(cmd[1]))

        if cmd_list:
            for cmd in cmd_list:
                make_button(cmd)

        dialog.make_button("Ok", ok)
        dialog.show()

    @staticmethod
    def show_message(text: str) -> None:
        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()

        dialog.root.bind("<Return>", lambda e: ok())
        dialog.make_button("Ok", ok)
        dialog.show()

    @staticmethod
    def show_input(text: str, cmd_ok: Callable[..., Any],
                   cmd_cancel: Optional[Callable[..., Any]] = None, value: str = "") -> None:
        dialog = Dialog(text)
        entry = EntryBox(dialog.top_frame, font=config.font, width=17, justify="center")

        def ok() -> None:
            text = entry.get()
            dialog.hide()
            cmd_ok(text)

        def cancel() -> None:
            dialog.hide()

            if cmd_cancel:
                cmd_cancel()

        if value:
            entry.insert(0, value)

        entry.bind("<Return>", lambda e: ok())
        entry.pack(padx=6, pady=6)
        dialog.make_button("Cancel", cancel)
        dialog.make_button("Ok", ok)
        dialog.show()
        entry.full_focus()

    @staticmethod
    def hide_all() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.hide()

    def __init__(self, text: str) -> None:
        self.make(text)
        Dialog.current_dialog = self

    def make(self, text: str) -> None:
        background = config.dialog_background
        foreground = config.dialog_foreground

        self.root = tk.Frame(app.root, bg=background)
        self.root.lift()
        container = tk.Frame(self.root, padx=10, pady=4, bg=background)
        container.pack()
        tk.Label(container, text=text, font=config.font, wraplength=500, bg=background, fg=foreground).pack(padx=6)
        self.top_frame = tk.Frame(container)
        self.top_frame.pack()
        self.button_frame = tk.Frame(container, bg=background)
        self.button_frame.pack()
        self.root.bind("<Escape>", lambda e: self.hide())
        self.root.bind("<FocusOut>", lambda e: self.hide())

    def show(self) -> None:
        self.root.update_idletasks()
        window_width = app.root.winfo_width()
        window_height = app.root.winfo_height()
        dialog_width = self.root.winfo_reqwidth()
        dialog_height = self.root.winfo_reqheight()
        x = (window_width - dialog_width) // 2
        y = (window_height - dialog_height) // 2
        self.root.place(x=x, y=y)
        self.root.focus_set()

    def hide(self) -> None:
        from .tooltips import ToolTip
        from .widgets import widgets
        from .keyboard import keyboard
        ToolTip.block()
        keyboard.block()
        widgets.focus_input()
        self.root.destroy()
        Dialog.current_dialog = None

    def make_button(self, text: str, command: Callable[..., Any]) -> None:
        button = widgetutils.get_button(self.button_frame, text, command, width=10, bigger=True)
        button.pack(side=tk.LEFT, padx=6, pady=8)
