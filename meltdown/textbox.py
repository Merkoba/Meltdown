# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional, Callable, List, Tuple

# Modules
from .app import app
from .args import args
from .dialogs import Dialog
from .keyboard import keyboard


class TextBox(tk.Text):
    def __init__(self, dialog: Dialog, text: str,
                 cmd_ok: Callable[..., Any],
                 cmd_cancel: Optional[Callable[..., Any]] = None,
                 commands: Optional[List[Tuple[str, Callable[..., Any]]]] = None) -> None:

        from .changes import Changes

        super().__init__(dialog.top_frame, undo=False)
        self.configure(font=app.theme.font("textbox"))
        self.configure(width=30, height=5)
        self.configure(highlightthickness=0)

        scrollbar_y = ttk.Scrollbar(dialog.top_frame, orient=tk.VERTICAL, style="Dialog.Vertical.TScrollbar")
        scrollbar_x = ttk.Scrollbar(dialog.top_frame, orient=tk.HORIZONTAL, style="Dialog.Horizontal.TScrollbar")

        self.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        if args.wrap_textbox:
            self.configure(wrap=tk.WORD)
        else:
            self.configure(wrap=tk.NONE)

        scrollbar_y.configure(command=self.yview)
        scrollbar_x.configure(command=self.xview)

        self.maxed = False
        self.dialog = dialog
        self.cmd_ok = cmd_ok
        self.cmd_cancel = cmd_cancel
        self.text = text
        self.commands = commands

        self.bind("<Control-v>", lambda e: self.paste())
        self.bind("<Return>", lambda e: self.on_enter())
        self.bind("<Escape>", lambda e: dialog.hide())
        self.bind("<Control-KeyPress-a>", lambda e: self.select_all())

        self.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        if args.scrollbars:
            scrollbar_y.grid(row=0, column=1, sticky="ns")

            if not args.wrap_textbox:
                scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.changes = Changes(self)

    def get_ans(self) -> Dict[str, Any]:
        return {"text": self.get_text(), "maxed": self.maxed}

    def ok(self) -> None:
        ans = self.get_ans()
        self.dialog.hide()
        self.cmd_ok(ans)

    def cancel(self) -> None:
        ans = self.get_ans()
        self.dialog.hide()

        if self.cmd_cancel:
            self.cmd_cancel(ans)

    def on_enter(self) -> None:
        if keyboard.ctrl:
            self.ok()

    def get_text(self) -> str:
        return self.get("1.0", tk.END).strip()

    def change_value(self) -> str:
        return self.get_text()

    def max(self) -> None:
        if self.maxed:
            value = self.get_text()
            self.dialog.hide()

            Dialog.show_textbox(self.text, self.cmd_ok,
                                self.cmd_cancel, value=value, commands=self.commands)
        else:
            self.maximize()
            self.maxed = True

    def select_all(self) -> str:
        self.tag_add("sel", "1.0", tk.END)
        return "break"

    def maximize(self) -> None:
        self.dialog.root.place(x=0, y=0, width=app.main_frame.winfo_width(),
                               height=app.main_frame.winfo_height())

        self.dialog.root.grid_columnconfigure(0, weight=1)
        self.dialog.root.grid_rowconfigure(0, weight=1)

        self.dialog.main.grid_columnconfigure(0, weight=1)
        self.dialog.main.grid_rowconfigure(0, weight=1)

        self.dialog.container.grid_columnconfigure(0, weight=1)
        self.dialog.container.grid_rowconfigure(1, weight=1)

        self.dialog.top_frame.grid_columnconfigure(0, weight=1)
        self.dialog.top_frame.grid_rowconfigure(0, weight=1)

        self.focus_set()

    def paste(self) -> None:
        try:
            start = self.index(tk.SEL_FIRST)
            end = self.index(tk.SEL_LAST)
            self.delete(start, end)
        except tk.TclError:
            pass

    def set_text(self, text: str, on_change: bool = True) -> None:
        self.delete("1.0", tk.END)
        self.insert("1.0", text)

        if on_change:
            self.changes.on_change()
