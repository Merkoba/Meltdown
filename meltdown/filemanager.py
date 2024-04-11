# Standard
import os
import json
from typing import Any
from pathlib import Path

# Modules
from .paths import paths
from .config import config
from .args import args
from . import utils


def save(path: Path, dictionary: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(dictionary, file, indent=4)


def load() -> None:
    if args.config:
        config.load_arg()
    else:
        config.load_file()

    load_models_file()
    load_inputs_file()
    load_systems_file()
    load_prepends_file()
    load_appends_file()


def load_models_file() -> None:
    from .model import model
    load_list_file(paths.models, "model", "models")
    model.check_config()


def load_inputs_file() -> None:
    load_list_file(paths.inputs, "input", "inputs")


def load_systems_file() -> None:
    load_list_file(paths.systems, "system", "systems")


def load_prepends_file() -> None:
    load_list_file(paths.prepends, "prepend", "prepends")


def load_appends_file() -> None:
    load_list_file(paths.appends, "append", "appends")


def load_list_file(path: Path, key: str, list_key: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    with open(path, "r", encoding="utf-8") as file:
        try:
            items = json.load(file)
        except BaseException:
            items = []

            if hasattr(config, key):
                item = getattr(config, key)

                if item:
                    items.append(item)

        setattr(config, list_key, items)


def add_model(text: str) -> None:
    add_to_list("models", text)


def add_input(text: str) -> None:
    add_to_list("inputs", text)


def add_system(text: str) -> None:
    add_to_list("systems", text)


def add_prepends(text: str) -> None:
    add_to_list("prepends", text)


def add_appends(text: str) -> None:
    add_to_list("appends", text)


def add_to_list(key: str, text: str) -> None:
    if not text:
        return

    items = getattr(config, key)
    new_items = [item for item in items if item != text]
    new_items.insert(0, text)
    new_items = new_items[:args.max_list_items]
    setattr(config, key, new_items)
    path = getattr(paths, key)
    save(path, new_items)


def open_log(name: str = "") -> None:
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
