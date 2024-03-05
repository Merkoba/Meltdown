# Standard
from pathlib import Path
from typing import List


class ConfigDefaults:
    name_user: str = "👽 You"
    name_ai: str = "😎 Melt"
    max_tokens: int = 250
    temperature: float = 0.8
    system: str = "Respond as a gentleman and a scholar who is a bit unhinged"
    top_k: int = 40
    top_p: float = 0.95
    model: str = ""
    context: int = 0
    seed: int = -1


class Config:
    def __init__(self) -> None:
        self.title = "Meltdown"
        self.program = "meltdown"
        self.width = 1000
        self.height = 730
        self.padx = 5
        self.pady = 8
        self.frame_padx = 0
        self.frame_pady = 0
        self.input_width = 11
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
        self.config_file = f"~/.config/{self.program}/config.json"
        self.models_file = f"~/.config/{self.program}/models.json"
        self.inputs_file = f"~/.config/{self.program}/inputs.json"
        self.logs_dir = f"~/.config/{self.program}/logs/"
        self.config_path = Path(self.config_file).expanduser().resolve()
        self.models_path = Path(self.models_file).expanduser().resolve()
        self.inputs_path = Path(self.inputs_file).expanduser().resolve()
        self.logs_path = Path(self.logs_dir).expanduser().resolve()
        self.models: List[str] = []
        self.inputs: List[str] = []

        self.model = ConfigDefaults.model
        self.name_user = ConfigDefaults.name_user
        self.name_ai = ConfigDefaults.name_ai
        self.max_tokens = ConfigDefaults.max_tokens
        self.temperature = ConfigDefaults.temperature
        self.system = ConfigDefaults.system
        self.top_k = ConfigDefaults.top_k
        self.top_p = ConfigDefaults.top_p
        self.context = ConfigDefaults.context
        self.seed = ConfigDefaults.seed

        self.intro = [
            "Welcome to Meltdown.",
            "Type a prompt and press Enter to continue.",
            "The specified model will load automatically.",
        ]

        self.saved_configs = [
            "model",
            "name_user",
            "name_ai",
            "max_tokens",
            "temperature",
            "system",
            "top_k",
            "top_p",
            "context",
            "seed",
        ]


config = Config()
