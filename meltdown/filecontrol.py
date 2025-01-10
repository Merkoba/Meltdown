from __future__ import annotations

# Standard
from typing import Any
from tkinter import filedialog

# Modules
from .tooltips import ToolTip
from .commands import commands
from .config import config
from .entrybox import EntryBox
from .args import args
from .paths import paths
from .dialogs import Dialog
from .tips import tips
from .utils import utils
from .files import files
from .menus import Menu
from . import widgetutils


class FileControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.input: EntryBox
        self.autocomplete: list[str] = []
        self.last_delete_press = 0.0

    def fill(self) -> None:
        from .widgets import widgets

        frame_data = widgets.frame_data_file
        self.file_label = widgetutils.make_label(frame_data, "File")
        self.file = widgetutils.make_entry(frame_data)
        frame_data.expand()
        widgets.file = self.file
        self.file.bind_mousewheel()
        ToolTip(self.file_label, tips["file"])
        ToolTip(self.file, tips["file"])

        self.recent_files_button = widgetutils.make_button(
            frame_data, "Recent", lambda: self.show_recent()
        )

        ToolTip(self.recent_files_button, tips["recent_files_button"])

        self.browse_file_button = widgetutils.make_button(
            frame_data, "Browse", lambda: self.browse()
        )

        ToolTip(self.browse_file_button, tips["browse_file_button"])

        self.open_file_button = widgetutils.make_button(
            frame_data, "Open", lambda: self.open_file()
        )

        ToolTip(self.open_file_button, tips["open_file_button"])

    def bind(self) -> None:
        self.file.bind("<Button-3>", lambda e: self.show_menu(e))

    def browse(self) -> None:
        from .widgets import widgets

        file = filedialog.askopenfilename(initialdir=widgets.get_dir(None, "files"))

        if file:
            self.set_file(file)

    def set_file(self, text: str) -> None:
        self.file.set_text(text)
        self.file.move_to_end()

    def show_context(self, event: Any = None, only_items: bool = False) -> None:
        from .widgets import widgets

        widgets.show_menu_items(
            "file",
            "files",
            lambda m: self.set_file(m),
            event,
            only_items=only_items,
            alt_cmd=lambda m: self.forget_file(m, event),
        )

    def forget_file(self, text: str, event: Any) -> None:
        files.remove_file(text)
        self.show_context(event)

    def show_recent(self) -> None:
        self.show_context(only_items=True)

    def show_menu(self, event: Any = None) -> None:
        self.show_context(event)

    def open_file(self) -> None:
        file = self.file.get()

        if not file:
            files.open_last_file()
            return

        app.open_generic(file)


filecontrol = FileControl()