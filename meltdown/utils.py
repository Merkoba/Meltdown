# Standard
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
