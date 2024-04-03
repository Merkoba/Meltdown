# Standard
import re
from difflib import SequenceMatcher


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
