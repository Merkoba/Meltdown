# Modules
from config import config

# Libraries
import tkinter as tk
from tkinter import ttk
from pathlib import Path


class App:
    def __init__(self) -> None:
        self.here = Path(__file__).parent.expanduser().resolve()
        self.root = tk.Tk()
        self.root.title(config.title)
        self.root.geometry(f"{config.width}x{config.height}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        icon_file = Path(self.here.parent, "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_file))

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


app = App()
