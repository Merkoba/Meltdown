# Standard
from typing import List, Any, Dict, Optional, Tuple, Callable


class Config:
    def __init__(self) -> None:
        self.max_log = 100
        self.max_list_items = 10
        self.system_delay = 3
        self.system_threshold = 70
        self.printlogs = False
        self.list_item_width = 100

        self.models: List[str] = []
        self.inputs: List[str] = []

        self.default_name_user: str = "Joe"
        self.default_name_ai: str = "Melt"
        self.default_max_tokens: int = 500
        self.default_temperature: float = 0.8
        self.default_system: str = "Your name is @name_ai and you are talking to @name_user. The current date is @date"
        self.default_top_k: int = 40
        self.default_top_p: float = 0.95
        self.default_model: str = ""
        self.default_context: int = 1
        self.default_seed: int = 326
        self.default_format: str = "auto"
        self.default_prepend: str = ""
        self.default_append: str = ""
        self.default_compact: bool = False
        self.default_output_font_size: int = 14
        self.default_threads: int = 6
        self.default_mlock: str = "yes"
        self.default_theme: str = "dark"

        self.model = self.default_model
        self.name_user = self.default_name_user
        self.name_ai = self.default_name_ai
        self.max_tokens = self.default_max_tokens
        self.temperature = self.default_temperature
        self.system = self.default_system
        self.top_k = self.default_top_k
        self.top_p = self.default_top_p
        self.context = self.default_context
        self.seed = self.default_seed
        self.format = self.default_format
        self.prepend = self.default_prepend
        self.append = self.default_append
        self.compact = self.default_compact
        self.output_font_size = self.default_output_font_size
        self.threads = self.default_threads
        self.mlock = self.default_mlock
        self.theme = self.default_theme

        self.intro = [
            "Welcome to Meltdown.",
            "Type a prompt and press Enter to continue.",
            "The specified model will load automatically.",
        ]

        self.clearables = [
            "system",
            "prepend",
            "append",
            "input",
            "name_user",
            "name_ai",
        ]

        self.validations: Dict[str, Callable[..., Any]] = {
            "context": lambda x: max(0, x),
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

    def show_config(self) -> None:
        from .display import display
        display.print("Config:")
        text = []

        for key in self.defaults():
            value = getattr(self, key)

            if value == "":
                value = "[Empty]"

            text.append(f"{key}: {value}")

        display.print("\n".join(text))


config = Config()
