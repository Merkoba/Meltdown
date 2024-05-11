# Standard
from typing import Optional

# Modules
from .utils import utils


def repeat_prompt(number: str, tab_id: Optional[str] = None) -> None:
    from .model import model
    from .display import display

    tab, convo, tab_id = display.get_tab_convo(tab_id)

    if (not tab) or (not convo):
        return

    if not convo.items:
        return

    index = utils.get_index(number, convo.items)

    if index < 0:
        return

    if index >= len(convo.items):
        return

    item = convo.items[index]

    if not item:
        return

    prompt_text = item.get("user")

    if not prompt_text:
        return

    prompt = {"text": prompt_text}
    model.stream(prompt, tab_id)
