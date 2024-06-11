from __future__ import annotations

# Standard
from typing import Any

# Modules
from .args import args
from .config import config
from .utils import utils
from .menus import Menu
from .dialogs import Dialog
from .files import files


def write(text: str | None = None, maxed: bool = False) -> None:
    from .textbox import TextBox

    def action(ans: dict[str, Any]) -> None:
        config.set("system", ans["text"])

    def reset(textbox: TextBox) -> None:
        value = config.get_default("system")

        if value:
            textbox.set_text(value)
            config.reset_one("system")

        textbox.focus_end()

    def on_right_click(event: Any, textbox: TextBox) -> None:
        menu = Menu()

        text = textbox.get_text()
        menu.add(text="Copy", command=lambda e: textbox.copy())
        menu.add(text="Paste", command=lambda e: textbox.paste())

        if text:
            menu.add(text="Clear", command=lambda e: textbox.clear())

        if text != config.get_default("system"):
            menu.add(text="Reset", command=lambda e: reset(textbox))

        items = files.get_list("systems")[: args.max_list_items]

        if items:

            def proc(item: str) -> None:
                config.set("system", item)
                textbox.set_text(item)
                textbox.focus_end()

            utils.fill_recent(menu, items, text, proc)

        menu.show(event)

    if text:
        config.set("system", text)
        return

    Dialog.show_textbox(
        "system",
        "System Prompt",
        lambda a: action(a),
        value=config.system,
        start_maximized=maxed,
        on_right_click=on_right_click,
    )
