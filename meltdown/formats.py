# Standard
import json
import tempfile
from pathlib import Path
from typing import Optional

# Modules
from .app import app
from .args import args
from .utils import utils
from .config import config
from .session import Conversation
from .output import Output
from .display import display
from .files import files


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
            if key in ("user", "ai"):
                prompt = Output.get_prompt(
                    key, show_avatar=avatars, put_colons=False, generic=generic
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
            if key in ("user", "ai"):
                prompt = Output.get_prompt(
                    key, show_avatar=avatars, put_colons=False, generic=generic
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


# ---


def program(mode: str, cmd: Optional[str] = None) -> None:
    if not cmd:
        if mode == "text":
            cmd = args.prog_text or args.program
        elif mode == "json":
            cmd = args.prog_json or args.program
        elif mode == "markdown":
            cmd = args.prog_markdown or args.program

    tabconvo = display.get_tab_convo(None)

    if not tabconvo:
        return

    if not tabconvo.convo.items:
        return

    if mode == "text":
        text = get_text(tabconvo.convo)
        ext = "txt"
    elif mode == "json":
        text = get_json(tabconvo.convo)
        ext = "json"
    elif mode == "markdown":
        text = get_markdown(tabconvo.convo)
        ext = "markdown"
    else:
        return

    tmpdir = tempfile.gettempdir()
    name = f"mlt_{utils.now_int()}.{ext}"
    path = Path(tmpdir, name)
    files.write(path, text)
    app.open_generic(str(path), opener=cmd)


# ---


def view_text(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_text(tabconvo.convo)
    name = display.get_tab_name(tabconvo.tab.tab_id)

    if text:
        new_tab = display.make_tab(name=f"{name} Text", mode="ignore")

        if not new_tab:
            return

        display.print(text, tab_id=new_tab)
        display.to_top(tab_id=new_tab)


def view_json(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_json(tabconvo.convo)
    name = display.get_tab_name(tabconvo.tab.tab_id)

    if text:
        new_tab = display.make_tab(name=f"{name} JSON", mode="ignore")

        if not new_tab:
            return

        display.print(text, tab_id=new_tab)
        display.to_top(tab_id=new_tab)


def view_markdown(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_markdown(tabconvo.convo)
    name = display.get_tab_name(tabconvo.tab.tab_id)

    if text:
        new_tab = display.make_tab(name=f"{name} Markdown", mode="ignore")

        if not new_tab:
            return

        display.print(text, tab_id=new_tab)
        display.format_text(tab_id=new_tab, mode="all")
        display.to_top(tab_id=new_tab)


# ---


def copy_text(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_text(tabconvo.convo)

    if not text:
        return

    utils.copy(text)


def copy_json(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_json(tabconvo.convo)

    if not text:
        return

    utils.copy(text)


def copy_markdown(tab_id: Optional[str] = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_markdown(tabconvo.convo)

    if not text:
        return

    utils.copy(text)
