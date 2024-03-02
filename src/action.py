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


def load_model():
    from model import model
    config.model = config.model_text.get()
    model.load()


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


def update_name_1() -> None:
    name_1 = config.name_1_text.get()

    if name_1:
        config.name_1 = config.name_1_text.get()


def update_name_2() -> None:
    name_2 = config.name_2_text.get()

    if name_2:
        config.name_2 = config.name_2_text.get()


def update_max_tokens() -> None:
    max_tokens = config.max_tokens_text.get()

    try:
        max_tokens = int(max_tokens)
    except BaseException:
        return

    if max_tokens:
        config.max_tokens = config.max_tokens_text.get()


def update_temperature() -> None:
    temperature = config.temperature_text.get()

    try:
        temperature = float(temperature)
    except BaseException:
        return

    if temperature:
        config.temperature = config.temperature_text.get()


def show_output_menu(event) -> None:
    config.output_menu.post(event.x_root, event.y_root)


def hide_output_menu() -> None:
    config.output_menu.unpost()


def select_all() -> None:
    config.output_text.tag_add("sel", "1.0", "end")


def copy_all() -> None:
    text = config.output_text.get("1.0", "end-1c").strip()
    pyperclip.copy(text)