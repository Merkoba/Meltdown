# Modules
from config import config
from framedata import FrameData

# Standard
import tkinter as tk
from typing import Any, Union, Tuple, Callable


class Widgets:
    def __init__(self, **kwargs) -> None:
        self.name_1: tk.Entry = kwargs.get("name_1")
        self.name_2: tk.Entry = kwargs.get("name_2")
        self.max_tokens: tk.Entry = kwargs.get("max_tokens")
        self.temperature: tk.Entry = kwargs.get("temperature")
        self.system: tk.Entry = kwargs.get("system")
        self.model: tk.Entry = kwargs.get("model")
        self.top_k: tk.Entry = kwargs.get("top_k")
        self.top_p: tk.Entry = kwargs.get("top_p")
        self.output: tk.Text = kwargs.get("output")
        self.input: tk.Entry = kwargs.get("input")
        self.output_menu: tk.Menu = kwargs.get("output_menu")
        self.model_menu: tk.Menu = kwargs.get("model_menu")


widgets = Widgets()


def do_grid(d: FrameData, widget: tk.Widget, sticky) -> None:
    widget.grid(row=0, column=d.col, padx=config.padx, pady=config.pady, sticky=sticky)


def make_frame() -> tk.Frame:
    frame = tk.Frame(config.app)
    frame.grid(row=config.frame_number, column=0, padx=config.frame_padx,
               pady=config.frame_pady, sticky="nsew")
    frame.configure(background=config.background_color)
    config.frame_number += 1
    return frame


def make_text(d: FrameData, sticky: str = "w", state="normal") -> tk.Text:
    widget = tk.Text(d.frame, font=config.font, wrap="word", state=state)
    widget.configure(background=config.text_background, foreground=config.text_foreground)
    widget.configure(bd=0, highlightthickness=0)
    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def make_input(d: FrameData, value: str = "", width: Union[int, None] = None, sticky: str = "w") -> tk.Entry:
    w = width if width else config.input_width
    widget = tk.Entry(d.frame, font=config.font, width=w)
    widget.configure(background=config.input_background, foreground=config.input_foreground)
    widget.configure(bd=0, highlightthickness=0, insertbackground="white")
    do_grid(d, widget, sticky)

    if value:
        widget.insert(0, value)

    d.col += 1
    return widget


def make_button(d: FrameData, text: str, command: Union[Callable[..., Any], None] = None, sticky: str = "w") -> tk.Button:
    cmd = command if command else None
    widget = tk.Button(d.frame, text=text, command=cmd, font=config.font_button)
    widget.configure(background=config.button_background, foreground=config.button_foreground)
    widget.configure(bd=0, highlightthickness=0)
    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def make_label(d: FrameData, text: str, sticky: str = "w") -> tk.Label:
    widget = tk.Label(d.frame, text=f"{text}:", font=config.font)
    widget.configure(background=config.background_color, foreground=config.foreground_color)
    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def insert_text(widget: tk.Text, text: str, disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.insert(tk.END, text)

    if disable:
        widget.configure(state="disabled")


def set_text(widget: tk.Text, text: str, disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.delete(0, tk.END)
    widget.insert(0, text)

    if disable:
        widget.configure(state="disabled")
