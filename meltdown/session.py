# Modules
from .config import config
from .widgets import widgets

# Standard
import json
from typing import List, Dict, Any
from tkinter import filedialog
from pathlib import Path


class Document:
    def __init__(self, _id: str, name: str) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []

    def add(self, context_dict: Dict[str, str]) -> None:
        self.items.append(context_dict)
        self.limit()
        session.save()

    def limit(self) -> None:
        if config.context:
            self.items = self.items[-config.context:]
        else:
            self.clear()

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

    def add(self, tab_id: str) -> Document:
        tab = widgets.display.get_tab(tab_id)
        name = widgets.display.get_tab_name(tab_id)
        session = Document(tab.document_id, name)
        self.items[tab.document_id] = session
        return session

    def remove(self, document_id: str) -> None:
        if document_id in self.items:
            del self.items[document_id]
            self.save()

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

        self.load_items(path)

    def load_items(self, path: Path) -> None:
        with open(path, "r") as file:
            try:
                items = json.load(file)
            except BaseException:
                items = []

        for item in items:
            try:
                session = Document(item["id"], item["name"])
                session.items = item["items"]
                self.items[session.id] = session
                widgets.display.make_tab(session.name, session.id)
                session.print()
            except BaseException:
                pass

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

        widgets.display.close_all_tabs(True)
        self.load_items(path)

    def to_json(self) -> str:
        sessions_list = [document.to_dict() for document in session.items.values()]
        return json.dumps(sessions_list, indent=4)


session = Session()
