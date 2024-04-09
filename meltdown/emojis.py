# Standard
from typing import Dict

# Modules
from .args import args


emojis: Dict[str, str] = {
    "unloaded": "👻",
    "local": "🫠",
    "remote": "🌐",
    "storage": "💾",
}


def get(name: str) -> str:
    return emojis.get(name, "")


def text(text: str, name: str) -> str:
    if not args.emojis:
        return text

    emoji = get(name)

    if emoji:
        return f"{emoji} {text}"
    else:
        return text
