# Modules
from .config import config

# Standard
import tkinter as tk
from tkinter import ttk
from pathlib import Path


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.here = Path(__file__).parent.expanduser().resolve()
        self.root.title(config.title)
        self.root.geometry(f"{config.width}x{config.height}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        icon_path = Path(self.here, "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_path))

        style = ttk.Style()
        style.configure("TCombobox", foreground="white")
        style.map("TCombobox", fieldbackground=[("readonly", config.button_background)], fieldforeground=[("readonly", "white")])
        style.map("TCombobox", selectbackground=[("readonly", "transparent")], selectforeground=[("readonly", "white")])
        style.configure("TCombobox", borderwidth=0)
        style.configure("TCombobox.Listbox", padding=0)
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

    def run(self) -> None:
        self.root.mainloop()

    def exit(self) -> None:
        self.root.quit()

    def exists(self) -> bool:
        try:
            return app.root.winfo_exists()
        except tk.TclError:
            return False

    def show_about(self) -> None:
        from . import widgetutils
        widgetutils.show_message("Meltdown v1.0.0")


app = App()
