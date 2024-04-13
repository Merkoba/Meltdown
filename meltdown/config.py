# Standard
import json
from typing import List, Any, Dict, Optional, Callable, IO
from tkinter import filedialog
from pathlib import Path

# Modules
from . import utils


class Config:
    def __init__(self) -> None:
        self.max_log = 50
        self.input_memory_max = 30
        self.changes_delay = 250

        # Added for mypy
        self.models: List[str] = []
        self.inputs: List[str] = []

        system_lines = [
            "Your name is @name_ai.",
            "You are talking to @name_user.",
            "The current date is @date.",
        ]

        self.default_name_user: str = "Joe"
        self.default_name_ai: str = "Melt"
        self.default_max_tokens: int = 0
        self.default_temperature: float = 0.8
        self.default_system: str = "\n".join(system_lines)
        self.default_top_k: int = 40
        self.default_top_p: float = 0.95
        self.default_model: str = ""
        self.default_history: int = 1
        self.default_seed: int = 326
        self.default_format: str = "auto"
        self.default_prepend: str = ""
        self.default_append: str = ""
        self.default_compact: bool = False
        self.default_output_font_size: int = 14
        self.default_threads: int = 6
        self.default_mlock: str = "yes"
        self.default_theme: str = "dark"
        self.default_gpu_layers = 33
        self.default_context = 2048
        self.default_avatar_user = "👽"
        self.default_avatar_ai = "😎"

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
        self.prepend = self.default_prepend
        self.append = self.default_append
        self.compact = self.default_compact
        self.output_font_size = self.default_output_font_size
        self.threads = self.default_threads
        self.mlock = self.default_mlock
        self.theme = self.default_theme
        self.gpu_layers = self.default_gpu_layers
        self.context = self.default_context
        self.avatar_user = self.default_avatar_user
        self.avatar_ai = self.default_avatar_ai

        self.clearables = [
            "system",
            "prepend",
            "append",
            "input",
            "name_user",
            "name_ai",
            "avatar_user",
            "avatar_ai",
        ]

        self.model_keys = [
            "model",
            "context",
            "threads",
            "gpu_layers",
            "mlock",
            "format",
        ]

        self.validations: Dict[str, Callable[..., Any]] = {
            "history": lambda x: max(0, x),
        }

    def defaults(self) -> Dict[str, Any]:
        items: Dict[str, Any] = {}

        for key in dir(self):
            if key.startswith("default_"):
                name = key.replace("default_", "")
                value = getattr(self, key)
                items[name] = value

        return items

    def get_default(self, key: str) -> Optional[Any]:
        name = f"default_{key}"

        if hasattr(self, name):
            return getattr(self, name)
        else:
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
            conf[key] = getattr(self, key)

        return json.dumps(conf)

    def save_state(self, name: str = "") -> None:
        from .display import display
        from .paths import paths
        from .args import args
        from . import emojis

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

        conf = self.get_string()

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(conf)

        if not args.quiet:
            name = Path(file_path).name
            msg = f"Config saved as {name}"
            display.print(emojis.text(msg, "storage"))

    def load_state(self, name: str = "") -> None:
        from .paths import paths
        from .widgets import widgets

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
            return

        with open(path, "r", encoding="utf-8") as file:
            self.apply(file)
            widgets.fill()

    def apply(self, file: IO[str]) -> None:
        try:
            conf = json.load(file)
        except BaseException:
            conf = {}

        for key in self.defaults():
            setattr(self, key, conf.get(key, getattr(self, key)))

    def load_file(self) -> None:
        from .paths import paths

        if not paths.config.exists():
            paths.config.parent.mkdir(parents=True, exist_ok=True)
            paths.config.touch(exist_ok=True)

        with open(paths.config, "r", encoding="utf-8") as file:
            self.apply(file)

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

            with open(path, "r", encoding="utf-8") as file:
                self.apply(file)
                self.save()
        except BaseException as e:
            utils.error(e)
            args.config = ""
            self.load_file()

    def save(self) -> None:
        from .paths import paths
        from . import filemanager

        conf = {}

        for key in self.defaults():
            conf[key] = getattr(self, key)

        filemanager.save(paths.config, conf)

    def update(self, key: str) -> bool:
        from .widgets import widgets

        if not hasattr(self, key):
            return False

        widget = getattr(widgets, key)

        if widget:
            return self.set(key, widget.get())
        else:
            return False

    def set(self, key: str, value: Any) -> bool:
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

        if key == "model":
            self.on_model_change()
        elif key == "output_font_size":
            self.on_output_font_change()

        if key in self.model_keys:
            model.unload()

        return True

    def reset(self, force: bool = False) -> None:
        from .app import app
        from .model import model
        from .widgets import widgets
        from .dialogs import Dialog

        keep = ("model", "theme")

        def action() -> None:
            for key in self.defaults():
                if key in keep:
                    continue

                default = self.get_default(key)

                if default is not None:
                    setattr(self, key, default)

            self.on_model_change()
            self.on_output_font_change()
            widgets.fill()
            app.check_compact()
            self.save()
            model.unload(True)

        if force:
            action()
            return

        Dialog.show_confirm("This will remove your custom configs"
                            "\nand refresh the widgets", action)

    def reset_one(self, key: str, focus: bool = True) -> None:
        from .widgets import widgets

        if not hasattr(self, key):
            return

        default = self.get_default(key)

        if getattr(self, key) == default:
            return

        self.set(key, default)
        widgets.fill_widget(key, getattr(self, key), focus=focus)

    def on_model_change(self) -> None:
        from .model import model
        model.check_config(False)

    def on_output_font_change(self) -> None:
        from .display import display
        display.update_font()

    def menu(self) -> None:
        from .dialogs import Dialog

        cmds = []
        cmds.append(("Reset", lambda: self.reset()))
        cmds.append(("Load", lambda: self.load_state()))
        cmds.append(("Save", lambda: self.save_state()))
        Dialog.show_commands("Config Menu", commands=cmds)

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

    def command(self, text: str = "") -> None:
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


config = Config()
