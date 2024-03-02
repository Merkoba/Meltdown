# Standard
import time
from typing import Tuple


def get_time() -> float:
    return time.time()


def seconds_string(name: str, start: float, end: float) -> str:
    num = round(start - end, 2)
    return f"{name} in {num} seconds"


def check_time(name: str, last_time: float) -> Tuple[str, float]:
    now = get_time()
    seconds_str = seconds_string(name, now, last_time)
    return seconds_str, now


def now() -> float:
    return time.time()


def now_int() -> int:
    return int(time.time())
