# Standard
import re
import logging
from logging.handlers import RotatingFileHandler
from difflib import SequenceMatcher
from typing import Union, Optional
from pathlib import Path


error_logger: Optional[logging.Logger] = None


def similarity(a: str, b: str) -> float:
    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio()


def check_match(a: str, b: str) -> bool:
    if a == b:
        return True

    if similarity(a, b) >= 0.8:
        return True

    return False


def escape_regex(chars: str) -> str:
    escaped_chars = [re.escape(char) for char in chars]
    return "".join(escaped_chars)


def msg(text: str) -> None:
    print(text)


def error(error: Union[str, BaseException]) -> None:
    from .args import args

    if args.log_errors:
        if not error_logger:
            create_error_logger()

        if error_logger:
            error_logger.error(error)

    if args.errors:
        print("Error:", error)


def create_error_logger() -> None:
    from .paths import paths

    global error_logger

    if not paths.errors.exists():
        paths.errors.mkdir(parents=True, exist_ok=True)

    file_path = Path(paths.errors, "error.log")
    error_logger = logging.getLogger(__name__)
    error_logger.setLevel(logging.ERROR)
    error_handler = RotatingFileHandler(file_path, maxBytes=2000, backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_logger.addHandler(error_handler)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    error_handler.setFormatter(formatter)
