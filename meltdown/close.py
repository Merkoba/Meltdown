# Standard
from typing import List, TYPE_CHECKING, Optional

# Modules
from .args import args
from .display import display
from .dialogs import Dialog
from .utils import utils


if TYPE_CHECKING:
    from .display import Tab


def close_tab(
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

    n = display.num_tabs()
    Dialog.show_confirm(f"Close all tabs ({n}) ?", lambda: action())


def get_old_tabs() -> List["Tab"]:
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


def close_old_tabs(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    tabs = get_old_tabs()

    if not tabs:
        return

    def action() -> None:
        for tab in tabs:
            close_tab(tab_id=tab.tab_id, force=True, make_empty=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tabs)
    Dialog.show_confirm(f"Close old tabs ({n}) ?", lambda: action())


def close_other_tabs(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    current = display.current_tab
    tab_ids = [tab_id for tab_id in ids if tab_id != current]

    def action() -> None:
        for tab_id in tab_ids:
            close_tab(tab_id, force=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tab_ids)
    Dialog.show_confirm(f"Close other tabs ({n}) ?", lambda: action())


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

    n = len(tabs)
    Dialog.show_confirm(f"Close tabs to the left ({n}) ?", lambda: action())


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

    n = len(tabs)
    Dialog.show_confirm(f"Close tabs to the right ({n}) ?", lambda: action())


def get_empty_tabs() -> List["Tab"]:
    ids = display.tab_ids()
    empty_tabs = []

    for tab_id in ids:
        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            continue

        if not tabconvo.convo.items:
            empty_tabs.append(tabconvo.tab)

    return empty_tabs


def close_empty_tabs(force: bool = False) -> None:
    ids = display.tab_ids()

    if len(ids) <= 1:
        return

    tabs = get_empty_tabs()

    if not tabs:
        return

    def action() -> None:
        for tab in tabs:
            close_tab(tab_id=tab.tab_id, force=True, make_empty=True)

    if force or (not args.confirm_close):
        action()
        return

    n = len(tabs)
    Dialog.show_confirm(f"Close empty tabs ({n}) ?", lambda: action())
