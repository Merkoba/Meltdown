from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any
from collections.abc import Callable
from PIL import Image, ImageTk
from pathlib import Path

# Modules
from .app import app
from .entrybox import EntryBox
from .buttonbox import ButtonBox
from .args import args
from .utils import utils
from . import widgetutils


Answer = dict[str, Any]


class Dialog:
    current_dialog: Dialog | None = None
    current_textbox: tk.Widget | None = None

    @staticmethod
    def open() -> bool:
        return Dialog.current_dialog is not None

    @staticmethod
    def get_entry() -> str:
        if Dialog.current_dialog:
            if Dialog.current_dialog.entry:
                return Dialog.current_dialog.entry.get()

        return ""

    @staticmethod
    def show_dialog(
        text: str,
        commands: list[tuple[str, Callable[..., Any]]] | None = None,
        image: Path | None = None,
        use_entry: bool = False,
        entry_mode: str = "normal",
        value: str = "",
        top_frame: bool = False,
        image_width: int = 270,
    ) -> None:
        from .menus import Menu

        dialog = Dialog(text, top_frame=top_frame)

        # ------

        if image:
            img = Image.open(image)
            width, height = img.size
            new_width = image_width
            new_height = int(new_width * height / width)
            img = img.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(img)  # type: ignore
            label = tk.Label(dialog.image_frame, image=photo)  # type: ignore
            label.mlt_image = photo  # type: ignore
            label.pack(side=tk.LEFT, padx=0, pady=8)

        # ------

        if use_entry:
            dialog.entry = EntryBox(
                dialog.top_frame,
                font=app.theme.font(),
                width=20,
                justify="center",
                style="Dialog.TEntry",
                mode=entry_mode,
            )

            if value:
                dialog.entry.insert(0, value)

            def copy(text: str | None = None) -> None:
                if not dialog.entry:
                    return

                if not text:
                    text = dialog.entry.get()

                if not text:
                    return

                utils.copy(text)
                dialog.entry.focus_set()

            def paste() -> None:
                if not dialog.entry:
                    return

                utils.paste(dialog.entry)
                dialog.entry.focus_set()

            def on_right_click(event: Any) -> None:
                if not dialog.entry:
                    return

                menu = Menu()
                text = dialog.entry.get()
                selected = dialog.entry.get_selected()

                if text:
                    menu.add(text="Copy", command=lambda e: copy(selected))

                menu.add(text="Paste", command=lambda e: paste())
                menu.show(event)

            def entry_up() -> None:
                dialog.root.focus_set()

            dialog.root.bind("<Up>", lambda e: entry_up())
            dialog.entry.bind("<Return>", lambda e: dialog.enter())
            dialog.entry.bind("<Escape>", lambda e: dialog.hide())
            dialog.entry.bind("<Down>", lambda e: dialog.root.focus_set())
            dialog.entry.bind("<Button-3>", lambda e: on_right_click(e))
            dialog.entry.pack(padx=3, pady=3)

        # ------

        def make_cmd(cmd: tuple[str, Callable[..., Any]]) -> None:
            def generic(func: Callable[..., Any]) -> None:
                ans = {"entry": Dialog.get_entry()}
                dialog.hide()
                func(ans)

            dialog.make_button(cmd[0], lambda: generic(cmd[1]))

        if commands:
            for cmd in commands:
                make_cmd(cmd)

        if commands:
            dialog.highlight_last_button()

        dialog.show()

        if dialog.entry:
            dialog.entry.focus_end()

    @staticmethod
    def show_confirm(
        text: str,
        cmd_ok: Callable[..., Any] | None = None,
        cmd_cancel: Callable[..., Any] | None = None,
    ) -> None:
        def ok(ans: Answer) -> None:
            if cmd_ok:
                cmd_ok()

        def cancel(ans: Answer) -> None:
            if cmd_cancel:
                cmd_cancel()

        Dialog.show_dialog(text, [("Cancel", cancel), ("Ok", ok)])

    @staticmethod
    def show_message(text: str) -> None:
        def ok(ans: Answer) -> None:
            pass

        Dialog.show_dialog(text, [("Ok", ok)])

    @staticmethod
    def show_input(
        text: str,
        cmd_ok: Callable[..., Any],
        cmd_cancel: Callable[..., Any] | None = None,
        value: str = "",
        mode: str = "normal",
    ) -> None:
        def ok(ans: Answer) -> None:
            cmd_ok(ans["entry"])

        def cancel(ans: Answer) -> None:
            if cmd_cancel:
                cmd_cancel()

        Dialog.show_dialog(
            text,
            [("Cancel", cancel), ("Ok", ok)],
            use_entry=True,
            entry_mode=mode,
            value=value,
            top_frame=True,
        )

    @staticmethod
    def show_textbox(
        id: str,
        text: str,
        cmd_ok: Callable[..., Any],
        cmd_cancel: Callable[..., Any] | None = None,
        value: str = "",
        start_maximized: bool = False,
        on_right_click: Callable[..., Any] | None = None,
    ) -> None:
        from .textbox import TextBox

        if Dialog.open():
            curr = Dialog.current_dialog

            if curr:
                if curr.id == id:
                    tb = Dialog.current_textbox

                    if tb:
                        tb.focus_set()

                    return

        dialog = Dialog(text, top_frame=True, id=id)

        textbox = TextBox(
            dialog,
            text=text,
            cmd_ok=cmd_ok,
            cmd_cancel=cmd_cancel,
            on_right_click=on_right_click,
        )

        def do_max() -> None:
            dialog.focus_hide_enabled = False
            textbox.max()

        dialog.make_button("Max", lambda: do_max())
        dialog.make_button("Cancel", textbox.cancel)
        dialog.make_button("Ok", textbox.ok)

        dialog.show()
        dialog.highlight_last_button()
        textbox.insert(tk.END, value)
        textbox.focus_set()

        Dialog.current_textbox = textbox

        if start_maximized:
            textbox.max()

    @staticmethod
    def hide_all() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.hide()

    @staticmethod
    def focus_all() -> None:
        if Dialog.current_dialog:
            Dialog.current_dialog.focus()

    def __init__(self, text: str, top_frame: bool = False, id: str = "") -> None:
        Dialog.hide_all()

        self.id = id
        self.buttons: list[ButtonBox] = []

        self.make(text, with_top_frame=top_frame)

        self.highlighted = False
        self.current_button: int | None = None
        self.entry: EntryBox | None = None

        self.root.bind("<Left>", lambda e: self.left())
        self.root.bind("<Right>", lambda e: self.right())
        self.root.bind("<Return>", lambda e: self.enter())

        Dialog.current_dialog = self
        Dialog.current_textbox = None

    def make(self, text: str, with_top_frame: bool = False) -> None:
        from .menus import Menu

        background = app.theme.dialog_background
        foreground = app.theme.dialog_foreground
        border = app.theme.dialog_border

        self.root = tk.Frame(app.main_frame, background=border)
        self.main = tk.Frame(self.root, background=background)
        bwidth = app.theme.dialog_border_width
        self.main.grid(row=0, column=0, padx=bwidth, pady=bwidth, sticky="nsew")
        self.root.lift()

        self.container = tk.Frame(self.main, padx=10, pady=4, background=background)
        self.container.grid(row=0, column=0, sticky="nsew")

        text_label = tk.Label(self.container, text=text, font=app.theme.font())

        text_label.configure(
            wraplength=500, background=background, foreground=foreground
        )

        text_label.grid(row=0, column=0, sticky="nsew")

        if with_top_frame:
            self.top_frame = tk.Frame(self.container)
            self.top_frame.grid(row=1, column=0, sticky="nsew")
            self.top_frame.configure(background=app.theme.dialog_top_frame)

        self.image_frame = tk.Frame(self.container, background=background)
        self.image_frame.grid(row=2, column=0)

        self.buttons_frame = tk.Frame(self.container, background=background)
        self.buttons_frame.grid(row=3, column=0)

        self.focus_hide_enabled = True

        def bind(widget: tk.Widget) -> None:
            widget.bind("<Escape>", lambda e: self.hide())
            widget.bind("<ButtonPress-1>", lambda e: Menu.hide_all())
            widget.bind("<FocusOut>", lambda e: self.focus_hide())

            for child in widget.winfo_children():
                bind(child)

        bind(self.root)

    def focus_hide(self) -> None:
        if self.focus_hide_enabled:
            self.hide()

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
        from .menus import Menu

        if Menu.current_menu:
            return

        ToolTip.block()
        keyboard.block()
        inputcontrol.focus()
        self.root.destroy()
        Dialog.current_dialog = None

    def make_button(self, text: str, command: Callable[..., Any]) -> None:
        button = widgetutils.get_button(self.buttons_frame, text, command)
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
        elif args.wrap:
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
        elif args.wrap:
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

    def highlight_last_button(self) -> None:
        self.highlight_button(len(self.buttons) - 1)

    def enter(self) -> None:
        if self.current_button is not None:
            button = self.buttons[self.current_button]

            if button and button.command:
                button.command()

    def focus(self) -> None:
        self.root.focus_set()
