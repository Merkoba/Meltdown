# Modules
from .app import app
from .argparser import ArgParser

# Standard
from typing import Any, Dict, List


class Args:
    def __init__(self) -> None:
        title = app.manifest["title"]
        version = app.manifest["version"]
        vinfo = f"{title} {version}"

        self.arguments: Dict[str, Any] = {
            "version": {"action": "version", "help": "Check the version of the program", "version": vinfo},
        }

        self.aliases: Dict[str, List[str]] = {}

    def parse(self) -> None:
        ArgParser(app.manifest["title"], self.arguments, self.aliases, self)


args = Args()
