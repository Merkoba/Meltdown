# Standard
import json

# Modules
from .args import args
from .config import config
from .session import Conversation
from .output import Output


# ---


def get_json(conversation: Conversation) -> str:
    ensure_ascii = args.ascii_logs
    return to_json(conversation, ensure_ascii=ensure_ascii)


def to_json(conversation: Conversation, ensure_ascii: bool = True) -> str:
    obj = conversation.to_dict()

    if config.name_user:
        obj["name_user"] = config.name_user

    if config.name_ai:
        obj["name_ai"] = config.name_ai

    if config.avatar_user:
        obj["avatar_user"] = config.avatar_user

    if config.avatar_ai:
        obj["avatar_ai"] = config.avatar_ai

    return json.dumps(obj, indent=4, ensure_ascii=ensure_ascii)


# ---


def get_text(conversation: Conversation, mode: str = "normal") -> str:
    if mode == "minimal":
        avatars = False
        separate = False
        files = False
        names = True
    else:
        avatars = args.avatars_in_logs
        separate = args.separate_logs
        files = args.files_in_logs
        names = args.names_in_logs

    return to_text(
        conversation, avatars=avatars, names=names, separate=separate, files=files
    )


def to_text(
    conversation: Conversation,
    avatars: bool = False,
    names: bool = True,
    separate: bool = False,
    files: bool = True,
) -> str:
    log = ""
    generic = not names

    for i, item in enumerate(conversation.items):
        for key in item:
            if key == "user":
                prompt = Output.get_prompt(
                    "user", show_avatar=avatars, put_colons=False, generic=generic
                )

                log += f"{prompt}: "
            elif key == "ai":
                prompt = Output.get_prompt(
                    "ai", show_avatar=avatars, put_colons=False, generic=generic
                )

                log += f"{prompt}: "
            else:
                continue

            log += item[key] + "\n\n"

            if files and (key == "user"):
                file = item.get("file", "")

                if file:
                    log += f"File: {file}\n\n"

        if (i < len(conversation.items) - 1) and separate:
            log += "---\n\n"

    return log.strip()


# ---


def get_markdown(conversation: Conversation) -> str:
    avatars = args.avatars_in_logs
    separate = args.separate_logs
    files = args.files_in_logs
    names = args.names_in_logs

    return to_markdown(
        conversation, avatars=avatars, names=names, separate=separate, files=files
    )


def to_markdown(
    conversation: Conversation,
    avatars: bool = False,
    names: bool = True,
    separate: bool = False,
    files: bool = True,
) -> str:
    log = ""
    generic = not names

    for i, item in enumerate(conversation.items):
        for key in item:
            if key == "user":
                prompt = Output.get_prompt(
                    "user", show_avatar=avatars, put_colons=False, generic=generic
                )

                log += f"**{prompt}**:"
            elif key == "ai":
                prompt = Output.get_prompt(
                    "ai", show_avatar=avatars, put_colons=False, generic=generic
                )

                log += f"**{prompt}**:"
            else:
                continue

            log += f" {item[key].strip()}\n\n"

            if files and (key == "user"):
                file = item.get("file", "")

                if file:
                    log += f"**File:** {file}\n\n"

        if (i < len(conversation.items) - 1) and separate:
            log += "---\n\n"

    return log.strip()
