from __future__ import annotations

# Standard
import json
from typing import Any
from collections.abc import Callable
from tkinter import filedialog
from pathlib import Path

# Modules
from .utils import utils
from .memory import memory


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
        self.similar_threshold = 0.7
        self.trim_threshold = 15
        self.split_long_length = 35
        self.recent_label = "--- Recent ---"
        self.rentry_site = "https://rentry.org"

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
        self.default_seed = -1
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
        self.default_logits = "normal"

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
        self.logits = self.default_logits

        self.locals = [
            "theme",
            "font_size",
            "font_family",
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
        from .paths import paths
        from .args import args
        from .files import files

        if name == "last":
            self.save_last()
            return

        if not paths.configs.exists():
            paths.configs.mkdir(parents=True, exist_ok=True)

        if name:
            file_path = str(Path(paths.configs, f"{name}.json"))
        else:
            file_path = filedialog.asksaveasfilename(
                initialdir=paths.configs,
                defaultextension=".json",
                filetypes=[("Config Files", "*.json")],
            )

        if not file_path:
            return

        path = Path(file_path)
        conf = self.get_string()
        files.write(path, conf)
        memory.set_value("last_config", path.stem)

        if not args.quiet:
            utils.saved_path(path)

    def load_state(self, name: str | None = None) -> None:
        from .args import args
        from .paths import paths
        from .display import display
        from .files import files

        if name == "last":
            self.load_last()
            return

        if not paths.configs.exists():
            paths.configs.mkdir(parents=True, exist_ok=True)

        if name:
            fname = files.full_name(name)
            path = Path(paths.configs, fname)
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

        self.apply(path)
        self.after_load()
        memory.set_value("last_config", path.stem)

        if not args.quiet:
            utils.loaded_path(path)

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

    def set(
        self, key: str, value: Any, on_change: bool = True, prints: bool = False
    ) -> bool:
        from .model import model
        from .widgets import widgets
        from .display import display

        vtype = self.get_default(key).__class__

        if vtype is str:
            value = str(value)
        elif vtype is int:
            try:
                value = int(value)
            except BaseException:
                widgets.fill_widget(key, self.get_default(key))

                if prints:
                    display.print("Invalid value.")

                return False
        elif vtype is float:
            try:
                value = float(value)
            except BaseException:
                widgets.fill_widget(key, self.get_default(key))

                if prints:
                    display.print("Invalid value.")

                return False
        elif vtype is bool:
            if utils.is_bool_true(value):
                value = True
            elif utils.is_bool_false(value):
                value = False
            else:
                return False

        if key in self.validations:
            value = self.validations[key](value)

        current = getattr(self, key)
        widgets.fill_widget(key, value)

        if current == value:
            if prints:
                display.print("Already set to that.")

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
        from .dialogs import Dialog, Commands

        cmds = Commands()
        cmds.add("Open", lambda a: self.open_directory())
        cmds.add("Load", lambda a: self.load_state())
        cmds.add("Reset", lambda a: self.reset())
        cmds.add("Save", lambda a: self.save_state())

        Dialog.show_dialog("Config Menu", commands=cmds)

    def set_command(self, cmd: str) -> None:
        from .display import display
        from .args import args

        if not cmd:
            display.print("Format: [name] [value]")
            return

        name, value = utils.cmd_value(cmd)

        if not name:
            return

        name = name.strip()
        value = value.strip()

        if not hasattr(self, name):
            display.print("Invalid config.")
            return

        value = utils.empty_string(value)

        if value == "reset":
            self.reset_one(name, focus=False)
            value = ""
        elif not self.set(name, value, prints=True):
            return

        if not args.quiet:
            svalue = getattr(self, name)

            if svalue == "":
                svalue = "[Empty]"

            display.print(f"Config: `{name}` set to `{svalue}`", do_format=True)

    def command(self, cmd: str | None = None) -> None:
        if not cmd:
            self.menu()
            return

        self.set_command(cmd)

    def save_last(self) -> None:
        if not memory.last_config:
            return

        self.save_state(memory.last_config)

    def load_last(self) -> None:
        if not memory.last_config:
            return

        self.load_state(memory.last_config)

    def open_directory(self) -> None:
        from .app import app
        from .paths import paths

        paths.configs.mkdir(parents=True, exist_ok=True)
        app.open_generic(str(paths.configs))


config = Config()
