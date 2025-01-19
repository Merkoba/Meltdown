from __future__ import annotations

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any
from collections.abc import Callable
from PIL import Image, ImageTk  # type: ignore
from pathlib import Path

# Modules
from .app import app
from .entrybox import EntryBox
from .buttonbox import ButtonBox
from .args import args
from .utils import utils
from .widgetutils import widgetutils


Answer = dict[str, Any]
Action = Callable[..., Any]


class Command:
    def __init__(self, text: str, cmd: Action, no_hide: bool = False) -> None:
        self.text = text
        self.cmd = cmd
        self.no_hide = no_hide

    def build(self, dialog: Dialog) -> None:
        def generic(func: Action) -> None:
            ans = {
                "entry": Dialog.get_entry(),
                "msgbox": Dialog.get_msgbox(),
            }

            if not self.no_hide:
                dialog.hide()

            func(ans)

        if dialog.commands:
            num_cmds = len(dialog.commands.items)
        else:
            num_cmds = 0

        dialog.make_button(self.text, lambda: generic(self.cmd), num_cmds)


class Commands:
    def __init__(self) -> None:
        self.items: list[Command] = []

    def add(self, text: str, cmd: Action, no_hide: bool = False) -> None:
        command = Command(text, cmd, no_hide)
        self.items.append(command)


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
    def get_msgbox() -> str:
        if Dialog.current_dialog:
            if Dialog.current_dialog.msgbox:
                return Dialog.current_dialog.msgbox.get("1.0", tk.END)

        return ""

    @staticmethod
    def show_dialog(
        text: str = "",
        commands: Commands | None = None,
        image: Path | None = None,
        use_entry: bool = False,
        entry_mode: str = "normal",
        value: str = "",
        top_frame: bool = False,
        image_width: int = 270,
        msgbox: str | None = None,
    ) -> None:
        from .menus import Menu

        if use_entry or msgbox:
            top_frame = True

        dialog = Dialog(text, top_frame=top_frame)

        # ------

        if image:
            img_file = Image.open(image)
            width, height = img_file.size
            new_width = image_width
            new_height = int(new_width * height / width)
            img = img_file.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(dialog.image_frame, image=photo)
            label.mlt_image = photo  # type: ignore
            label.pack(side=tk.LEFT, padx=0, pady=8)

        # ------

        if use_entry:
            dialog.entry = EntryBox(
                dialog.top_frame,
                font=app.theme.font(),
                width=app.theme.input_width,
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

            def clear() -> None:
                if not dialog.entry:
                    return

                dialog.entry.clear()

            def on_right_click(event: Any) -> None:
                if not dialog.entry:
                    return

                menu = Menu()
                text = dialog.entry.get()
                selected = dialog.entry.get_selected()

                if text:
                    menu.add(text="Copy", command=lambda e: copy(selected))

                menu.add(text="Paste", command=lambda e: paste())

                if text:
                    menu.add(text="Clear", command=lambda e: clear())

                menu.show(event)

            dialog.entry.bind("<Return>", lambda e: dialog.enter())
            dialog.entry.bind("<Escape>", lambda e: dialog.hide())
            dialog.entry.bind("<Button-3>", lambda e: on_right_click(e))
            dialog.entry.pack(padx=3, pady=3)

        # ------

        if msgbox:
            mbox_scrollbar_y = ttk.Scrollbar(
                dialog.top_frame, orient=tk.VERTICAL, style="Dialog.Vertical.TScrollbar"
            )

            dialog.msgbox = tk.Text(dialog.top_frame)
            dialog.msgbox.insert("1.0", msgbox)

            dialog.msgbox.configure(
                state="disabled", wrap=tk.WORD, font=app.theme.font()
            )

            dialog.msgbox.configure(
                height=app.theme.msgbox_height, width=app.theme.msgbox_width
            )

            dialog.msgbox.configure(background=app.theme.textbox_background)
            dialog.msgbox.configure(foreground=app.theme.textbox_foreground)
            dialog.msgbox.configure(borderwidth=0, highlightthickness=0)
            dialog.msgbox.configure(yscrollcommand=mbox_scrollbar_y.set)
            mbox_scrollbar_y.configure(command=dialog.msgbox.yview)
            mbox_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

            dialog.msgbox.pack(padx=3, pady=3)

        # ------

        dialog.commands = commands or None

        if commands:
            for cmd in commands.items:
                cmd.build(dialog)

        if commands:
            if dialog.entry:
                dialog.highlight_no_button()
            else:
                dialog.highlight_last_button()

        dialog.show()
        app.update()

        def focus() -> None:
            if dialog.entry:
                dialog.entry.focus_end()

        if dialog.entry:
            app.root.after(0, focus)

    @staticmethod
    def show_confirm(
        text: str,
        cmd_ok: Action | None = None,
        cmd_cancel: Action | None = None,
    ) -> None:
        def ok(ans: Answer) -> None:
            if cmd_ok:
                cmd_ok()

        def cancel(ans: Answer) -> None:
            if cmd_cancel:
                cmd_cancel()

        cmds = Commands()
        cmds.add("Cancel", cancel)
        cmds.add("Ok", ok)
        Dialog.show_dialog(text, cmds)

    @staticmethod
    def show_message(text: str, copy_text: str | None = None) -> None:
        def ok(ans: Answer) -> None:
            pass

        def copy(ans: Answer) -> None:
            ctext = copy_text or text
            utils.copy(ctext)

        cmds = Commands()
        cmds.add("Copy", copy)
        cmds.add("Ok", ok)
        Dialog.show_dialog(text, cmds)

    @staticmethod
    def show_msgbox(title: str, text: str) -> None:
        def ok(ans: Answer) -> None:
            pass

        def copy(ans: Answer) -> None:
            utils.copy(ans["msgbox"])

        cmds = Commands()
        cmds.add("Copy", copy)
        cmds.add("Ok", ok)
        Dialog.show_dialog(title, commands=cmds, msgbox=text)

    @staticmethod
    def show_input(
        text: str,
        cmd_ok: Action,
        cmd_cancel: Action | None = None,
        value: str = "",
        mode: str = "normal",
    ) -> None:
        def ok(ans: Answer) -> None:
            cmd_ok(ans["entry"])

        def cancel(ans: Answer) -> None:
            if cmd_cancel:
                cmd_cancel(None)

        def reveal(ans: Answer) -> None:
            if not Dialog.current_dialog:
                return

            if not Dialog.current_dialog.entry:
                return

            Dialog.current_dialog.entry.reveal()
            Dialog.current_dialog.entry.focus_start()

        cmds = Commands()

        if mode == "password":
            cmds.add("Cancel", cancel)
            cmds.add("Reveal", reveal, True)
            cmds.add("Ok", ok)
        else:
            cmds.add("Cancel", cancel)
            cmds.add("Ok", ok)

        Dialog.show_dialog(
            text,
            cmds,
            use_entry=True,
            entry_mode=mode,
            value=value,
        )

    @staticmethod
    def show_textbox(
        id_: str,
        text: str,
        cmd_ok: Action,
        cmd_cancel: Action | None = None,
        value: str = "",
        start_maximized: bool = False,
        on_right_click: Action | None = None,
    ) -> None:
        from .textbox import TextBox

        if Dialog.open():
            curr = Dialog.current_dialog

            if curr:
                if curr.id_ == id_:
                    tb = Dialog.current_textbox

                    if tb:
                        tb.focus_set()

                    return

        dialog = Dialog(text, top_frame=True, id_=id_)

        textbox = TextBox(
            dialog,
            text=text,
            cmd_ok=cmd_ok,
            cmd_cancel=cmd_cancel,
            on_right_click=on_right_click,
        )

        def do_max() -> None:
            textbox.max()

        dialog.make_button("Max", lambda: do_max())
        dialog.make_button("Cancel", textbox.cancel)
        dialog.make_button("Ok", textbox.ok)

        dialog.show()
        dialog.highlight_no_button()
        textbox.insert_text(value)
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

    def __init__(self, text: str, top_frame: bool = False, id_: str = "") -> None:
        Dialog.hide_all()

        self.id_ = id_
        self.buttons: list[ButtonBox] = []
        self.commands: Commands | None = None
        self.max_buttons = 8

        self.make(text, with_top_frame=top_frame)

        self.highlighted = False
        self.current_button: int | None = None
        self.entry: EntryBox | None = None
        self.msgbox: tk.Text | None = None

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

        def bind(widget: tk.Widget) -> None:
            widget.bind("<Escape>", lambda e: self.hide())
            widget.bind("<ButtonPress-1>", lambda e: Menu.hide_all())

            for child in widget.winfo_children():
                bind(child)

        bind(self.root)

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

    def make_button(self, text: str, command: Action, num_cmds: int = 0) -> None:
        button = widgetutils.get_button(self.buttons_frame, text, command)
        num = len(self.buttons)
        div = 3

        if num_cmds > self.max_buttons:
            row = num // div
            column = num % div
        else:
            row = 0
            column = num

        button.grid(row=row, column=column, padx=6, pady=8)
        self.buttons.append(button)
        self.root.bind(str(num + 1), lambda e: command())

    def left(self) -> None:
        if not len(self.buttons):
            return

        if self.current_button is None:
            new_index = len(self.buttons) - 1
        elif self.current_button > 0:
            new_index = self.current_button - 1
        elif args.wrap_menus:
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
        elif args.wrap_menus:
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

    def highlight_no_button(self) -> None:
        for button in self.buttons:
            button.set_style("normal")

        self.current_button = -1
        self.highlighted = False

    def enter(self) -> None:
        if self.current_button is not None:
            button = self.buttons[self.current_button]

            if button and button.command:
                button.command()

    def focus(self) -> None:
        self.root.focus_set()
