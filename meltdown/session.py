# Modules
from .config import config
from .display import display
from .paths import paths
from .args import args
from . import timeutils
from .output import Output

# Standard
import json
from typing import List, Dict, Any, Optional
from tkinter import filedialog
from pathlib import Path


test_session = {
    "id": "test123",
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
        {"assistant": "_This is an italic sentence_\n_This is an italic sentence_"},
        {"user": "Snippet Test"},
        {"assistant":
            "```python\na = 123\nprint('Hello, World!')\n```\n\n" +
            "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
         },
        {"user": "Snippet Test 2"},
        {"assistant":
            "Here is some code:\n\n```\na = 123\nprint('Hello, World!')\n```\n\n" +
            "Here is more code:\n\n```\nlet a = 123\nconsole.log('Hello, World!')\n```"
         },
        {"user": "URL Test"},
        {"assistant": "Here are some urls https://aa.com and http://cc.com and ftp://44.com\n" +
         "Here are some urls https://aa.com and http://cc.com\nftp://44.com"},
        {"user": "Normal Sentence"},
        {"assistant": "Here is a normal sentence"},
    ],
}


class Document:
    def __init__(self, _id: str, name: str) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []
        self.loaded = False
        self.last_modified = 0.0

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
        tab = display.get_tab_by_document_id(self.id)

        if tab:
            for item in self.items:
                for key in item:
                    if key == "user":
                        display.prompt("user", item[key], tab_id=tab.tab_id)
                    elif key == "assistant":
                        display.prompt("ai", item[key], tab_id=tab.tab_id)
                    else:
                        continue

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
        self.items: Dict[str, Document] = {}

    def add(self, name: str) -> Document:
        doc_id = str(timeutils.now())
        document = Document(doc_id, name)
        document.loaded = True
        self.items[doc_id] = document
        return document

    def remove(self, document_id: str) -> None:
        if document_id in self.items:
            del self.items[document_id]
            self.save()

    def get_document(self, document_id: str) -> Optional[Document]:
        return self.items[document_id]

    def get_current_document(self) -> Optional[Document]:
        tab = display.get_current_tab()

        if tab:
            return self.get_document(tab.document_id)
        else:
            return None

    def change_name(self, document_id: str, name: str) -> None:
        if document_id in self.items:
            self.items[document_id].name = name
            self.save()

    def clear(self, document_id: str) -> None:
        if document_id in self.items:
            self.items[document_id].clear()
            self.save()

    def save(self) -> None:
        if not paths.session.exists():
            paths.session.parent.mkdir(parents=True, exist_ok=True)

        with open(paths.session, "w") as file:
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

            with open(path, "r") as file:
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
        self.items = {}
        display.close_all_tabs(force=True)

    def load_items(self, path: Path) -> None:
        display.close_all_tabs(force=True, make_empty=False)

        with open(path, "r") as file:
            try:
                items = json.load(file)
            except BaseException as e:
                items = []

        if args.test:
            items.append(test_session)

        if not items:
            return

        for item in items:
            document = Document(item["id"], item["name"])
            document.items = item["items"]
            self.items[document.id] = document
            display.make_tab(document.name, document.id, select_tab=False)

        tab_ids = display.tab_ids()

        if tab_ids:
            display.select_tab(tab_ids[-1])

    def save_state(self) -> None:
        if not paths.sessions.exists():
            paths.sessions.mkdir(parents=True, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            initialdir=paths.sessions,
            defaultextension=".json",
            filetypes=[("Session Files", "*.json")],
        )

        if not file_path:
            return

        with open(file_path, "w") as file:
            file.write(self.to_json())

    def load_state(self) -> None:
        if not paths.sessions.exists():
            paths.sessions.mkdir(parents=True, exist_ok=True)

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

            document = self.get_document(tab.document_id)

            if not document:
                continue

            new_items[document.id] = document

        self.items = new_items
        self.save()

    def to_json(self) -> str:
        sessions_list = [document.to_dict() for document in
                         self.items.values() if document.items and (document.id != "test123")]
        return json.dumps(sessions_list, indent=4)


session = Session()
