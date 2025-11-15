from __future__ import annotations

# Standard
import tkinter as tk
from typing import Any

# Modules
from .app import app
from .config import config
from .model import model
from .entrybox import EntryBox
from .files import files
from .filepicker import FilePicker


class ModelControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.model: EntryBox

    def fill(self) -> None:
        from .widgets import widgets

        self.model = widgets.model

    def bind(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_context(e))

    def show_context(
        self,
        event: Any = None,
        only_items: bool = False,
        target: tk.Widget | None = None,
    ) -> None:
        from .widgets import widgets

        if model.model_loading:
            return

        widgets.show_menu_items(
            "model",
            "models",
            lambda m: self.set(m),
            event,
            only_items=only_items,
            alt_cmd=lambda m: self.forget(m, event),
            target=target,
        )

    def set(self, m: str) -> None:
        config.set("model", m)

    def apply_history(self, inputs: list[str]) -> None:
        text = inputs[self.history_index]
        self.set(text)
        self.model.focus_end()

    def get_history_list(self) -> list[str]:
        return files.get_list("models")

    def history_up(self) -> None:
        models = self.get_history_list()

        if not models:
            return

        if self.history_index == -1:
            self.history_index = 0
        else:
            self.history_index = (self.history_index + 1) % len(models)

        self.apply_history(models)

    def history_down(self) -> None:
        models = self.get_history_list()

        if not models:
            return

        if self.history_index == -1:
            self.history_index = len(models) - 1
        else:
            self.history_index = (self.history_index - 1) % len(models)

        self.apply_history(models)

    def reset_history_index(self) -> None:
        self.history_index = -1

    def forget(self, m: str, event: Any) -> None:
        files.remove_model(m)
        self.show_context(event)

    def show_recent(self, event: Any = None, target: tk.Widget | None = None) -> None:
        self.show_context(event, only_items=True, target=target)

    def browse(self) -> None:
        from .widgets import widgets

        if model.model_loading:
            return

        initial_dir = widgets.get_dir("model", "models")
        file = FilePicker.create("Select Model", initial_dir)

        if file:
            self.set(file)

    def change(self, name: str) -> None:
        if not name:
            return

        name = name.lower()
        list = files.get_list("models")

        if not list:
            return

        for item in list:
            if name in item.lower():
                self.set(item)
                return

    def is_focused(self) -> bool:
        focused = app.focused()

        if not focused:
            return False

        if isinstance(focused, EntryBox):
            return focused == self.model

        return False


modelcontrol = ModelControl()
