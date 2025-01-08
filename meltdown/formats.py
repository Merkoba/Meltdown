from __future__ import annotations

# Standard
import json
import tempfile
from pathlib import Path

# Modules
from .app import app
from .args import args
from .utils import utils
from .config import config
from .session import Conversation
from .output import Output
from .display import display
from .files import files
from .dialogs import Dialog, Commands


# ---


def get_names(mode: str) -> tuple[str, str]:
    name_user = ""
    name_ai = ""

    if mode == "log":
        if args.log_name_user:
            name_user = args.log_name_user

        if args.log_name_ai:
            name_ai = args.log_name_ai
    elif mode == "upload":
        if args.upload_name_user:
            name_user = args.upload_name_user

        if args.upload_name_ai:
            name_ai = args.upload_name_ai

    if not name_user:
        if config.name_user:
            name_user = config.name_user

    if not name_ai:
        if config.name_ai:
            name_ai = config.name_ai

    return name_user, name_ai


def get_avatars(mode: str) -> bool:
    if mode == "log":
        return args.avatars_in_logs

    if mode == "upload":
        return args.avatars_in_uploads

    return False


def get_separate(mode: str) -> bool:
    if mode == "log":
        return args.separate_logs

    if mode == "upload":
        return args.separate_uploads

    return True


def get_files(mode: str) -> bool:
    if mode == "log":
        return args.files_in_logs

    if mode == "upload":
        return args.files_in_uploads

    return True


def get_generic(mode: str) -> bool:
    if mode == "log":
        return args.generic_names_logs

    if mode == "upload":
        return args.generic_names_uploads

    return False


def get_json(conversation: Conversation, name_mode: str = "normal") -> str:
    ensure_ascii = args.ascii_logs
    return to_json(conversation, ensure_ascii=ensure_ascii, name_mode=name_mode)


def to_json(
    conversation: Conversation,
    ensure_ascii: bool = True,
    name_mode: str = "normal",
) -> str:
    obj = conversation.to_dict()
    name_user, name_ai = get_names(name_mode)

    if config.name_user:
        obj["name_user"] = name_user

    if config.name_ai:
        obj["name_ai"] = name_ai

    if config.avatar_user:
        obj["avatar_user"] = config.avatar_user

    if config.avatar_ai:
        obj["avatar_ai"] = config.avatar_ai

    return json.dumps(obj, indent=4, ensure_ascii=ensure_ascii)


# ---


def get_text(
    conversation: Conversation, mode: str = "normal", name_mode: str = "normal"
) -> str:
    if mode == "minimal":
        avatars = False
        separate = False
        files = False
        generic = True
    else:
        avatars = get_avatars(name_mode)
        separate = get_separate(name_mode)
        files = get_files(name_mode)
        generic = get_generic(name_mode)

    return to_text(
        conversation,
        avatars=avatars,
        generic=generic,
        separate=separate,
        files=files,
        name_mode=name_mode,
    )


def to_text(
    conversation: Conversation,
    avatars: bool = False,
    generic: bool = True,
    separate: bool = False,
    files: bool = True,
    name_mode: str = "normal",
) -> str:
    log = ""
    name_user, name_ai = get_names(name_mode)

    for i, item in enumerate(conversation.items):
        for key in ["user", "ai"]:
            prompt = Output.get_prompt(
                key,
                show_avatar=avatars,
                put_colons=False,
                generic=generic,
                name_user=name_user,
                name_ai=name_ai,
            )

            log += f"{prompt}: "
            log += getattr(item, key) + "\n\n"

            if files and (key == "user"):
                file = item.file

                if file:
                    log += f"File: {file}\n\n"

        if (i < len(conversation.items) - 1) and separate:
            log += "---\n\n"

    return log.strip()


# ---


def get_markdown(
    conversation: Conversation, mode: str = "all", name_mode: str = "normal"
) -> str:
    avatars = get_avatars(name_mode)
    separate = get_separate(name_mode)
    files = get_files(name_mode)
    generic = get_generic(name_mode)

    return to_markdown(
        conversation,
        avatars=avatars,
        generic=generic,
        separate=separate,
        files=files,
        mode=mode,
        name_mode=name_mode,
    )


