# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional, Callable

# Modules
from .app import app
from .args import args
from .dialogs import Dialog
from .keyboard import keyboard


class TextBox(tk.Text):
    def __init__(
        self,
        dialog: Dialog,
        text: str,
        cmd_ok: Callable[..., Any],
        cmd_cancel: Optional[Callable[..., Any]] = None,
        on_right_click: Optional[Callable[..., Any]] = None,
    ) -> None:
        from .changes import Changes

        super().__init__(dialog.top_frame, undo=False)
        self.configure(font=app.theme.font("textbox"))
        self.configure(width=30, height=5)
        self.configure(highlightthickness=0)

        scrollbar_y = ttk.Scrollbar(
            dialog.top_frame, orient=tk.VERTICAL, style="Dialog.Vertical.TScrollbar"
        )
        scrollbar_x = ttk.Scrollbar(
            dialog.top_frame, orient=tk.HORIZONTAL, style="Dialog.Horizontal.TScrollbar"
        )

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
        self.on_right_click = on_right_click
        self.text = text
        self.set_binds()

        self.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        if args.scrollbars:
            scrollbar_y.grid(row=0, column=1, sticky="ns")

            if not args.wrap_textbox:
                scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.changes = Changes(self)

    def set_binds(self) -> None:
        self.bind("<ButtonRelease-3>", lambda e: self.right_click(e))
        self.bind("<Tab>", lambda e: self.on_tab())
        self.bind("<Control-v>", lambda e: self.paste())
        self.bind("<Return>", lambda e: self.on_enter())
        self.bind("<Escape>", lambda e: self.dialog.hide())
        self.bind("<Control-KeyPress-a>", lambda e: self.select_all())
        self.bind("<Left>", lambda e: self.on_left())
        self.bind("<Right>", lambda e: self.on_right())

    def on_tab(self) -> str:
        from .autocomplete import autocomplete

        autocomplete.check(widget=self)
        return "break"

    def right_click(self, event: Any) -> None:
        if not self.on_right_click:
            return

        self.on_right_click(event, self)

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

            Dialog.show_textbox(
                self.text,
                self.cmd_ok,
                self.cmd_cancel,
                value=value,
            )
        else:
            self.maximize()
            self.maxed = True

    def select_all(self) -> str:
        self.tag_add("sel", "1.0", tk.END)
        return "break"

    def deselect_all(self) -> None:
        self.tag_remove("sel", "1.0", tk.END)

    def maximize(self) -> None:
        self.dialog.root.place(
            x=0,
            y=0,
            width=app.main_frame.winfo_width(),
            height=app.main_frame.winfo_height(),
        )

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

    def delete_text(self, start: int, chars: int) -> None:
        insert_index = self.index(tk.INSERT)
        line = int(insert_index.split(".")[0])
        s_start = f"{line}.{start}"
        s_end = f"{line}.{start + chars}"
        self.delete(s_start, s_end)

    def insert_text(self, text: str, index: int = -1) -> None:
        insert_index = self.index(tk.INSERT)

        if index < 0:
            index = int(insert_index.split(".")[1])

        line = int(insert_index.split(".")[0])
        s_index = f"{line}.{index}"
        self.insert(s_index, text)

    def on_left(self) -> str:
        from .keyboard import keyboard

        if keyboard.ctrl or keyboard.shift:
            return ""

        if self.tag_ranges("sel"):
            self.mark_set(tk.INSERT, tk.SEL_FIRST)
            self.tag_remove(tk.SEL, "1.0", tk.END)
            return "break"

        return ""

    def on_right(self) -> str:
        from .keyboard import keyboard

        if keyboard.ctrl or keyboard.shift:
            return ""

        if self.tag_ranges("sel"):
            self.mark_set(tk.INSERT, tk.SEL_LAST)
            self.tag_remove(tk.SEL, "1.0", tk.END)
            return "break"

        return ""
