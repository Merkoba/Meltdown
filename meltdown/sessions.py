# Modules
from .config import config
from .widgets import widgets

# Standard
import json
from typing import List, Dict, Any


class Session:
    def __init__(self, _id: str, name: str) -> None:
        self.id = _id
        self.name = name
        self.items: List[Dict[str, str]] = []

    def add(self, context_dict: Dict[str, str]) -> None:
        self.items.append(context_dict)
        self.limit()
        sessions.save()

    def limit(self) -> None:
        if config.context:
            self.items = self.items[-config.context:]
        else:
            self.clear()

    def clear(self) -> None:
        self.items = []
        sessions.save()

    def print(self) -> None:
        tab = widgets.display.get_tab_by_session_id(self.id)

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


class Sessions:
    def __init__(self) -> None:
        self.items: Dict[str, Session] = {}

    def add(self, tab_id: str) -> Session:
        tab = widgets.display.get_tab(tab_id)
        name = widgets.display.get_tab_name(tab_id)
        session = Session(tab.session_id, name)
        self.items[tab.session_id] = session
        return session

    def remove(self, session_id: str) -> None:
        if session_id in self.items:
            del self.items[session_id]
            self.save()

    def change_name(self, session_id: str, name: str) -> None:
        if session_id in self.items:
            self.items[session_id].name = name
            self.save()

    def clear(self, session_id: str) -> None:
        if session_id in self.items:
            self.items[session_id].clear()
            self.save()

    def save(self) -> None:
        if not config.sessions_path.exists():
            config.sessions_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config.sessions_path, "w") as file:
            file.write(self.to_json())

    def load(self) -> None:
        path = config.sessions_path

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        with open(path, "r") as file:
            try:
                items = json.load(file)
            except BaseException:
                items = []

        try:
            if items:
                for item in items:
                    session = Session(item["id"], item["name"])
                    session.items = item["items"]
                    self.items[session.id] = session
                    widgets.display.make_tab(session.name, session.id)
                    session.print()
        except BaseException:
            pass

    def to_json(self) -> str:
        sessions_list = [session.to_dict() for session in sessions.items.values()]
        return json.dumps(sessions_list, indent=4)


sessions = Sessions()
