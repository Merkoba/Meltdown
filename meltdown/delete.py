# Standard
from typing import Optional

# Modules
from .args import args
from .utils import utils
from .dialogs import Dialog


def delete_items(
    tab_id: Optional[str] = None,
    start: bool = False,
    number: Optional[str] = None,
    keep: Optional[str] = None,
    mode: str = "normal",
    force: bool = False,
) -> None:
    from .display import display
    from .session import session

    tab, convo, tab_id = display.get_tab_convo(tab_id)

    if (not tab) or (not convo):
        return

    if not convo.items:
        return

    if convo.id == "ignore":
        return

    if (keep is not None) or (mode == "above") or (mode == "below"):
        if len(convo.items) <= 1:
            return

    def check_index(index: int) -> bool:
        if (not convo) or (not convo.items):
            return False

        if index < 0:
            return False

        if index >= len(convo.items):
            return False

        return True

    def action() -> None:
        if not tab_id:
            return

        if not tab:
            return

        if (not convo) or (not convo.items):
            return

        if number is not None:
            index = utils.get_index(number, convo.items)

            if not check_index(index):
                return

            if mode == "normal":
                convo.items.pop(index)
            elif mode == "above":
                convo.items = convo.items[index:]
            elif mode == "below":
                convo.items = convo.items[: index + 1]
        elif keep is not None:
            index = utils.get_index(keep, convo.items)

            if not check_index(index):
                return

            convo.items = [convo.items[index]]
        elif start:
            convo.items.pop(0)
        else:
            convo.items.pop()

        session.save()
        display.reset_tab(tab)

        if convo.items:
            convo.print()

    if not args.confirm_delete:
        force = True

    if force:
        action()
        return

    Dialog.show_confirm("Delete item(s)?", lambda: action())
