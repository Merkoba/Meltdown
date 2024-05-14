# Standard
import json
from typing import List, Dict, Any, Optional
from tkinter import filedialog
from pathlib import Path

# Modules
from .app import app
from .config import config
from .display import display
from .paths import paths
from .args import args
from .dialogs import Dialog
from .output import Output
from .utils import utils
from . import tests
from . import close


class Conversation:
    def __init__(
        self, _id: str, name: str, created: float = 0.0, last_modified: float = 0.0
    ) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []
        self.last_modified = last_modified

        if created == 0.0:
            self.created = utils.now()
        else:
            self.created = created

    def add(self, context_dict: Dict[str, str]) -> None:
        self.last_modified = utils.now()
        self.items.append(context_dict)
        self.limit()
        session.do_save()

    def limit(self) -> None:
        self.items = self.items[-config.max_log :]

    def clear(self) -> None:
        self.last_modified = utils.now()
        self.items = []
        session.save()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def print(self) -> None:
        if not self.items:
            return

        tab = display.get_tab_by_conversation_id(self.id)

        if not tab:
            return

        if not args.auto_scroll:
            display.disable_auto_scroll(tab.tab_id)

        for item in self.items:
            for key in item:
                if key == "user":
                    display.prompt(
                        "user",
                        item[key],
                        tab_id=tab.tab_id,
                        to_bottom=False,
                        file=item.get("file", ""),
                    )
                elif key == "assistant":
                    display.prompt("ai", item[key], tab_id=tab.tab_id, to_bottom=False)
                else:
                    continue

        display.format_text(tab.tab_id)
        display.enable_auto_scroll(tab.tab_id)
        display.check_scroll_buttons(tab.tab_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created,
            "last_modified": self.last_modified,
            "items": self.items,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def to_text(self) -> str:
        log = ""

        for item in self.items:
            for key in item:
                if key == "user":
                    if args.avatars_in_logs:
                        log += Output.get_prompt("user")
                    else:
                        log += Output.get_prompt(
                            "user", show_avatar=False, colon_space=False
                        )
                elif key == "assistant":
                    if args.avatars_in_logs:
                        log += Output.get_prompt("ai")
                    else:
                        log += Output.get_prompt(
                            "ai", show_avatar=False, colon_space=False
                        )
                else:
                    continue

                log += item[key] + "\n\n"

                if args.files_in_logs:
                    file = item.get("file", "")

                    if file:
                        log += f"File: {file}\n\n"

        return log.strip()


class Session:
    def __init__(self) -> None:
        self.conversations: Dict[str, Conversation] = {}
        self.save_after = ""

    def add(self, name: str, conv_id: Optional[str] = None) -> Conversation:
        if not conv_id:
            conv_id = str(utils.now())

        conversation = Conversation(conv_id, name)
        conversation.last_modified = utils.now()
        self.conversations[conv_id] = conversation
        return conversation

    def remove(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.save()

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.conversations.get(conversation_id)

    def change_name(self, conversation_id: str, name: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].name = name
            self.save()

    def clear(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()
            self.save()

    def clear_save(self) -> None:
        if self.save_after:
            app.root.after_cancel(self.save_after)
            self.save_after = ""

    def save(self) -> None:
        self.clear_save()
        self.save_after = app.root.after(config.save_delay, lambda: self.do_save())

    def do_save(self) -> None:
        self.clear_save()

        if args.temporary:
            return

        if not paths.session.exists():
            paths.session.parent.mkdir(parents=True, exist_ok=True)

        with paths.session.open("w", encoding="utf-8") as file:
            file.write(self.to_json())

    def load_arg(self) -> None:
        try:
            name = args.session

            if not name.endswith(".json"):
                name += ".json"

            path = Path(name)

            if (not path.exists()) or (not path.is_file()):
                path = Path(paths.sessions, name)

            if (not path.exists()) or (not path.is_file()):
                args.session = ""
                self.load()
                return

            self.load_items(path)
        except BaseException as e:
            utils.error(e)
            args.session = ""
            self.load()

    def load(self) -> None:
        if args.session:
            self.load_arg()
            return

        if args.clean:
            return

        path = paths.session

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
        try:
            self.load_items(path)
        except BaseException as e:
            utils.error(e)
            self.reset()

    def reset(self) -> None:
        self.conversations = {}
        close.close_all_tabs(force=True)

    def load_items(self, path: Path) -> None:
        close.close_all_tabs(force=True, make_empty=False)

        with path.open("r", encoding="utf-8") as file:
            try:
                items = json.load(file)
            except BaseException:
                utils.msg("Creating empty session.json")
                items = []

        if args.test:
            items.append(tests.format_test)

        if not items:
            return

        for item in items:
            conversation = Conversation(
                item["id"],
                name=item["name"],
                created=item.get("created", 0.0),
                last_modified=item.get("last_modified", 0.0),
            )

            conversation.items = item["items"]
            self.conversations[conversation.id] = conversation

            display.make_tab(
                conversation.name, conversation.id, select_tab=False, save=False
            )

    def save_state(self, name: Optional[str] = None) -> None:
        if not paths.sessions.exists():
            paths.sessions.mkdir(parents=True, exist_ok=True)

        if name:
            file_path = str(Path(paths.sessions, f"{name}.json"))
        else:
            file_path = filedialog.asksaveasfilename(
                initialdir=paths.sessions,
                defaultextension=".json",
                filetypes=[("Session Files", "*.json")],
            )

            if not file_path:
                return

        path = Path(file_path)

        with path.open("w", encoding="utf-8") as file:
            file.write(self.to_json())

        if not args.quiet:
            name = path.name
            msg = f"Session saved as {name}"
            display.print(utils.emoji_text(msg, "storage"))

    def load_state(self, name: Optional[str] = None) -> None:
        if not paths.sessions.exists():
            paths.sessions.mkdir(parents=True, exist_ok=True)

        if name:
            path = Path(paths.sessions, f"{name}.json")
        else:
            file_path = filedialog.askopenfilename(
                initialdir=paths.sessions,
            )

            if not file_path:
                return

            path = Path(file_path)

        if (not path.exists()) or (not path.is_file()):
            if not args.quiet:
                display.print("Session file not found.")

            return

        try:
            self.load_items(path)
            display.select_last_tab()
            self.save()
        except BaseException as e:
            utils.error(e)
            self.reset()

    def update(self) -> None:
        tabs = display.tab_ids()
        new_items = {}

        for tab_id in tabs:
            tab = display.get_tab(tab_id)

            if not tab:
                continue

            conversation = self.get_conversation(tab.conversation_id)

            if not conversation:
                continue

            new_items[conversation.id] = conversation

        self.conversations = new_items
        self.save()

    def to_json(self) -> str:
        def check(conversation: Conversation) -> bool:
            if conversation.id == "ignore":
                return False

            if not args.allow_empty:
                if not conversation.items:
                    return False

            return True

        sessions_list = [
            conversation.to_dict()
            for conversation in self.conversations.values()
            if check(conversation)
        ]

        return json.dumps(sessions_list, indent=4)

    def menu(self) -> None:
        cmds = []
        cmds.append(("Load", lambda: self.load_state()))
        cmds.append(("Save", lambda: self.save_state()))
        Dialog.show_commands("Session Menu", commands=cmds)


session = Session()
