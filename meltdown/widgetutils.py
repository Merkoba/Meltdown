# Modules
from .config import config
from .app import app
from .framedata import FrameData

# Libraries
import pyperclip  # type: ignore

# Standard
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Any, Union, Callable, Literal, Optional, List


def do_grid(d: FrameData, widget: tk.Widget, sticky: str) -> None:
    widget.grid(row=0, column=d.col, padx=config.padx, pady=config.pady, sticky=sticky)
    d.col += 1


def make_frame() -> tk.Frame:
    frame = tk.Frame(app.root)
    frame.grid(row=config.frame_number, column=0, padx=config.frame_padx,
               pady=config.frame_pady, sticky="nsew")
    frame.configure(background=config.background_color)
    config.frame_number += 1
    return frame


def make_text(d: FrameData, sticky: str = "w", state: Literal["normal", "disabled"] = "normal") -> tk.Text:
    widget = tk.Text(d.frame, font=config.font, wrap="word", state=state)
    widget.configure(background=config.text_background, foreground=config.text_foreground)
    widget.configure(bd=0, highlightthickness=0)
    do_grid(d, widget, sticky)
    return widget


def make_input(d: FrameData, value: str = "", width: Optional[int] = None, sticky: str = "w") -> tk.Entry:
    w = width if width else config.input_width
    widget = tk.Entry(d.frame, font=config.font, width=w)
    widget.configure(background=config.input_background, foreground=config.input_foreground)
    widget.configure(bd=0, highlightthickness=0, insertbackground="white")
    do_grid(d, widget, sticky)

    if value:
        widget.insert(0, value)

    return widget


def make_button(d: FrameData, text: str, command: Optional[Callable[..., Any]] = None, sticky: str = "w") -> tk.Button:
    widget = tk.Button(d.frame, text=text, font=config.font_button)
    widget.configure(background=config.button_background, foreground=config.button_foreground)
    widget.configure(bd=0, highlightthickness=0, disabledforeground="white")

    if command:
        widget.configure(command=command)

    do_grid(d, widget, sticky)
    return widget


def make_label(d: FrameData, text: str, sticky: str = "w") -> tk.Label:
    widget = tk.Label(d.frame, text=f"{text}:", font=config.font)
    widget.configure(background=config.background_color, foreground=config.foreground_color)
    do_grid(d, widget, sticky)
    return widget


def make_select(d: FrameData, values: Optional[List[Any]] = None, sticky: str = "w") -> ttk.Combobox:
    v = values if values else ["empty"]
    widget = ttk.Combobox(d.frame, values=v, state="readonly",
                          font=config.font, style="TCombobox", width=config.select_width)
    do_grid(d, widget, sticky)
    return widget


def make_menu() -> tk.Menu:
    widget = tk.Menu(app.root, tearoff=0, font=config.font,
                     bg="#3D4555", fg="white", activebackground="#33393B", activeforeground="white")
    return widget


def insert_text(widget: Union[tk.Text, tk.Entry], text: Union[str, int, float], disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.insert(tk.END, str(text))

    if disable:
        widget.configure(state="disabled")


def set_text(widget: Union[tk.Text, tk.Entry], text: Union[str, int, float], disable: bool = False) -> None:
    widget.configure(state="normal")

    if isinstance(widget, tk.Entry):
        widget.delete(0, tk.END)
        widget.insert(0, str(text))
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


def get_text(widget: tk.Text) -> str:
    return widget.get("1.0", "end-1c").strip()


def copy_all(widget: tk.Text) -> None:
    text = widget.get("1.0", "end-1c").strip()
    pyperclip.copy(text)


def clear_text(widget: Union[tk.Text, tk.Entry], disable: bool = False) -> None:
    set_text(widget, "", disable)


def to_bottom(widget: tk.Text) -> None:
    widget.yview_moveto(1.0)


def show_confirm(text: str, cmd_ok: Callable[..., Any], cmd_cancel: Optional[Callable[..., Any]]) -> None:
    text = clean_string(text)
    result = messagebox.askquestion("Confirmation", text)

    if result == "yes":
        cmd_ok()
    elif cmd_cancel:
        cmd_cancel()


def show_message(text: str) -> None:
    text = clean_string(text)
    messagebox.showinfo("Information", text)


def clean_string(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
