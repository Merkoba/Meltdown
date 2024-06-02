from __future__ import annotations

# Modules
from .args import args
from .display import display
from .model import model
from .utils import utils
from . import formats


def summarize(tab_id: str | None = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = formats.get_text(tabconvo.convo, "minimal")

    if not text:
        text = display.get_text(tab_id)

        if not text:
            return

    prompt = {}

    sumprompt = args.summarize_prompt
    sumprompt = utils.replace_keywords(sumprompt)

    prompt["user"] = "Please summarize this."
    prompt["text"] = f"{sumprompt}: "
    prompt["text"] += text

    tab_id = display.make_tab()

    if not tab_id:
        return

    model.stream(prompt, tab_id=tab_id)
