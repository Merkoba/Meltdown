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
        self.resize()
        self.root.grid_columnconfigure(0, weight=1)
        icon_path = Path(self.here, "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_path))

        style = ttk.Style()

        # padding=[left, top, right, bottom])
        style.configure("Normal.TCombobox", foreground="white")
        style.map("Normal.TCombobox", fieldbackground=[("readonly", config.button_background)], fieldforeground=[("readonly", "white")])
        style.map("Normal.TCombobox", selectbackground=[("readonly", "transparent")], selectforeground=[("readonly", "white")])
        style.configure("Normal.TCombobox", borderwidth=0)
        style.configure("Normal.TCombobox.Listbox", padding=0)
        style.configure("Normal.TCombobox", padding=[6, 2, 0, 2])
        self.root.option_add("*TCombobox*Listbox.font", ("sans", 13))

        style.configure("Disabled.TCombobox", padding=[6, 2, 0, 2])
        style.configure("Disabled.TCombobox", borderwidth=0)

        style.configure("Normal.TButton", background=config.button_background)
        style.configure("Normal.TButton", foreground=config.button_foreground)
        style.configure("Normal.TButton", borderwidth=0)
        style.configure("Normal.TButton", padding=[0, 0, 0, 0])
        style.configure("Normal.TButton", font=config.font_button)

        style.configure("Green.TButton", background=config.green_background)
        style.configure("Green.TButton", foreground=config.button_foreground)
        style.configure("Green.TButton", borderwidth=0)
        style.configure("Green.TButton", padding=[0, 0, 0, 0])
        style.configure("Green.TButton", font=config.font_button)

        style.configure("Disabled.TButton", borderwidth=0)
        style.configure("Disabled.TButton", padding=[0, 0, 0, 0])
        style.configure("Disabled.TButton", font=config.font_button)

        style.map("Disabled.TButton",
                  background=[("disabled", config.background_disabled), ("active", config.background_disabled)],
                  foreground=[("disabled", config.button_foreground)],
                  )

        style.map("Normal.TButton",
                  background=[("active", config.button_background_hover)]
                  )

        style.map("Green.TButton",
                  background=[("active", config.green_button_background_hover)]
                  )

    def run(self) -> None:
        self.root.mainloop()

    def exit(self) -> None:
        self.root.quit()

    def exists(self) -> bool:
        try:
            return app.root.winfo_exists()
        except RuntimeError:
            return False
        except tk.TclError:
            return False

    def show_about(self) -> None:
        from . import widgetutils
        widgetutils.show_message(f"{config.title} v{config.version}")

    def resize(self) -> None:
        self.root.geometry(f"{config.width}x{config.height}")


app = App()
