# Standard
import os
import json
import subprocess
import threading
from typing import Optional, Dict

# Libraries
import psutil  # type: ignore

# Modules
from .widgets import widgets
from .args import args
from .app import app
from .utils import utils


Info = Dict[str, Optional[int]]


def get_psutil_info() -> Info:
    info: Info = {}

    cpu: Optional[int] = None
    ram: Optional[int] = None
    temp: Optional[int] = None

    if args.system_cpu:
        cpu = int(psutil.cpu_percent(interval=1))
        widgets.cpu.set(utils.padnum(cpu) + "%")

    if args.system_ram:
        ram = int(psutil.virtual_memory().percent)
        widgets.ram.set(utils.padnum(ram) + "%")

    if args.system_temp:
        temps = psutil.sensors_temperatures()
        ktemps = temps.get("k10temp")

        if ktemps:
            for ktemp in ktemps:
                # This one works with AMD Ryzen
                if ktemp.label == "Tctl":
                    temp = int(ktemp.current)
                    break

        if temp:
            widgets.temp.set(utils.padnum(temp) + "°")
        else:
            widgets.temp.set("N/A")

    info["cpu"] = cpu
    info["ram"] = ram
    info["temp"] = temp

    return info


def get_gpu_info() -> Info:
    info: Info = {}

    gpu_use: Optional[int] = None
    gpu_ram: Optional[int] = None
    gpu_temp: Optional[int] = None

    # This works with AMD GPUs | rocm-smi must be installed
    if args.system_gpu or args.system_gpu_ram or args.system_gpu_temp:
        rocm_smi = "/opt/rocm/bin/rocm-smi"

        if not os.path.isfile(rocm_smi):
            return info

        cmd = [
            rocm_smi,
            "--showtemp",
            "--showuse",
            "--showmemuse",
            "--json",
        ]

        result = None

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except BaseException as e:
            utils.error(e)
            return info

        if result and result.returncode == 0:
            ans = json.loads(result.stdout)

            if "card0" in ans:
                gpu_data = ans["card0"]

                if args.system_gpu:
                    gpu_use = int(float(gpu_data.get("GPU use (%)", 0)))
                    widgets.gpu.set(utils.padnum(int(gpu_use)) + "%")

                if args.system_gpu_ram:
                    gpu_ram = int(float(gpu_data.get("GPU memory use (%)", 0)))
                    widgets.gpu_ram.set(utils.padnum(int(gpu_ram)) + "%")

                if args.system_gpu_temp:
                    gpu_temp = int(
                        float(gpu_data.get("Temperature (Sensor junction) (C)", 0))
                    )
                    widgets.gpu_temp.set(utils.padnum(int(gpu_temp)) + "°C")

    info["gpu_use"] = gpu_use
    info["gpu_ram"] = gpu_ram
    info["gpu_temp"] = gpu_temp

    return info


def get_info() -> None:
    cpu_info = get_psutil_info()
    gpu_info = get_gpu_info()

    if args.system_colors:
        set_colors(cpu_info, gpu_info)


def set_colors(cpu_info: Info, gpu_info: Info) -> None:
    cpu = cpu_info.get("cpu")
    ram = cpu_info.get("ram")
    temp = cpu_info.get("temp")

    gpu_use = gpu_info.get("gpu_use")
    gpu_ram = gpu_info.get("gpu_ram")
    gpu_temp = gpu_info.get("gpu_temp")

    if cpu is not None:
        check_color("cpu", cpu)

    if ram is not None:
        check_color("ram", ram)

    if temp is not None:
        check_color("temp", temp)

    if gpu_use is not None:
        check_color("gpu", gpu_use)

    if gpu_ram is not None:
        check_color("gpu_ram", gpu_ram)

    if gpu_temp is not None:
        check_color("gpu_temp", gpu_temp)


def check_color(name: str, var: int) -> None:
    if getattr(args, f"system_{name}"):
        label = getattr(widgets, f"{name}_text")

        if var >= args.system_threshold:
            label.configure(foreground=app.theme.system_heavy)
        else:
            label.configure(foreground=app.theme.system_normal)


def check() -> None:
    utils.sleep(1)

    while True:
        if app.system_frame_visible:
            try:
                get_info()
            except BaseException as e:
                utils.error(e)

        utils.sleep(args.system_delay)


def start() -> None:
    if not args.system:
        return

    if not args.quiet:
        msg = f"Updating system monitors every {args.system_delay} seconds"
        utils.msg(msg)

    thread = threading.Thread(target=lambda: check())
    thread.daemon = True
    thread.start()
