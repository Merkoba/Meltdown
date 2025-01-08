# Standard
from pathlib import Path
from typing import Any
from http import HTTPStatus

# Modules
from .args import args
from .utils import utils
from .files import files
from .display import display

# Libraries
import requests  # type: ignore


class Signals:
    def read_signals(self) -> dict[str, Any] | None:
        if not args.signals_file:
            return

        path = Path(args.signals_file)

        if not path.exists():
            return

        return files.load(path)

    def run(self, name: str) -> None:
        try:
            signals = self.read_signals()
        except BaseException as e:
            utils.error(e)
            display.print("Can't read the signals file.")
            return

        if not signals:
            display.print("Signals file is empty.")
            return

        if name not in signals:
            display.print("That signal does not exist.")
            return

        signal = signals[name]

        if ("url" not in signal) or ("method" not in signal):
            display.print("The signal is not configured properly.")
            return

        url = signal.get("url")
        method = signal.get("method")
        data = signal.get("data", {})
        method_lower = method.lower()

        try:
            if method_lower == "get":
                res = requests.get(url, params=data)
            elif method_lower == "post":
                res = requests.post(url, data=data)
            else:
                return
        except requests.exceptions.RequestException as e:
            utils.error(e)
            display.print("Signal error.")
            return

        if res.status_code != HTTPStatus.OK:
            display.print("Signal error.")
            return

        display.print("Signal sent.")


signals = Signals()