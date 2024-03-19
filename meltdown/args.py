# Modules
from .app import app
from .argparser import ArgParser

# Standard
from typing import Any, Dict, List


class Args:
    def __init__(self) -> None:
        self. no_tooltips = False
        self.width = -1
        self.height = -1
        self.test = False

    class Internal:
        title = app.manifest["title"]
        version = app.manifest["version"]
        vinfo = f"{title} {version}"

        arguments: Dict[str, Any] = {
            "version": {"action": "version", "help": "Check the version of the program", "version": vinfo},
            "no-tooltips": {"action": "store_true", "help": "Don't show tooltips"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
            "test": {"action": "store_true", "help": "Make a test tab"},
        }

        aliases: Dict[str, List[str]] = {}

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self.Internal.aliases, self)
        ap.normal("no_tooltips")
        ap.normal("width")
        ap.normal("height")
        ap.normal("test")


args = Args()
