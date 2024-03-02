# Modules
from config import config
import widgets
import tkinter as tk
from tkinter import filedialog

# Libraries
import pyperclip


def output(text: str, linebreak=True) -> None:
    left = ""
    right = ""

    if output_length() and (last_character() != "\n"):
        left = "\n"

    if linebreak:
        right = "\n"

    text = left + text + right
    widgets.insert_text(config.output_text, text, True)
    to_bottom()


def insert(text: str) -> None:
    widgets.insert_text(config.output_text, text, True)
    to_bottom()


def to_bottom() -> None:
    config.output_text.yview_moveto(1.0)


def output_length() -> int:
    return len(config.output_text.get("1.0", "end-1c"))


def last_character() -> str:
    text = config.output_text.get("1.0", "end-1c")
    return text[-1] if text else None


def submit() -> None:
    from model import model
    text = config.input_text.get()

    if text:
        clear_input()
        model.stream(text)


def clear_output() -> None:
    config.output_text.config(state="normal")
    config.output_text.delete(1.0, "end")
    config.output_text.config(state="disabled")


def clear_input():
    config.input_text.delete(0, "end")


def prompt(num: int) -> None:
    name = getattr(config, f"name_{num}")
    prompt = f"{name}: "
    output(prompt, False)


def show_output_menu(event) -> None:
    config.output_menu.post(event.x_root, event.y_root)


def hide_output_menu() -> None:
    config.output_menu.unpost()


def select_all() -> None:
    config.output_text.tag_add("sel", "1.0", "end")


def copy_all() -> None:
    text = config.output_text.get("1.0", "end-1c").strip()
    pyperclip.copy(text)


def show_model_menu(event) -> None:
    if not config.models:
        return

    config.model_menu.delete(0, tk.END)

    for model in config.models:
        config.model_menu.add_command(label=model, command=lambda m=model: set_model(m))

    if event:
        config.model_menu.post(event.x_root, event.y_root)
    else:
        show_menu_at_center(config.model_menu)


def hide_model_menu() -> None:
    config.model_menu.unpost()


def hide_menus() -> None:
    hide_output_menu()
    hide_model_menu()


def set_model(model: str) -> None:
    widgets.set_text(config.model_text, model)
    config.update_model()


def show_menu_at_center(menu: tk.Menu) -> None:
    config.app.update_idletasks()
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
    widgets.set_text(config.model_text, file)
    config.update_model()
