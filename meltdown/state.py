# Modules
from .paths import paths
from .config import config
from .widgets import widgets
from . import dialogs
from . import timeutils

# Standard
import os
import json
from typing import Optional, Any, IO, List
from pathlib import Path
from tkinter import filedialog


def save_file(path: Path, obj: Any) -> None:
    with open(path, "w") as file:
        json.dump(obj, file, indent=4)


def load_files() -> None:
    load_config_file()
    load_models_file()
    load_inputs_file()
    load_systems_file()
    load_prepends_file()
    load_appends_file()


def load_config_file() -> None:
    if not paths.config.exists():
        paths.config.parent.mkdir(parents=True, exist_ok=True)
        paths.config.touch(exist_ok=True)

    with open(paths.config, "r") as file:
        apply_config(file)


def get_config_string() -> str:
    conf = {}

    for key in config.defaults():
        conf[key] = getattr(config, key)

    return json.dumps(conf)


def save_config_state() -> None:
    if not paths.configs.exists():
        paths.configs.mkdir(parents=True, exist_ok=True)

    file_path = filedialog.asksaveasfilename(
        initialdir=paths.configs,
        defaultextension=".json",
        filetypes=[("Config Files", "*.json")],
    )

    if not file_path:
        return

    conf = get_config_string()

    with open(file_path, "w") as file:
        file.write(conf)


def load_config_state() -> None:
    if not paths.configs.exists():
        paths.configs.mkdir(parents=True, exist_ok=True)

    file_path = filedialog.askopenfilename(
        initialdir=paths.configs,
    )

    if not file_path:
        return

    path = Path(file_path)

    if (not path.exists()) or (not path.is_file()):
        return

    with open(path, "r") as file:
        apply_config(file)
        widgets.fill()


def apply_config(file: IO[str]) -> None:
    try:
        conf = json.load(file)
    except BaseException:
        conf = {}

    for key in config.defaults():
        setattr(config, key, conf.get(key, getattr(config, key)))


def load_models_file() -> None:
    load_list_file(paths.models, "model", "models")
    check_models()


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

    with open(path, "r") as file:
        try:
            items = json.load(file)
        except BaseException:
            items = []

            if hasattr(config, key):
                item = getattr(config, key)

                if item:
                    items.append(item)

        setattr(config, list_key, items)


def save_config() -> None:
    conf = {}

    for key in config.defaults():
        conf[key] = getattr(config, key)

    save_file(paths.config, conf)


def check_models(save: bool = True) -> None:
    if (not config.model) and config.models:
        config.model = config.models[0]

        if save:
            save_config()


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
    new_items = new_items[:config.max_list_items]
    setattr(config, key, new_items)
    path = getattr(paths, key)
    save_file(path, new_items)


def update_config(key: str) -> bool:
    if not hasattr(config, key):
        return False

    vtype = config.get_default(key).__class__
    widget = getattr(widgets, key)
    valuestr = widget.get()

    if vtype == str:
        value = valuestr
    elif vtype == int:
        try:
            value = int(valuestr)
        except BaseException as e:
            widgets.fill_widget(key, config.get_default(key))
            return False
    elif vtype == float:
        try:
            value = float(valuestr)
        except BaseException as e:
            widgets.fill_widget(key, config.get_default(key))
            return False

    current = getattr(config, key)

    if value != current:
        set_config(key, value)
        setattr(config, key, value)
        return True

    return False


def set_config(key: str, value: Any) -> None:
    setattr(config, key, value)
    save_config()

    if key == "model":
        on_model_change()
    elif key == "format":
        on_format_change()


def reset_config() -> None:
    from .app import app
    from .model import model

    def reset() -> None:
        for key in config.defaults():
            default = config.get_default(key)

            if default is not None:
                setattr(config, key, default)

        on_model_change(False)
        on_format_change(False)
        widgets.fill()
        app.check_compact()
        save_config()
        model.unload(True)

    dialogs.show_confirm("This will remove your custom configs"
                         "\nand refresh the widgets", reset, None)


def reset_one_config(key: str) -> None:
    default = config.get_default(key)

    if getattr(config, key) == default:
        return

    set_config(key, default)
    widgets.fill_widget(key, getattr(config, key), focus=True)


def get_models_dir() -> Optional[str]:
    models = [config.model] + config.models

    for model in models:
        path = Path(model)

        if path.exists() and path.is_file():
            return str(path.parent)

    return None


def save_log() -> None:
    dialogs.show_confirm("Save the output to a file?", do_save_log, None)


def do_save_log() -> None:
    text = widgets.display.get_output_text()

    if not text:
        return

    lines = text.splitlines()
    new_lines = []

    for line in lines:
        if line.startswith(">> Log saved as"):
            continue

        new_lines.append(line)

    text = "\n".join(new_lines)
    text = timeutils.date() + "\n\n" + text
    name = widgets.display.get_current_tab_name().lower()
    name = name.replace(" ", "_")
    paths.logs.mkdir(parents=True, exist_ok=True)
    file_name = name + ".txt"
    file_path = Path(paths.logs, file_name)
    num = 2

    while file_path.exists():
        file_name = f"{name}_{num}.txt"
        file_path = Path(paths.logs, file_name)
        num += 1

        if num > 9999:
            break

    with open(file_path, "w") as file:
        file.write(text)

    widgets.display.print(f"\n>> Log saved as {file_name}")
    print(f"Log saved at {file_path}")


def on_model_change(unload: bool = True) -> None:
    from .model import model
    check_models(False)

    if model.loaded_model != config.model:
        if unload:
            model.unload()


def on_format_change(load: bool = True) -> None:
    from .model import model

    if model.loaded_format != config.format:
        if load:
            model.load()


def open_logs_dir() -> None:
    from .app import app
    path = paths.logs
    path.mkdir(parents=True, exist_ok=True)
    os_name = os.name.lower()

    if os_name == "posix":
        # Linux
        app.run_command([f"xdg-open", str(path)])
    elif os_name == "nt":
        # Windows
        app.run_command([f"start", str(path)])
    elif os_name == "darwin":
        # macOS
        app.run_command([f"open", str(path)])
    else:
        print(f"Unrecognized OS: {os_name}")
