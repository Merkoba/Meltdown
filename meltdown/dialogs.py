# Modules
from .app import app
from .entrybox import EntryBox
from .buttonbox import ButtonBox
from .args import args
from . import widgetutils

# Standard
from typing import Any, Callable, List, Optional, Tuple
import tkinter as tk
from PIL import Image, ImageTk  # type: ignore
from pathlib import Path


class Dialog:
    current_dialog: Optional["Dialog"] = None

    @staticmethod
    def open() -> bool:
        return Dialog.current_dialog is not None

    @staticmethod
    def show_confirm(text: str, cmd_ok: Optional[Callable[..., Any]] = None,
                     cmd_cancel: Optional[Callable[..., Any]] = None) -> None:
        if Dialog.open():
            return

        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()

            if cmd_ok:
                cmd_ok()

        def cancel() -> None:
            dialog.hide()

            if cmd_cancel:
                cmd_cancel()

        dialog.make_button("Cancel", cancel)
        dialog.make_button("Ok", ok)
        dialog.highlight_button(1)
        dialog.show()

    @staticmethod
    def show_commands(text: str,
                      commands: List[Tuple[str, Callable[..., Any]]],
                      image: Optional[Path] = None) -> None:
        if Dialog.open():
            return

        dialog = Dialog(text)

        if image:
            img = Image.open(image)
            width, height = img.size
            new_width = 270
            new_height = int(new_width * height / width)
            img = img.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(dialog.image_frame, image=photo)
            label.mlt_image = photo  # type: ignore
            label.pack(side=tk.LEFT, padx=0, pady=8)

        def generic(func: Callable[..., Any]) -> None:
            dialog.hide()
            func()

        def make_button(cmd: Tuple[str, Callable[..., Any]]) -> None:
            dialog.make_button(cmd[0], lambda: generic(cmd[1]))

        if commands:
            for cmd in commands:
                make_button(cmd)

        dialog.highlight_button(len(dialog.buttons) - 1)
        dialog.show()

    @staticmethod
    def show_message(text: str) -> None:
        if Dialog.open():
            return

        dialog = Dialog(text)

        def ok() -> None:
            dialog.hide()

        dialog.make_button("Ok", ok)
        dialog.highlight_button(0)
        dialog.show()

    @staticmethod
    def show_input(text: str, cmd_ok: Callable[..., Any],
                   cmd_cancel: Optional[Callable[..., Any]] = None, value: str = "") -> None:
        if Dialog.open():
            return

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

        entry.bind("<Return>", lambda e: dialog.enter())
        entry.bind("<Escape>", lambda e: dialog.hide())
        entry.bind("<Down>", lambda e: dialog.root.focus_set())
        dialog.root.bind("<Up>", lambda e: entry.focus_set())
        entry.pack(padx=6, pady=6)
        dialog.make_button("Cancel", cancel)
        dialog.make_button("Ok", ok)
        dialog.show()
        dialog.highlight_button(1)
        entry.full_focus()

    @staticmethod
    def hide_all() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.hide()

    @staticmethod
    def focus() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.root.focus_set()

    def __init__(self, text: str) -> None:
        self.buttons: List[ButtonBox] = []
        self.make(text)

        self.highlighted = False
        self.current_button: Optional[int] = None
        self.root.bind("<Left>", lambda e: self.left())
        self.root.bind("<Right>", lambda e: self.right())
        self.root.bind("<Return>", lambda e: self.enter())

        Dialog.current_dialog = self

    def make(self, text: str) -> None:
        background = app.theme.dialog_background
        foreground = app.theme.dialog_foreground
        border = app.theme.dialog_border

        self.root = tk.Frame(app.main_frame, background=border)
        self.main = tk.Frame(self.root, background=background)
        bwidth = app.theme.dialog_border_width
        self.main.pack(padx=bwidth, pady=bwidth)
        self.root.lift()
        container = tk.Frame(self.main, padx=10, pady=4, background=background)
        container.pack()
        tk.Label(container, text=text, font=app.theme.font, wraplength=500, background=background, foreground=foreground).pack(padx=6)
        self.top_frame = tk.Frame(container)
        self.top_frame.pack()
        self.image_frame = tk.Frame(container, background=background)
        self.image_frame.pack()
        self.button_frame = tk.Frame(container, background=background)
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
        num = len(self.buttons)
        self.root.bind(str(num), lambda e: command())

    def left(self) -> None:
        if not len(self.buttons):
            return

        if self.current_button is None:
            new_index = len(self.buttons) - 1
        elif self.current_button > 0:
            new_index = self.current_button - 1
        else:
            if args.wrap:
                new_index = len(self.buttons) - 1
            else:
                return

        self.highlight_button(new_index)

    def right(self) -> None:
        if not len(self.buttons):
            return

        if self.current_button is None:
            new_index = 0
        elif self.current_button < len(self.buttons) - 1:
            new_index = self.current_button + 1
        else:
            if args.wrap:
                new_index = 0
            else:
                return

        self.highlight_button(new_index)

    def highlight_button(self, index: int) -> None:
        self.current_button = index

        for i, button in enumerate(self.buttons):
            if i == index:
                button.set_style("highlight")
            else:
                button.set_style("normal")

        self.highlighted = True

    def enter(self) -> None:
        if self.current_button is not None:
            button = self.buttons[self.current_button]

            if button and button.command:
                button.command()
