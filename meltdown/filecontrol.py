from __future__ import annotations

# Standard
from typing import Any

# Modules
from .app import app
from .tooltips import ToolTip
from .entrybox import EntryBox
from .widgetutils import widgetutils
from .tips import tips
from .files import files
from .filepicker import FilePicker


class FileControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.file: EntryBox

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

        initial_dir = widgets.get_dir(None, "files")
        file = FilePicker.create("Load File", initial_dir)

        if file:
            self.set(file)

    def set(self, text: str) -> None:
        self.file.set_text(text)
        self.file.move_to_end()

    def show_context(self, event: Any = None, only_items: bool = False) -> None:
        from .widgets import widgets

        widgets.show_menu_items(
            "file",
            "files",
            lambda m: self.set(m),
            event,
            only_items=only_items,
            alt_cmd=lambda m: self.forget(m, event),
        )

    def forget(self, text: str, event: Any) -> None:
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

    def apply_history(self, inputs: list[str]) -> None:
        text = inputs[self.history_index]
        self.set(text)
        self.file.focus_end()

    def get_history_list(self) -> list[str]:
        return files.get_list("files")

    def history_up(self) -> None:
        files = self.get_history_list()

        if not files:
            return

        if self.history_index == -1:
            self.history_index = 0
        else:
            if self.history_index == len(files) - 1:
                self.clear()
                return

            self.history_index = (self.history_index + 1) % len(files)

        self.apply_history(files)

    def history_down(self) -> None:
        files = self.get_history_list()

        if not files:
            return

        if self.history_index == -1:
            self.history_index = len(files) - 1
        else:
            if self.history_index == 0:
                self.clear()
                return

            self.history_index = (self.history_index - 1) % len(files)

        self.apply_history(files)

    def clear(self) -> None:
        self.file.clear()
        self.reset_history_index()

    def reset_history_index(self) -> None:
        self.history_index = -1


filecontrol = FileControl()
