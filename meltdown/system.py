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
    if args.monitor_cpu:
        cpu = int(psutil.cpu_percent(interval=1))
        widgets.cpu.set(padnum(cpu) + "%")

    if args.monitor_ram:
        ram = int(psutil.virtual_memory().percent)
        widgets.ram.set(padnum(ram) + "%")

    if args.monitor_temp:
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

    if args.monitor_colors:
        threshold = args.system_threshold

        if args.monitor_cpu:
            if cpu >= threshold:
                widgets.cpu_text.configure(foreground=app.theme.monitor_heavy)
            else:
                widgets.cpu_text.configure(foreground=app.theme.monitor_normal)

        if args.monitor_ram:
            if ram >= threshold:
                widgets.ram_text.configure(foreground=app.theme.monitor_heavy)
            else:
                widgets.ram_text.configure(foreground=app.theme.monitor_normal)

        if args.monitor_temp:
            if temp:
                if temp >= threshold:
                    widgets.temp_text.configure(foreground=app.theme.monitor_heavy)
                else:
                    widgets.temp_text.configure(foreground=app.theme.monitor_normal)


def check() -> None:
    timeutils.sleep(1)

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
