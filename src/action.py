# Modules
from config import config
import widgets

# Libraries
import pyperclip


def output(text: str, linebreak=True) -> None:
    if linebreak:
        text = text + "\n"

    widgets.insert_text(config.output_text, text, True)


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
