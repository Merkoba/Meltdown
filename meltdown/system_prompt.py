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
from .textbox import TextBox


class SystemPrompt:
    def write(self, text: str | None = None, maxed: bool = False) -> None:
        if text:
            config.set("system", text)
            return

        Dialog.show_textbox(
            "system",
            "System Prompt",
            lambda a: self.action(a),
            value=config.system,
            start_maximized=maxed,
            on_right_click=self.on_right_click,
        )

    def action(self, ans: dict[str, Any]) -> None:
        config.set("system", ans["text"])

    def on_right_click(self, event: Any, textbox: TextBox) -> None:
        menu = Menu()
        text = textbox.get_text()
        menu.add(text="Copy", command=lambda e: textbox.copy())
        menu.add(text="Paste", command=lambda e: textbox.paste())

        if text:
            menu.add(text="Clear", command=lambda e: textbox.clear())

        if text != config.get_default("system"):
            menu.add(text="Reset", command=lambda e: self.reset(textbox))

        items = files.get_list("systems")[: args.max_list_items]

        if items:

            def cmd(s: str) -> None:
                config.set("system", s)
                textbox.set_text(s)
                textbox.focus_end()

            def forget(s: str) -> None:
                files.remove_system(s)
                self.on_right_click(event, textbox)

            utils.fill_recent(menu, items, text, cmd, alt_cmd=lambda s: forget(s))

        menu.show(event)

    def reset(self, textbox: TextBox) -> None:
        value = config.get_default("system")

        if value:
            textbox.set_text(value)
            config.reset_one("system")

        textbox.focus_end()


system_prompt = SystemPrompt()