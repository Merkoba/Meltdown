# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, Union, Callable, Optional, List, Tuple

# Modules
from .app import app
from .utils import utils
from .args import args
from .entrybox import EntryBox
from .buttonbox import ButtonBox
from .framedata import FrameData


def do_grid(
    widget: tk.Widget,
    col: int,
    padx: Optional[int] = None,
    pady: Optional[int] = None,
) -> None:
    if padx is not None:
        px = (padx, padx)
    else:
        px = (app.theme.padx, 0)

    if pady is not None:
        py = (pady, pady)
    else:
        py = (app.theme.pady, 0)

    widget.grid(row=0, column=col, padx=px, pady=py, sticky="ew")


def make_frame(
    parent: Optional[tk.Frame] = None,
    col: int = 0,
    row: Optional[int] = None,
) -> FrameData:
    p = app.main_frame if not parent else parent
    frame = tk.Frame(p)
    padx = (app.theme.frame_padx, 0)
    pady = (app.theme.frame_pady, 0)
    row = row if (row is not None) else FrameData.frame_number
    frame.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")
    frame.bind("<Button-1>", lambda e: app.on_frame_click())
    frame.configure(background=app.theme.background_color)
    return FrameData(frame)


def make_scrollable_frame(parent: tk.Frame, col: int) -> Tuple[tk.Frame, tk.Canvas]:
    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
    frame = tk.Frame(canvas, background=app.theme.background_color)

    frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.configure(
        borderwidth=0, highlightthickness=0, background=app.theme.background_color
    )

    canvas.grid(column=col, row=0, sticky="ew", padx=10)
    return frame, canvas


def make_entry(
    frame_data: FrameData,
    value: str = "",
    width: Optional[int] = None,
) -> EntryBox:
    w = width if width else app.theme.entry_width

    widget = EntryBox(frame_data.frame, width=w, style="Normal.TEntry")

    do_grid(widget, col=frame_data.col)
    frame_data.col += 1

    if value:
        widget.set_text(value)

    return widget


def get_button(
    parent: tk.Frame,
    text: str,
    command: Optional[Callable[..., Any]] = None,
    style: Optional[str] = None,
    width: Optional[int] = None,
    bigger: bool = False,
) -> ButtonBox:
    return ButtonBox(parent, text, command, style=style, width=width, bigger=bigger)


def make_button(
    frame_data: FrameData,
    text: str,
    command: Optional[Callable[..., Any]] = None,
    bigger: bool = False,
    pady: Optional[int] = None,
    style: Optional[str] = None,
    width: Optional[int] = None,
) -> ButtonBox:
    if args.short_buttons:
        text = utils.shorten(text)

    widget = get_button(
        frame_data.frame, text, command, style=style, width=width, bigger=bigger
    )

    do_grid(
        widget,
        col=frame_data.col,
        pady=pady,
    )

    frame_data.col += 1
    return widget


def make_label(
    frame_data: FrameData,
    text: str,
    padx: Optional[int] = None,
    pady: Optional[int] = None,
    ignore_short: bool = False,
    colons: bool = True,
) -> tk.Label:
    text = f"{text}:" if colons else text

    if args.short_labels and (not ignore_short):
        text = utils.shorten(text)

    widget = tk.Label(frame_data.frame, text=text, font=app.theme.font())

    widget.configure(
        background=app.theme.background_color, foreground=app.theme.foreground_color
    )

    if args.show_labels:
        do_grid(widget, col=frame_data.col, padx=padx, pady=pady)

    frame_data.col += 1
    return widget


def make_combobox(
    frame_data: FrameData,
    values: Optional[List[Any]] = None,
    width: Optional[int] = None,
) -> ttk.Combobox:
    v = values if values else ["empty"]
    w = width if width else app.theme.combobox_width

    widget = ttk.Combobox(
        frame_data.frame,
        values=v,
        state="readonly",
        font=app.theme.font("combobox"),
        style="Normal.TCombobox",
        width=w,
    )

    # Remove mousewheel events
    widget.bind_class("TCombobox", "<MouseWheel>", lambda e: "break")
    widget.bind_class("TCombobox", "<Button-4>", lambda e: "break")
    widget.bind_class("TCombobox", "<Button-5>", lambda e: "break")

    do_grid(widget, col=frame_data.col)
    frame_data.col += 1
    return widget


def set_select(widget: ttk.Combobox, value: Union[str, int, float]) -> None:
    widget.set(str(value))
