from __future__ import annotations

# Standard
from pathlib import Path
from typing import Any
from http import HTTPStatus

# Modules
from .args import args
from .utils import utils
from .files import files
from .display import display
from . import formats

# Libraries
import requests  # type: ignore


class Signals:
    def __init__(self) -> None:
        self.timeout = 10

    def read_signals(self) -> Any | None:
        if not args.signals_file:
            return None

        path = Path(args.signals_file)

        if not path.exists():
            return None

        return files.load(path)

    def run(self, name: str) -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

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
        required = ["url", "content_key"]

        if not all(key in signal for key in required):
            display.print("The signal is not configured properly.")
            return

        url = signal.get("url")
        content_key = signal.get("content_key")
        content_length = signal.get("content_length", 0)
        method = signal.get("method", "post")
        items = signal.get("items", "all")
        format_ = signal.get("format", "json")
        single_line = signal.get("single_line", False)
        data = signal.get("data", {})
        content = self.get_content(format_, items)

        if not content:
            display.print("No content to send.")
            return

        if single_line:
            content = content.replace("\n", " ").strip()

        if content_length > 0:
            content = content[:content_length].strip()

        data[content_key] = content
        method_lower = method.lower()

        try:
            if method_lower == "get":
                res = requests.get(url, params=data, timeout=self.timeout)
            elif method_lower == "post":
                res = requests.post(url, data=data, timeout=self.timeout)
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

    def get_content(self, format_: str = "json", items: str = "all") -> str | None:
        tabconvo = display.get_tab_convo()

        if not tabconvo:
            return None

        if not tabconvo.convo.items:
            return None

        text = ""

        if format_ == "text":
            text = formats.get_text(tabconvo.convo)
        elif format_ == "json":
            text = formats.get_json(tabconvo.convo)
        elif format_ == "markdown":
            text = formats.get_markdown(tabconvo.convo)

        return text.strip()


signals = Signals()
