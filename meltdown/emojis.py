# Modules
from .args import args

storage = "💾"
unloaded = "👻"
local = "🫠"
remote = "🌐"


def text(text: str, name: str) -> str:
    if args.emojis:
        if name == "storage":
            emoji = storage
        elif name == "unloaded":
            emoji = unloaded
        elif name == "local":
            emoji = local
        elif name == "remote":
            emoji = remote
        else:
            emoji = ""
    else:
        emoji = ""

    if emoji:
        return f"{emoji} {text}"
    else:
        return text
