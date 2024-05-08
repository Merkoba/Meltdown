# Standard
from typing import Optional

# Modules
from .args import args
from .display import display
from .session import session
from .model import model


def summarize(tab_id: Optional[str] = None) -> None:
    if not tab_id:
        tab_id = display.current_tab

    tab = display.get_tab(tab_id)

    if not tab:
        return

    conversation = session.get_conversation(tab.conversation_id)

    if not conversation:
        return

    text = conversation.to_text()

    if not text:
        return

    prompt = {}
    prompt["user"] = "Please summarize this."
    prompt["text"] = f"{args.summarize_prompt}: "
    prompt["text"] += text

    tab_id = display.make_tab()
    model.stream(prompt, tab_id=tab_id)
