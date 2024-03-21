# Modules
from .buttonbox import ButtonBox
from .app import app

# Standard
import tkinter as tk


class Bottom(tk.Frame):
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        super().__init__(parent)
        self.button = ButtonBox(self, text="Go To Bottom", command=self.to_bottom, bigger=True)
        self.button.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.tab_id = tab_id
        self.visible = True
        self.grid(row=1, column=0, sticky="nsew")
        self.grid_remove()

    def show(self) -> None:
        if self.visible or (not app.exists()):
            return

        self.visible = True
        self.grid()

    def hide(self) -> None:
        if (not self.visible) or (not app.exists()):
            return

        self.visible = False
        self.grid_remove()

    def to_bottom(self) -> None:
        from .display import display
        display.to_bottom(self.tab_id)
