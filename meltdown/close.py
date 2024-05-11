# Standard
from typing import List, TYPE_CHECKING

# Modules
from .args import args
from .display import display
from .dialogs import Dialog
from .utils import utils


if TYPE_CHECKING:
    from .display import Tab


def close_tab(
    tab_id: str = "",
    force: bool = False,
    make_empty: bool = True,
    force_empty: bool = False,
    full: bool = True,
) -> None:
    if display.num_tabs() <= 1:
        return

    if not tab_id:
        tab_id = display.book.current()

    if not tab_id:
        return

    tab = display.get_tab(tab_id)

    if not tab:
        return

    if force_empty:
        if tab.mode == "ignore":
            force = True

        if display.tab_is_empty(tab_id):
            force = True

    def action() -> None:
        display.book.close(tab_id)
        display.update_current_tab()
        display.remove_tab(tab_id)

        if display.num_tabs() == 0:
            if make_empty:
                display.make_tab()

    if force:
        action()
        return

    cmds = []

    if full and get_old_tabs():
        cmds.append(("Old", lambda: close_old_tabs()))

    cmds.append(("Others", lambda: close_other_tabs()))
    cmds.append(("Left", lambda: close_tabs_left()))
    cmds.append(("Right", lambda: close_tabs_right()))

    if full:
        cmds.append(("All", lambda: close_all_tabs()))

    cmds.append(("Ok", lambda: action()))
    Dialog.show_commands("Close tab?", cmds)


def close_all_tabs(force: bool = False, make_empty: bool = True) -> None:
    def action() -> None:
        for tab_id in display.tab_ids():
            close_tab(tab_id=tab_id, force=True, make_empty=make_empty)

    if force or (not args.confirm_close):
        action()
        return

    Dialog.show_confirm("Close all tabs?", lambda: action())


def get_old_tabs() -> List["Tab"]:
    from .session import session

    ids = display.tab_ids()
    old_tabs = []

    max_minutes = args.old_tabs_minutes
    max_date = utils.now() - (60 * max_minutes)

    for tab_id in ids:
        tab = display.get_tab(tab_id)

        if not tab:
            continue

        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            continue

        if conversation.last_modified < max_date:
            old_tabs.append(tab)

    return old_tabs


def close_old_tabs(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    def action() -> None:
        for tab in get_old_tabs():
            close_tab(tab_id=tab.tab_id, force=True, make_empty=True)

    if force or (not args.confirm_close):
        action()
        return

    Dialog.show_confirm("Close old tabs?", lambda: action())


def close_other_tabs(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    current = display.current_tab

    def action() -> None:
        for tab_id in ids:
            if tab_id != current:
                close_tab(tab_id=tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    Dialog.show_confirm("Close other tabs?", lambda: action())


def close_tabs_left(force: bool = False) -> None:
    tab_ids = display.tab_ids()

    if len(tab_ids) <= 1:
        return

    index = display.index(display.current_tab)
    tabs = tab_ids[:index]

    def action() -> None:
        for tab_id in tabs:
            close_tab(tab_id=tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    Dialog.show_confirm("Close tabs to the left?", lambda: action())


def close_tabs_right(force: bool = False) -> None:
    tab_ids = display.tab_ids()

    if len(tab_ids) <= 1:
        return

    index = display.index(display.current_tab)
    tabs = tab_ids[index + 1 :]

    def action() -> None:
        for tab_id in tabs:
            close_tab(tab_id=tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    Dialog.show_confirm("Close tabs to the right?", lambda: action())
