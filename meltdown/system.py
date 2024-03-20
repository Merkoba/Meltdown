# Modules
from .config import config
from .widgets import widgets
from .args import args
from .theme import Theme
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
        widgets.temp.set("N/A")

    if args.monitor_colors:
        if cpu >= config.system_threshold:
            widgets.cpu_text.configure(foreground=Theme.red_color)
        else:
            widgets.cpu_text.configure(foreground=Theme.green_color)

        if ram >= config.system_threshold:
            widgets.ram_text.configure(foreground=Theme.red_color)
        else:
            widgets.ram_text.configure(foreground=Theme.green_color)

        if temp:
            if temp >= config.system_threshold:
                widgets.temp_text.configure(foreground=Theme.red_color)
            else:
                widgets.temp_text.configure(foreground=Theme.green_color)


def check() -> None:
    while True:
        if not config.compact:
            try:
                get_info()
            except BaseException:
                pass

        timeutils.sleep(config.system_delay)


def start() -> None:
    if not args.monitors:
        return

    thread = threading.Thread(target=check, args=())
    thread.daemon = True
    thread.start()
