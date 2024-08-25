# Standard
import tkinter as tk

# Modules
from .app import app
from .args import args

# Modules
from .buttonbox import ButtonBox
from .tooltips import ToolTip
from .tips import tips
from .autoscroll import autoscroll


class Bottom(tk.Frame):
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        super().__init__(parent)
        self.bottom_text = "Go To Bottom"
        self.auto_scroll_text = "Auto-Scroll"

        self.bottom_button = ButtonBox(
            self, text=self.bottom_text, command=self.to_bottom
        )

        ToolTip(self.bottom_button, tips["bottom_button"])
        self.bottom_button.grid(row=0, column=0, sticky="nsew")
        self.bottom_button.set_bind("<Button-4>", lambda e: self.scroll_up())
        self.bottom_button.set_bind("<Button-5>", lambda e: self.scroll_down())
        self.bottom_button.set_bind("<Button-2>", lambda e: self.auto_scroll())
        self.bottom_button.set_bind("<ButtonRelease-3>", lambda e: self.auto_scroll())

        self.auto_scroll_button = ButtonBox(
            self, text=self.auto_scroll_text, command=self.auto_scroll, style="alt"
        )

        tip = f"Delay: {args.auto_scroll_delay} ms"
        ToolTip(self.auto_scroll_button, tip)

        if args.show_auto_scroll:
            self.auto_scroll_button.grid(row=0, column=1, sticky="nsew")

        self.auto_scroll_button.set_bind("<Button-2>", lambda e: self.auto_scroll())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.parent = parent
        self.tab_id = tab_id
        self.visible = True
        self.delay = 500
        self.show_debouncer = ""
        self.buttons_enabled = True
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
            self.bottom_button.set_text(self.bottom_text)
            self.auto_scroll_button.set_text(self.auto_scroll_text)
            self.check_auto_scroll()
            self.buttons_enabled = True
            return

        if (not args.bottom) or self.visible or (not app.exists()):
            return

        self.check_auto_scroll()
        self.visible = True
        self.show_debouncer = app.root.after(self.delay, self.do_show)

    def hide(self) -> None:
        if not args.bottom_autohide:
            self.bottom_button.set_style("disabled")
            self.bottom_button.set_text("")
            self.auto_scroll_button.set_style("disabled")
            self.auto_scroll_button.set_text("")
            self.buttons_enabled = False
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

        ToolTip.hide_all()
        display.scroll_up(self.tab_id, disable_auto_scroll=True)

    def scroll_down(self) -> None:
        from .display import display

        ToolTip.hide_all()
        display.scroll_down(self.tab_id, disable_auto_scroll=True)

    def set_text(self, text: str) -> None:
        self.bottom_button.set_text(text)

    def auto_scroll(self) -> None:
        autoscroll.toggle("down")

    def check_enabled(self) -> bool:
        return self.visible and self.buttons_enabled and app.exists()

    def on_auto_scroll_enabled(self) -> None:
        if not self.check_enabled():
            return

        self.auto_scroll_button.set_style("active")

    def on_auto_scroll_disabled(self) -> None:
        if not self.check_enabled():
            return

        self.auto_scroll_button.set_style("alt")

    def check_auto_scroll(self) -> None:
        if autoscroll.enabled:
            self.auto_scroll_button.set_style("active")
        else:
            self.auto_scroll_button.set_style("alt")
