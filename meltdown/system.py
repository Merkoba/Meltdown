from __future__ import annotations

# Standard
import json
import subprocess
import threading
import tkinter as tk
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
from .model import model
from .widgetutils import widgetutils


class System:
    def __init__(self) -> None:
        self.cpu: int | None = None
        self.ram: int | None = None
        self.temp: int | None = None
        self.gpu_use: int | None = None
        self.gpu_ram: int | None = None
        self.gpu_temp: int | None = None
        self.clean = True

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

        self.clean = False

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

    def check_color(self, name: str, var: int, reset: bool = False) -> None:
        if getattr(args, f"system_{name}"):
            label = getattr(widgets, f"{name}_text")

            if reset:
                label.configure(foreground=app.theme.foreground_color)
            elif var >= args.system_threshold:
                label.configure(foreground=app.theme.system_heavy)
            else:
                label.configure(foreground=app.theme.system_normal)

    def start_loop(self) -> None:
        utils.sleep(1)
        o_check = True

        while True:
            if app.system_frame_enabled:
                check = True

                if args.system_suspend >= 1:
                    date = model.stream_date_local

                    if not date:
                        check = False
                    else:
                        mins = (utils.now() - date) / 60

                        if mins >= args.system_suspend:
                            check = False

                changed = check != o_check
                o_check = check

                if changed:
                    if args.system_auto_hide:
                        if check:
                            widgets.system_frame.grid()
                        else:
                            widgets.system_frame.grid_remove()

                if check:
                    try:
                        self.get_info()
                    except BaseException as e:
                        utils.error(e)
                elif changed:
                    self.reset()

            utils.sleep(args.system_delay)

    def start(self) -> None:
        if args.system_delay < 1:
            return

        if not args.quiet:
            m = utils.singular_or_plural(args.system_delay, "sec", "secs")
            msg = f"System monitors active ({args.system_delay} {m})"
            utils.msg(msg)

        thread = threading.Thread(target=lambda: self.start_loop())
        thread.daemon = True
        thread.start()

    def reset(self) -> None:
        if self.clean:
            return

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

        self.check_color("cpu", 0, True)
        self.check_color("ram", 0, True)
        self.check_color("temp", 0, True)
        self.check_color("gpu", 0, True)
        self.check_color("gpu_ram", 0, True)
        self.check_color("gpu_temp", 0, True)

        self.clean = True

    def add_items(self) -> None:
        data = FrameData(widgets.scroller_system)
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
