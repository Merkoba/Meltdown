# Standard
from pathlib import Path

# Libaries
import appdirs  # type: ignore

# Modules
from .app import app
from .args import args


class Paths:
    def __init__(self) -> None:
        self.config: Path
        self.models: Path
        self.inputs: Path
        self.systems: Path
        self.files: Path
        self.session: Path
        self.commands: Path
        self.autocomplete: Path

        self.configs: Path
        self.sessions: Path
        self.logs: Path
        self.apikey: Path
        self.errors: Path

        self.nouns: Path

    def setup(self) -> None:
        program = app.manifest["program"]

        if args.dev:
            program += "_dev"

        config_dir = appdirs.user_config_dir()
        self.config = Path(config_dir, program, "config.json")
        self.models = Path(config_dir, program, "models.json")
        self.inputs = Path(config_dir, program, "inputs.json")
        self.systems = Path(config_dir, program, "systems.json")
        self.files = Path(config_dir, program, "files.json")
        self.session = Path(config_dir, program, "session.json")
        self.commands = Path(config_dir, program, "commands.json")
        self.autocomplete = Path(config_dir, program, "autocomplete.json")

        data_dir = appdirs.user_data_dir()
        self.configs = Path(data_dir, program, "configs")
        self.sessions = Path(data_dir, program, "sessions")
        self.logs = Path(data_dir, program, "logs")
        self.apikey = Path(data_dir, program, "apikey.txt")
        self.errors = Path(data_dir, program, "errors")

        self.nouns = Path(app.here, "nouns.txt")


paths = Paths()
