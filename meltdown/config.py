# Standard
from pathlib import Path
from typing import List, Any, Dict, Optional


class Config:
    def __init__(self) -> None:
        self.title = "Meltdown"
        self.program = "meltdown"
        self.width = 777
        self.height = 744
        self.padx = 5
        self.pady = 8
        self.frame_padx = 0
        self.frame_pady = 0
        self.input_width = 10
        self.input_width_small = 6
        self.select_width = 11
        self.dialog_color = "#252933"
        self.font = ("sans", 14)
        self.font_button = ("sans", 10)
        self.frame_number = 0
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.button_background = "#446CA1"
        self.stop_background = "#3F9687"
        self.stop_background_disabled = "#2B303B"
        self.button_foreground = "white"
        self.input_background = "#2B303B"
        self.input_foreground = "white"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.max_list_items = 12
        self.avatar_user = "👽"
        self.avatar_ai = "😎"

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
        self.default_max_tokens: int = 250
        self.default_temperature: float = 0.8
        self.default_system: str = "Your name is @name_ai and you refer to me as @name_user"
        self.default_top_k: int = 40
        self.default_top_p: float = 0.95
        self.default_model: str = ""
        self.default_context: int = 0
        self.default_seed: int = -1
        self.default_format: str = "auto"
        self.default_prepend = ""
        self.default_append = ""

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

        self.intro = [
            "Welcome to Meltdown.",
            "Type a prompt and press Enter to continue.",
            "The specified model will load automatically.",
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
