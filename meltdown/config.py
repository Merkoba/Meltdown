# Standard
from pathlib import Path
from typing import List, Any, Dict, Optional


class Config:
    def __init__(self) -> None:
        self.title = "Meltdown"
        self.program = "meltdown"
        self.version = "1.2.0"
        self.width = 812
        self.height = 752
        self.padx = 4
        self.pady = 6
        self.frame_padx = 0
        self.frame_pady = 0
        self.entry_width = 10
        self.entry_width_small = 7
        self.combobox_width = 11
        self.dialog_color = "#252933"
        self.font = ("sans", 14)
        self.font_button = ("sans", 13)
        self.font_combobox = ("sans", 13)
        self.font_tab = ("sans", 11)
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.red_color = "#FF6B6B"
        self.green_color = "#44B3A1"
        self.button_background = "#446CA1"
        self.button_background_hover = "#387ADF"
        self.green_button_background_hover = "#944E63"
        self.green_background = "#3F9687"
        self.background_disabled = "#2B303B"
        self.button_foreground = "white"
        self.entry_background = "#2B303B"
        self.entry_foreground = "white"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.max_list_items = 12
        self.avatar_user = "👽"
        self.avatar_ai = "😎"
        self.system_delay = 3
        self.system_threshold = 70
        self.printlogs = False

        self.config_file = f"~/.config/{self.program}/config.json"
        self.configs_dir = f"~/.config/{self.program}/configs/"
        self.models_file = f"~/.config/{self.program}/models.json"
        self.inputs_file = f"~/.config/{self.program}/inputs.json"
        self.systems_file = f"~/.config/{self.program}/systems.json"
        self.prepends_file = f"~/.config/{self.program}/prepends.json"
        self.appends_file = f"~/.config/{self.program}/appends.json"
        self.logs_dir = f"~/.config/{self.program}/logs/"

        self.config_path = Path(self.config_file).expanduser().resolve()
        self.configs_path = Path(self.configs_dir).expanduser().resolve()
        self.models_path = Path(self.models_file).expanduser().resolve()
        self.inputs_path = Path(self.inputs_file).expanduser().resolve()
        self.systems_path = Path(self.systems_file).expanduser().resolve()
        self.prepends_path = Path(self.prepends_file).expanduser().resolve()
        self.appends_path = Path(self.appends_file).expanduser().resolve()
        self.logs_path = Path(self.logs_dir).expanduser().resolve()

        self.models: List[str] = []
        self.inputs: List[str] = []
        self.systems: List[str] = []

        self.default_name_user: str = "Joe"
        self.default_name_ai: str = "Melt"
        self.default_max_tokens: int = 500
        self.default_temperature: float = 0.8
        self.default_system: str = "Your name is @name_ai and you are talking to @name_user"
        self.default_top_k: int = 40
        self.default_top_p: float = 0.95
        self.default_model: str = ""
        self.default_context: int = 1
        self.default_seed: int = 326
        self.default_format: str = "auto"
        self.default_prepend: str = ""
        self.default_append: str = ""
        self.default_compact: bool = False

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


config = Config()
