# Standard
import re
import tkinter as tk
from typing import Optional

# Modules
from .app import app
from .dialogs import Dialog


def find(
    tab_id: Optional[str] = None,
    widget: Optional[tk.Text] = None,
    query: Optional[str] = None,
) -> None:
    from .display import display

    if not tab_id:
        tab_id = display.current_tab

    tab = display.get_tab(tab_id)

    if not tab:
        return

    tab.find.show(widget=widget, query=query)

    if query:
        tab.find.find_next()


def find_next(case_insensitive: bool = True) -> None:
    from .display import display

    tab = display.get_current_tab()

    if not tab:
        return

    if not tab.find.visible:
        tab.find.show()
        return

    tab.find.find_next(case_insensitive)


def hide_find() -> None:
    from .display import display

    tab = display.get_current_tab()

    if not tab:
        return

    tab.find.hide()


def find_all(query: Optional[str] = None) -> None:
    if query:
        find_all_text(query)
    else:
        Dialog.show_input("Find text in all tabs", lambda s: find_all_text(s))


def find_all_text(query: str) -> None:
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

        if query_lower in value.lower():
            return True

        return False

    def check_tab(tab: Tab) -> bool:
        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return False

        if conversation.id == "ignore":
            return False

        for item in conversation.items:
            for key in item:
                value = item[key]

                if find(value):
                    if not tab.loaded:
                        display.load_tab(tab.tab_id)
                        app.update()

                    display.select_tab(tab.tab_id)
                    tab.find.show(query=query)
                    return True

        return False

    tabs = []
    index = -1

    for page in display.book.pages:
        tab = display.get_tab(page.id)

        if tab:
            tabs.append(tab)

            if tab.tab_id == display.current_tab:
                index = len(tabs) - 1

    if index >= 0:
        tabs = tabs[index + 1 :] + tabs[: index + 1]

    for tab in tabs:
        if check_tab(tab):
            return
