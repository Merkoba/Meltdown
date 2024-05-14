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
        profile = args.profile

        if profile:
            location = Path(program, profile)
        else:
            location = Path(program, "main")

        config_dir = appdirs.user_config_dir()
        self.config = Path(config_dir, location, "config.json")
        self.models = Path(config_dir, location, "models.json")
        self.inputs = Path(config_dir, location, "inputs.json")
        self.systems = Path(config_dir, location, "systems.json")
        self.files = Path(config_dir, location, "files.json")
        self.session = Path(config_dir, location, "session.json")
        self.commands = Path(config_dir, location, "commands.json")
        self.autocomplete = Path(config_dir, location, "autocomplete.json")

        data_dir = appdirs.user_data_dir()
        self.configs = Path(data_dir, location, "configs")
        self.sessions = Path(data_dir, location, "sessions")
        self.logs = Path(data_dir, location, "logs")
        self.apikey = Path(data_dir, location, "apikey.txt")
        self.errors = Path(data_dir, location, "errors")

        self.nouns = Path(app.here, "nouns.txt")


paths = Paths()
