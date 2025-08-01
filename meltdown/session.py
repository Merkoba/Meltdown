from __future__ import annotations

# Standard
import json
from typing import Any
from tkinter import filedialog
from pathlib import Path
from collections import OrderedDict

# Modules
from .app import app
from .config import config
from .display import display
from .paths import paths
from .args import args
from .dialogs import Dialog, Commands
from .utils import utils
from .files import files
from .close import close
from .tests import tests
from .memory import memory


class Item:
    @staticmethod
    def from_dict(data: dict[str, Any]) -> Item:
        return Item(
            model=data.get("model", ""),
            user=data.get("user", ""),
            ai=data.get("ai", ""),
            file=data.get("file", ""),
            date=data.get("date", None),
            duration=data.get("duration", None),
            seed=data.get("seed", None),
            history=data.get("history", None),
            max_tokens=data.get("max_tokens", None),
            temperature=data.get("temperature", None),
            top_k=data.get("top_k", None),
            top_p=data.get("top_p", None),
            format_=data.get("format", None),
        )

    def __init__(
        self,
        model: str,
        user: str,
        ai: str,
        file: str,
        date: float | None,
        duration: float | None,
        seed: int | None,
        history: int | None,
        max_tokens: int | None,
        temperature: float | None,
        top_k: int | None,
        top_p: float | None,
        format_: str | None,
    ) -> None:
        self.date = date
        self.duration = duration
        self.user = user
        self.ai = ai
        self.file = file
        self.model = model
        self.seed = seed
        self.history = history
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.format = format_

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "duration": self.duration,
            "user": self.user,
            "ai": self.ai,
            "file": self.file,
            "model": self.model,
            "seed": self.seed,
            "history": self.history,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "format": self.format,
        }


class Conversation:
    def __init__(
        self,
        _id: str,
        name: str,
        created: float = 0.0,
        last_modified: float = 0.0,
        pin: bool = False,
    ) -> None:
        self.id = _id
        self.name = name
        self.items: list[Item] = []
        self.last_modified = last_modified
        self.pin = pin

        if created == 0.0:
            self.created = utils.now()
        else:
            self.created = created

    def add(self, data: dict[str, Any]) -> Item:
        item = Item.from_dict(data)
        self.last_modified = utils.now()
        self.items.append(item)
        self.limit()
        session.do_save()
        return item

    def update(self) -> None:
        self.last_modified = utils.now()
        session.do_save()

    def limit(self) -> None:
        self.items = self.items[-config.max_log :]

    def clear(self) -> None:
        self.last_modified = utils.now()
        self.items = []
        session.save()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def set_name(self, name: str) -> None:
        self.name = name
        session.save()

    def set_pin(self, value: bool) -> None:
        self.pin = value
        session.save()

    def print(self) -> None:
        if not self.items:
            return

        tab = display.get_tab_by_conversation_id(self.id)

        if not tab:
            return

        if not args.auto_bottom:
            display.disable_auto_bottom(tab.tab_id)

        for item in self.items:
            display.prompt(
                "user",
                item.user,
                tab_id=tab.tab_id,
                to_bottom=False,
                file=item.file,
            )

            display.prompt("ai", item.ai, tab_id=tab.tab_id, to_bottom=False)

        display.format_text(tab.tab_id)
        display.enable_auto_bottom(tab.tab_id)
        display.check_scroll_buttons(tab.tab_id)

    def to_dict(self) -> dict[str, Any]:
        item_list = [item.to_dict() for item in self.items]

        return {
            "id": self.id,
            "name": self.name,
            "created": self.created,
            "last_modified": self.last_modified,
            "pin": self.pin,
            "items": item_list,
        }

    def count(self) -> int:
        return len(self.items)


class Session:
    def __init__(self) -> None:
        self.conversations: OrderedDict[str, Conversation] = OrderedDict()
        self.save_after = ""

    def add(
        self, name: str, conv_id: str | None = None, position: str = "end"
    ) -> Conversation:
        if not conv_id:
            conv_id = str(utils.now())

        conversation = Conversation(conv_id, name)
        conversation.last_modified = utils.now()

        if position == "start":
            self.conversations = OrderedDict(
                [(conv_id, conversation), *self.conversations.items()]
            )
        else:
            self.conversations[conv_id] = conversation

        return conversation

    def remove(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.save()

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self.conversations.get(conversation_id)

    def clear(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()
            self.save()

    def clear_save(self) -> None:
        if self.save_after:
            app.root.after_cancel(self.save_after)
            self.save_after = ""

    def save(self) -> None:
        if not app.exists():
            return

        self.clear_save()
        self.save_after = app.root.after(config.save_delay, lambda: self.do_save())

    def do_save(self) -> None:
        self.clear_save()

        if args.temporary:
            return

        if not paths.session.exists():
            paths.session.parent.mkdir(parents=True, exist_ok=True)

        files.write(paths.session, self.to_json())

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
        self.conversations = OrderedDict()
        close.close_all(force=True)

    def load_items(self, path: Path) -> None:
        close.close_all(force=True, make_empty=False)

        try:
            items = files.load(path)
        except BaseException:
            if not args.quiet:
                utils.msg("Creating empty session.json")

            items = []

        if args.test:
            test = tests.get(args.test)

            if test:
                items.append(test)

        if not items:
            return

        for i, item in enumerate(items):
            if args.max_tabs > 0:
                if i >= args.max_tabs:
                    break

            convo = Conversation(
                item["id"],
                name=item["name"],
                created=item.get("created", 0.0),
                last_modified=item.get("last_modified", 0.0),
                pin=item.get("pin", False),
            )

            for it in item["items"]:
                item_obj = Item.from_dict(it)
                convo.items.append(item_obj)

            self.conversations[convo.id] = convo

            tab_id = display.make_tab(
                convo.name, convo.id, select_tab=False, save=False
            )

            if not tab_id:
                break

    def save_state(self, name: str | None = None) -> None:
        if name == "last":
            self.save_last()
            return

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
        files.write(path, self.to_json())
        memory.set_value("last_session", path.stem)

        if not args.quiet:
            utils.saved_path(path)

    def load_state(self, name: str | None = None) -> None:
        if name == "last":
            self.load_last()
            return

        if not paths.sessions.exists():
            paths.sessions.mkdir(parents=True, exist_ok=True)

        if name:
            fname = files.full_name(name)
            path = Path(paths.sessions, fname)
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
            memory.set_value("last_session", path.stem)
            display.select_last_tab()
            self.save()
        except BaseException as e:
            utils.error(e)
            self.reset()

    def update(self) -> None:
        tabs = display.tab_ids()
        new_items = OrderedDict()

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
        cmds = Commands()
        cmds.add("Open", lambda a: self.open_directory())
        cmds.add("Load", lambda a: self.load_state())
        cmds.add("Save", lambda a: self.save_state())

        Dialog.show_dialog("Session Menu", commands=cmds)

    def save_last(self) -> None:
        if not memory.last_session:
            return

        self.save_state(memory.last_session)

    def load_last(self) -> None:
        if not memory.last_session:
            return

        self.load_state(memory.last_session)

    def count(self) -> int:
        return sum(c.count() for c in self.conversations.values())

    def open_directory(self) -> None:
        paths.sessions.mkdir(parents=True, exist_ok=True)
        app.open_generic(str(paths.sessions))


session = Session()
