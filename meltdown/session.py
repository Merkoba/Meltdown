# Modules
from .config import config
from .display import display
from .paths import paths
from .args import args
from .dialogs import Dialog
from .output import Output
from . import timeutils

# Standard
import json
from typing import List, Dict, Any, Optional
from tkinter import filedialog
from pathlib import Path


test_conversation = {
    "id": "ignore",
    "name": "Test",
    "items": [
        {"user": "Highlight Test"},
        {"assistant": "Here is a `highlight` and `a longer highlight`.\nHere is a `highlight` and `a longer highlight`."},
        {"user": "Highlight Test 2"},
        {"assistant": "`another highlight 123`"},
        {"user": "Bold Test"},
        {"assistant": "Here is a bold **word** and **a bold sentence**.\nHere is a bold **word** and **a bold sentence**."},
        {"user": "Bold Test 2"},
        {"assistant": "\n1) **Some Item:** Description\n2) **Another Item:** Description\n3) **Third Item:** Description"},
        {"user": "Bold Test 3"},
        {"assistant": "**This is a bold sentence**\n**This is a bold sentence**"},
        {"user": "Italic Test with Asterisk"},
        {"assistant": "Here is an italic *word* and *an italic sentence*.\nHere is an italic *word* and *an italic sentence*."},
        {"user": "Italic Test with Underscore"},
        {"assistant": "Here is a an italic _word_ and _an italic sentence_.\nHere is a an italic _word_ and _an italic sentence_."},
        {"user": "Italic Test 3"},
        {"assistant": "*This is an italic sentence*\n*This is an italic sentence*"},
        {"user": "Italic Test 4"},
        {"assistant": "_This is an italic sentence_ 2\n_This is an italic sentence_ 2"},
        {"user": "Snippet Test"},
        {"assistant":
            "```python\na = 123\nprint('Hello, World!')\n```\n\n" +
            "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
         },
        {"user": "Snippet Test 2"},
        {"assistant":
            "Here is some code:\n\n```\na = 123\nprint('Hello, World!')\n```\n\n" +
            "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
         },
        {"user": "Snippet Test 3"},
        {"assistant":
            "```python\na = 123\nprint('Hello, World!')\n```"
         },
        {"user": "URL Test"},
        {"assistant": "Here are some urls https://aa.com and http://cc.com and ftp://44.com\n" +
         "Here are some urls https://aa.com and http://cc.com\nftp://44.com"},
        {"user": "Normal Sentence"},
        {"assistant": "Here is a normal sentence"},
        {"user": "Loading dolphin-2_6-phi-2.Q5_K_M.gguf"},
        {"assistant": "Ok"},
    ],
}


class Conversation:
    def __init__(self, _id: str, name: str, last_modified: float = 0.0) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []
        self.last_modified = last_modified

    def add(self, context_dict: Dict[str, str]) -> None:
        self.last_modified = timeutils.now()
        self.items.append(context_dict)
        self.limit()
        session.save()

    def limit(self) -> None:
        self.items = self.items[-config.max_log:]

    def clear(self) -> None:
        self.items = []
        session.save()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def print(self) -> None:
        tab = display.get_tab_by_conversation_id(self.id)

        if tab:
            for item in self.items:
                for key in item:
                    if key == "user":
                        display.prompt("user", item[key], tab_id=tab.tab_id, to_bottom=False)
                    elif key == "assistant":
                        display.prompt("ai", item[key], tab_id=tab.tab_id, to_bottom=False)
                    else:
                        continue

            tab.output.format_text()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "last_modified": self.last_modified,
            "items": self.items,
        }

    def to_log(self) -> str:
        log = ""

        for item in self.items:
            for key in item:
                if key == "user":
                    log += Output.get_prompt("user")
                elif key == "assistant":
                    log += Output.get_prompt("ai")
                else:
                    continue

                log += item[key] + "\n"

        return log


class Session:
    def __init__(self) -> None:
        self.conversations: Dict[str, Conversation] = {}

    def add(self, name: str, conv_id: str = "") -> Conversation:
        if not conv_id:
            conv_id = str(timeutils.now())

        conversation = Conversation(conv_id, name)
        conversation.last_modified = timeutils.now()
        self.conversations[conv_id] = conversation
        return conversation

    def remove(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.save()

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.conversations.get(conversation_id)

    def get_current_conversation(self) -> Optional[Conversation]:
        tab = display.get_current_tab()

        if tab:
            return self.get_conversation(tab.conversation_id)
        else:
            return None

    def change_name(self, conversation_id: str, name: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].name = name
            self.save()

    def clear(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()
            self.save()

    def save(self) -> None:
        if not paths.session.exists():
            paths.session.parent.mkdir(parents=True, exist_ok=True)

        with open(paths.session, "w", encoding="utf-8") as file:
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
            print(e)
            args.session = ""
            self.load()

    def load(self) -> None:
        if args.session:
            self.load_arg()
            return

        path = paths.session

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
        try:
            self.load_items(path)
        except BaseException as e:
            print(e)
            self.reset()

    def reset(self) -> None:
        self.conversations = {}
        display.close_all_tabs(force=True)

    def load_items(self, path: Path) -> None:
        display.close_all_tabs(force=True, make_empty=False)

        with open(path, "r", encoding="utf-8") as file:
            try:
                items = json.load(file)
            except BaseException:
                items = []

        if args.test:
            items.append(test_conversation)

        if not items:
            return

        for item in items:
            conversation = Conversation(item["id"], item["name"], item.get("last_modified", 0.0))
            conversation.items = item["items"]
            self.conversations[conversation.id] = conversation
            display.make_tab(conversation.name, conversation.id,
                             select_tab=False, save=False)

    def save_state(self, name: str = "") -> None:
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

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.to_json())

        display.print(f"{config.disk} Session saved")

    def load_state(self, name: str = "") -> None:
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
            return

        try:
            self.load_items(path)
            display.select_last_tab()
            self.save()
        except BaseException as e:
            print(e)
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

        sessions_list = [conversation.to_dict() for conversation in
                         self.conversations.values() if check(conversation)]

        return json.dumps(sessions_list, indent=4)

    def menu(self) -> None:
        cmds = []
        cmds.append(("Load", lambda: self.load_state()))
        cmds.append(("Save", lambda: self.save_state()))
        Dialog.show_commands("Session Menu", commands=cmds)


session = Session()
