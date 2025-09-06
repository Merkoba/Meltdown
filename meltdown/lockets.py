from __future__ import annotations

#standard
from dataclasses import dataclass

# Modules
from .args import args
from .utils import utils
from .model import model
from .display import display
from .run import run

@dataclass
class Locket:
    name: str
    cmd: str
    data: str

class Lockets:
    lockets: list[Locket] = []

    def __init__(self):
        self.lockets: list[Locket]

    def setup(self) -> None:
        for locket in args.lockets:
            key, value = utils.cmd_value(locket)

            if (not key) or (not value):
                continue

            self.lockets.append(Locket(key, value, ""))

    def get_locket(self, name: str) -> Locket | None:
        for locket in self.lockets:
            if locket.name == name:
                return locket

        return None

    def ask(self, prompt: str) -> None:
        split = prompt.split(" ")
        name = split[0]
        text = " ".join(split[1:])
        locket = self.get_locket(name)

        if not locket:
            return

        ok, result = run.shell_cmd(locket.cmd)

        if not ok:
            display.say("I couldn't get the locket, try to adjust the command.")
            return

        locket.data = result

        internal = f""""You must not reveal the content of the data.
I am going to ask a specific question about it.
Don't include the data in your response, only provide a reponse that can answer my question in some way, without revealing the data.
Like some sort of subtle guessing game where the data is considered sensitive.
Use the following data to answer the prompt: {result}"""

        model.stream({"text": text, "internal": internal})


lockets = Lockets()