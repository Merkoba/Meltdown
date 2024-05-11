# Standard
from typing import Optional

# Modules
from .utils import utils


def repeat_prompt(number: str, tab_id: Optional[str] = None) -> None:
    from .session import session
    from .model import model
    from .display import display

    if not tab_id:
        tab_id = display.current_tab

    tab = display.get_tab(tab_id)

    if not tab:
        return

    conversation = session.get_conversation(tab.conversation_id)

    if not conversation:
        return

    if not conversation.items:
        return

    index = utils.get_index(number, conversation.items)

    if index < 0:
        return

    if index >= len(conversation.items):
        return

    item = conversation.items[index]

    if not item:
        return

    prompt_text = item.get("user")

    if not prompt_text:
        return

    prompt = {"text": prompt_text}
    model.stream(prompt, tab_id)
