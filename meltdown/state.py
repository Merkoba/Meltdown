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
    if not config.models_path.exists():
        config.models_path.parent.mkdir(parents=True, exist_ok=True)
        config.models_path.touch(exist_ok=True)

    with open(config.models_path, "r") as file:
        try:
            models = json.load(file)
        except BaseException:
            models = []

            if config.model:
                models.append(config.model)

        config.models = models

    check_models()


def load_inputs_file() -> None:
    if not config.inputs_path.exists():
        config.inputs_path.parent.mkdir(parents=True, exist_ok=True)
        config.inputs_path.touch(exist_ok=True)

    with open(config.inputs_path, "r") as file:
        try:
            inputs = json.load(file)
        except BaseException:
            inputs = []

        config.inputs = inputs


def check_models(save: bool = True) -> None:
    if (not config.model) and config.models:
        config.model = config.models[0]

        if save:
            save_config()


def save_config() -> None:
    conf = {}

    for key in config.defaults():
        conf[key] = getattr(config, key)

    save_file(config.config_path, conf)


def add_model(model_path: str) -> None:
    config.models = [item for item in config.models if item != model_path]
    config.models.insert(0, model_path)

    if len(config.models) > 100:
        config.models.pop()

    save_models()


def save_models() -> None:
    save_file(config.models_path, config.models)


def add_input(text: str) -> None:
    config.inputs = [item for item in config.inputs if item != text]
    config.inputs.insert(0, text)

    if len(config.inputs) > 100:
        config.inputs.pop()

    save_inputs()


def save_inputs() -> None:
    save_file(config.inputs_path, config.inputs)


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
            add_model(config.model)
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
        save_config()
        model.load(config.model)

    widgetutils.show_confirm("Reset config? This will remove your custom configs"
                             " and refresh the widgets.", reset, None)


def reset_one_config(key: str) -> None:
    from .model import model
    default = config.get_default(key)

    if getattr(config, key) == default:
        return

    setattr(config, key, default)
    widgets.fill_widget(key, getattr(config, key))
    save_config()

    if key == "format":
        model.load(config.model)


def reset_models() -> None:
    from . import widgetutils

    def reset() -> None:
        config.models = []
        widgets.fill()
        save_models()

    widgetutils.show_confirm("Reset models? This will empty the list"
                             " of recent models.", reset, None)


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
