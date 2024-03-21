# Modules
from .buttonbox import ButtonBox
from .app import app
from .output import Output

# Standard
import tkinter as tk


class Bottom(tk.Frame):
    def __init__(self, parent: tk.Frame, tab_id: str, output: Output) -> None:
        super().__init__(parent)
        self.button = ButtonBox(self, text="Go To Bottom", command=self.to_bottom, bigger=True)
        self.button.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.tab_id = tab_id
        self.visible = True
        self.debouncer = ""
        self.delay = 200
        self.output = output
        self.grid(row=1, column=0, sticky="nsew")
        self.grid_remove()

    def cancel_debouncer(self) -> None:
        if self.debouncer:
            app.root.after_cancel(self.debouncer)

    def show(self) -> None:
        self.cancel_debouncer()

        if not self.visible and app.exists():
            self.debouncer = app.root.after(self.delay, self.do_show)

    def do_show(self) -> None:
        if self.visible or (not app.exists()):
            return

        self.cancel_debouncer()
        self.visible = True
        self.grid()

    def hide(self) -> None:
        self.cancel_debouncer()

        if self.visible and app.exists():
            self.debouncer = app.root.after(self.delay, self.do_hide)

    def do_hide(self) -> None:
        if (not self.visible) or (not app.exists()):
            return

        self.cancel_debouncer()
        self.visible = False
        self.grid_remove()

    def to_bottom(self) -> None:
        from .display import display
        display.to_bottom(self.tab_id)
