from __future__ import annotations

# Modules
from .app import app
from .config import config
from .entrybox import EntryBox
from .textbox import TextBox


class Changes:
    def __init__(self, widget: EntryBox | TextBox) -> None:
        self.widget = widget
        self.changes_delay = config.changes_delay
        self.changes_after = ""
        self.changes: list[str] = [""]
        self.changes_index = 0

        widget.bind("<Control-KeyPress-z>", lambda e: self.undo())
        widget.bind("<Control-KeyPress-Z>", lambda e: self.undo())
        widget.bind("<Control-Shift-KeyPress-z>", lambda e: self.redo())
        widget.bind("<Control-Shift-KeyPress-Z>", lambda e: self.redo())

    def undo(self) -> None:
        self.changes_index -= 1

        if self.changes_index < 0:
            self.changes_index = 0
            return

        text = self.changes[self.changes_index]
        self.widget.set_text(text, on_change=False)

    def redo(self) -> None:
        self.changes_index += 1

        if self.changes_index >= len(self.changes):
            self.changes_index = len(self.changes) - 1
            return

        text = self.changes[self.changes_index]
        self.widget.set_text(text, on_change=False)

    def on_change(self) -> None:
        if self.changes_after:
            app.root.after_cancel(self.changes_after)

        self.changes_after = app.root.after(
            self.changes_delay, lambda: self.do_on_change()
        )

    def do_on_change(self) -> None:
        if not self.widget.winfo_exists():
            return

        text = self.widget.change_value()

        if self.changes[-1] == text:
            return

        self.changes.append(text)

        if len(self.changes) > 50:
            self.changes = self.changes[-config.max_changes :]

        self.changes_index = len(self.changes) - 1
