from __future__ import annotations

# Standard
import json
from typing import Any
from collections.abc import Callable
from tkinter import filedialog
from pathlib import Path

# Modules
from .utils import utils


class Config:
    def __init__(self) -> None:
        self.max_log = 50
        self.changes_delay = 250
        self.max_changes = 50
        self.max_file_list = 100
        self.save_delay = 500
        self.save_after = ""
        self.token_limit = 0.88
        self.max_name_length = 50
        self.max_file_name_length = 50
        self.max_tabs = 999
        self.similar_threshold = 0.7
        self.trim_threshold = 4

        self.default_system = """
Your name is ((name_ai)).
You are talking to ((name_user)).
No need to introduce yourself.
No need to greet me, just answer.
""".strip()

        self.default_avatar_user = "🥶"
        self.default_avatar_ai = "🫠"
        self.default_name_user = "Joe"
        self.default_name_ai = "Melt"
        self.default_context = 2048
        self.default_max_tokens = 2048
        self.default_temperature = 0.8
        self.default_top_k = 40
        self.default_top_p = 0.95
        self.default_model = ""
        self.default_history = 2
        self.default_seed = 326
        self.default_format = "auto"
        self.default_before = ""
        self.default_after = ""
        self.default_font_size = 14
        self.default_font_family = "sans-serif"
        self.default_threads = 6
        self.default_mlock = "yes"
        self.default_theme = "dark"
        self.default_gpu_layers = 33
        self.default_stop = "<|im_start|> ;; <|im_end|>"
        self.default_mode = "text"
        self.default_theme = "dark"
        self.default_last_log = ""
        self.default_logits = "normal"
        self.default_last_program = ""
        self.default_last_config = ""
        self.default_last_session = ""

        self.model = self.default_model
        self.name_user = self.default_name_user
        self.name_ai = self.default_name_ai
        self.max_tokens = self.default_max_tokens
        self.temperature = self.default_temperature
        self.system = self.default_system
        self.top_k = self.default_top_k
        self.top_p = self.default_top_p
        self.history = self.default_history
        self.seed = self.default_seed
        self.format = self.default_format
        self.before = self.default_before
        self.after = self.default_after
        self.font_size = self.default_font_size
        self.font_family = self.default_font_family
        self.threads = self.default_threads
        self.mlock = self.default_mlock
        self.theme = self.default_theme
        self.gpu_layers = self.default_gpu_layers
        self.context = self.default_context
        self.avatar_user = self.default_avatar_user
        self.avatar_ai = self.default_avatar_ai
        self.stop = self.default_stop
        self.mode = self.default_mode
        self.theme = self.default_theme
        self.last_log = self.default_last_log
        self.logits = self.default_logits
        self.last_program = self.default_last_program
        self.last_config = self.default_last_config
        self.last_session = self.default_last_session

        self.locals = [
            "theme",
            "font_size",
            "font_family",
            "last_log",
            "last_program",
            "last_config",
            "last_session",
        ]

        self.clearables = [
            "system",
            "before",
            "after",
            "stop",
            "input",
            "name_user",
            "name_ai",
            "avatar_user",
            "avatar_ai",
            "file",
        ]

        self.model_keys = [
            "model",
            "context",
            "threads",
            "gpu_layers",
            "mlock",
            "format",
            "mode",
            "logits",
        ]

        self.modes = ["text", "image"]

        self.validations: dict[str, Callable[..., Any]] = {
            "history": lambda x: max(0, x),
            "name_user": lambda x: self.get_default("name_user") if not x else x,
            "name_ai": lambda x: self.get_default("name_ai") if not x else x,
        }

    def defaults(self) -> dict[str, Any]:
        items: dict[str, Any] = {}

        for key in dir(self):
            if key.startswith("default_"):
                name = key.replace("default_", "")
                value = getattr(self, key)
                items[name] = value

        return items

    def get(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)

        return None

    def get_default(self, key: str) -> Any:
        name = f"default_{key}"

        if hasattr(self, name):
            return getattr(self, name)

        return None

    def print_config(self) -> None:
        from .display import display

        display.print("Config:")
        text = []

        for key in sorted(self.defaults()):
            value = getattr(self, key)

            if value == "":
                value = "[Empty]"

            text.append(f"{key}: {value}")

        display.print("\n".join(text))

    def get_string(self) -> str:
        conf = {}

        for key in self.defaults():
            if key in self.locals:
                continue

            conf[key] = getattr(self, key)

        return json.dumps(conf)

    def load(self) -> None:
        from .args import args

        if args.config:
            self.load_arg()
        else:
            self.load_file()

    def save_state(self, name: str | None = None) -> None:
        from .display import display
        from .paths import paths
        from .args import args
        from .files import files

        if name == "last":
            self.save_last()
            return

        if name:
            file_path = str(Path(paths.configs, f"{name}.json"))
        else:
            if not paths.configs.exists():
                paths.configs.mkdir(parents=True, exist_ok=True)

            file_path = filedialog.asksaveasfilename(
                initialdir=paths.configs,
                defaultextension=".json",
                filetypes=[("Config Files", "*.json")],
            )

        if not file_path:
            return

        path = Path(file_path)
        self.last_config = path.stem
        conf = self.get_string()
        files.write(path, conf)

        if not args.quiet:
            name = path.name
            msg = f'Config saved as "{name}"'
            display.print(utils.emoji_text(msg, "storage"))

    def load_state(self, name: str | None = None) -> None:
        from .args import args
        from .paths import paths
        from .display import display

        if name == "last":
            self.load_last()
            return

        if not paths.configs.exists():
            paths.configs.mkdir(parents=True, exist_ok=True)

        if name:
            path = Path(paths.configs, f"{name}.json")
        else:
            file_path = filedialog.askopenfilename(
                initialdir=paths.configs,
            )

            if not file_path:
                return

            path = Path(file_path)

        if (not path.exists()) or (not path.is_file()):
            if not args.quiet:
                display.print("Config file not found.")

            return

        self.last_config = path.stem
        self.apply(path)
        self.after_load()

        if not args.quiet:
            f_name = path.name
            msg = f'Loaded config "{f_name}"'
            display.print(utils.emoji_text(msg, "storage"))

    def after_load(self) -> None:
        from .widgets import widgets
        from .model import model

        widgets.fill()
        model.unload(True)
        self.save()

    def apply(self, path: Path) -> None:
        from .args import args
        from .files import files

        try:
            conf = files.load(path)
        except BaseException:
            if not args.quiet:
                utils.msg("Creating empty config.json")

            conf = {}

        for key in self.defaults():
            setattr(self, key, conf.get(key, getattr(self, key)))

    def load_file(self) -> None:
        from .paths import paths

        if not paths.config.exists():
            paths.config.parent.mkdir(parents=True, exist_ok=True)
            paths.config.touch(exist_ok=True)

        self.apply(paths.config)

    def load_arg(self) -> None:
        from .args import args
        from .paths import paths

        try:
            name = args.config

            if not name.endswith(".json"):
                name += ".json"

            path = Path(name)

            if (not path.exists()) or (not path.is_file()):
                path = Path(paths.configs, name)

            if (not path.exists()) or (not path.is_file()):
                args.config = ""
                self.load_file()
                return

            self.apply(path)
            self.save()
        except BaseException as e:
            utils.error(e)
            args.config = ""
            self.load_file()

    def clear_save(self) -> None:
        from .app import app

        if self.save_after:
            app.root.after_cancel(self.save_after)
            self.save_after = ""

    def save(self) -> None:
        from .app import app

        if not app.exists():
            return

        self.clear_save()
        self.save_after = app.root.after(self.save_delay, lambda: self.do_save())

    def do_save(self) -> None:
        from .paths import paths
        from .files import files

        self.clear_save()
        conf = {}

        for key in self.defaults():
            conf[key] = getattr(self, key)

        files.save(paths.config, conf)

    def update(self, key: str) -> bool:
        from .widgets import widgets

        if not hasattr(self, key):
            return False

        widget = getattr(widgets, key)

        if widget:
            return self.set(key, widget.get())

        return False

    def set_value(self, key: str, value: Any) -> None:
        if getattr(self, key) == value:
            return

        setattr(self, key, value)
        self.save()

    def set(self, key: str, value: Any, on_change: bool = True) -> bool:
        from .model import model
        from .widgets import widgets

        vtype = self.get_default(key).__class__

        if vtype == str:
            value = str(value)
        elif vtype == int:
            try:
                value = int(value)
            except BaseException:
                widgets.fill_widget(key, self.get_default(key))
                return False
        elif vtype == float:
            try:
                value = float(value)
            except BaseException:
                widgets.fill_widget(key, self.get_default(key))
                return False
        elif vtype == bool:
            value = bool(value)

        if key in self.validations:
            value = self.validations[key](value)

        current = getattr(self, key)
        widgets.fill_widget(key, value)

        if current == value:
            return False

        setattr(self, key, value)
        self.save()

        if on_change:
            if (key == "font_size") or (key == "font_family"):
                self.on_font_change(key)

            if key in self.model_keys:
                model.unload()

        return True

    def reset(self, force: bool = False) -> None:
        from .dialogs import Dialog

        keep = ("model",)

        def action() -> None:
            for key in self.defaults():
                if key in keep:
                    continue

                if key in self.locals:
                    continue

                default = self.get_default(key)

                if default is not None:
                    setattr(self, key, default)

            self.after_load()

        if force:
            action()
            return

        Dialog.show_confirm(
            "This will remove your custom configs\nand refresh the widgets", action
        )

    def reset_one(self, key: str, focus: bool = True, on_change: bool = True) -> None:
        from .widgets import widgets

        if not hasattr(self, key):
            return

        default = self.get_default(key)

        if getattr(self, key) == default:
            return

        self.set(key, default, on_change=on_change)
        widgets.fill_widget(key, getattr(self, key), focus=focus)

    def on_font_change(self, key: str) -> None:
        from .display import display

        display.update_font(key)

    def menu(self) -> None:
        from .dialogs import Dialog

        cmds = []
        cmds.append(("Reset", lambda a: self.reset()))
        cmds.append(("Load", lambda a: self.load_state()))
        cmds.append(("Save", lambda a: self.save_state()))

        Dialog.show_dialog("Config Menu", commands=cmds)

    def set_command(self, command: str) -> None:
        from .display import display
        from .args import args

        if not command:
            return

        parts = command.split(" ")

        if len(parts) < 2:
            return

        key = parts[0]

        if not hasattr(self, key):
            return

        value = " ".join(parts[1:])

        if value == "reset":
            self.reset_one(key, focus=False)

            if not args.quiet:
                display.print(f"{key}: {getattr(self, key)}")

            return

        self.set(key, value)

        if not args.quiet:
            display.print(f"{key}: {value}")

    def command(self, text: str | None = None) -> None:
        from .display import display

        if not text:
            self.menu()
            return

        if " " in text:
            self.set_command(text)
            return

        if hasattr(self, text):
            value = getattr(self, text)
            display.print(f"{text}: {value}")

    def save_last(self) -> None:
        if not self.last_config:
            return

        self.save_state(self.last_config)

    def load_last(self) -> None:
        if not self.last_config:
            return

        self.load_state(self.last_config)


config = Config()
