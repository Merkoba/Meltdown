# Modules
from config import config
from config import ConfigDefaults
from widgets import widgets

# Standard
import json
from typing import Optional
from pathlib import Path

saved_configs = [
    "model",
    "name_1",
    "name_2",
    "max_tokens",
    "temperature",
    "system",
    "top_k",
    "top_p",
]


def load_config_file() -> None:
    if not config.config_path.exists():
        config.config_path.parent.mkdir(parents=True, exist_ok=True)
        config.config_path.touch(exist_ok=True)

    with open(config.config_path, "r") as file:
        try:
            conf = json.load(file)
        except BaseException:
            conf = {}

        for key in saved_configs:
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


def check_models(save: bool = True) -> None:
    if (not config.model) and config.models:
        config.model = config.models[0]

        if save:
            save_config(False)


def save_config(announce: bool = True) -> None:
    conf = {}

    for key in saved_configs:
        conf[key] = getattr(config, key)

    with open(config.config_path, "w") as file:
        json.dump(conf, file, indent=4)

    if announce:
        widgets.print("Config saved.")


def save_models() -> None:
    with open(config.models_path, "w") as file:
        json.dump(config.models, file, indent=4)

    widgets.print("Models saved.")


def update_name_1() -> None:
    name_1 = widgets.name_1.get()

    if name_1 and (name_1 != config.name_1):
        config.name_1 = name_1
        save_config()


def update_name_2() -> None:
    name_2 = widgets.name_2.get()

    if name_2 and (name_2 != config.name_2):
        config.name_2 = name_2
        save_config()


def update_max_tokens() -> None:
    max_tokens_str = widgets.max_tokens.get()

    try:
        max_tokens = int(max_tokens_str)
    except BaseException:
        return

    if max_tokens and (max_tokens != config.max_tokens):
        config.max_tokens = max_tokens
        save_config()


def update_temperature() -> None:
    temperature_str = widgets.temperature.get()

    try:
        temperature = float(temperature_str)
    except BaseException:
        return

    if temperature and (temperature != config.temperature):
        config.temperature = temperature
        save_config()


def update_system() -> None:
    system = widgets.system.get()

    if system and (system != config.system):
        config.system = system
        save_config()


def update_model() -> None:
    from model import model
    model_path = widgets.model.get()

    if not model_path:
        return

    if model_path != config.model:
        config.model = model_path
        save_config()

    add_model(model_path)
    model.load(model_path)


def update_top_k() -> None:
    top_k_str = widgets.top_k.get()

    try:
        top_k = int(top_k_str)
    except BaseException:
        return

    if top_k and (top_k != config.top_k):
        config.top_k = top_k
        save_config()


def update_top_p() -> None:
    top_p_str = widgets.top_p.get()

    try:
        top_p = float(top_p_str)
    except BaseException:
        return

    if top_p and (top_p != config.top_p):
        config.top_p = top_p
        save_config()


def add_model(model_path: str) -> None:
    config.models = [item for item in config.models if item != model_path]
    config.models.insert(0, model_path)
    save_models()


def do_reset_config() -> None:
    for key in saved_configs:
        setattr(config, key, getattr(ConfigDefaults, key))

    check_models(False)
    save_config()
    widgets.fill()


def reset_config() -> None:
    import widgetutils
    widgetutils.show_confirm("Reset config?", do_reset_config, None)


def do_reset_models() -> None:
    config.models = []
    save_models()
    widgets.fill()


def reset_models() -> None:
    import widgetutils
    widgetutils.show_confirm("Reset models?", do_reset_models, None)


def get_models_dir() -> Optional[str]:
    models = [config.model] + config.models

    for model in models:
        path = Path(model)

        if path.exists() and path.is_file():
            return str(path.parent)

    return None


def models_info() -> None:
    import widgetutils
    widgetutils.show_message("The models you load are saved here automatically.")
