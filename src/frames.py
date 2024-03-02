# Modules
from config import config
import widgets
from framedata import FrameData
import action


def get_d() -> FrameData:
    return FrameData(widgets.make_frame(), 0)


def frame_model() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    widgets.make_label(d, "Model")
    config.model_text = widgets.make_input(d, sticky="ew", placeholder="Enter path to a model")
    widgets.make_button(d, "Load", lambda: action.load_model())
    widgets.make_button(d, "Clear", lambda: action.clear_output())


def frame_settings() -> None:
    d = get_d()
    width = 10
    widgets.make_label(d, "Name 1")
    config.name_1_text = widgets.make_input(d, placeholder="Name 1", width=width)
    widgets.make_label(d, "Name 2")
    config.name_2_text = widgets.make_input(d, placeholder="Name 2", width=width)
    widgets.make_label(d, "Tokens")
    config.max_tokens_text = widgets.make_input(d, placeholder="Tokens", width=width)
    widgets.make_label(d, "Temp")
    config.temperature_text = widgets.make_input(d, placeholder="Temperature", width=width)
    config.name_1_text.bind("<FocusOut>", lambda e: action.update_name_1())
    config.name_2_text.bind("<FocusOut>", lambda e: action.update_name_2())
    config.max_tokens_text.bind("<FocusOut>", lambda e: action.update_max_tokens())
    config.temperature_text.bind("<FocusOut>", lambda e: action.update_temperature())


def frame_system() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    widgets.make_label(d, "Instuctions")
    config.system_text = widgets.make_input(d, sticky="ew",
                                            placeholder="Add instructions to tell the bot how to act")


def frame_output() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(0, weight=1)
    d.frame.grid_rowconfigure(0, weight=0)
    config.output_text = widgets.make_text(d, state="disabled", sticky="nsew")
    config.output_text.config(bg="grey", fg="white", highlightthickness=0, bd=0)


def frame_input() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(0, weight=1)
    config.input_text = widgets.make_input(d, sticky="ew", placeholder="Ask something to x")
    widgets.make_button(d, "Submit", lambda: action.submit())
    config.input_text.bind("<Return>", lambda e: action.submit())


def fill() -> None:
    widgets.insert_text(config.model_text, config.model)
    widgets.insert_text(config.name_1_text, config.name_1)
    widgets.insert_text(config.name_2_text, config.name_2)
    widgets.insert_text(config.max_tokens_text, config.max_tokens)
    widgets.insert_text(config.temperature_text, config.temperature)
    widgets.insert_text(config.system_text, config.system)


def setup() -> None:
    fill()
    config.input_text.focus_set()
