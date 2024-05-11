# Standard
from typing import Optional

# Modules
from .utils import utils


def repeat_prompt(number: str, tab_id: Optional[str] = None) -> None:
    from .model import model
    from .display import display

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

    prompt_text = item.get("user")

    if not prompt_text:
        return

    prompt = {"text": prompt_text}
    model.stream(prompt, tabconvo.tab.tab_id)
