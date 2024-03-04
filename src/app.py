# Modules
from config import config

# Libraries
import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry(f"{config.width}x{config.height}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        style = ttk.Style()
        style.configure("TCombobox", foreground="white")
        style.map("TCombobox", fieldbackground=[("readonly", config.button_background)], fieldforeground=[("readonly", "white")])
        style.map("TCombobox", selectbackground=[("readonly", "transparent")], selectforeground=[("readonly", "white")])
        style.configure("TCombobox", borderwidth=0)
        style.configure("TCombobox.Listbox", padding=0)
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

    def exit(self) -> None:
        self.root.quit()


app = App()
