# Standard
from typing import Optional

# Modules
from .args import args
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

    if not tab_id:
        tab_id = display.current_tab

    tab = display.get_tab(tab_id)

    if not tab:
        return

    conversation = session.get_conversation(tab.conversation_id)

    if not conversation:
        return

    if not conversation.items:
        return

    if conversation.id == "ignore":
        return

    if (keep is not None) or (mode == "above") or (mode == "below"):
        if len(conversation.items) <= 1:
            return

    def get_index(arg: str) -> int:
        if arg == "first":
            index = 0
        elif arg == "second":
            index = 1
        elif arg == "third":
            index = 2
        elif arg == "last":
            if conversation and conversation.items:
                index = len(conversation.items) - 1
            else:
                index = -1
        else:
            try:
                index = int(arg) - 1
            except BaseException:
                index = -1

        return index

    def check_index(index: int) -> bool:
        if (not conversation) or (not conversation.items):
            return False

        if index < 0:
            return False

        if index >= len(conversation.items):
            return False

        return True

    def action() -> None:
        if not tab_id:
            return

        if not tab:
            return

        if (not conversation) or (not conversation.items):
            return

        if number is not None:
            index = get_index(number)

            if not check_index(index):
                return

            if mode == "normal":
                conversation.items.pop(index)
            elif mode == "above":
                conversation.items = conversation.items[index:]
            elif mode == "below":
                conversation.items = conversation.items[: index + 1]
        elif keep is not None:
            index = get_index(keep)

            if not check_index(index):
                return

            conversation.items = [conversation.items[index]]
        elif start:
            conversation.items.pop(0)
        else:
            conversation.items.pop()

        session.save()
        tab.output.clear_text()
        display.reset_tab(tab)
        display.show_header(tab_id)

        if conversation.items:
            conversation.print()

    if not args.confirm_delete:
        force = True

    if force:
        action()
        return

    Dialog.show_confirm("Delete item(s)?", lambda: action())
