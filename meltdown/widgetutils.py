# Modules
from .config import config
from .app import app
from .enums import Fill, FillLiteral
from .entrybox import EntryBox

# Libraries
import pyperclip  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any, Union, Callable, Literal, Optional, List


frame_number = 0


def do_pack(widget: tk.Widget,
            fill: Optional[Fill] = None, right_padding: Optional[int] = None,
            bottom_padding: Optional[int] = None,
            padx: Optional[int] = None, pady: Optional[int] = None) -> None:
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


def make_frame(parent: Optional[ttk.Notebook] = None,
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


def make_text(parent: tk.Frame, fill: Optional[Fill] = None,
              state: Literal["normal", "disabled"] = "normal",
              right_padding: Optional[int] = None) -> tk.Text:
    scrollbar = ttk.Scrollbar(parent, style="Normal.Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    widget = tk.Text(parent, font=config.font, wrap="word", state=state, yscrollcommand=scrollbar.set)
    widget.configure(background=config.text_background, foreground=config.text_foreground)
    widget.configure(bd=4, highlightthickness=0, relief="flat")
    do_pack(widget, fill=fill, right_padding=right_padding, padx=0, pady=1)
    scrollbar.configure(command=widget.yview)
    return widget


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


def get_button(parent: tk.Frame, text: str) -> ttk.Button:
    return ttk.Button(parent, text=text, style="Normal.TButton")


def make_button(parent: tk.Frame, text: str,
                command: Optional[Callable[..., Any]] = None, fill: Optional[Fill] = None,
                right_padding: Optional[int] = None, bottom_padding: Optional[int] = None,
                pady: Optional[int] = None) -> ttk.Button:
    widget = get_button(parent, text)

    if command:
        widget.configure(command=lambda: command())

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
    do_pack(widget, fill=fill, right_padding=right_padding)
    return widget


def insert_text(widget: Union[tk.Text], text: Union[str, int, float], disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.insert(tk.END, str(text))

    if disable:
        widget.configure(state="disabled")


def set_text(widget: Union[tk.Text, EntryBox], text: Union[str, int, float],
             disable: bool = False, move: bool = False) -> None:
    widget.configure(state="normal")

    if isinstance(widget, EntryBox):
        widget.set_text(str(text))

        if move:
            widget.xview_moveto(1.0)
    elif isinstance(widget, tk.Text):
        widget.delete("1.0", tk.END)
        widget.insert("1.0", str(text))

    if disable:
        widget.configure(state="disabled")


def set_select(widget: ttk.Combobox, value: Union[str, int, float]) -> None:
    widget.set(str(value))


def show_menu_at_center(menu: tk.Menu) -> None:
    app.root.update_idletasks()
    menu.update_idletasks()
    window_width = app.root.winfo_width()
    window_height = app.root.winfo_height()
    window_x = app.root.winfo_rootx()
    window_y = app.root.winfo_rooty()

    menu_width = menu.winfo_reqwidth()
    menu_height = menu.winfo_reqheight()

    x = window_x + (window_width - menu_width) // 2
    y = window_y + (window_height - menu_height) // 2

    menu.post(x, y)


def last_character(widget: Union[tk.Text]) -> str:
    text = widget.get("1.0", "end-1c")
    return text[-1] if text else ""


def text_length(widget: Union[tk.Text]) -> int:
    return len(widget.get("1.0", "end-1c"))


def select_all(widget: tk.Text) -> None:
    widget.tag_add("sel", "1.0", "end")


def deselect_all(widget: tk.Text) -> None:
    widget.tag_remove("sel", "1.0", "end")


def get_text(widget: tk.Text) -> str:
    return widget.get("1.0", "end-1c").strip()


def copy(text: str) -> None:
    pyperclip.copy(text)


def paste(widget: EntryBox) -> None:
    text = pyperclip.paste()
    set_text(widget, text)


def clear_text(widget: Union[tk.Text, EntryBox], disable: bool = False) -> None:
    set_text(widget, "", disable)


def to_top(widget: tk.Text) -> None:
    widget.yview_moveto(0.0)


def to_bottom(widget: tk.Text) -> None:
    widget.yview_moveto(1.0)
