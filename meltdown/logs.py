# Standard
import json
from pathlib import Path

# Modules
from .app import app
from .config import config
from .dialogs import Dialog
from .display import display
from .args import args
from .session import session
from .session import Conversation
from .paths import paths
from . import timeutils
from . import filemanager


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

    def save_file(self, text: str, name: str, ext: str, all: bool) -> None:
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

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        if not all:
            if not args.quiet:
                if args.emojis:
                    msg = f"{config.disk} Log saved as {file_name}"
                else:
                    msg = f"Log saved as {file_name}"

                display.print(msg)

            if args.on_log:
                app.run_command([args.on_log, str(file_path)])

    def to_json(self, all: bool = False) -> None:
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

            text = self.get_json(conversation)

            if not text:
                continue

            num += 1
            self.save_file(text, conversation.name, "json", all)

        if all:
            if args.quiet:
                return

            if args.emojis:
                if num == 1:
                    msg = f"{config.disk} {num} JSON log saved"
                else:
                    msg = f"{config.disk} {num} JSON logs saved"
            else:
                if num == 1:
                    msg = f"{num} JSON log saved"
                else:
                    msg = f"{num} JSON logs saved"

            display.print(msg)

    def get_json(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        text = conversation.to_dict()

        if not text:
            return ""

        json_text = json.dumps(text, indent=4)
        return json_text

    def to_text(self, all: bool = False) -> None:
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

            text = self.get_text(conversation)

            if not text:
                continue

            num += 1
            self.save_file(text, conversation.name, "txt", all)

        if all:
            if args.quiet:
                return

            if args.emojis:
                if num == 1:
                    msg = f"{config.disk} {num} text log saved"
                else:
                    msg = f"{config.disk} {num} text logs saved"
            else:
                if num == 1:
                    msg = f"{num} text log saved"
                else:
                    msg = f"{num} text logs saved"

            display.print(msg)

    def get_text(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
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

    def open(self) -> None:
        filemanager.open_logs_dir()


logs = Logs()
