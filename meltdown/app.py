# Standard
import os
import sys
import json
import subprocess
import shutil
import tempfile
import platform
import urllib.parse
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import List, Any, Optional

# Modules
from .config import config
from .theme import Theme
from .utils import utils


class App:
    def __init__(self) -> None:
        self.here = Path(__file__).parent.expanduser().resolve()

        with open(Path(self.here, "manifest.json", encoding="utf-8"), "r") as file:
            self.manifest = json.load(file)

        title = self.manifest["title"]
        self.root = tk.Tk(className=self.manifest["program"])
        self.root.title(title)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        self.main_frame.configure(background="red")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.minsize(100, 100)
        self.autorun_delay = 250
        self.setup_images()
        self.setup_focus()
        self.setup_binds()
        self.theme: Theme
        self.sticky = False
        self.exit_delay = 100
        self.exit_after: str = ""
        self.streaming = False
        self.loading = False
        self.loaded = False
        self.checks_delay = 200
        self.system_frame_visible = True

        self.intro = [
            f"Welcome to {title}.",
            "Write a prompt and press Enter.",
            "Use /help to learn more.",
        ]

    def setup_images(self) -> None:
        self.icon_path = Path(self.here, "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=self.icon_path))
        self.image_path = Path(self.here, "image.jpg")

    def set_style(self) -> None:
        style = ttk.Style()
        self.root.configure(background=self.theme.background_color)
        self.main_frame.configure(background=self.theme.background_color)

        # padding=[left, top, right, bottom])

        style.configure("Normal.TCombobox", foreground=self.theme.combobox_foreground)
        style.map(
            "Normal.TCombobox",
            fieldbackground=[("readonly", self.theme.combobox_background)],
            fieldforeground=[("readonly", self.theme.combobox_foreground)],
        )
        style.map(
            "Normal.TCombobox",
            selectbackground=[("readonly", "transparent")],
            selectforeground=[("readonly", self.theme.combobox_foreground)],
        )
        style.configure("Normal.TCombobox", borderwidth=0)
        style.configure("Normal.TCombobox.Listbox", padding=0)
        style.configure("Normal.TCombobox", padding=[4, 2, 0, 2])
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

        style.map(
            "Disabled.TCombobox",
            fieldbackground=[("readonly", self.theme.combobox_background)],
            fieldforeground=[("readonly", self.theme.combobox_foreground)],
        )
        style.configure("Disabled.TCombobox", padding=[4, 2, 0, 2])
        style.configure("Disabled.TCombobox", borderwidth=0)

        style.configure("Normal.TEntry", fieldbackground=self.theme.entry_background)
        style.configure("Normal.TEntry", foreground=self.theme.entry_foreground)
        style.configure("Normal.TEntry", borderwidth=0)
        style.configure("Normal.TEntry", padding=[4, 0, 0, 0])
        style.configure("Normal.TEntry", insertcolor=self.theme.entry_insert)
        style.configure(
            "Normal.TEntry", selectbackground=self.theme.entry_selection_background
        )
        style.configure(
            "Normal.TEntry", selectforeground=self.theme.entry_selection_foreground
        )

        style.configure(
            "Normal.Vertical.TScrollbar",
            gripcount=0,
            background=self.theme.scrollbar_2,
            troughcolor=self.theme.scrollbar_1,
            borderwidth=0,
        )

        style.map(
            "Normal.Vertical.TScrollbar",
            background=[("disabled", self.theme.scrollbar_1)],
            troughcolor=[("disabled", self.theme.scrollbar_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Normal.Horizontal.TScrollbar",
            gripcount=0,
            background=self.theme.scrollbar_2,
            troughcolor=self.theme.scrollbar_1,
            borderwidth=0,
        )

        style.map(
            "Normal.Horizontal.TScrollbar",
            background=[("disabled", self.theme.scrollbar_1)],
            troughcolor=[("disabled", self.theme.scrollbar_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Dialog.Vertical.TScrollbar",
            gripcount=0,
            background=self.theme.scrollbar_dialog_2,
            troughcolor=self.theme.scrollbar_dialog_1,
            borderwidth=0,
        )

        style.map(
            "Dialog.Vertical.TScrollbar",
            background=[("disabled", self.theme.scrollbar_dialog_1)],
            troughcolor=[("disabled", self.theme.scrollbar_dialog_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Dialog.Horizontal.TScrollbar",
            gripcount=0,
            background=self.theme.scrollbar_dialog_2,
            troughcolor=self.theme.scrollbar_dialog_1,
            borderwidth=0,
        )

        style.map(
            "Dialog.Horizontal.TScrollbar",
            background=[("disabled", self.theme.scrollbar_dialog_1)],
            troughcolor=[("disabled", self.theme.scrollbar_dialog_1)],
            borderwidth=[("disabled", 0)],
        )

    def setup(self) -> None:
        self.check_commandoc()
        self.check_compact()
        self.check_display()
        self.check_sticky()

    def check_display(self) -> None:
        from .args import args

        if args.display:
            self.hide_frames()

    def run(self) -> None:
        self.root.mainloop()

    def exit(self, delay: Optional[float] = None) -> None:
        self.cancel_exit()
        d = int((delay * 1000)) if delay else self.exit_delay
        d = d if d >= self.exit_delay else self.exit_delay
        self.exit_after = self.root.after(d, lambda: self.root.destroy())

    def cancel_exit(self, feedback: bool = False) -> None:
        from .display import display

        if self.exit_after:
            self.root.after_cancel(self.exit_after)
            self.exit_after = ""

            if feedback:
                display.print("Exit cancelled")
        elif feedback:
            display.print("No exit to cancel")

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

        lines = [
            f"{title} v{version}",
            f"Developed by {author}",
            "All Rights Reserved",
        ]

        cmds = []
        cmds.append(("Commands", lambda: self.show_help("commands")))
        cmds.append(("Arguments", lambda: self.show_help("arguments")))
        cmds.append(("Keyboard", lambda: self.show_help("keyboard")))
        cmds.append(("Ok", lambda: None))

        Dialog.show_commands("\n".join(lines), cmds, image=self.image_path)

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
        from .args import args

        width = args.width if args.width != -1 else self.theme.width
        height = args.height if args.height != -1 else self.theme.height
        self.root.geometry(f"{width}x{height}")

        if args.maximize:
            app.update()
            self.maximize(False)

    def update(self) -> None:
        self.root.update_idletasks()

    def update_bottom(self) -> None:
        from .display import display

        display.to_bottom()

        def action() -> None:
            self.update()
            display.to_bottom()

        self.root.after(100, lambda: action())

    def resize(self) -> None:
        self.unmaximize(False)
        self.set_geometry()
        self.update_bottom()

    def toggle_compact(self) -> None:
        if config.compact:
            self.disable_compact()
        else:
            self.enable_compact()

    def enable_compact(self) -> None:
        from .widgets import widgets
        from .args import args

        if args.display:
            return

        confs = [
            args.compact_model,
            args.compact_system,
            args.compact_details,
            args.compact_buttons,
            args.compact_addons,
            args.compact_input,
        ]

        custom = any(confs)

        if custom:
            if args.compact_model:
                widgets.model_frame.grid_remove()

            if args.compact_system:
                widgets.system_frame.grid_remove()
                self.system_frame_visible = False

            if args.compact_details:
                widgets.details_frame.grid_remove()

            if args.compact_buttons:
                widgets.buttons_frame.grid_remove()

            if args.compact_addons:
                widgets.addons_frame.grid_remove()

            if args.compact_input:
                widgets.input_frame.grid_remove()
        else:
            widgets.system_frame.grid_remove()
            widgets.details_frame.grid_remove()
            widgets.addons_frame.grid_remove()
            self.system_frame_visible = False

        self.after_compact(True)

    def disable_compact(self) -> None:
        from .widgets import widgets
        from .args import args

        if args.display:
            return

        widgets.model_frame.grid()
        widgets.system_frame.grid()
        widgets.details_frame.grid()
        widgets.buttons_frame.grid()
        widgets.addons_frame.grid()
        widgets.input_frame.grid()
        self.system_frame_visible = True
        self.after_compact(False)

    def after_compact(self, enabled: bool) -> None:
        from .inputcontrol import inputcontrol
        from .display import display
        from .config import config

        self.update()
        display.to_bottom()
        inputcontrol.focus()
        config.set("compact", enabled)

    def check_compact(self) -> None:
        from .args import args

        if args.full:
            self.disable_compact()
        elif args.compact:
            self.enable_compact()
        elif config.compact:
            self.enable_compact()
        else:
            self.disable_compact()

    def get_opener(self) -> str:
        system = platform.system()
        opener = ""

        if system == "Darwin":
            opener = "open"
        elif system == "Windows":
            opener = "start"
        else:
            opener = "xdg-open"

        return opener

    def run_command(self, cmd: List[str]) -> None:
        try:
            subprocess.Popen(
                cmd,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        except BaseException as e:
            utils.error(e)

    def open_url(self, url: str) -> None:
        from .args import args

        if not url:
            return

        if args.browser:
            cmd = [args.browser, url]
        else:
            cmd = [self.get_opener(), url]

        self.run_command(cmd)

    def search_text(self, text: str) -> None:
        base_url = "https://www.google.com/search?"
        query_params = {"q": text}
        url = base_url + urllib.parse.urlencode(query_params)
        self.open_url(url)

    def open_task_manager(self) -> None:
        from .args import args

        if args.terminal == "auto":
            if shutil.which("alacritty"):
                cmd = ["alacritty", "-e"]
            elif shutil.which("terminator"):
                cmd = ["terminator", "-e"]
            elif shutil.which("konsole"):
                cmd = ["konsole", "-e"]
            elif shutil.which("xterm"):
                cmd = ["urxvt", "-e"]
            elif shutil.which("xterm"):
                cmd = ["xterm", "-e"]
            else:
                return
        else:
            cmd = [args.terminal, "-e"]

        if args.task_manager == "auto":
            if shutil.which("btop"):
                cmd.extend(["btop"])
            elif shutil.which("htop"):
                cmd.extend(["htop"])
            elif shutil.which("top"):
                cmd.extend(["top"])
            else:
                return
        else:
            cmd.extend([args.task_manager])

        self.run_command(cmd)

    def setup_focus(self) -> None:
        self.root.bind("<FocusIn>", lambda e: self.on_focus_in(e))
        self.root.bind("<FocusOut>", lambda e: self.on_focus_out(e))

    def on_focus_in(self, event: Any) -> None:
        from .dialogs import Dialog
        from .menus import Menu

        what = str(event.widget)

        if what == ".":
            Dialog.focus_all()
            Menu.focus_all()

    def on_focus_out(self, event: Any) -> None:
        from .keyboard import keyboard

        what = str(event.widget)

        if what == ".":
            keyboard.reset()

    def prepare(self) -> None:
        self.set_theme()
        self.set_style()
        self.set_geometry()

    def set_theme(self) -> None:
        from .args import args
        from .light_theme import LightTheme
        from .dark_theme import DarkTheme
        from .config import config

        if args.theme and (args.theme != config.theme):
            config.set("theme", args.theme)

        if config.theme == "light":
            self.theme = LightTheme()
        else:
            self.theme = DarkTheme()

    def toggle_theme(self) -> None:
        from .dialogs import Dialog
        from .config import config

        if config.theme == "light":
            new_theme = "dark"
        else:
            new_theme = "light"

        def action() -> None:
            config.set("theme", new_theme)
            Dialog.show_message("Theme will change after restarting the program")

        Dialog.show_confirm(f"Use the {new_theme} theme?", action)

    def setup_binds(self) -> None:
        self.main_frame.bind("<Button-1>", lambda e: self.on_frame_click())

    def on_frame_click(self) -> None:
        self.hide_all()

    def toggle_fullscreen(self) -> None:
        if self.root.attributes("-fullscreen"):
            self.unfullscreen()
        else:
            self.fullscreen()

    def fullscreen(self) -> None:
        self.root.attributes("-fullscreen", True)

    def unfullscreen(self) -> None:
        self.root.attributes("-fullscreen", False)

    def show_help(self, what: str, mode: Optional[str] = None) -> None:
        from .display import display
        from .commands import commands
        from .keyboard import keyboard
        from .args import args

        if what == "commands":
            tab_id = display.make_tab("Commands", mode="ignore")
            commands.show_help(tab_id=tab_id, mode=mode)
        elif what == "arguments":
            tab_id = display.make_tab("Arguments", mode="ignore")
            args.show_help(tab_id=tab_id, mode=mode)
        elif what == "keyboard":
            tab_id = display.make_tab("Keyboard", mode="ignore")
            keyboard.show_help(tab_id=tab_id, mode=mode)

        display.to_top(tab_id=tab_id)

    def hide_all(self) -> None:
        from .dialogs import Dialog
        from .menus import Menu
        from .tooltips import ToolTip

        Dialog.hide_all()
        Menu.hide_all()
        ToolTip.hide_all()

    def hide_frames(self) -> None:
        from .widgets import widgets

        widgets.model_frame.grid_remove()
        widgets.system_frame.grid_remove()
        widgets.details_frame.grid_remove()
        widgets.buttons_frame.grid_remove()
        widgets.addons_frame.grid_remove()
        widgets.input_frame.grid_remove()

    def autorun(self) -> None:
        from .args import args
        from .commands import commands

        if not args.autorun:
            return

        def action() -> None:
            commands.exec(args.autorun)

        self.root.after(self.autorun_delay, lambda: action())

    def stats(self) -> None:
        from .display import display
        from .commands import commands
        from .keyboard import keyboard
        from .args import args

        lines = []
        lines.append(f"Commands: {len(commands.commands)}")
        lines.append(f"Arguments: {len(vars(args))}")
        lines.append(f"Keyboard: {len(keyboard.commands)}")

        display.print("\n".join(lines))

    def toggle_sticky(self) -> None:
        if self.sticky:
            self.disable_sticky()
        else:
            self.enable_sticky()

    def enable_sticky(self) -> None:
        self.sticky = True
        self.root.attributes("-topmost", True)

    def disable_sticky(self) -> None:
        self.sticky = False
        self.root.attributes("-topmost", False)

    def check_sticky(self) -> None:
        from .args import args

        if args.sticky:
            self.enable_sticky()

    def check_commandoc(self) -> None:
        from .args import args
        from .commands import commands

        if args.commandoc:
            commands.run("commandoc", args.commandoc)
            sys.exit(0)

    def do_checks(self) -> None:
        from .model import model
        from .commands import commands
        from .widgets import widgets
        from .display import display

        if model.streaming:
            if not self.streaming:
                self.streaming = True
                widgets.enable_stop_button()
        else:
            if self.streaming:
                self.streaming = False
                widgets.disable_stop_button()
                display.stream_stopped()
                commands.after_stream()

        model_empty = widgets.model.get() == ""

        if model.model_loading or (model_empty and (not model.loaded_model)):
            if not self.loading:
                self.loading = True
                widgets.disable_load_button()
                widgets.disable_format_select()
        else:
            if self.loading:
                self.loading = False
                widgets.enable_load_button()
                widgets.enable_format_select()

        if model.loaded_model:
            if not self.loaded:
                self.loaded = True
                widgets.load_button.set_text("Unload")

                self.update()
                widgets.model.move_to_end()
        else:
            if self.loaded:
                self.loaded = False
                widgets.load_button.set_text("Load")

                self.update()
                widgets.model.move_to_end()

    def start_checks(self) -> None:
        self.do_checks()
        app.root.after(self.checks_delay, self.start_checks)

    def program(self, mode: str, cmd: Optional[str] = None) -> None:
        from .args import args
        from .session import session
        from .display import display

        if not cmd:
            if mode == "text":
                cmd = args.progtext or args.program
            elif mode == "json":
                cmd = args.progjson or args.program

        if not cmd:
            display.print("No program specified.")
            return

        conversation = session.get_current_conversation()

        if not conversation:
            return

        if mode == "text":
            text = conversation.to_text()
            ext = "txt"
        elif mode == "json":
            text = conversation.to_json()
            ext = "json"
        else:
            return

        tmpdir = tempfile.gettempdir()
        name = f"mlt_{utils.now_int()}.{ext}"
        path = os.path.join(tmpdir, name)

        with open(path, "w", encoding="utf-8") as file:
            file.write(text)

        self.run_command([cmd, path])


app = App()
