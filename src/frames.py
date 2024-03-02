# Modules
from config import config
import widgets as w
from widgets import widgets
from framedata import FrameData
import actions
import state

# Standard
import tkinter as tk


def get_d() -> FrameData:
    return FrameData(w.make_frame(), 0)


def frame_model() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    w.make_label(d, "Model")
    widgets.model = w.make_input(d, sticky="ew")
    w.make_button(d, "Browse", lambda: actions.browse_model())
    w.make_button(d, "Recent", lambda: actions.show_model_menu(None))


def frame_settings() -> None:
    d = get_d()
    w.make_label(d, "Name 1")
    widgets.name_1 = w.make_input(d)
    w.make_label(d, "Name 2")
    widgets.name_2 = w.make_input(d)
    w.make_label(d, "Tokens")
    widgets.max_tokens = w.make_input(d)
    w.make_label(d, "Temp")
    widgets.temperature = w.make_input(d)


def frame_system() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    w.make_label(d, "System")
    widgets.system = w.make_input(d, sticky="ew")
    w.make_label(d, "Top K")
    widgets.top_k = w.make_input(d)
    w.make_label(d, "Top P")
    widgets.top_p = w.make_input(d)


def frame_output() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(0, weight=1)
    d.frame.grid_rowconfigure(0, weight=1)
    widgets.output = w.make_text(d, state="disabled", sticky="nsew")


def frame_input() -> None:
    d = get_d()
    d.frame.grid_columnconfigure(1, weight=1)
    w.make_label(d, "Prompt")
    widgets.input = w.make_input(d, sticky="ew")
    w.make_button(d, "Submit", lambda: actions.submit())


def fill() -> None:
    w.insert_text(widgets.model, config.model)
    w.insert_text(widgets.name_1, config.name_1)
    w.insert_text(widgets.name_2, config.name_2)
    w.insert_text(widgets.max_tokens, config.max_tokens)
    w.insert_text(widgets.temperature, config.temperature)
    w.insert_text(widgets.system, config.system)
    w.insert_text(widgets.top_k, config.top_k)
    w.insert_text(widgets.top_p, config.top_p)


def setup() -> None:
    fill()

    widgets.model_menu = tk.Menu(config.app, tearoff=0, font=config.font)
    widgets.model.bind("<Button-3>", lambda e: actions.show_model_menu(e))
    widgets.model.bind("<Button-1>", lambda e: actions.hide_menus())
    widgets.model.bind("<Button-1>", lambda e: actions.hide_menus())

    widgets.output_menu = tk.Menu(config.app, tearoff=0, font=config.font)
    widgets.output_menu.add_command(label="Clear", command=lambda: actions.clear_output())
    widgets.output_menu.add_command(label="Select All", command=lambda: actions.select_all())
    widgets.output_menu.add_command(label="Copy All", command=lambda: actions.copy_all())
    widgets.output.bind("<Button-3>", lambda e: actions.show_output_menu(e))
    widgets.output.bind("<Button-1>", lambda e: actions.hide_menus())
    widgets.output.bind("<Button-1>", lambda e: actions.hide_menus())

    widgets.input.bind("<Return>", lambda e: actions.submit())

    widgets.name_1.bind("<FocusOut>", lambda e: state.update_name_1())
    widgets.name_2.bind("<FocusOut>", lambda e: state.update_name_2())
    widgets.max_tokens.bind("<FocusOut>", lambda e: state.update_max_tokens())
    widgets.temperature.bind("<FocusOut>", lambda e: state.update_temperature())
    widgets.system.bind("<FocusOut>", lambda e: state.update_system())
    widgets.model.bind("<FocusOut>", lambda e: state.update_model())
    widgets.top_k.bind("<FocusOut>", lambda e: state.update_top_k())
    widgets.top_p.bind("<FocusOut>", lambda e: state.update_top_p())

    widgets.input.focus_set()
