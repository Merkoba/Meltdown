# Modules
from config import config
import widgets as w
from widgets import widgets
import tkinter as tk
from tkinter import filedialog
import state

# Libraries
import pyperclip


def exists() -> bool:
    try:
        return config.app.winfo_exists()
    except tk.TclError:
        return False


def output(text: str, linebreak=True) -> None:
    if not exists():
        return

    left = ""
    right = ""

    if output_length() and (last_character() != "\n"):
        left = "\n"

    if linebreak:
        right = "\n"

    text = left + text + right
    w.insert_text(widgets.output, text, True)
    to_bottom()


def insert(text: str) -> None:
    if not exists():
        return

    w.insert_text(widgets.output, text, True)
    to_bottom()


def to_bottom() -> None:
    widgets.output.yview_moveto(1.0)


def output_length() -> int:
    return len(widgets.output.get("1.0", "end-1c"))


def last_character() -> str:
    text = widgets.output.get("1.0", "end-1c")
    return text[-1] if text else None


def submit() -> None:
    from model import model
    text = widgets.input.get()

    if text:
        clear_input()
        model.stream(text)


def clear_output() -> None:
    widgets.output.config(state="normal")
    widgets.output.delete(1.0, "end")
    widgets.output.config(state="disabled")


def clear_input():
    widgets.input.delete(0, "end")


def prompt(num: int) -> None:
    name = getattr(config, f"name_{num}")
    prompt = f"{name}: "
    output(prompt, False)


def show_output_menu(event) -> None:
    widgets.output_menu.post(event.x_root, event.y_root)


def hide_output_menu() -> None:
    widgets.output_menu.unpost()


def select_all() -> None:
    widgets.output.tag_add("sel", "1.0", "end")


def copy_all() -> None:
    text = widgets.output.get("1.0", "end-1c").strip()
    pyperclip.copy(text)


def show_model_menu(event) -> None:
    if not config.models:
        return

    widgets.model_menu.delete(0, tk.END)

    for model in config.models:
        widgets.model_menu.add_command(label=model, command=lambda m=model: set_model(m))

    if event:
        widgets.model_menu.post(event.x_root, event.y_root)
    else:
        show_menu_at_center(widgets.model_menu)


def hide_model_menu() -> None:
    widgets.model_menu.unpost()


def hide_menus() -> None:
    hide_output_menu()
    hide_model_menu()


def set_model(model: str) -> None:
    w.set_text(widgets.model, model)
    state.update_model()


def show_menu_at_center(menu: tk.Menu) -> None:
    update()
    menu.update_idletasks()
    window_width = config.app.winfo_width()
    window_height = config.app.winfo_height()
    window_x = config.app.winfo_rootx()
    window_y = config.app.winfo_rooty()

    menu_width = menu.winfo_reqwidth()
    menu_height = menu.winfo_reqheight()

    x = window_x + (window_width - menu_width) // 2
    y = window_y + (window_height - menu_height) // 2

    menu.post(x, y)


def browse_model() -> None:
    file = filedialog.askopenfilename()
    w.set_text(widgets.model, file)
    state.update_model()


def update() -> None:
    config.app.update_idletasks()


def intro() -> None:
    output("Welcome to Meltdown")
    output("Type a prompt and press Enter to continue")
    output("The specified model with load automatically")


def show_model() -> None:
    w.set_text(widgets.model, config.model)
