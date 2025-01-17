from __future__ import annotations

# Standard
import json
from typing import Any
from pathlib import Path

# Modules
from .app import app
from .paths import paths
from .config import config
from .args import args


class Files:
    def __init__(self) -> None:
        self.models_list: list[str] = []
        self.inputs_list: list[str] = []
        self.systems_list: list[str] = []
        self.files_list: list[str] = []

        self.models_loaded = False
        self.inputs_loaded = False
        self.systems_loaded = False
        self.files_loaded = False

    def save(self, path: Path, dictionary: Any) -> None:
        with path.open("w", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    def load_list(self, key: str) -> None:
        path: Path = getattr(paths, key)

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        name = f"{key}_list"

        try:
            items = self.load(path)
        except BaseException:
            items = []

            if hasattr(self, name):
                item = getattr(self, name)

                if item:
                    items.append(item)

        setattr(self, name, items)

    def add_model(self, text: str) -> None:
        self.add_to_list("models", text)

    def remove_model(self, text: str) -> None:
        self.remove_from_list("models", text)

    def add_input(self, text: str) -> None:
        self.add_to_list("inputs", text)

    def remove_input(self, text: str) -> None:
        self.remove_from_list("inputs", text)

    def add_system(self, text: str) -> None:
        if text == config.default_system:
            return

        self.add_to_list("systems", text)

    def remove_system(self, text: str) -> None:
        self.remove_from_list("systems", text)

    def add_file(self, text: str) -> None:
        self.add_to_list("files", text)

    def remove_file(self, text: str) -> None:
        self.remove_from_list("files", text)

    def add_to_list(self, key: str, text: str) -> None:
        if not text:
            return

        text = text[: args.list_item_max_length]

        if not getattr(self, f"{key}_loaded"):
            self.load_list(key)

        name = f"{key}_list"
        items = getattr(self, name)
        new_items = [item for item in items if item != text]
        new_items.insert(0, text)
        new_items = new_items[: config.max_file_list]
        setattr(self, name, new_items)
        path = getattr(paths, key)
        self.save(path, new_items)

    def remove_from_list(self, key: str, text: str) -> None:
        if not text:
            return

        if not getattr(self, f"{key}_loaded"):
            self.load_list(key)

        name = f"{key}_list"
        items = getattr(self, name)
        new_items = [item for item in items if item != text]
        setattr(self, name, new_items)
        path = getattr(paths, key)
        self.save(path, new_items)

    def get_list(self, what: str) -> list[str]:
        if not getattr(self, f"{what}_loaded"):
            self.load_list(what)

        lst = getattr(self, f"{what}_list")
        return lst or []

    def open_last_file(self) -> None:
        if self.files_list:
            file = self.files_list[0]
            app.open_generic(file)

    def load(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def read(self, path: Path) -> str:
        with path.open("r", encoding="utf-8") as file:
            return file.read().strip()

    def write(self, path: Path, text: str) -> None:
        with path.open("w", encoding="utf-8") as file:
            file.write(text)

    def clean_path(self, path: str) -> str:
        return path.replace("file://", "", 1)

    def full_name(self, name: str, ext: str = "json") -> str:
        if name.endswith(f".{ext}"):
            return name

        return f"{name}.{ext}"


files = Files()
