# Standard
import json
from pathlib import Path

# Modules
from .app import app
from .dialogs import Dialog
from .display import display
from .args import args
from .session import session
from .session import Conversation
from .paths import paths
from .files import files
from .utils import utils
from . import emojis


class Logs:
    def menu(self) -> None:
        cmds = []
        cmds.append(("Open", lambda: self.open()))
        cmds.append(("Save All", lambda: self.save_all()))
        cmds.append(("To JSON", lambda: self.to_json()))
        cmds.append(("To Text", lambda: self.to_text()))
        Dialog.show_commands("Save conversation to a file?", cmds)

    def save_all(self) -> None:
        cmds = []
        cmds.append(("To JSON", lambda: self.to_json(True)))
        cmds.append(("To Text", lambda: self.to_text(True)))
        Dialog.show_commands("Save all conversations?", cmds)

    def save_file(
        self, text: str, name: str, ext: str, all: bool, overwrite: bool, mode: str
    ) -> None:
        text = text.strip()
        name = name.replace(" ", "_").lower()
        paths.logs.mkdir(parents=True, exist_ok=True)
        file_name = name + f".{ext}"
        file_path = Path(paths.logs, file_name)
        num = 2

        if not overwrite:
            while file_path.exists():
                file_name = f"{name}_{num}.{ext}"
                file_path = Path(paths.logs, file_name)
                num += 1

                if num > 9999:
                    break

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        if not all:
            if not args.quiet and args.log_feedback:
                msg = f"Log saved as {file_name}"
                display.print(emojis.text(msg, "storage"))

            cmd = ""

            if (mode == "text") and args.on_log_text:
                cmd = args.on_log_text
            elif (mode == "json") and args.on_log_json:
                cmd = args.on_log_json
            elif args.on_log:
                cmd = args.on_log

            if cmd:
                app.run_command([cmd, str(file_path)])

    def save(self, mode: str, all: bool, name: str) -> None:
        num = 0
        conversations = []

        if all:
            for key in session.conversations:
                conversations.append(session.get_conversation(key))
        else:
            conversations.append(session.get_current_conversation())

        if mode == "text":
            ext = "txt"
        elif mode == "json":
            ext = "json"

        for conversation in conversations:
            if not conversation:
                continue

            if mode == "text":
                text = self.get_text(conversation)
            elif mode == "json":
                text = self.get_json(conversation)

            if not text:
                continue

            num += 1

            if not name:
                name = conversation.name
                overwrite = False
            else:
                overwrite = True

            self.save_file(text, name, ext, all, overwrite=overwrite, mode=mode)

        if all:
            if args.quiet or (not args.log_feedback):
                return

            if mode == "text":
                s = "text"
            elif mode == "json":
                s = "JSON"

            if num == 1:
                msg = f"{num} {s} log saved"
            else:
                msg = f"{num} {s} logs saved"

            display.print(emojis.text(msg, "storage"))

    def to_json(self, all: bool = False, name: str = "") -> None:
        self.save("json", all, name)

    def get_json(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        return conversation.to_json()

    def to_text(self, all: bool = False, name: str = "") -> None:
        self.save("text", all, name)

    def get_text(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        text = conversation.to_text()

        if not text:
            return ""

        full_text = ""
        full_text += conversation.name + "\n"
        full_text += utils.date() + "\n\n"
        full_text += text
        return full_text

    def open(self, name: str = "") -> None:
        files.open_log(name)


logs = Logs()
