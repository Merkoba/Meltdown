# Standard
import time
from typing import Tuple
from datetime import datetime


def seconds_string(name: str, start: float, end: float) -> str:
    num = round(start - end, 2)
    return f"{name} in {num} seconds"


def check_time(name: str, last_time: float) -> Tuple[str, float]:
    now = now()
    seconds_str = seconds_string(name, now, last_time)
    return seconds_str, now


def now() -> float:
    return time.time()


def now_int() -> int:
    return int(time.time())


def date() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def sleep(seconds: float) -> None:
    time.sleep(seconds)
