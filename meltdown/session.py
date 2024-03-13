# Modules
from .config import config
from .widgets import widgets
from . import timeutils

# Standard
import json
from typing import List, Dict, Any, Optional
from tkinter import filedialog
from pathlib import Path


class Document:
    def __init__(self, _id: str, name: str) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []
        self.loaded = False

    def add(self, context_dict: Dict[str, str]) -> None:
        self.items.append(context_dict)
        self.limit()
        session.save()

    def limit(self) -> None:
        self.items = self.items[-config.max_log:]

    def clear(self) -> None:
        self.items = []
        session.save()

    def print(self) -> None:
        tab = widgets.display.get_tab_by_document_id(self.id)

        if tab:
            for item in self.items:
                for key in item:
                    if key == "user":
                        widgets.prompt("user", tab_id=tab.tab_id)
                    elif key == "assistant":
                        widgets.prompt("ai", tab_id=tab.tab_id)
                    else:
                        continue

                    widgets.display.insert(item[key], tab_id=tab.tab_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "items": self.items
        }


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

    def change_name(self, document_id: str, name: str) -> None:
        if document_id in self.items:
            self.items[document_id].name = name
            self.save()

    def clear(self, document_id: str) -> None:
        if document_id in self.items:
            self.items[document_id].clear()
            self.save()

    def save(self) -> None:
        if not config.session_path.exists():
            config.session_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config.session_path, "w") as file:
            file.write(self.to_json())

    def load(self) -> None:
        path = config.session_path

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
        widgets.display.close_all_tabs(force=True)

    def load_items(self, path: Path) -> None:
        widgets.display.close_all_tabs(force=True, make_empty=False)

        with open(path, "r") as file:
            try:
                items = json.load(file)
            except BaseException:
                items = []

        if not items:
            return

        for item in items:
            document = Document(item["id"], item["name"])
            document.items = item["items"]
            self.items[document.id] = document
            widgets.display.make_tab(document.name, document.id, select_tab=False)

        tab_ids = widgets.display.tab_ids()

        if tab_ids:
            widgets.display.select_tab(tab_ids[-1])

    def save_state(self) -> None:
        if not config.sessions_path.exists():
            config.sessions_path.mkdir(parents=True, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            initialdir=config.sessions_path,
            defaultextension=".json",
            filetypes=[("Session Files", "*.json")],
        )

        if not file_path:
            return

        with open(file_path, "w") as file:
            file.write(self.to_json())

    def load_state(self) -> None:
        if not config.sessions_path.exists():
            config.sessions_path.mkdir(parents=True, exist_ok=True)

        file_path = filedialog.askopenfilename(
            initialdir=config.sessions_path,
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

    def to_json(self) -> str:
        sessions_list = [document.to_dict() for document in self.items.values() if document.items]
        return json.dumps(sessions_list, indent=4)


session = Session()
