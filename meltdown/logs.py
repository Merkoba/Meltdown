# Modules
from .dialogs import Dialog
from .display import display
from .args import args
from .session import session
from .session import Conversation

# Standard
import json
from pathlib import Path
from .paths import paths
from .app import app
from . import timeutils


def log_menu() -> None:
    conversation = session.get_current_conversation()

    if (not conversation) or (not conversation.items):
        Dialog.show_message("No conversation to save")
        return

    cmds = []
    cmds.append(("Cancel", lambda: None))
    cmds.append(("Save All", lambda: save_all()))
    cmds.append(("To JSON", lambda: log_to_json()))
    cmds.append(("To Text", lambda: log_to_text()))
    Dialog.show_commands("Save conversation to a file?", cmds)


def save_all() -> None:
    conversation = session.get_current_conversation()

    if (not conversation) or (not conversation.items):
        Dialog.show_message("No conversation to save")
        return

    cmds = []
    cmds.append(("Cancel", lambda: None))
    cmds.append(("To JSON", lambda: log_to_json(True)))
    cmds.append(("To Text", lambda: log_to_text(True)))
    Dialog.show_commands("Save all conversations?", cmds)


def save_log_file(text: str, name: str, ext: str, all: bool) -> None:
    text = text.strip()
    name = name.replace(" ", "_").lower()
    paths.logs.mkdir(parents=True, exist_ok=True)
    file_name = name + f".{ext}"
    file_path = Path(paths.logs, file_name)
    num = 2

    while file_path.exists():
        file_name = f"{name}_{num}.{ext}"
        file_path = Path(paths.logs, file_name)
        num += 1

        if num > 9999:
            break

    with open(file_path, "w") as file:
        file.write(text)

    if not all:
        display.print(f">> Log saved as {file_name}")

        if args.on_log:
            app.run_command([args.on_log, str(file_path)])


def log_to_json(all: bool = False) -> None:
    conversations = []
    num = 0

    if all:
        for key in session.conversations:
            conversations.append(session.get_conversation(key))
    else:
        conversations.append(session.get_current_conversation())

    for conversation in conversations:
        if not conversation:
            continue

        text = get_json_log(conversation)

        if not text:
            return

        num += 1
        save_log_file(text, conversation.name, "json", all)

    if all:
        if num == 1:
            s = f">> {num} JSON log saved"
        else:
            s = f">> {num} JSON logs saved"

        display.print(s)


def get_json_log(conversation: Conversation) -> str:
    if not conversation:
        return ""

    text = conversation.to_dict()

    if not text:
        return ""

    json_text = json.dumps(text, indent=4)
    return json_text


def log_to_text(all: bool = False) -> None:
    conversations = []
    num = 0

    if all:
        for key in session.conversations:
            conversations.append(session.get_conversation(key))
    else:
        conversations.append(session.get_current_conversation())

    for conversation in conversations:
        if not conversation:
            continue

        text = get_text_log(conversation)

        if not text:
            return

        num += 1
        save_log_file(text, conversation.name, "txt", all)

    if all:
        if num == 1:
            s = f">> {num} text log saved"
        else:
            s = f">> {num} text logs saved"

        display.print(s)


def get_text_log(conversation: Conversation) -> str:
    if not conversation:
        return ""

    text = conversation.to_log()

    if not text:
        return ""

    lines = text.split("\n")
    lines = [line for line in lines if line.strip()]

    full_text = ""
    full_text += conversation.name + "\n"
    full_text += timeutils.date() + "\n\n"
    full_text += "\n\n".join(lines)
    return full_text
