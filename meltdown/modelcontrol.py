from __future__ import annotations

# Standard
from typing import Any

# Modules
from .model import model
from .entrybox import EntryBox
from .files import files


class ModelControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.model: EntryBox

    def fill(self) -> None:
        from .widgets import widgets

        self.model = widgets.model

    def bind(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_context(e))

    def show_context(self, event: Any = None, only_items: bool = False) -> None:
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
        )

    def set(self, text: str) -> None:
        self.model.set_text(text)
        self.model.move_to_end()

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
            if self.history_index == len(models) - 1:
                self.clear()
                return

            self.history_index = (self.history_index + 1) % len(models)

        self.apply_history(models)

    def history_down(self) -> None:
        models = self.get_history_list()

        if not models:
            return

        if self.history_index == -1:
            self.history_index = len(models) - 1
        else:
            if self.history_index == 0:
                self.clear()
                return

            self.history_index = (self.history_index - 1) % len(models)

        self.apply_history(models)

    def clear(self) -> None:
        self.model.clear()
        self.reset_history_index()

    def reset_history_index(self) -> None:
        self.history_index = -1

    def forget(self, m: str, event: Any) -> None:
        files.remove_model(m)
        self.show_context(event)

    def show_recent(self) -> None:
        self.show_context(only_items=True)


modelcontrol = ModelControl()
