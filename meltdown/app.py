# Modules
from .config import config

# Standard
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import subprocess
from typing import List
import shutil


class App:
    def __init__(self) -> None:
        self.here = Path(__file__).parent.expanduser().resolve()

        with open(Path(self.here, "manifest.json"), "r") as file:
            self.manifest = json.load(file)

        self.root = tk.Tk(className=self.manifest["program"])
        self.root.title(self.manifest["title"])
        self.root.grid_columnconfigure(0, weight=1)
        self.set_geometry()
        self.setup_icon()
        self.setup_style()

    def setup_icon(self) -> None:
        icon_path = Path(self.here, "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_path))

    def setup_style(self) -> None:
        style = ttk.Style()
        self.root.configure(background=config.background_color)

        # padding=[left, top, right, bottom])

        style.configure("Normal.TCombobox", foreground="white")
        style.map("Normal.TCombobox", fieldbackground=[("readonly", config.combobox_background)], fieldforeground=[("readonly", "white")])
        style.map("Normal.TCombobox", selectbackground=[("readonly", "transparent")], selectforeground=[("readonly", "white")])
        style.configure("Normal.TCombobox", borderwidth=0)
        style.configure("Normal.TCombobox.Listbox", padding=0)
        style.configure("Normal.TCombobox", padding=[4, 2, 0, 2])
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

        style.map("Disabled.TCombobox", fieldbackground=[("readonly", config.combobox_background)], fieldforeground=[("readonly", "white")])
        style.configure("Disabled.TCombobox", padding=[4, 2, 0, 2])
        style.configure("Disabled.TCombobox", borderwidth=0)

        style.configure("Normal.TEntry", fieldbackground=config.entry_background)
        style.configure("Normal.TEntry", foreground=config.entry_foreground)
        style.configure("Normal.TEntry", borderwidth=0)
        style.configure("Normal.TEntry", padding=[4, 0, 0, 0])
        style.configure("Normal.TEntry", insertcolor="white")

        style.configure("Input.TEntry", fieldbackground="white")
        style.configure("Input.TEntry", foreground="black")
        style.configure("Input.TEntry", borderwidth=1)
        style.configure("Input.TEntry", padding=[4, 0, 0, 0])
        style.configure("Input.TEntry", insertcolor="black")

        style.configure("Normal.TNotebook", borderwidth=0)
        style.configure("Normal.TNotebook", background=config.entry_background)
        style.configure("Normal.TNotebook.Tab", padding=[18, 2])
        style.configure("Normal.TNotebook.Tab", font=config.font_tab)

        style.map("Normal.TNotebook.Tab", background=[
            ("selected", "#494D62"),
            ("!selected", "#2B303B"),
        ])

        style.map("Normal.TNotebook.Tab", foreground=[
            ("selected", "white"),
            ("!selected", "white"),
        ])

        style.layout("Normal.TNotebook.Tab", [
            ("Notebook.tab", {"sticky": "nswe", "children": [
                ("Notebook.padding", {"side": "top", "sticky": "nswe", "children": [
                    ("Notebook.label", {"side": "top", "sticky": ""})
                ]})
            ],
            })])

        style.configure("Normal.Vertical.TScrollbar", gripcount=0,
                        background="#494D62", troughcolor="#333B4B", borderwidth=0)

        style.map("Normal.Vertical.TScrollbar",
                  background=[("disabled", "#333B4B")],
                  troughcolor=[("disabled", "#333B4B")],
                  borderwidth=[("disabled", 0)])

    def setup(self) -> None:
        self.check_compact()

    def run(self) -> None:
        self.root.mainloop()

    def exit(self) -> None:
        self.root.destroy()

    def exists(self) -> bool:
        try:
            return self.root.winfo_exists()
        except RuntimeError:
            return False
        except tk.TclError:
            return False

    def show_about(self) -> None:
        from .dialogs import Dialog
        title = self.manifest["title"]
        version = self.manifest["version"]
        author = self.manifest["author"]
        licens = self.manifest["license"]

        lines = [
            f"{title} v{version}",
            "Interface for llama.cpp",
            f"Developer: {author}",
            f"License: {licens}",
        ]

        Dialog.show_message("\n".join(lines))

    def toggle_maximize(self) -> None:
        if self.root.attributes("-zoomed"):
            self.unmaximize()
        else:
            self.maximize()

    def maximize(self, update: bool = True) -> None:
        self.root.attributes("-zoomed", True)

        if update:
            self.update_bottom()

    def unmaximize(self, update: bool = True) -> None:
        self.root.attributes("-zoomed", False)

        if update:
            self.update_bottom()

    def set_geometry(self) -> None:
        self.root.geometry(f"{config.width}x{config.height}")

    def update(self) -> None:
        self.root.update_idletasks()

    def update_bottom(self) -> None:
        from .widgets import widgets
        widgets.display.output_bottom()

        def action() -> None:
            self.update()
            widgets.display.output_bottom()

        self.root.after(100, lambda: action())

    def resize(self) -> None:
        self.unmaximize(False)
        self.set_geometry()
        self.update_bottom()

    def toggle_compact(self) -> None:
        from . import state

        if config.compact:
            self.disable_compact()
        else:
            self.enable_compact()

        state.set_config("compact", not config.compact)

    def enable_compact(self) -> None:
        from .widgets import widgets
        widgets.system_frame.grid_remove()
        widgets.details_frame.grid_remove()
        widgets.addons_frame.grid_remove()
        self.after_compact()

    def disable_compact(self) -> None:
        from .widgets import widgets
        widgets.system_frame.grid()
        widgets.details_frame.grid()
        widgets.addons_frame.grid()
        self.after_compact()

    def after_compact(self) -> None:
        from .widgets import widgets
        self.update()
        widgets.display.output_bottom()
        widgets.focus_input()

    def check_compact(self) -> None:
        if config.compact:
            self.enable_compact()
        else:
            self.disable_compact()

    def run_command(self, cmd: List[str]) -> None:
        try:
            subprocess.Popen(cmd, start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except BaseException as e:
            print(e)

    def open_task_manager(self) -> None:
        if shutil.which("alacritty"):
            cmd = ["alacritty", "-e"]
        elif shutil.which("konsole"):
            cmd = ["konsole", "-e"]
        elif shutil.which("xterm"):
            cmd = ["xterm", "-e"]
        else:
            return

        if shutil.which("btop"):
            cmd.extend(["btop"])
        elif shutil.which("htop"):
            cmd.extend(["htop"])
        elif shutil.which("top"):
            cmd.extend(["top"])
        else:
            return

        self.run_command(cmd)


app = App()
