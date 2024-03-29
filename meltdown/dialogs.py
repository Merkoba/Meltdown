# Modules
from .app import app
from .entrybox import EntryBox
from .buttonbox import ButtonBox
from . import widgetutils

# Standard
from typing import Any, Callable, List, Optional, Tuple
import tkinter as tk


class Dialog:
    current_dialog: Optional["Dialog"] = None

    @staticmethod
    def show_confirm(text: str, cmd_ok: Optional[Callable[..., Any]] = None,
                     cmd_cancel: Optional[Callable[..., Any]] = None) -> None:
        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()

            if cmd_ok:
                cmd_ok()

        def cancel() -> None:
            dialog.hide()

            if cmd_cancel:
                cmd_cancel()

        dialog.root.bind("1", lambda e: cancel())
        dialog.root.bind("2", lambda e: ok())
        dialog.make_button("Cancel", cancel)
        dialog.make_button("Ok", ok)
        dialog.current_button = 1
        dialog.show()

    @staticmethod
    def show_commands(text: str,
                      commands: List[Tuple[str, Callable[..., Any]]],
                      on_enter: Optional[Callable[..., Any]] = None) -> None:
        dialog = Dialog(text)

        def generic(func: Callable[..., Any]) -> None:
            dialog.hide()
            func()

        def make_button(cmd: Tuple[str, Callable[..., Any]], num: int) -> None:
            dialog.make_button(cmd[0], lambda: generic(cmd[1]))

            if num >= 1 and num <= 9:
                dialog.root.bind(str(num), lambda e: generic(cmd[1]))

        if commands:
            for i, cmd in enumerate(commands):
                make_button(cmd, i + 1)

        dialog.current_button = len(dialog.buttons) - 1
        dialog.show()

    @staticmethod
    def show_message(text: str) -> None:
        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()

        dialog.make_button("Ok", ok)
        dialog.current_button = 0
        dialog.show()

    @staticmethod
    def show_input(text: str, cmd_ok: Callable[..., Any],
                   cmd_cancel: Optional[Callable[..., Any]] = None, value: str = "") -> None:
        dialog = Dialog(text)
        entry = EntryBox(dialog.top_frame, font=app.theme.font, width=17, justify="center")

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

        entry.bind("<Escape>", lambda e: dialog.hide())
        entry.pack(padx=6, pady=6)
        dialog.make_button("Cancel", cancel)
        dialog.make_button("Ok", ok)
        dialog.show()
        dialog.current_button = 1
        entry.full_focus()

    @staticmethod
    def hide_all() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.hide()

    def __init__(self, text: str) -> None:
        self.buttons: List[ButtonBox] = []
        self.make(text)

        self.current_button: Optional[int] = None
        self.root.bind("<Left>", lambda e: self.left())
        self.root.bind("<Right>", lambda e: self.right())
        self.root.bind("<Return>", lambda e: self.enter())

        Dialog.current_dialog = self

    def make(self, text: str) -> None:
        background = app.theme.dialog_background
        foreground = app.theme.dialog_foreground
        border = app.theme.border_color

        self.root = tk.Frame(app.main_frame, bg=border)
        self.main = tk.Frame(self.root, bg=background)
        self.main.pack(padx=app.theme.border_width, pady=app.theme.border_width)
        self.root.lift()
        container = tk.Frame(self.main, padx=10, pady=4, bg=background)
        container.pack()
        tk.Label(container, text=text, font=app.theme.font, wraplength=500, bg=background, fg=foreground).pack(padx=6)
        self.top_frame = tk.Frame(container)
        self.top_frame.pack()
        self.button_frame = tk.Frame(container, bg=background)
        self.button_frame.pack()
        self.root.bind("<Escape>", lambda e: self.hide())
        self.root.bind("<FocusOut>", lambda e: self.hide())

    def show(self) -> None:
        self.root.update_idletasks()
        window_width = app.main_frame.winfo_width()
        window_height = app.main_frame.winfo_height()
        dialog_width = self.root.winfo_reqwidth()
        dialog_height = self.root.winfo_reqheight()
        x = (window_width - dialog_width) // 2
        y = (window_height - dialog_height) // 2
        self.root.place(x=x, y=y)
        self.root.focus_set()

    def hide(self) -> None:
        from .tooltips import ToolTip
        from .inputcontrol import inputcontrol
        from .keyboard import keyboard
        ToolTip.block()
        keyboard.block()
        inputcontrol.focus()
        self.root.destroy()
        Dialog.current_dialog = None

    def make_button(self, text: str, command: Callable[..., Any]) -> None:
        button = widgetutils.get_button(self.button_frame, text, command, bigger=True)
        button.pack(side=tk.LEFT, padx=6, pady=8)
        self.buttons.append(button)

    def left(self) -> None:
        if not len(self.buttons):
            return

        if self.current_button is None:
            self.current_button = len(self.buttons) - 1
        elif self.current_button > 0:
            self.current_button -= 1

        self.highlight_button()

    def right(self) -> None:
        if not len(self.buttons):
            return

        if self.current_button is None:
            self.current_button = 0
        elif self.current_button < len(self.buttons) - 1:
            self.current_button += 1

        self.highlight_button()

    def highlight_button(self) -> None:
        for i, button in enumerate(self.buttons):
            if i == self.current_button:
                button.set_style("highlight")
            else:
                button.set_style("normal")

    def enter(self) -> None:
        if self.current_button is not None:
            button = self.buttons[self.current_button]

            if button and button.command:
                button.command()
