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
        self.openai_apikey: Path
        self.google_apikey: Path
        self.errors: Path

        self.nouns: Path

    def setup(self) -> None:
        program = app.manifest["program"]
        location = Path(program, args.profile)

        config_dir = appdirs.user_config_dir()
        self.config_dir = Path(config_dir, location)
        self.config = Path(self.config_dir, "config.json")
        self.models = Path(self.config_dir, "models.json")
        self.inputs = Path(self.config_dir, "inputs.json")
        self.systems = Path(self.config_dir, "systems.json")
        self.files = Path(self.config_dir, "files.json")
        self.session = Path(self.config_dir, "session.json")
        self.commands = Path(self.config_dir, "commands.json")
        self.autocomplete = Path(self.config_dir, "autocomplete.json")

        data_dir = appdirs.user_data_dir()
        self.data_dir = Path(data_dir, location)
        self.configs = Path(self.data_dir, "configs")
        self.sessions = Path(self.data_dir, "sessions")

        if args.logs_dir:
            self.logs = Path(args.logs_dir)
        else:
            self.logs = Path(self.data_dir, "logs")

        self.openai_apikey = Path(self.data_dir, "openai_apikey.txt")
        self.google_apikey = Path(self.data_dir, "google_apikey.txt")
        self.errors = Path(self.data_dir, "errors")

        self.nouns = Path(app.here, "nouns.txt")


paths = Paths()
