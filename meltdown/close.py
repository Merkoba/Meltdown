# Standard
from typing import TYPE_CHECKING, Optional

# Modules
from .args import args
from .display import display
from .dialogs import Dialog
from .utils import utils


if TYPE_CHECKING:
    from .display import Tab


def get_old_tabs() -> list["Tab"]:
    ids = display.tab_ids()
    old_tabs = []

    max_minutes = args.old_tabs_minutes
    max_date = utils.now() - (60 * max_minutes)

    for tab_id in ids:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            continue

        if tabconvo.convo.last_modified < max_date:
            old_tabs.append(tabconvo.tab)

    return old_tabs


def get_empty_tabs() -> list["Tab"]:
    ids = display.tab_ids()
    empty_tabs = []

    for tab_id in ids:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            continue

        if not tabconvo.convo.items:
            empty_tabs.append(tabconvo.tab)

    return empty_tabs


def get_left_tabs(tab_id: str) -> list[str]:
    tab_ids = display.tab_ids()
    index = display.index(tab_id)
    return tab_ids[:index]


def get_right_tabs(tab_id: str) -> list[str]:
    tab_ids = display.tab_ids()
    index = display.index(tab_id)
    return tab_ids[index + 1 :]


def get_other_tabs(tab_id: str) -> list[str]:
    ids = display.tab_ids()
    return [tid for tid in ids if tid != tab_id]


# -----------------


def close(
    tab_id: Optional[str] = None,
    force: bool = False,
    make_empty: bool = True,
    force_empty: bool = False,
    full: bool = True,
) -> None:
    if display.num_tabs() == 0:
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

    if full and get_empty_tabs():
        cmds.append(("Empty", lambda a: close_empty()))

    if full and get_old_tabs():
        cmds.append(("Old", lambda a: close_old()))

    if get_other_tabs(tab_id):
        cmds.append(("Others", lambda a: close_other(tab_id=tab_id)))

    if get_left_tabs(tab_id):
        cmds.append(("Left", lambda a: close_left(tab_id=tab_id)))

    if get_right_tabs(tab_id):
        cmds.append(("Right", lambda a: close_right(tab_id=tab_id)))

    if full:
        cmds.append(("All", lambda a: close_all()))

    if not cmds:
        return

    cmds.append(("Ok", lambda a: action()))
    Dialog.show_dialog("Close tab?", cmds)


def close_all(force: bool = False, make_empty: bool = True) -> None:
    def action() -> None:
        for tab_id in display.tab_ids():
            close(tab_id=tab_id, force=True, make_empty=make_empty)

    if force or (not args.confirm_close):
        action()
        return

    n = display.num_tabs()
    Dialog.show_confirm(f"Close all tabs ({n}) ?", lambda: action())


def close_old(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    tabs = get_old_tabs()

    if not tabs:
        return

    def action() -> None:
        for tab in tabs:
            close(tab_id=tab.tab_id, force=True, make_empty=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tabs)
    Dialog.show_confirm(f"Close old tabs ({n}) ?", lambda: action())


def close_other(force: bool = False, tab_id: Optional[str] = None) -> None:
    if not tab_id:
        tab_id = display.current_tab

    tab_ids = get_other_tabs(tab_id)

    def action() -> None:
        for tab_id in tab_ids:
            close(tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tab_ids)
    Dialog.show_confirm(f"Close other tabs ({n}) ?", lambda: action())


def close_left(force: bool = False, tab_id: Optional[str] = None) -> None:
    if not tab_id:
        tab_id = display.current_tab

    tab_ids = get_left_tabs(tab_id)

    if not tab_ids:
        return

    def action() -> None:
        for tab_id in tab_ids:
            close(tab_id=tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tab_ids)
    Dialog.show_confirm(f"Close tabs to the left ({n}) ?", lambda: action())


def close_right(force: bool = False, tab_id: Optional[str] = None) -> None:
    if not tab_id:
        tab_id = display.current_tab

    tab_ids = get_right_tabs(tab_id)

    if not tab_ids:
        return

    def action() -> None:
        for tab_id in tab_ids:
            close(tab_id=tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tab_ids)
    Dialog.show_confirm(f"Close tabs to the right ({n}) ?", lambda: action())


def close_empty(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    tabs = get_empty_tabs()

    if not tabs:
        return

    def action() -> None:
        for tab in tabs:
            close(tab_id=tab.tab_id, force=True, make_empty=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tabs)
    Dialog.show_confirm(f"Close empty tabs ({n}) ?", lambda: action())
