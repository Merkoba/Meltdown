# Standard
from typing import Optional

# Modules
from .utils import utils


def action(mode: str, number: str, tab_id: Optional[str] = None) -> None:
    from .model import model
    from .display import display
    from .output import Output

    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    if not tabconvo.convo.items:
        return

    index = utils.get_index(number, tabconvo.convo.items)

    if index < 0:
        return

    if index >= len(tabconvo.convo.items):
        return

    item = tabconvo.convo.items[index]

    if not item:
        return

    user_text = item.get("user")
    ai_text = item.get("assistant")

    if mode == "repeat":
        if user_text:
            prompt = {"text": user_text}
            model.stream(prompt, tabconvo.tab.tab_id)
    elif mode == "copy":
        texts = []

        if user_text:
            text = ""
            text += Output.get_prompt("user")
            text += user_text
            texts.append(text)

        if ai_text:
            text = ""
            text += Output.get_prompt("ai")
            text += ai_text
            texts.append(text)

        text = "\n\n".join(texts)

        if text:
            utils.copy(text)
