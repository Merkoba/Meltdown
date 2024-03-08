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
from typing import Any, Union, Callable, Literal, Optional, List, Tuple


def do_grid(d: FrameData, widget: tk.Widget, sticky: str, right_padding: Optional[int] = None) -> None:
    padx = (config.padx, right_padding if right_padding else config.padx)
    widget.grid(row=0, column=d.col, padx=padx, pady=config.pady, sticky=sticky)
    d.col += 1


def make_frame() -> tk.Frame:
    frame = tk.Frame(app.root)
    frame.grid(row=config.frame_number, column=0, padx=config.frame_padx,
               pady=config.frame_pady, sticky="nsew")
    frame.configure(background=config.background_color)
    config.frame_number += 1
    return frame


def make_text(d: FrameData, sticky: str = "w",
              state: Literal["normal", "disabled"] = "normal",
              right_padding: Optional[int] = None) -> tk.Text:
    widget = tk.Text(d.frame, font=config.font, wrap="word", state=state)
    widget.configure(background=config.text_background, foreground=config.text_foreground)
    widget.configure(bd=0, highlightthickness=0)
    do_grid(d, widget, sticky, right_padding=right_padding)
    return widget


def make_entry(d: FrameData, value: str = "",
               width: Optional[int] = None, sticky: str = "w",
               right_padding: Optional[int] = None) -> ttk.Entry:
    w = width if width else config.input_width
    widget = ttk.Entry(d.frame, font=config.font, width=w, style="Normal.TEntry")
    do_grid(d, widget, sticky, right_padding=right_padding)

    if value:
        widget.insert(0, value)

    return widget


def get_button(parent: tk.Frame, text: str) -> ttk.Button:
    return ttk.Button(parent, text=text, style="Normal.TButton", takefocus=False)


def make_button(d: FrameData, text: str,
                command: Optional[Callable[..., Any]] = None,
                sticky: str = "w", right_padding: Optional[int] = None) -> ttk.Button:
    widget = get_button(d.frame, text)

    if command:
        widget.configure(command=command)

    do_grid(d, widget, sticky, right_padding=right_padding)
    return widget


def make_label(d: FrameData, text: str, sticky: str = "w",
               right_padding: Optional[int] = None) -> tk.Label:
    widget = tk.Label(d.frame, text=f"{text}:", font=config.font)
    widget.configure(background=config.background_color, foreground=config.foreground_color)
    do_grid(d, widget, sticky, right_padding=right_padding)
    return widget


def make_combobox(d: FrameData, values: Optional[List[Any]] = None,
                  sticky: str = "w", right_padding: Optional[int] = None) -> ttk.Combobox:
    v = values if values else ["empty"]
    widget = ttk.Combobox(d.frame, values=v, state="readonly",
                          font=config.font_select, style="Normal.TCombobox", width=config.select_width)
    do_grid(d, widget, sticky, right_padding=right_padding)
    return widget


def make_menu() -> tk.Menu:
    widget = tk.Menu(app.root, tearoff=0, font=config.font,
                     bg="#3D4555", fg="white", activebackground="#33393B", activeforeground="white")
    return widget


def insert_text(widget: Union[tk.Text, ttk.Entry], text: Union[str, int, float], disable: bool = False) -> None:
    widget.configure(state="normal")
    widget.insert(tk.END, str(text))

    if disable:
        widget.configure(state="disabled")


def set_text(widget: Union[tk.Text, ttk.Entry], text: Union[str, int, float],
             disable: bool = False, move: bool = False) -> None:
    widget.configure(state="normal")

    if isinstance(widget, ttk.Entry):
        widget.delete(0, tk.END)
        widget.insert(0, str(text))

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


def get_text(widget: tk.Text) -> str:
    return widget.get("1.0", "end-1c").strip()


def copy(text: str) -> None:
    pyperclip.copy(text)


def paste(widget: ttk.Entry) -> None:
    text = pyperclip.paste()
    set_text(widget, text)


def clear_text(widget: Union[tk.Text, ttk.Entry], disable: bool = False) -> None:
    set_text(widget, "", disable)


def make_dialog(title: str, text: str) -> Tuple[tk.Toplevel, tk.Frame]:
    dialog = tk.Toplevel(app.root)
    dialog.title(title)
    tk.Label(dialog, text=text, font=config.font, wraplength=500).pack(padx=6)
    button_frame = tk.Frame(dialog)
    button_frame.pack()
    return dialog, button_frame


def show_dialog(dialog: tk.Toplevel) -> None:
    dialog.transient(app.root)
    dialog.grab_set()
    dialog.update()
    x = app.root.winfo_rootx() + (app.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
    y = app.root.winfo_rooty() + (app.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry("+%d+%d" % (x, y))
    dialog.wait_window()


def make_dialog_button(parent: tk.Frame, text: str, command: Callable[..., Any], side: Literal["left", "right"]) -> None:
    button = get_button(parent, text)
    button.configure(command=command)
    button.pack(side=side, padx=6, pady=8)


def show_confirm(text: str, cmd_ok: Callable[..., Any], cmd_cancel: Optional[Callable[..., Any]]) -> None:
    def ok() -> None:
        dialog.destroy()
        cmd_ok()

    def cancel() -> None:
        dialog.destroy()

        if cmd_cancel:
            cmd_cancel()

    dialog, button_frame = make_dialog("Confirm", text)
    make_dialog_button(button_frame, "Ok", ok, "left")
    make_dialog_button(button_frame, "Cancel", cancel, "right")
    show_dialog(dialog)


def show_message(text: str) -> None:
    def ok() -> None:
        dialog.destroy()

    dialog, button_frame = make_dialog("Information", text)
    make_dialog_button(button_frame, "Ok", ok, "left")
    show_dialog(dialog)


def clean_string(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def to_top(widget: tk.Text) -> None:
    widget.yview_moveto(0.0)


def to_bottom(widget: tk.Text) -> None:
    widget.yview_moveto(1.0)
