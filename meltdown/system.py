# Standard
import json
import subprocess
import threading
from typing import Optional

# Libraries
import psutil  # type: ignore

# Modules
from .widgets import widgets
from .args import args
from .app import app
from . import timeutils


def padnum(num: int) -> str:
    return str(num).zfill(3)


def check_color(name: str, var: Optional[int]) -> None:
    if var is None:
        return

    if getattr(args, f"system_{name}"):
        label = getattr(widgets, f"{name}_text")

        if var >= args.system_threshold:
            label.configure(foreground=app.theme.system_heavy)
        else:
            label.configure(foreground=app.theme.system_normal)


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

    # This works with AMD GPUs | rocm-smi must be installed
    if args.system_gpu or args.system_gpu_ram or args.system_gpu_temp:
        cmd = ["/opt/rocm/bin/rocm-smi", "--showtemp", "--showuse", "--showmemuse", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            ans = json.loads(result.stdout)

            if "card0" in ans:
                gpu_data = ans["card0"]

                if args.system_gpu:
                    gpu_use = int(float(gpu_data.get("GPU use (%)", 0)))
                    widgets.gpu.set(padnum(int(gpu_use)) + "%")

                if args.system_gpu_ram:
                    gpu_ram = int(float(gpu_data.get("GPU memory use (%)", 0)))
                    widgets.gpu_ram.set(padnum(int(gpu_ram)) + "%")

                if args.system_gpu_temp:
                    gpu_temp = int(float(gpu_data.get("Temperature (Sensor junction) (C)", 0)))
                    widgets.gpu_temp.set(padnum(int(gpu_temp)) + "°C")

    if args.system_colors:
        check_color("cpu", cpu)
        check_color("ram", ram)
        check_color("temp", temp)
        check_color("gpu", gpu_use)
        check_color("gpu_ram", gpu_ram)
        check_color("gpu_temp", gpu_temp)


def check() -> None:
    timeutils.sleep(1)

    while True:
        if app.system_frame_visible:
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
