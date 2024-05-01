# Standard
import re
import time
import random
import logging
import inspect
import tkinter as tk
from logging.handlers import RotatingFileHandler
from difflib import SequenceMatcher
from typing import Union, Optional, Tuple, List
from pathlib import Path
from datetime import datetime

# Libraries
from rich.console import Console  # type: ignore

# Modules
from . import pyperclip


class Utils:
    def __init__(self) -> None:
        self.error_logger: Optional[logging.Logger] = None
        self.console = Console()
        self.nouns: List[str] = []

    def similarity(self, a: str, b: str) -> float:
        matcher = SequenceMatcher(None, a, b)
        return matcher.ratio()

    def check_match(self, a: str, b: str) -> bool:
        if a == b:
            return True

        if self.similarity(a, b) >= 0.8:
            return True

        return False

    def escape_regex(self, chars: str) -> str:
        escaped_chars = [re.escape(char) for char in chars]
        return "".join(escaped_chars)

    def msg(self, text: str) -> None:
        self.console.print(text)

    def error(self, error: Union[str, BaseException]) -> None:
        from .args import args

        caller = inspect.stack()[1]
        fname = Path(caller[1]).name
        line = caller[2]
        name = caller[3]

        errmsg = f"{fname} | {name} | {line} | {error}"

        if args.log_errors:
            if not self.error_logger:
                self.create_error_logger()

            if self.error_logger:
                self.error_logger.error(errmsg)

        if args.errors:
            self.console.print_exception(show_locals=True)

    def create_error_logger(self) -> None:
        from .paths import paths

        if not paths.errors.exists():
            paths.errors.mkdir(parents=True, exist_ok=True)

        file_path = Path(paths.errors, "error.log")
        self.error_logger = logging.getLogger(__name__)
        self.error_logger.setLevel(logging.ERROR)
        error_handler = RotatingFileHandler(file_path, maxBytes=2000, backupCount=5)
        error_handler.setLevel(logging.ERROR)
        self.error_logger.addHandler(error_handler)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        error_handler.setFormatter(formatter)

    def seconds_string(self, name: str, start: float, end: float) -> str:
        num = round(start - end, 2)
        return f"{name} in {num} seconds"

    def check_time(self, name: str, last_time: float) -> Tuple[str, float]:
        time_now = self.now()
        seconds_str = self.seconds_string(name, time_now, last_time)
        return seconds_str, time_now

    def now(self) -> float:
        return time.time()

    def now_int(self) -> int:
        return int(time.time())

    def date(self) -> str:
        time_now = datetime.now()
        return time_now.strftime("%Y-%m-%d %H:%M:%S")

    def to_date(self, timestamp: float) -> str:
        dt_object = datetime.fromtimestamp(timestamp)
        hour = dt_object.strftime("%I").lstrip("0")
        return dt_object.strftime(f"%b %d %Y - {hour}:%M %p")

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def today(self) -> str:
        def add_suffix(day: int) -> str:
            if 10 <= day % 100 <= 20:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            return f"{day}{suffix}"

        current_time = datetime.now()
        suffix = add_suffix(current_time.day)
        return current_time.strftime("%A {0} of %B %Y").format(suffix)

    def copy(self, text: str) -> None:
        pyperclip.copy(text)  # type: ignore

    def paste(self, widget: tk.Widget) -> None:
        from .entrybox import EntryBox
        from .textbox import TextBox

        assert isinstance(widget, (EntryBox, TextBox))

        text = self.get_paste()

        if not text:
            return

        widget.set_text(text)

    def get_paste(self) -> str:
        return pyperclip.paste().strip()  # type: ignore

    def padnum(self, num: int) -> str:
        return str(num).zfill(3)

    def random_noun(self) -> str:
        from .paths import paths

        if not self.nouns:
            with paths.nouns.open("r", encoding="utf-8") as file:
                self.nouns = file.read().strip().splitlines()

        return random.choice(self.nouns)

    def replace_keywords(self, content: str) -> str:
        from .args import args
        from .config import config
        from .display import display

        if not args.use_keywords:
            return content

        char = args.keychar

        if config.name_user:
            content = content.replace(f"{char}name_user", config.name_user)

        if config.name_ai:
            content = content.replace(f"{char}name_ai", config.name_ai)

        content = content.replace(f"{char}date", self.today())
        content = content.replace(f"{char}now", str(self.now_int()))
        content = content.replace(f"{char}name", display.get_tab_name())

        def replace_noun(match: re.Match[str]) -> str:
            return self.random_noun()

        char_2 = re.escape(args.keychar)
        pattern = re.compile(f"{char_2}noun")
        return pattern.sub(replace_noun, content)


utils = Utils()
