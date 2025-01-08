from __future__ import annotations

# Standard
import json
from pathlib import Path

# Modules
from .app import app
from .config import config
from .dialogs import Dialog, Commands
from .display import display
from .args import args
from .session import session
from .session import Conversation
from .paths import paths
from .utils import utils
from .files import files
from . import formats


class Logs:
    def menu(self, full: bool = True, tab_id: str | None = None) -> None:
        cmds = Commands()

        if full:
            cmds.add("Save All", lambda a: self.save_all())

        cmds.add("Markdown", lambda a: self.to_markdown(tab_id=tab_id))
        cmds.add("JSON", lambda a: self.to_json(tab_id=tab_id))
        cmds.add("Text", lambda a: self.to_text(tab_id=tab_id))

        Dialog.show_dialog("Save conversation to a file?", cmds)

    def save_all(self) -> None:
        cmds = Commands()
        cmds.add("Markdown", lambda a: self.to_markdown(True))
        cmds.add("JSON", lambda a: self.to_json(True))
        cmds.add("Text", lambda a: self.to_text(True))

        Dialog.show_dialog("Save all conversations?", cmds)

    def save_file(
        self, text: str, name: str, ext: str, save_all: bool, overwrite: bool, mode: str
    ) -> str:
        text = text.strip()
        paths.logs.mkdir(parents=True, exist_ok=True)
        file_name = name + f".{ext}"
        file_path = Path(paths.logs, file_name)
        num = 2

        if (not overwrite) and args.increment_logs:
            while file_path.exists():
                file_name = f"{name}_{num}.{ext}"
                file_path = Path(paths.logs, file_name)
                num += 1

                if num > 9999:
                    break

        files.write(file_path, text)

        if not save_all:
            if not args.quiet and args.log_feedback:
                utils.saved_path("Log", file_path)

            cmd = ""

            if args.open_on_log:
                app.open_generic(str(file_path))
            else:
                if (mode == "text") and args.on_log_text:
                    cmd = args.on_log_text
                elif (mode == "json") and args.on_log_json:
                    cmd = args.on_log_json
                elif (mode == "markdown") and args.on_log_markdown:
                    cmd = args.on_log_markdown
                elif args.on_log:
                    cmd = args.on_log

                if cmd:
                    app.run_program(cmd, str(file_path))

        return str(file_path)

    def save(
        self,
        mode: str,
        save_all: bool,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        num = 0
        last_log = ""
        ext = formats.get_ext(mode)
        overwrite = bool(name)

        def save(content: str, name_: str) -> None:
            nonlocal num, last_log

            if not content:
                return

            num += 1

            if args.clean_names:
                name_ = utils.clean_name(name_)

            name_ = name_[: config.max_file_name_length].strip(" _")

            last_log = self.save_file(
                content, name_, ext, save_all, overwrite=overwrite, mode=mode
            )

        if save_all:
            conversations = [
                session.get_conversation(key) for key in session.conversations
            ]
        else:
            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                return

            conversations = [tabconvo.convo]

        if (len(conversations) > 1) and args.concat_logs:
            contents = []

            for conversation in conversations:
                if not conversation:
                    continue

                if not conversation.items:
                    continue

                contents.append(self.get_content(mode, conversation))

            if mode == "text":
                content = "\n\n---\n\n".join(contents)
            elif mode == "json":
                cont = "[\n" + ",\n".join(contents) + "\n]"
                content = json.dumps(json.loads(cont), indent=4)
            elif mode == "markdown":
                content = "\n\n---\n\n".join(contents)
            else:
                content = ""

            name_ = f"{len(contents)}_{utils.random_word()}"
            save(content, name_)
        else:
            for conversation in conversations:
                if not conversation:
                    continue

                if not conversation.items:
                    continue

                content = self.get_content(mode, conversation)
                name_ = name or conversation.name
                save(content, name_)

        if save_all:
            if args.quiet or (not args.log_feedback):
                return

            f_type = formats.get_name(mode)
            word = utils.singular_or_plural(num, "log", "logs")
            msg = f"{num} {f_type} {word} saved."
            display.print(utils.emoji_text(msg, "storage"))

        if last_log:
            config.set_value("last_log", last_log)

    def to_json(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("json", save_all, name, tab_id=tab_id)

    def to_markdown(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("markdown", save_all, name, tab_id=tab_id)

    def get_json(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        return formats.get_json(conversation)

    def to_text(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("text", save_all, name, tab_id=tab_id)

    def get_text(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        text = formats.get_text(conversation)

        if not text:
            return ""

        full_text = ""
        full_text += f"Name: {conversation.name}\n"

        date_created = utils.to_date(conversation.created)
        full_text += f"Created: {date_created}\n"

        date_saved = utils.to_date(utils.now())
        full_text += f"Saved: {date_saved}"

        full_text += "\n\n---\n\n"
        full_text += text

        return full_text

    def get_markdown(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        text = formats.get_markdown(conversation)

        if not text:
            return ""

        full_text = ""
        full_text += f"# {conversation.name}\n\n"

        date_created = utils.to_date(conversation.created)
        full_text += f"**Created:** {date_created}\n"

        date_saved = utils.to_date(utils.now())
        full_text += f"**Saved:** {date_saved}"

        full_text += "\n\n---\n\n"
        full_text += text

        return full_text

    def open_last_log(self) -> None:
        if not config.last_log:
            return

        app.open_generic(config.last_log)

    def get_content(self, mode: str, conversation: Conversation) -> str:
        if mode == "text":
            text = self.get_text(conversation)
        elif mode == "json":
            text = self.get_json(conversation)
        elif mode == "markdown":
            text = self.get_markdown(conversation)
        else:
            text = ""

        return text.strip()


logs = Logs()
