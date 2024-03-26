# Modules
from .dialogs import Dialog
from .display import display
from .args import args

# Standard
import json
from pathlib import Path
from .paths import paths
from .app import app
from . import timeutils


def save_log() -> None:
    cmds = []
    cmds.append(("Cancel", lambda: None))
    cmds.append(("To JSON", lambda: log_to_json()))
    cmds.append(("To Text", lambda: log_to_text()))
    Dialog.show_commands("Save conversation to a file?",
                         cmds, on_enter=lambda: log_to_text())


def save_log_file(text: str, ext: str) -> None:
    text = text.strip()
    name = display.get_current_tab_name().lower()
    name = name.replace(" ", "_")
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

    display.print(f">> Log saved as {file_name}")
    print(f"Log saved at {file_path}")

    if args.on_log:
        app.run_command([args.on_log, str(file_path)])


def log_to_json() -> None:
    from .session import session
    document = session.get_current_document()

    if not document:
        return

    text = document.to_dict()

    if not text:
        return

    json_text = json.dumps(text, indent=4)
    save_log_file(json_text, "json")


def log_to_text() -> None:
    from .session import session
    document = session.get_current_document()

    if not document:
        return

    text = document.to_log()

    if not text:
        return

    lines = text.split("\n")
    lines = [line for line in lines if line.strip()]

    full_text = ""
    full_text += document.name + "\n"
    full_text += timeutils.date() + "\n\n"
    full_text += "\n\n".join(lines)

    save_log_file(full_text, "txt")
