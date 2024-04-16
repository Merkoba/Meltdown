# Standard
import os
import json
from typing import Any, List
from pathlib import Path

# Modules
from .paths import paths
from .config import config
from .args import args
from .utils import utils


class Files:
    def __init__(self) -> None:
        self.models_list: List[str] = []
        self.inputs_list: List[str] = []
        self.systems_list: List[str] = []
        self.prepends_list: List[str] = []
        self.appends_list: List[str] = []

        self.models_loaded = False
        self.inputs_loaded = False
        self.systems_loaded = False
        self.prepends_loaded = False
        self.appends_loaded = False

    def save(self, path: Path, dictionary: Any) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    def load(self) -> None:
        if args.config:
            config.load_arg()
        else:
            config.load_file()

    def load_list(self, key: str) -> None:
        path: Path = getattr(paths, key)

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        with open(path, "r", encoding="utf-8") as file:
            name = f"{key}_list"

            try:
                items = json.load(file)
            except BaseException as e:
                utils.error(e)
                items = []

                if hasattr(self, name):
                    item = getattr(self, name)

                    if item:
                        items.append(item)

            setattr(self, name, items)

    def add_model(self, text: str) -> None:
        self.add_to_list("models", text)

    def add_input(self, text: str) -> None:
        self.add_to_list("inputs", text)

    def add_system(self, text: str) -> None:
        self.add_to_list("systems", text)

    def add_prepends(self, text: str) -> None:
        self.add_to_list("prepends", text)

    def add_appends(self, text: str) -> None:
        self.add_to_list("appends", text)

    def add_to_list(self, key: str, text: str) -> None:
        if not text:
            return

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

    def open_log(self, name: str = "") -> None:
        from .app import app

        path = paths.logs
        path.mkdir(parents=True, exist_ok=True)
        os_name = os.name.lower()

        if name:
            path = Path(path, name)

        spath = str(path)

        if os_name == "posix":
            # Linux
            app.run_command(["xdg-open", spath])
        elif os_name == "nt":
            # Windows
            app.run_command(["start", spath])
        elif os_name == "darwin":
            # macOS
            app.run_command(["open", spath])
        else:
            utils.error(f"Unrecognized OS: {os_name}")

    def get_list(self, what: str) -> List[str]:
        if not getattr(self, f"{what}_loaded"):
            self.load_list(what)

        lst = getattr(self, f"{what}_list")
        return lst or []


files = Files()
