# Modules
from .config import config
from .theme import Theme

# Standard
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import subprocess
from typing import List, Any
import shutil
import platform
import urllib.parse


class App:
    def __init__(self) -> None:
        self.here = Path(__file__).parent.expanduser().resolve()

        with open(Path(self.here, "manifest.json", encoding="utf-8"), "r") as file:
            self.manifest = json.load(file)

        title = self.manifest["title"]
        self.root = tk.Tk(className=self.manifest["program"])
        self.root.title(title)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(background="red")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.minsize(100, 100)
        self.setup_images()
        self.setup_focus()
        self.setup_binds()
        self.theme: Theme

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
            "Normal.TCombobox", fieldbackground=[
                ("readonly", self.theme.combobox_background)], fieldforeground=[
                ("readonly", self.theme.combobox_foreground)])
        style.map("Normal.TCombobox", selectbackground=[("readonly", "transparent")],
                  selectforeground=[("readonly", self.theme.combobox_foreground)])
        style.configure("Normal.TCombobox", borderwidth=0)
        style.configure("Normal.TCombobox.Listbox", padding=0)
        style.configure("Normal.TCombobox", padding=[4, 2, 0, 2])
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

        style.map(
            "Disabled.TCombobox", fieldbackground=[
                ("readonly", self.theme.combobox_background)], fieldforeground=[
                ("readonly", self.theme.combobox_foreground)])
        style.configure("Disabled.TCombobox", padding=[4, 2, 0, 2])
        style.configure("Disabled.TCombobox", borderwidth=0)

        style.configure("Normal.TEntry", fieldbackground=self.theme.entry_background)
        style.configure("Normal.TEntry", foreground=self.theme.entry_foreground)
        style.configure("Normal.TEntry", borderwidth=0)
        style.configure("Normal.TEntry", padding=[4, 0, 0, 0])
        style.configure("Normal.TEntry", insertcolor=self.theme.entry_insert)
        style.configure("Normal.TEntry", selectbackground=self.theme.entry_selection_background)
        style.configure("Normal.TEntry", selectforeground=self.theme.entry_selection_foreground)

        style.configure("Normal.Vertical.TScrollbar", gripcount=0,
                        background=self.theme.scrollbar_2, troughcolor=self.theme.scrollbar_1, borderwidth=0)

        style.map("Normal.Vertical.TScrollbar",
                  background=[("disabled", self.theme.scrollbar_1)],
                  troughcolor=[("disabled", self.theme.scrollbar_1)],
                  borderwidth=[("disabled", 0)])

        style.configure("Normal.Horizontal.TScrollbar", gripcount=0,
                        background=self.theme.scrollbar_2, troughcolor=self.theme.scrollbar_1, borderwidth=0)

        style.map("Normal.Horizontal.TScrollbar",
                  background=[("disabled", self.theme.scrollbar_1)],
                  troughcolor=[("disabled", self.theme.scrollbar_1)],
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

        if args.maximized:
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
        widgets.system_frame.grid_remove()
        widgets.details_frame.grid_remove()
        widgets.addons_frame.grid_remove()
        self.after_compact(True)

    def disable_compact(self) -> None:
        from .widgets import widgets
        widgets.system_frame.grid()
        widgets.details_frame.grid()
        widgets.addons_frame.grid()
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
            subprocess.Popen(cmd, start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except BaseException as e:
            print(e)

    def open_url(self, url: str) -> None:
        if not url:
            return

        cmd = [self.get_opener(), url]
        self.run_command(cmd)

    def search_text(self, text: str) -> None:
        base_url = "https://www.google.com/search?"
        query_params = {"q": text}
        url = base_url + urllib.parse.urlencode(query_params)
        self.open_url(url)

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

    def setup_focus(self) -> None:
        self.root.bind("<FocusIn>", lambda e: self.on_focus_in(e))
        self.root.bind("<FocusOut>", lambda e: self.on_focus_out(e))

    def on_focus_in(self, event: Any) -> None:
        from .dialogs import Dialog
        from .menus import Menu
        what = str(event.widget)

        if what == ".":
            Dialog.focus()
            Menu.focus()

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

    def show_intro(self, tab_id: str = "") -> None:
        from .display import display
        text = "\n".join(self.intro)
        display.print(text, tab_id=tab_id)

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
        from .dialogs import Dialog
        from .menus import Menu
        Dialog.hide_all()
        Menu.hide_all()

    def toggle_fullscreen(self) -> None:
        if self.root.attributes("-fullscreen"):
            self.unfullscreen()
        else:
            self.fullscreen()

    def fullscreen(self) -> None:
        self.root.attributes("-fullscreen", True)

    def unfullscreen(self) -> None:
        self.root.attributes("-fullscreen", False)

    def show_help(self, what: str) -> None:
        from .display import display
        from .commands import commands
        from .keyboard import keyboard
        from .args import args

        if what == "commands":
            tab_id = display.make_tab("Commands", mode="ignore")
            commands.show_help(tab_id=tab_id)
        elif what == "arguments":
            tab_id = display.make_tab("Arguments", mode="ignore")
            args.show_help(tab_id=tab_id)
        elif what == "keyboard":
            tab_id = display.make_tab("Keyboard", mode="ignore")
            keyboard.show_help(tab_id=tab_id)

        display.to_top(tab_id=tab_id)


app = App()
