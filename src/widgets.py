# Modules
from config import config
from framedata import FrameData

# Libraries
import tkinter as tk

# Standard
from typing import Any, Union, Tuple, Callable


def do_grid(d: FrameData, widget: tk.Widget, sticky) -> None:
    widget.grid(row=0, column=d.col, padx=config.padx, pady=config.pady, sticky=sticky)


def make_frame() -> tk.Frame:
    frame = tk.Frame(config.app)
    frame.grid(row=config.frame_number, column=0, padx=config.frame_padx,
               pady=config.frame_pady, sticky="nsew")
    config.frame_number += 1
    return frame


def make_text(d: FrameData, sticky: str = "w", state="normal") -> tk.Text:
    widget = tk.Text(d.frame, font=config.font, wrap="word", state=state)
    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def make_input(d: FrameData, value: str = "", width: Union[int, None] = None, sticky: str = "w",
               placeholder: str = "") -> tk.Entry:
    w = width if width else config.text_width
    widget = tk.Entry(d.frame, font=config.font, width=w)
    do_grid(d, widget, sticky)

    if value:
        widget.insert(0, value)

    d.col += 1
    return widget


def make_button(d: FrameData, text: str, command: Callable[..., Any], color: str = "grey",
                text_color: Union[str, None] = None, hover_color: Union[Tuple[str, str], None] = None,
                sticky: str = "w") -> tk.Button:
    widget = tk.Button(d.frame, text=text, command=command, font=config.font,
                       fg=color, text_color=text_color, hover_color=hover_color, )

    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def make_label(d: FrameData, text: str, sticky: str = "w") -> tk.Label:
    widget = tk.Label(d.frame, text=f"{text}:", font=config.font)
    do_grid(d, widget, sticky)
    d.col += 1
    return widget


def insert_text(widget: tk.Text, text: str, disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.insert(tk.END, text)

    if disable:
        widget.configure(state="disabled")
