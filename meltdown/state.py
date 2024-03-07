# Modules
from .config import config
from .widgets import widgets
from . import timeutils

# Standard
import json
from typing import Optional, Any, IO
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
    if not config.config_path.exists():
        config.config_path.parent.mkdir(parents=True, exist_ok=True)
        config.config_path.touch(exist_ok=True)

    with open(config.config_path, "r") as file:
        apply_config(file)


def get_config_string() -> str:
    conf = {}

    for key in config.defaults():
        conf[key] = getattr(config, key)

    return json.dumps(conf)


def save_config_state() -> None:
    if not config.configs_path.exists():
        config.configs_path.mkdir(parents=True, exist_ok=True)

    file_path = filedialog.asksaveasfilename(
        initialdir=config.configs_path,
        defaultextension=".json",
        filetypes=[("Config Files", "*.json")],
    )

    if not file_path:
        return

    conf = get_config_string()

    with open(file_path, "w") as file:
        file.write(conf)


def load_config_state() -> None:
    if not config.configs_path.exists():
        config.configs_path.mkdir(parents=True, exist_ok=True)

    file_path = filedialog.askopenfilename(
        initialdir=config.configs_path,
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
    load_list_file(config.models_path, "model", "models")
    check_models()


def load_inputs_file() -> None:
    load_list_file(config.inputs_path, "input", "inputs")


def load_systems_file() -> None:
    load_list_file(config.systems_path, "system", "systems")


def load_prepends_file() -> None:
    load_list_file(config.prepends_path, "system", "prepends")


def load_appends_file() -> None:
    load_list_file(config.appends_path, "system", "appends")


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

    save_file(config.config_path, conf)


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
    path = getattr(config, key + "_path")
    save_file(path, new_items)


def update_config(key: str) -> bool:
    vtype = config.get_default(key).__class__
    widget = getattr(widgets, key)
    valuestr = widget.get()

    if vtype == str:
        value = valuestr
    elif vtype == int:
        try:
            value = int(valuestr)
        except BaseException as e:
            print(e)
            return False
    elif vtype == float:
        try:
            value = float(valuestr)
        except BaseException as e:
            print(e)
            return False

    current = getattr(config, key)

    if value != current:
        setattr(config, key, value)

        if key == "model":
            on_model_change()
        elif key == "context":
            on_context_change()
        elif key == "format":
            on_format_change()

        save_config()
        return True

    return False


def reset_config() -> None:
    from . import widgetutils
    from .model import model

    def reset() -> None:
        for key in config.defaults():
            setattr(config, key, config.get_default(key))

        check_models(False)
        widgets.fill()
        model.load()
        save_config()

    widgetutils.show_confirm("This will remove your custom configs"
                             "\nand refresh the widgets", reset, None)


def reset_one_config(key: str) -> None:
    default = config.get_default(key)

    if getattr(config, key) == default:
        return

    setattr(config, key, default)
    widgets.fill_widget(key, getattr(config, key))

    if key == "model":
        on_model_change()
    elif key == "context":
        on_context_change()
    elif key == "format":
        on_format_change()

    save_config()


def get_models_dir() -> Optional[str]:
    models = [config.model] + config.models

    for model in models:
        path = Path(model)

        if path.exists() and path.is_file():
            return str(path.parent)

    return None


def save_log() -> None:
    log = widgets.get_output()

    if log:
        log = timeutils.date() + "\n\n" + log
        config.logs_path.mkdir(parents=True, exist_ok=True)
        file_name = str(timeutils.now_int()) + ".txt"
        logpath = Path(config.logs_path, file_name)

        with open(logpath, "w") as file:
            file.write(log)

        widgets.print(f"\n>> Log saved as {file_name}")
        print(f"Log saved at {logpath}")


def on_model_change() -> None:
    from .model import model
    check_models(False)
    model.unload()


def on_context_change() -> None:
    from .model import model
    model.reset_context()


def on_format_change() -> None:
    from .model import model
    model.load()
