# Modules
from .config import config
from .widgets import widgets
from . import timeutils

# Standard
import json
from typing import Optional, Any
from pathlib import Path


def save_file(path: Path, obj: Any) -> None:
    with open(path, "w") as file:
        json.dump(obj, file, indent=4)


def load_files() -> None:
    load_config_file()
    load_models_file()
    load_inputs_file()
    load_systems_file()


def load_config_file() -> None:
    if not config.config_path.exists():
        config.config_path.parent.mkdir(parents=True, exist_ok=True)
        config.config_path.touch(exist_ok=True)

    with open(config.config_path, "r") as file:
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


def load_list_file(path: Path, key: str, list_key: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    with open(path, "r") as file:
        try:
            items = json.load(file)
        except BaseException:
            items = []
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


def add_model(model_path: str) -> None:
    add_to_list("models", model_path)


def add_input(text: str) -> None:
    add_to_list("inputs", text)


def add_system(text: str) -> None:
    add_to_list("systems", text)


def add_to_list(key: str, text: str) -> None:
    items = getattr(config, key)
    new_items = [item for item in items if item != text]
    new_items.insert(0, text)

    if len(new_items) > config.max_list_items:
        items.pop()

    setattr(config, key, new_items)
    path = getattr(config, key + "_path")
    save_file(path, new_items)


def update_config(key: str) -> bool:
    from .model import model
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
            model.load(config.model)
        elif key == "context":
            model.reset_context()
        elif key == "format":
            model.load(config.model)

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
        model.load(config.model)
        save_config()

    widgetutils.show_confirm("Reset config? This will remove your custom configs"
                             " and refresh the widgets.", reset, None)


def reset_one_config(key: str) -> None:
    from .model import model
    default = config.get_default(key)

    if getattr(config, key) == default:
        return

    setattr(config, key, default)
    widgets.fill_widget(key, getattr(config, key))

    if key == "format":
        model.load(config.model)
    elif key == "model":
        check_models(False)
        model.load(config.model)

    save_config()


def reset_list(key: str) -> None:
    from . import widgetutils

    def reset() -> None:
        setattr(config, key, [])
        widgets.fill()
        path = getattr(config, key + "_path")
        save_file(path, [])

    widgetutils.show_confirm(f"Reset this? This will empty the {key}.", reset, None)


def get_models_dir() -> Optional[str]:
    models = [config.model] + config.models

    for model in models:
        path = Path(model)

        if path.exists() and path.is_file():
            return str(path.parent)

    return None


def save_log() -> None:
    from . import widgetutils
    log = widgetutils.get_text(widgets.output)

    if log:
        clean_log = "\n".join(log.split("\n")[len(config.intro):]).strip()

        if not clean_log:
            return

        full_log = timeutils.date() + "\n\n" + clean_log
        config.logs_path.mkdir(parents=True, exist_ok=True)
        file_name = str(timeutils.now_int()) + ".txt"

        with open(Path(config.logs_path, file_name), "w") as file:
            file.write(full_log)

        widgets.print(f"\n>> Log saved as {file_name}")
