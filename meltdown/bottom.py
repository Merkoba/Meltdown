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

        self.bottom_button = ButtonBox(
            self, text="Go To Bottom", command=self.to_bottom
        )

        ToolTip(self.bottom_button, tips["bottom_button"])
        self.bottom_button.grid(row=0, column=0, sticky="nsew")
        self.bottom_button.set_bind("<Button-4>", lambda e: self.scroll_up())
        self.bottom_button.set_bind("<Button-5>", lambda e: self.scroll_down())

        self.auto_scroll_button = ButtonBox(
            self, text="Auto-Scroll", command=self.auto_scroll, style="alt"
        )

        tip = f"Delay: {args.auto_scroll_delay} ms"
        ToolTip(self.auto_scroll_button, tip)
        self.auto_scroll_button.grid(row=0, column=1, sticky="nsew")

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
            self.bottom_button.set_style("normal")
            self.bottom_button.set_text("Go To Bottom")
            return

        if (not args.bottom) or self.visible or (not app.exists()):
            return

        self.visible = True
        self.show_debouncer = app.root.after(self.delay, self.do_show)

    def hide(self) -> None:
        if not args.bottom_autohide:
            self.bottom_button.set_style("disabled")
            self.bottom_button.set_text("")
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
        self.bottom_button.set_text(text)

    def auto_scroll(self) -> None:
        from .display import display

        display.toggle_auto_scroll()

    def on_auto_scroll_enabled(self) -> None:
        self.auto_scroll_button.set_font(app.theme.font("button_highlight"))

    def on_auto_scroll_disabled(self) -> None:
        self.auto_scroll_button.set_font(app.theme.font("button"))
