# Standard
import tkinter as tk

# Modules
from .app import app
from .args import args

# Modules
from .buttonbox import ButtonBox
from .tooltips import ToolTip
from .tips import tips


class Bottom(tk.Frame):
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        super().__init__(parent)

        self.button = ButtonBox(
            self, text="Go To Bottom", command=self.to_bottom, bigger=True
        )

        ToolTip(self.button, tips["bottom"])
        self.button.grid(row=0, column=0, sticky="nsew")
        self.button.set_bind("<Button-4>", lambda e: self.scroll_up())
        self.button.set_bind("<Button-5>", lambda e: self.scroll_down())
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.tab_id = tab_id
        self.visible = True
        self.delay = 500
        self.show_debouncer = ""
        self.grid(row=2, column=0, sticky="nsew")

        if args.bottom_autohide:
            self.grid_remove()

    def do_show(self) -> None:
        if (not args.bottom) or (not self.visible):
            return

        self.grid()

    def cancel_show(self) -> None:
        if not self.show_debouncer:
            return

        app.root.after_cancel(self.show_debouncer)
        self.show_debouncer = ""

    def show(self) -> None:
        if not args.bottom_autohide:
            self.button.set_style("normal")
            self.button.set_text("Go To Bottom")
            return

        if (not args.bottom) or self.visible or (not app.exists()):
            return

        self.visible = True
        self.show_debouncer = app.root.after(self.delay, self.do_show)

    def hide(self) -> None:
        if not args.bottom_autohide:
            self.button.set_style("disabled")
            self.button.set_text("")
            return

        if (not self.visible) or (not app.exists()):
            return

        self.cancel_show()
        self.visible = False
        self.grid_remove()

    def to_bottom(self) -> None:
        from .display import display

        display.to_bottom(self.tab_id)

    def scroll_up(self) -> None:
        from .display import display

        display.scroll_up(self.tab_id)

    def scroll_down(self) -> None:
        from .display import display

        display.scroll_down(self.tab_id)

    def set_text(self, text: str) -> None:
        self.button.set_text(text)
