# Modules
from .config import config
from .widgets import widgets
from . import timeutils

# Standard
import threading

# Libraries
import psutil  # type: ignore
from typing import Optional


def padnum(num: int) -> str:
    return str(num).zfill(3)


def get_info() -> None:
    cpu = int(psutil.cpu_percent(interval=1))
    ram = int(psutil.virtual_memory().percent)
    temps = psutil.sensors_temperatures()
    temp: Optional[int] = None

    if "k10temp" in temps:
        ktemps = temps["k10temp"]

        for ktemp in ktemps:
            # This one works with AMD Ryzen
            if ktemp.label == "Tctl":
                temp = int(ktemp.current)
                break

    widgets.cpu.set(padnum(cpu) + "%")
    widgets.ram.set(padnum(ram) + "%")

    if temp:
        widgets.temp.set(padnum(temp) + "°C")
    else:
        widgets.temp.set("???°C")

    if cpu >= config.system_threshold:
        widgets.cpu_label.configure(foreground=config.red_color)
    else:
        widgets.cpu_label.configure(foreground=config.green_color)

    if ram >= config.system_threshold:
        widgets.ram_label.configure(foreground=config.red_color)
    else:
        widgets.ram_label.configure(foreground=config.green_color)

    if temp:
        if temp >= config.system_threshold:
            widgets.temp_label.configure(foreground=config.red_color)
        else:
            widgets.temp_label.configure(foreground=config.green_color)


def check() -> None:
    while True:
        if not config.compact:
            get_info()

        timeutils.sleep(config.system_delay)


def start() -> None:
    thread = threading.Thread(target=check, args=())
    thread.daemon = True
    thread.start()
