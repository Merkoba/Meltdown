# Modules
from .args import args
from .utils import utils
from .model import model
from .run import run

class Lockets:
    def __init__(self):
        self.lockets: dict[str, str] = {}

    def setup(self) -> None:
        for locket in args.lockets:
            key, value = utils.cmd_value(locket)

            if (not key) or (not value):
                continue

            self.lockets[key] = value

    def ask(self, name: str, prompt: str) -> None:
        cmd = self.locks[name]

        if not cmd:
            return

        run.run_shell(cmd)
        model.prompt(prompt)


lockets = Lockets()