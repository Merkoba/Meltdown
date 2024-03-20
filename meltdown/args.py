# Modules
from .app import app
from .argparser import ArgParser

# Standard
from typing import Any, Dict, List


class Args:
    def __init__(self) -> None:
        self.tooltips = True
        self.scrollbars = True
        self.colors = True
        self.avatars = True
        self.monitors = True
        self.compact = False
        self.test = False
        self.width = -1
        self.height = -1

    class Internal:
        title = app.manifest["title"]
        version = app.manifest["version"]
        vinfo = f"{title} {version}"

        arguments: Dict[str, Any] = {
            "test": {"action": "store_true", "help": "Make a test tab for debugging"},
            "version": {"action": "version", "help": "Check the version of the program", "version": vinfo},
            "no-tooltips": {"action": "store_false", "help": "Don't show tooltips"},
            "no-scrollbars": {"action": "store_false", "help": "Don't show scrollbars"},
            "no-colors": {"action": "store_false", "help": "Don't show user colors"},
            "no-avatars": {"action": "store_false", "help": "Don't show user avatars"},
            "no-monitors": {"action": "store_false", "help": "Don't show system monitors"},
            "compact": {"action": "store_true", "help": "Start in compact mode"},
            "width": {"type": int, "help": "Width of the window"},
            "height": {"type": int, "help": "Height of the window"},
        }

        aliases: Dict[str, List[str]] = {}

    def parse(self) -> None:
        ap = ArgParser(app.manifest["title"], self.Internal.arguments, self.Internal.aliases, self)
        ap.normal("no_tooltips", "tooltips")
        ap.normal("no_scrollbars", "scrollbars")
        ap.normal("no_colors", "colors")
        ap.normal("no_avatars", "avatars")
        ap.normal("no_monitors", "monitors")
        ap.normal("compact")
        ap.normal("width")
        ap.normal("height")
        ap.normal("test")


args = Args()
