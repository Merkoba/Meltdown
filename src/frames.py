# Modules
from config import config
import widgets
from framedata import FrameData
import action

# Standard
import tkinter as tk


def get_d() -> FrameData:
    return FrameData(widgets.make_frame(), 0)


def frame_model() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    widgets.make_label(d, "Model")
    config.model_text = widgets.make_input(d, sticky="ew")
    widgets.make_button(d, "Load", lambda: action.load_model())


def frame_settings() -> None:
    d = get_d()
    width = 11
    widgets.make_label(d, "Name 1")
    config.name_1_text = widgets.make_input(d, width=width)
    widgets.make_label(d, "Name 2")
    config.name_2_text = widgets.make_input(d, width=width)
    widgets.make_label(d, "Tokens")
    config.max_tokens_text = widgets.make_input(d, width=width)
    widgets.make_label(d, "Temp")
    config.temperature_text = widgets.make_input(d, width=width)


def frame_system() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    widgets.make_label(d, "Instuctions")
    config.system_text = widgets.make_input(d, sticky="ew")


def frame_output() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(0, weight=1)
    d.frame.grid_rowconfigure(0, weight=0)
    config.output_text = widgets.make_text(d, state="disabled", sticky="nsew")


def frame_input() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(0, weight=1)
    config.input_text = widgets.make_input(d, sticky="ew")
    widgets.make_button(d, "Submit", lambda: action.submit())


def fill() -> None:
    widgets.insert_text(config.model_text, config.model)
    widgets.insert_text(config.name_1_text, config.name_1)
    widgets.insert_text(config.name_2_text, config.name_2)
    widgets.insert_text(config.max_tokens_text, config.max_tokens)
    widgets.insert_text(config.temperature_text, config.temperature)
    widgets.insert_text(config.system_text, config.system)


def setup() -> None:
    fill()
    config.output_menu = tk.Menu(config.app, tearoff=0, font=config.font)
    config.output_menu.add_command(label="Clear", command=lambda: action.clear_output())
    config.output_menu.add_command(label="Select All", command=lambda: action.select_all())
    config.output_menu.add_command(label="Copy All", command=lambda: action.copy_all())
    config.output_text.bind("<Button-3>", lambda e: action.show_output_menu(e))
    config.output_text.bind("<Button-1>", lambda e: action.hide_output_menu())
    config.name_1_text.bind("<FocusOut>", lambda e: config.update_name_1())
    config.name_2_text.bind("<FocusOut>", lambda e: config.update_name_2())
    config.max_tokens_text.bind("<FocusOut>", lambda e: config.update_max_tokens())
    config.temperature_text.bind("<FocusOut>", lambda e: config.update_temperature())
    config.system_text.bind("<FocusOut>", lambda e: config.update_system())
    config.input_text.bind("<Return>", lambda e: action.submit())
    config.input_text.focus_set()
