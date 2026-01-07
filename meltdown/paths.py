# Standard
from pathlib import Path

# Libaries
import appdirs  # type: ignore

# Modules
from .app import app
from .args import args
from .utils import utils


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
        self.memory: Path
        self.configs: Path
        self.sessions: Path
        self.logs: Path
        self.openai_key: Path
        self.google_key: Path
        self.anthropic_key: Path
        self.errors: Path
        self.nouns: Path
        self.memories: Path

    def error(self, what: str) -> None:
        utils.msg(f"Error: Can't find or create the '{what}' directory.")

    def setup(self) -> bool:
        program = app.manifest["program"]
        location = Path(program, args.profile)

        # Config

        try:
            if args.config_dir:
                config_dir = Path(args.config_dir)
            else:
                config_dir = Path(appdirs.user_config_dir())

            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_dir = Path(config_dir, location)
            self.config = Path(self.config_dir, "config.json")
            self.configs = Path(self.config_dir, "configs")
        except Exception:
            self.error("config")
            return False

        # Data

        try:
            if args.data_dir:
                data_dir = Path(args.data_dir)
            else:
                data_dir = Path(appdirs.user_data_dir())

            data_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            self.error("data")
            return False

        self.data_dir = Path(data_dir, location)
        self.sessions = Path(self.data_dir, "sessions")
        self.inputs = Path(self.data_dir, "inputs.json")
        self.files = Path(self.data_dir, "files.json")
        self.session = Path(self.data_dir, "session.json")
        self.autocomplete = Path(self.data_dir, "autocomplete.json")
        self.commands = Path(self.data_dir, "commands.json")
        self.models = Path(self.data_dir, "models.json")
        self.systems = Path(self.data_dir, "systems.json")
        self.memory = Path(self.data_dir, "memory.json")
        self.memories = Path(self.data_dir, "memories")

        if args.logs_dir:
            self.logs = Path(args.logs_dir)
        else:
            self.logs = Path(self.data_dir, "logs")

        self.openai_key = Path(self.data_dir, "openai_key.txt")
        self.google_key = Path(self.data_dir, "google_key.txt")
        self.anthropic_key = Path(self.data_dir, "anthropic_key.txt")
        self.errors = Path(self.data_dir, "errors")

        # Assets

        self.nouns = Path(app.here, "nouns.txt")
        return True


paths = Paths()