def to_markdown(
    conversation: Conversation,
    avatars: bool = False,
    generic: bool = True,
    separate: bool = False,
    files: bool = True,
    mode: str = "all",
    name_mode: str = "normal",
) -> str:
    log = ""

    if mode == "last":
        items = conversation.items[-1:]
    else:
        items = conversation.items

    name_user, name_ai = get_names(name_mode)

    for i, item in enumerate(items):
        for key in ["user", "ai"]:
            prompt = Output.get_prompt(
                key,
                show_avatar=avatars,
                put_colons=False,
                generic=generic,
                name_user=name_user,
                name_ai=name_ai,
            )

            log += f"**{prompt}**:"
            log += f" {getattr(item, key).strip()}\n\n"

            if files and (key == "user"):
                file = item.file

                if file:
                    log += f"**File:** {file}\n\n"

        if (i < len(items) - 1) and separate:
            log += "---\n\n"

    return log.strip()


# ---


def do_open(mode: str, cmd: str | None = None, text: str | None = None) -> None:
    if not cmd:
        if mode == "text":
            cmd = args.program_text or args.program
        elif mode == "json":
            cmd = args.program_json or args.program
        elif mode == "markdown":
            cmd = args.program_markdown or args.program

    tabconvo = display.get_tab_convo(None)

    if not tabconvo:
        return

    if not tabconvo.convo.items:
        return

    if not text:
        if mode == "text":
            text = get_text(tabconvo.convo)
        elif mode == "json":
            text = get_json(tabconvo.convo)
        elif mode == "markdown":
            text = get_markdown(tabconvo.convo)
        else:
            return

    ext = get_ext(mode)
    tmpdir = tempfile.gettempdir()
    name = f"mlt_{utils.now_int()}.{ext}"
    path = Path(tmpdir, name)
    files.write(path, text)
    app.open_generic(str(path), opener=cmd)


# ---


def do_view(mode: str) -> None:
    if mode == "text":
        view_text()
    elif mode == "json":
        view_json()
    elif mode == "markdown":
        view_markdown()


def view_text(tab_id: str | None = None) -> None:
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


def view_json(tab_id: str | None = None) -> None:
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


def view_markdown(tab_id: str | None = None) -> None:
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


def do_copy(mode: str) -> None:
    if mode == "text":
        copy_text()
    elif mode == "json":
        copy_json()
    elif mode == "markdown":
        copy_markdown()


def copy_text(tab_id: str | None = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_text(tabconvo.convo)

    if not text:
        return

    utils.copy(text)


def copy_json(tab_id: str | None = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_json(tabconvo.convo)

    if not text:
        return

    utils.copy(text)


def copy_markdown(tab_id: str | None = None) -> None:
    tabconvo = display.get_tab_convo(tab_id)

    if not tabconvo:
        return

    text = get_markdown(tabconvo.convo)

    if not text:
        return

    utils.copy(text)


# ---


def do_use(mode: str) -> None:
    cmds = Commands()
    cmds.add("Open", lambda a: do_open(mode))
    cmds.add("View", lambda a: do_view(mode))
    cmds.add("Copy", lambda a: do_copy(mode))
    name = get_name(mode, True)

    Dialog.show_dialog(f"Use {name}", cmds)


def get_name(mode: str, capitalize: bool = False) -> str:
    name = ""

    if mode == "text":
        name = "text"
    elif mode == "json":
        name = "JSON"
    elif mode == "markdown":
        name = "markdown"

    if capitalize:
        if name != "JSON":
            name = name.capitalize()

    return name


def get_ext(mode: str) -> str:
    ext = ""

    if mode == "text":
        ext = "txt"
    elif mode == "json":
        ext = "json"
    elif mode == "markdown":
        ext = "md"

    return ext
