# Standard
import time
from typing import Tuple
from datetime import datetime


def seconds_string(name: str, start: float, end: float) -> str:
    num = round(start - end, 2)
    return f"{name} in {num} seconds"


def check_time(name: str, last_time: float) -> Tuple[str, float]:
    time_now = now()
    seconds_str = seconds_string(name, time_now, last_time)
    return seconds_str, time_now


def now() -> float:
    return time.time()


def now_int() -> int:
    return int(time.time())


def date() -> str:
    time_now = datetime.now()
    return time_now.strftime("%Y-%m-%d %H:%M:%S")


def sleep(seconds: float) -> None:
    time.sleep(seconds)


def today() -> str:
    def add_suffix(day: int) -> str:
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"

    current_time = datetime.now()
    suffix = add_suffix(current_time.day)
    return current_time.strftime("%A {0} of %B %Y").format(suffix)
