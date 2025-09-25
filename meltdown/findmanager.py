from __future__ import annotations

# Standard
import re
import tkinter as tk

# Modules
from .app import app
from .dialogs import Dialog


class FindManager:
    def toggle(self) -> None:
        from .display import display

        tab = display.get_current_tab()

        if not tab:
            return

        tab.get_find().toggle()

    def find(
        self,
        tab_id: str | None = None,
        widget: tk.Text | None = None,
        query: str | None = None,
    ) -> None:
        from .display import display

        if not tab_id:
            tab_id = display.current_tab

        tab = display.get_tab(tab_id)

        if not tab:
            return

        tab.get_find().show(widget=widget, query=query)

    def find_next(self, case_insensitive: bool = True, reverse: bool = False) -> None:
        from .display import display

        tab = display.get_current_tab()

        if not tab:
            return

        if not tab.get_find().visible:
            tab.get_find().show()
            return

        tab.get_find().find_next(case_insensitive, reverse=reverse)

    def find_prev(self, case_insensitive: bool = True) -> None:
        from .display import display

        tab = display.get_current_tab()

        if not tab:
            return

        if not tab.get_find().visible:
            tab.get_find().show()
            return

        tab.get_find().find_next(case_insensitive, reverse=True)

    def hide_find(self) -> None:
        from .display import display

        tab = display.get_current_tab()

        if not tab:
            return

        tab.get_find().hide()

    def find_all(self, query: str | None = None, reverse: bool = False) -> None:
        if query:
            self.find_all_text(query, reverse=reverse)
        else:
            Dialog.show_input("Find text in all tabs", lambda s: self.find_all_text(s))

    def find_all_text(self, query: str, reverse: bool = False) -> None:
        from .session import session
        from .display import Tab, display

        if not query:
            return

        query_lower = query.lower()
        is_regex = query.startswith("/") and query.endswith("/")

        if is_regex:
            regex_query = query[1:-1]
        else:
            regex_query = ""

        def find(value: str) -> bool:
            if is_regex and re.search(regex_query, value, re.IGNORECASE):
                return True

            return query_lower in value.lower()

        def check_tab(tab: Tab) -> bool:
            conversation = session.get_conversation(tab.conversation_id)

            if not conversation:
                return False

            if conversation.id.startswith("ignore"):
                return False

            for item in conversation.items:
                for key in ["user", "ai", "file"]:
                    value = getattr(item, key)

                    if find(value):
                        if not tab.loaded:
                            display.load_tab(tab.tab_id)
                            app.update()

                        display.select_tab(tab.tab_id)
                        tab.get_find().show(query=query)
                        return True

            return False

        tabs = []
        index = -1
        ids = display.book.ids()

        if reverse:
            ids = list(reversed(ids))

        for id_ in ids:
            tab = display.get_tab(id_)

            if tab:
                tabs.append(tab)

                if tab.tab_id == display.current_tab:
                    index = len(tabs) - 1

        if index >= 0:
            tabs = tabs[index + 1 :] + tabs[: index + 1]

        for tab in tabs:
            if check_tab(tab):
                return


findmanager = FindManager()
