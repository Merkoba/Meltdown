# Modules
from .config import config
from .app import app
from .enums import Fill, FillLiteral
from .entrybox import EntryBox
from .buttonbox import ButtonBox

# Libraries
import pyperclip  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, Union, Callable, Optional, List, Tuple


frame_number = 0


def do_pack(widget: tk.Widget,
            fill: Optional[Fill] = None, right_padding: Optional[int] = None,
            bottom_padding: Optional[int] = None,
            padx: Optional[int] = None,
            pady: Optional[int] = None) -> None:
    if padx is not None:
        px = (padx, padx)
    else:
        padx_right = right_padding if right_padding else 0
        px = (config.padx, padx_right)

    if pady is not None:
        py = (pady, pady)
    else:
        pady_bottom = bottom_padding if bottom_padding else 0
        py = (config.pady, pady_bottom)

    expand = True if fill else False
    fillmode: FillLiteral = fill if fill else Fill.NONE
    widget.pack(side="left", padx=px, pady=py, fill=fillmode.value, expand=expand)


def make_frame(parent: Union[ttk.Notebook, tk.Frame, None] = None,
               bottom_padding: Optional[int] = None) -> tk.Frame:
    global frame_number

    p = app.root if not parent else parent
    frame = tk.Frame(p)

    padx = (config.frame_padx, config.frame_padx)

    if bottom_padding is not None:
        pady = (config.frame_pady, bottom_padding)
    else:
        pady = (config.frame_pady, 0)

    frame.grid(row=frame_number, column=0, padx=padx,
               pady=pady, sticky="nsew")

    frame.configure(background=config.background_color)
    frame_number += 1
    return frame


def make_inner_frame(parent: tk.Frame, col: int) -> tk.Frame:
    frame = tk.Frame(parent, background=config.background_color)
    frame.grid(sticky="ew", column=col, row=0)
    return frame


def make_scrollable_frame(parent: tk.Frame, col: int) -> Tuple[tk.Frame, tk.Canvas]:
    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
    frame = tk.Frame(canvas, background=config.background_color)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.configure(borderwidth=0, highlightthickness=0, background=config.background_color)
    canvas.grid(column=col, row=0, sticky="ew", padx=10)
    return frame, canvas


def make_notebook(parent: tk.Frame, fill: Optional[Fill] = None,
                  right_padding: Optional[int] = None) -> ttk.Notebook:
    widget = ttk.Notebook(parent, style="Normal.TNotebook")
    do_pack(widget, fill=fill, right_padding=right_padding)
    return widget


def make_entry(parent: tk.Frame, value: str = "",
               width: Optional[int] = None, fill: Optional[Fill] = None,
               right_padding: Optional[int] = None) -> EntryBox:
    w = width if width else config.entry_width
    widget = EntryBox(parent, font=config.font, width=w, style="Normal.TEntry")
    do_pack(widget, fill=fill, right_padding=right_padding)

    if value:
        widget.set_text(value)

    return widget


def get_button(parent: tk.Frame, text: str,
               command: Optional[Callable[..., Any]] = None,
               style: Optional[str] = None, width: Optional[int] = None, bigger: bool = False) -> ButtonBox:
    return ButtonBox(parent, text, command, style=style, width=width, bigger=bigger)


def make_button(parent: tk.Frame, text: str,
                command: Optional[Callable[..., Any]] = None, fill: Optional[Fill] = None,
                right_padding: Optional[int] = None, bottom_padding: Optional[int] = None, bigger: bool = False,
                pady: Optional[int] = None, style: Optional[str] = None, width: Optional[int] = None) -> ButtonBox:
    widget = get_button(parent, text, command, style=style, width=width, bigger=bigger)
    do_pack(widget, fill=fill, right_padding=right_padding, bottom_padding=bottom_padding, pady=pady)
    return widget


def make_label(parent: tk.Frame, text: str, fill: Optional[Fill] = None,
               right_padding: Optional[int] = None) -> tk.Label:
    widget = tk.Label(parent, text=f"{text}:", font=config.font)
    widget.configure(background=config.background_color, foreground=config.foreground_color)
    do_pack(widget, fill=fill, right_padding=right_padding)
    return widget


def make_combobox(parent: tk.Frame, values: Optional[List[Any]] = None,
                  fill: Optional[Fill] = None, width: Optional[int] = None,
                  right_padding: Optional[int] = None) -> ttk.Combobox:
    v = values if values else ["empty"]
    w = width if width else config.combobox_width
    widget = ttk.Combobox(parent, values=v, state="readonly",
                          font=config.font_combobox, style="Normal.TCombobox", width=w)

    # Remove mousewheel events
    widget.bind_class("TCombobox", "<MouseWheel>", lambda e: "break")
    widget.bind_class("TCombobox", "<Button-4>", lambda e: "break")
    widget.bind_class("TCombobox", "<Button-5>", lambda e: "break")

    do_pack(widget, fill=fill, right_padding=right_padding)
    return widget


def set_select(widget: ttk.Combobox, value: Union[str, int, float]) -> None:
    widget.set(str(value))


def copy(text: str) -> None:
    pyperclip.copy(text)


def paste(widget: EntryBox) -> None:
    text = pyperclip.paste()
    widget.set_text(text)
