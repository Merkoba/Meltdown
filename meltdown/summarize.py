from .display import display
from .session import session
from .model import model


def summarize() -> None:
    tab = display.get_current_tab()

    if not tab:
        return

    conversation = session.get_conversation(tab.conversation_id)

    if not conversation:
        return

    text = conversation.to_text()

    prompt = {}
    prompt["text"] = "Summarize this in a concise manner: "
    prompt["text"] += text
    prompt["user"] = "Summarize this in a concise manner."

    tab_id = display.make_tab()
    model.stream(prompt, tab_id=tab_id)
