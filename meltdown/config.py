# Standard
from typing import List, Any, Dict, Optional, Tuple, Callable


class Config:
    def __init__(self) -> None:
        self.width = 784
        self.height = 752
        self.padx = 10
        self.pady = 10
        self.frame_padx = 0
        self.frame_pady = 0
        self.entry_width = 10
        self.entry_width_small = 6
        self.combobox_width = 11
        self.combobox_width_small = 7
        self.dialog_color = "#252933"
        self.font_family = "sans"
        self.font = (self.font_family, 14)
        self.font_button = (self.font_family, 12)
        self.font_combobox = (self.font_family, 13)
        self.font_tab = (self.font_family, 12)
        self.font_menu = (self.font_family, 13)
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.red_color = "#FF6B6B"
        self.green_color = "#44B3A1"
        self.button_width = 8
        self.button_background = "#446CA1"
        self.button_background_alt = "#3D4555"
        self.button_background_hover = "#387ADF"
        self.button_background_hover_alt = "#494D62"
        self.green_button_background_hover = "#944E63"
        self.green_background = "#3F9687"
        self.background_disabled = "#2B303B"
        self.button_foreground = "white"
        self.entry_background = "#2B303B"
        self.entry_foreground = "white"
        self.placeholder_color = "#494D62"
        self.separator_color = "#2B303B"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.combobox_background = "#2B303B"
        self.dialog_background = "white"
        self.dialog_foreground = "black"
        self.snippet_background = "#3D4555"
        self.snippet_foreground = "white"
        self.snippet_border = "#A0B8BF"
        self.snippet_header_color = "white"
        self.snippet_header_text = "#2B303B"
        self.max_list_items = 10
        self.avatar_user = "👽"
        self.avatar_ai = "😎"
        self.system_delay = 3
        self.system_threshold = 70
        self.printlogs = False
        self.max_log = 100

        self.models: List[str] = []
        self.inputs: List[str] = []
        self.systems: List[str] = []

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
        from .widgets import widgets
        widgets.display.print("")

        for key in self.defaults():
            value = getattr(self, key)

            if value == "":
                value = "[Empty]"

            widgets.display.print(f"{key}: {value}")

    def get_output_font(self) -> Tuple[str, int]:
        return (self.font_family, self.output_font_size)

    def get_snippet_font(self) -> Tuple[str, int]:
        return ("monospace", self.output_font_size)


config = Config()
