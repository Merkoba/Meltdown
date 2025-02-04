from __future__ import annotations

# Standard
import json
import tempfile
from pathlib import Path
from typing import Any

# Modules
from .app import app
from .args import args
from .utils import utils
from .config import config
from .session import Conversation
from .display import display
from .files import files
from .dialogs import Dialog, Commands


class Formats:
    def get_items(self, conversation: Conversation, mode: str) -> list[Any]:
        if mode == "last":
            return conversation.items[-1:]

        return conversation.items

    def get_names(self, mode: str) -> tuple[str, str]:
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

    def get_avatars(self, mode: str) -> bool:
        if mode == "log":
            return args.avatars_logs

        if mode == "upload":
            return args.avatars_uploads

        return True

    def get_separate(self, mode: str) -> bool:
        if mode == "log":
            return args.separate_logs

        if mode == "upload":
            return args.separate_uploads

        return True

    def get_files(self, mode: str) -> bool:
        if mode == "log":
            return args.files_logs

        if mode == "upload":
            return args.files_uploads

        return True

    def get_generic(self, mode: str) -> bool:
        if mode == "log":
            return args.generic_names_logs

        if mode == "upload":
            return args.generic_names_uploads

        return False

    def get_json(
        self, conversation: Conversation, mode: str = "all", name_mode: str = "normal"
    ) -> str:
        ensure_ascii = args.ascii_logs

        return self.to_json(
            conversation, ensure_ascii=ensure_ascii, mode=mode, name_mode=name_mode
        )

    def get_extra_info(self, name_mode: str) -> bool:
        if name_mode == "log":
            return args.extra_info_logs

        if name_mode == "upload":
            return args.extra_info_uploads

        return False

    def to_json(
        self,
        conversation: Conversation,
        ensure_ascii: bool = True,
        mode: str = "all",
        name_mode: str = "normal",
    ) -> str:
        obj = conversation.to_dict()
        items = self.get_items(conversation, mode)
        obj["items"] = [item.to_dict() for item in items]
        name_user, name_ai = self.get_names(name_mode)

        if config.name_user:
            obj["name_user"] = name_user

        if config.name_ai:
            obj["name_ai"] = name_ai

        if config.avatar_user:
            obj["avatar_user"] = config.avatar_user

        if config.avatar_ai:
            obj["avatar_ai"] = config.avatar_ai

        return json.dumps(obj, indent=4, ensure_ascii=ensure_ascii)

    def get_text(
        self, conversation: Conversation, mode: str = "all", name_mode: str = "normal"
    ) -> str:
        if mode == "minimal":
            avatars = False
            separate = False
            files = False
            generic = True
        else:
            avatars = self.get_avatars(name_mode)
            separate = self.get_separate(name_mode)
            files = self.get_files(name_mode)
            generic = self.get_generic(name_mode)

        return self.to_text(
            conversation,
            avatars=avatars,
            generic=generic,
            separate=separate,
            files=files,
            mode=mode,
            name_mode=name_mode,
        )

    def to_text(
        self,
        conversation: Conversation,
        avatars: bool = True,
        generic: bool = False,
        separate: bool = False,
        files: bool = True,
        mode: str = "all",
        name_mode: str = "normal",
    ) -> str:
        log = ""
        name_user, name_ai = self.get_names(name_mode)
        items = self.get_items(conversation, mode)

        for i, item in enumerate(items):
            for key in ["user", "ai"]:
                prompt = display.get_prompt(
                    key,
                    show_avatar=avatars,
                    generic=generic,
                    name_user=name_user,
                    name_ai=name_ai,
                )

                log += prompt
                log += getattr(item, key) + "\n\n"

                if files and (key == "user"):
                    file = item.file

                    if file:
                        log += f"File: {file}\n\n"

            if (i < len(items) - 1) and separate:
                log += "---\n\n"

        return log.strip()

    def get_markdown(
        self, conversation: Conversation, mode: str = "all", name_mode: str = "normal"
    ) -> str:
        avatars = self.get_avatars(name_mode)
        separate = self.get_separate(name_mode)
        files = self.get_files(name_mode)
        generic = self.get_generic(name_mode)

        return self.to_markdown(
            conversation,
            avatars=avatars,
            generic=generic,
            separate=separate,
            files=files,
            mode=mode,
            name_mode=name_mode,
        )

    def to_markdown(
        self,
        conversation: Conversation,
        avatars: bool = True,
        generic: bool = False,
        separate: bool = False,
        files: bool = True,
        mode: str = "all",
        name_mode: str = "normal",
    ) -> str:
        log = ""
        items = self.get_items(conversation, mode)
        name_user, name_ai = self.get_names(name_mode)
        extra_info = self.get_extra_info(name_mode)

        for i, item in enumerate(items):
            for key in ["user", "ai"]:
                prompt = display.get_prompt(
                    key,
                    show_avatar=avatars,
                    generic=generic,
                    name_user=name_user,
                    name_ai=name_ai,
                )

                if extra_info:
                    prompt += f" ({item.model})\n\n"

                log += prompt
                value = getattr(item, key).strip()

                if "```" in value and (not extra_info):
                    log += "\n\n"

                log += f"{value}\n\n"

                if files and (key == "user"):
                    file = item.file

                    if file:
                        log += f"**File:** {file}\n\n"

            if (i < len(items) - 1) and separate:
                log += "---\n\n"

        return log.strip()

    def do_open(
        self, mode: str, cmd: str | None = None, text: str | None = None
    ) -> None:
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
                text = self.get_text(tabconvo.convo)
            elif mode == "json":
                text = self.get_json(tabconvo.convo)
            elif mode == "markdown":
                text = self.get_markdown(tabconvo.convo)
            else:
                return

        ext = self.get_ext(mode)
        tmpdir = tempfile.gettempdir()
        name = f"mlt_{utils.now_int()}.{ext}"
        path = Path(tmpdir, name)
        files.write(path, text)
        app.open_generic(str(path), opener=cmd)

    def do_view(self, mode: str) -> None:
        if mode == "text":
            self.view_text()
        elif mode == "json":
            self.view_json()
        elif mode == "markdown":
            self.view_markdown()

    def view_text(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_text(tabconvo.convo, name_mode="log")
        name = display.get_tab_name(tabconvo.tab.tab_id)

        if text:
            new_tab = display.make_tab(name=f"{name} Text", mode="ignore")

            if not new_tab:
                return

            display.print(text, tab_id=new_tab)
            display.to_top(tab_id=new_tab)

    def view_json(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_json(tabconvo.convo, name_mode="log")
        name = display.get_tab_name(tabconvo.tab.tab_id)

        if text:
            new_tab = display.make_tab(name=f"{name} JSON", mode="ignore")

            if not new_tab:
                return

            display.print(text, tab_id=new_tab)
            display.to_top(tab_id=new_tab)

    def view_markdown(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_markdown(tabconvo.convo, name_mode="log")
        name = display.get_tab_name(tabconvo.tab.tab_id)

        if text:
            new_tab = display.make_tab(name=f"{name} Markdown", mode="ignore")

            if not new_tab:
                return

            display.print(text, tab_id=new_tab)
            display.format_text(tab_id=new_tab, mode="view", force=True)
            display.to_top(tab_id=new_tab)

    def do_copy(self, mode: str) -> None:
        if mode == "text":
            self.copy_text()
        elif mode == "json":
            self.copy_json()
        elif mode == "markdown":
            self.copy_markdown()

    def copy_text(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_text(tabconvo.convo)

        if not text:
            return

        utils.copy(text)

    def copy_json(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_json(tabconvo.convo)

        if not text:
            return

        utils.copy(text)

    def copy_markdown(self, tab_id: str | None = None) -> None:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = self.get_markdown(tabconvo.convo)

        if not text:
            return

        utils.copy(text)

    def do_use(self, mode: str) -> None:
        from .upload import upload

        cmds = Commands()
        cmds.add("Open", lambda a: self.do_open(mode))
        cmds.add("View", lambda a: self.do_view(mode))
        cmds.add("Copy", lambda a: self.do_copy(mode))
        cmds.add("Upload", lambda a: upload.upload(format_=mode))
        name = self.get_name(mode, True)

        Dialog.show_dialog(f"Use {name}", cmds)

    def get_name(self, mode: str, capitalize: bool = False) -> str:
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

    def get_ext(self, mode: str) -> str:
        ext = ""

        if mode == "text":
            ext = "txt"
        elif mode == "json":
            ext = "json"
        elif mode == "markdown":
            ext = "md"

        return ext


formats = Formats()
