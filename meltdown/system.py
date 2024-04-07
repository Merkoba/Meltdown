# Modules
from .config import config
from .widgets import widgets
from .args import args
from .app import app
from . import timeutils

# Standard
import threading

# Libraries
import psutil  # type: ignore
from typing import Optional


def padnum(num: int) -> str:
    return str(num).zfill(3)


def get_info() -> None:
    if args.system_cpu:
        cpu = int(psutil.cpu_percent(interval=1))
        widgets.cpu.set(padnum(cpu) + "%")

    if args.system_ram:
        ram = int(psutil.virtual_memory().percent)
        widgets.ram.set(padnum(ram) + "%")

    if args.system_temp:
        temps = psutil.sensors_temperatures()
        temp: Optional[int] = None

        if "k10temp" in temps:
            ktemps = temps["k10temp"]

            for ktemp in ktemps:
                # This one works with AMD Ryzen
                if ktemp.label == "Tctl":
                    temp = int(ktemp.current)
                    break

        if temp:
            widgets.temp.set(padnum(temp) + "°")
        else:
            widgets.temp.set("N/A")

    if args.system_colors:
        threshold = args.system_threshold

        if args.system_cpu:
            if cpu >= threshold:
                widgets.cpu_text.configure(foreground=app.theme.system_heavy)
            else:
                widgets.cpu_text.configure(foreground=app.theme.system_normal)

        if args.system_ram:
            if ram >= threshold:
                widgets.ram_text.configure(foreground=app.theme.system_heavy)
            else:
                widgets.ram_text.configure(foreground=app.theme.system_normal)

        if args.system_temp:
            if temp:
                if temp >= threshold:
                    widgets.temp_text.configure(foreground=app.theme.system_heavy)
                else:
                    widgets.temp_text.configure(foreground=app.theme.system_normal)


def check() -> None:
    timeutils.sleep(1)

    while True:
        if not config.compact:
            try:
                get_info()
            except BaseException:
                pass

        timeutils.sleep(args.system_delay)


def start() -> None:
    if not args.system:
        return

    thread = threading.Thread(target=lambda: check())
    thread.daemon = True
    thread.start()
