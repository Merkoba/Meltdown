# Standard
import json
import subprocess
import threading
import tkinter as tk
from typing import Optional
from pathlib import Path

# Libraries
import psutil  # type: ignore

# Modules
from .widgets import widgets
from .args import args
from .app import app
from .utils import utils
from .framedata import FrameData
from .tooltips import ToolTip
from .tips import tips
from . import widgetutils


class System:
    def __init__(self) -> None:
        self.cpu: Optional[int] = None
        self.ram: Optional[int] = None
        self.temp: Optional[int] = None
        self.gpu_use: Optional[int] = None
        self.gpu_ram: Optional[int] = None
        self.gpu_temp: Optional[int] = None

    def set_widget(self, widget: tk.StringVar, text: str) -> None:
        if app.exists():
            widget.set(text)

    def get_psutil_info(self) -> None:
        if args.system_cpu:
            self.cpu = int(psutil.cpu_percent(interval=1))
            self.set_widget(widgets.cpu, utils.padnum(self.cpu) + "%")

        if args.system_ram:
            self.ram = int(psutil.virtual_memory().percent)
            self.set_widget(widgets.ram, utils.padnum(self.ram) + "%")

        if args.system_temp:
            temps = psutil.sensors_temperatures()
            ktemps = temps.get("k10temp")

            if ktemps:
                for ktemp in ktemps:
                    # This one works with AMD Ryzen
                    if ktemp.label == "Tctl":
                        self.temp = int(ktemp.current)
                        break

            if self.temp:
                self.set_widget(widgets.temp, utils.padnum(self.temp) + "°")
            else:
                self.set_widget(widgets.temp, "N/A")

    def get_gpu_info(self) -> None:
        # This works with AMD GPUs | rocm-smi must be installed
        if args.system_gpu or args.system_gpu_ram or args.system_gpu_temp:
            rocm_smi = "/opt/rocm/bin/rocm-smi"

            if not Path(rocm_smi).is_file():
                return

            cmd = [
                rocm_smi,
                "--showtemp",
                "--showuse",
                "--showmemuse",
                "--json",
            ]

            result = None

            try:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=False
                )
            except BaseException:
                return

            if result and result.returncode == 0:
                ans = json.loads(result.stdout)

                if "card0" in ans:
                    gpu_data = ans["card0"]

                    if args.system_gpu:
                        self.gpu_use = int(float(gpu_data.get("GPU use (%)", 0)))

                        self.set_widget(
                            widgets.gpu, utils.padnum(int(self.gpu_use)) + "%"
                        )

                    if args.system_gpu_ram:
                        self.gpu_ram = int(float(gpu_data.get("GPU memory use (%)", 0)))

                        self.set_widget(
                            widgets.gpu_ram, utils.padnum(int(self.gpu_ram)) + "%"
                        )

                    if args.system_gpu_temp:
                        self.gpu_temp = int(
                            float(gpu_data.get("Temperature (Sensor junction) (C)", 0))
                        )

                        self.set_widget(
                            widgets.gpu_temp, utils.padnum(int(self.gpu_temp)) + "°C"
                        )

    def get_info(self) -> None:
        self.get_psutil_info()
        self.get_gpu_info()

        if args.system_colors:
            self.set_colors()

    def set_colors(self) -> None:
        if self.cpu is not None:
            self.check_color("cpu", self.cpu)

        if self.ram is not None:
            self.check_color("ram", self.ram)

        if self.temp is not None:
            self.check_color("temp", self.temp)

        if self.gpu_use is not None:
            self.check_color("gpu", self.gpu_use)

        if self.gpu_ram is not None:
            self.check_color("gpu_ram", self.gpu_ram)

        if self.gpu_temp is not None:
            self.check_color("gpu_temp", self.gpu_temp)

    def check_color(self, name: str, var: int) -> None:
        if getattr(args, f"system_{name}"):
            label = getattr(widgets, f"{name}_text")

            if var >= args.system_threshold:
                label.configure(foreground=app.theme.system_heavy)
            else:
                label.configure(foreground=app.theme.system_normal)

    def start_loop(self) -> None:
        utils.sleep(1)

        while True:
            if app.system_frame_enabled:
                try:
                    self.get_info()
                except BaseException as e:
                    utils.error(e)

            utils.sleep(args.system_delay)

    def start(self) -> None:
        if args.system_delay < 0.1:
            return

        if not args.quiet:
            msg = f"Updating system monitors every {args.system_delay} seconds"
            utils.msg(msg)

        thread = threading.Thread(target=lambda: self.start_loop())
        thread.daemon = True
        thread.start()

    def reset(self) -> None:
        self.cpu = None
        self.ram = None
        self.temp = None
        self.gpu_use = None
        self.gpu_ram = None
        self.gpu_temp = None

        text = "000%"

        self.set_widget(widgets.cpu, text)
        self.set_widget(widgets.ram, text)
        self.set_widget(widgets.temp, text)
        self.set_widget(widgets.gpu, text)
        self.set_widget(widgets.gpu_ram, text)
        self.set_widget(widgets.gpu_temp, text)

        self.check_color("cpu", 0)
        self.check_color("ram", 0)
        self.check_color("temp", 0)
        self.check_color("gpu", 0)
        self.check_color("gpu_ram", 0)
        self.check_color("gpu_temp", 0)

    def add_monitors(self, data: FrameData) -> None:
        first = False

        def make_monitor(name: str, label_text: str, mode: str) -> None:
            nonlocal first

            if not first:
                padx = (0, 0)
                first = True
            else:
                padx = (app.theme.padx, 0)

            label = widgetutils.make_label(
                data, label_text, ignore_short=(not args.short_system), padx=padx
            )

            label.configure(cursor="hand2")
            setattr(widgets, name, tk.StringVar())
            monitor_text = widgetutils.make_label(data, "", padx=(0, app.theme.padx))
            monitor_text.configure(textvariable=getattr(widgets, name))
            monitor_text.configure(cursor="hand2")
            setattr(widgets, f"{name}_text", monitor_text)
            tip = tips[f"system_{name}"]
            ToolTip(label, tip)
            ToolTip(monitor_text, tip)
            getattr(widgets, name).set("000%")

            label.bind("<Button-1>", lambda e: app.open_task_manager(mode))
            monitor_text.bind("<Button-1>", lambda e: app.open_task_manager(mode))

        if args.system_cpu:
            make_monitor("cpu", "CPU", "normal")

        if args.system_ram:
            make_monitor("ram", "RAM", "normal")

        if args.system_temp:
            make_monitor("temp", "TMP", "normal")

        if args.system_gpu:
            make_monitor("gpu", "GPU", "gpu")

        if args.system_gpu_ram:
            make_monitor("gpu_ram", "GPU RAM", "gpu")

        if args.system_gpu_temp:
            make_monitor("gpu_temp", "GPU TMP", "gpu")


system = System()
