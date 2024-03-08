# Modules
from .config import config
from .widgets import widgets
from . import timeutils

# Standard
import threading

# Libraries
import psutil  # type: ignore


def padnum(num: int) -> str:
    return str(num).zfill(3)


def get_info() -> None:
    cpu = int(psutil.cpu_percent(interval=1))
    ram = int(psutil.virtual_memory().percent)

    widgets.cpu.set(padnum(cpu) + "%")
    widgets.ram.set(padnum(ram) + "%")

    if cpu > config.system_threshold:
        widgets.cpu_label.configure(foreground=config.red_color)
    else:
        widgets.cpu_label.configure(foreground=config.green_color)

    if ram > config.system_threshold:
        widgets.ram_label.configure(foreground=config.red_color)
    else:
        widgets.ram_label.configure(foreground=config.green_color)


def check() -> None:
    while True:
        if not config.compact:
            get_info()

        timeutils.sleep(config.system_delay)


def start() -> None:
    thread = threading.Thread(target=check, args=())
    thread.daemon = True
    thread.start()
