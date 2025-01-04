from __future__ import annotations

# Standard
import re
import time
import random
import string
import logging
import inspect
import tkinter as tk
import importlib.util
from logging.handlers import RotatingFileHandler
from difflib import SequenceMatcher
from typing import Any
from pathlib import Path
from datetime import datetime
from typing import TYPE_CHECKING
from collections.abc import Callable

# Libraries
import rentrylib  # type: ignore
from rich.console import Console  # type: ignore

# Modules
from . import pyperclip

if TYPE_CHECKING:
    from .menus import Menu


class Utils:
    def __init__(self) -> None:
        self.error_logger: logging.Logger | None = None
        self.console = Console()
        self.nouns: list[str] = []
        self.protocols = ("http://", "https://")
        self.upload_service = "https://rentry.org"

    def similarity(self, a: str, b: str) -> float:
        matcher = SequenceMatcher(None, a, b)
        return matcher.ratio()

    def check_match(self, a: str, b: str) -> bool:
        from .config import config

        if a == b:
            return True

        return self.similarity(a, b) >= config.similar_threshold

    def most_similar(self, text: str, items: list[str]) -> str | None:
        from .config import config

        best_match: str | None = None
        best_ratio = 0.0

        for item in items:
            ratio = self.similarity(text, item)

            if ratio >= config.similar_threshold:
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = item

        return best_match

    def escape_regex(self, chars: str) -> str:
        escaped_chars = [re.escape(char) for char in chars]
        return "".join(escaped_chars)

    def msg(self, text: str) -> None:
        self.console.print(text)

    def error(self, error: str | BaseException) -> None:
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
        num = round(start - end, 1)
        m = self.singular_or_plural(num, "sec", "secs")
        return f"{name} ({num} {m})"

    def check_time(self, name: str, last_time: float) -> tuple[str, float]:
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

    def copy(self, text: str, command: bool = False) -> None:
        from .args import args
        from .app import app

        if command and args.on_copy:
            app.file_command(args.on_copy, text)

        pyperclip.copy(text)  # type: ignore

    def paste(self, widget: tk.Widget) -> None:
        from .entrybox import EntryBox
        from .textbox import TextBox

        if not isinstance(widget, (EntryBox, TextBox)):
            return

        text = self.get_paste()

        if not text:
            return

        widget.set_text(text)

    def get_paste(self) -> str:
        return pyperclip.paste().strip()  # type: ignore

    def padnum(self, num: int) -> str:
        return str(num).zfill(3)

    def random_word(self) -> str:
        vowels = "aeiou"
        consonants = "".join(set(string.ascii_lowercase) - set(vowels))

        def con() -> str:
            return random.choice(consonants)

        def vow() -> str:
            return random.choice(vowels)

        return con() + vow() + con() + vow() + con() + vow()

    def random_noun(self) -> str:
        return self.random_nouns(1)[0]

    def random_nouns(self, num: int) -> list[str]:
        from .paths import paths
        from .files import files

        if not self.nouns:
            self.nouns = files.read(paths.nouns).splitlines()

        return random.sample(self.nouns, num)

    def replace_keywords(self, content: str, words: str | None = None) -> str:
        from .args import args
        from .config import config
        from .display import display

        if not args.use_keywords:
            return content

        c1 = re.escape("((")
        c2 = re.escape("))")

        def replace(what: str) -> str:
            if what == "noun":
                return self.random_noun()

            if what == "user":
                return config.name_user

            if what == "ai":
                return config.name_ai

            if what == "date":
                return self.today()

            if what == "now":
                return str(self.now_int())

            if what == "name":
                return display.get_tab_name()

            if words and (what == "words"):
                return words

            return ""

        if config.name_user:
            pattern = re.compile(f"{c1}name_user{c2}")
            content = pattern.sub(lambda m: replace("user"), content)

        if config.name_ai:
            pattern = re.compile(f"{c1}name_ai{c2}")
            content = pattern.sub(lambda m: replace("ai"), content)

        pattern = re.compile(f"{c1}date{c2}")
        content = pattern.sub(lambda m: replace("date"), content)

        pattern = re.compile(f"{c1}now{c2}")
        content = pattern.sub(lambda m: replace("now"), content)

        pattern = re.compile(f"{c1}name{c2}")
        content = pattern.sub(lambda m: replace("name"), content)

        if words:
            pattern = re.compile(f"{c1}words{c2}")
            content = pattern.sub(lambda m: replace("words"), content)

        pattern = re.compile(f"{c1}noun{c2}")
        return pattern.sub(lambda m: replace("noun"), content)

    def get_emoji(self, name: str) -> str:
        from .args import args

        return getattr(args, f"emoji_{name}", "")

    def emoji_text(self, text: str, name: str) -> str:
        from .args import args

        if not args.emojis:
            return text

        emoji = self.get_emoji(name)

        if emoji:
            return f"{emoji} {text}"

        return text

    def shorten(self, text: str) -> str:
        words = re.split(r"[\s-]", text)
        return "".join(word[0].upper() for word in words if word)

    def singular_or_plural(self, num: float, singular: str, plural: str) -> str:
        if num == 1:
            return singular

        return plural

    def get_index(self, arg: str, items: list[Any]) -> int:
        if not items:
            return -1

        if arg == "first":
            index = 0
        elif arg == "second":
            index = 1
        elif arg == "third":
            index = 2
        elif arg == "last":
            index = len(items) - 1
        else:
            try:
                index = int(arg) - 1
            except BaseException:
                index = -1

        return index

    def time_ago(self, start_time: float, end_time: float) -> str:
        diff = end_time - start_time
        seconds = int(diff)

        if seconds < 60:
            word = self.singular_or_plural(seconds, "second", "seconds")
            return f"{seconds} {word} ago"

        minutes = seconds // 60

        if minutes < 60:
            word = self.singular_or_plural(minutes, "minute", "minutes")
            return f"{minutes} {word} ago"

        hours = minutes / 60

        if hours < 24:
            word = self.singular_or_plural(hours, "hour", "hours")
            return f"{hours:.1f} {word} ago"

        days = hours / 24

        if days < 30:
            word = self.singular_or_plural(days, "day", "days")
            return f"{days:.1f} {word} ago"

        months = days / 30

        if months < 12:
            word = self.singular_or_plural(months, "month", "months")
            return f"{months:.1f} {word} ago"

        years = months / 12
        word = self.singular_or_plural(years, "year", "years")
        return f"{years:.1f} {word} ago"

    def smart_quotes(self, text: str) -> str:
        if text.startswith('"') and text.endswith('"'):
            return text

        return f'"{text}"'

    def clean_name(self, name: str) -> str:
        name = re.sub(r"[\s]", "_", name)
        name = re.sub(r"[^\w]", "_", name)
        name = re.sub("_+", "_", name)
        name = name.rstrip(" _").lower()

        if not name:
            name = self.random_word()

        return name

    def random_prompt(self) -> None:
        from .model import model

        noun = self.random_noun()
        text = f"Tell me about: {noun}"
        prompt = {"text": text}
        model.stream(prompt)

    def remove_multiple_lines(self, text: str) -> str:
        pattern = re.compile(r"\n{3,}")
        return pattern.sub("\n\n", text)

    def is_url(self, text: str) -> bool:
        pattern = re.compile(r"https?://\S+")
        return bool(pattern.match(text))

    def shorten_path(self, text: str) -> str:
        from .args import args

        if not args.shorten_paths:
            return text

        if text.startswith("/"):
            parts = text.split("/")

            if len(parts) < 3:
                return text

            last_part = parts[-1]
            rest_parts = [part[0] for part in parts[:-1] if part]
            partstr = "/".join(rest_parts)
            return f"/{partstr}/{last_part}"

        if self.is_url(text):
            for protocol in self.protocols:
                if text.startswith(protocol):
                    return text[len(protocol) :]

        return text

    def chars_to_kb(self, chars: int) -> float:
        num = chars / 1024
        return round(num, 2)

    def clean_text(self, text: str) -> str:
        allowed = (" ", "-", "_")
        return "".join(e for e in text if e.isalnum() or (e in allowed))

    def remove_multiple_spaces(self, text: str) -> str:
        return " ".join(text.split())

    def bullet_points(self, text: str) -> str:
        char = "•"
        return f"{char} {text}"

    def replace_linebreaks(self, text: str) -> str:
        text = " ".join(text.split("\n"))
        return self.remove_multiple_spaces(text)

    def get_words(self, text: str) -> list[str]:
        return re.findall(r"\w+", text)

    def trim_words(self, text: str, length: int) -> str:
        from .config import config

        trimmed = ""

        if len(text) <= length:
            trimmed = text
        else:
            trimmed = text[:length]
            space_index = trimmed.rfind(" ")

            if space_index > -1:
                diff = len(trimmed) - len(trimmed[:space_index])

                if diff < config.trim_threshold:
                    trimmed = trimmed[:space_index]

        return trimmed.strip()

    def remove_trails(self, text: str) -> str:
        return text.rstrip(" ,.;")

    def compact_text(self, text: str, length: int) -> str:
        text = self.replace_linebreaks(text).strip()
        text = self.trim_words(text, length)
        return self.remove_trails(text)

    def last_slash(self, text: str) -> str:
        return text.split("/")[-1]

    def split_long(self, text: str, length: int = 0) -> str:
        from .config import config

        if not length:
            length = config.split_long_length

        if len(text) >= length:
            half = len(text) // 2
            first_half = text[:half]
            second_half = text[half:]

            return f"{first_half}\n{second_half}"

        return text

    def fill_recent(
        self,
        menu: Menu,
        items: list[str],
        value: str,
        cmd: Callable[..., Any],
        label: bool = True,
        short: bool = False,
        alt_cmd: Callable[..., Any] | None = None,
    ) -> None:
        from .args import args
        from .config import config

        if not items:
            return

        if label:
            menu.add(text=config.recent_label, disabled=True)

        def forget(item: str) -> None:
            if alt_cmd:
                alt_cmd(item)

        def add_item(item: str) -> None:
            if item == value:
                return

            text = item

            if short:
                text = self.shorten_path(text)

            text = self.bullet_points(text[: args.list_item_width])
            text = self.replace_linebreaks(text)

            menu.add(
                text=text,
                command=lambda e: cmd(item),
                alt_command=lambda e: forget(item),
            )

        for item in items:
            add_item(item)

    def no_break(self, text: str) -> str:
        return text.replace(" ", "\u00a0")

    def untab_text(self, text: str) -> str:
        lines = text.splitlines()
        spaces = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        min_space = min(spaces) if spaces else 0
        return "\n".join(line[min_space:] for line in lines)

    def check_home(self, path: Path) -> str:
        home = str(Path.home())
        spath = str(path)

        if spath.startswith(home):
            spath = spath.replace(home, "~")

        return spath

    def saved_path(self, what: str, path: Path) -> None:
        from .display import display

        spath = self.check_home(path)
        msg = f"{what} {spath}"
        display.print(self.emoji_text(msg, "storage"))
        display.format_text(mode="last")

    def text_upload(self, tab_id: str | None = None) -> None:
        from .dialogs import Dialog
        from .app import app

        def action() -> None:
            Dialog.hide_all()
            app.update()
            self.do_text_upload(tab_id)

        Dialog.show_confirm(
            f"Upload conversation to\n{self.upload_service}", lambda: action()
        )

    def do_text_upload(self, tab_id: str | None = None) -> str:
        from .args import args
        from .display import display
        from .dialogs import Dialog
        from .formats import get_markdown

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = get_markdown(tabconvo.convo)

        page = rentrylib.RentryPage(
            text=text,
            edit_code=args.upload_edit_code,
        )

        Dialog.show_message(f"{self.upload_service}/{page.site}")

    def try_import(self, name: str) -> Any:
        spec = importlib.util.find_spec(name)

        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        return None


utils = Utils()
