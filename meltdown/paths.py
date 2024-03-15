# Modules
from .app import app

# Libaries
import appdirs  # type: ignore

# Standard
from pathlib import Path


class Paths:
    def __init__(self) -> None:
        program = app.manifest["program"]

        config_dir = appdirs.user_config_dir()
        self.config = Path(config_dir, program, "config.json")
        self.models = Path(config_dir, program, "models.json")
        self.inputs = Path(config_dir, program, "inputs.json")
        self.systems = Path(config_dir, program, "systems.json")
        self.prepends = Path(config_dir, program, "prepends.json")
        self.appends = Path(config_dir, program, "appends.json")
        self.session = Path(config_dir, program, "session.json")

        data_dir = appdirs.user_data_dir()
        self.configs = Path(data_dir, program, "configs")
        self.sessions = Path(data_dir, program, "sessions")
        self.logs = Path(data_dir, program, "logs")


paths = Paths()