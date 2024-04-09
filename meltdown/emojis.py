# Standard
from typing import Dict

# Modules
from .args import args


emojis: Dict[str, str] = {}
emojis["storage"] = "💾"
emojis["unloaded"] = "👻"
emojis["local"] = "🫠"
emojis["remote"] = "🌐"


def text(text: str, name: str) -> str:
    if not args.emojis:
        return text

    emoji = emojis.get(name, "")

    if emoji:
        return f"{emoji} {text}"
    else:
        return text


def get(name: str) -> str:
    return emojis.get(name, "")
