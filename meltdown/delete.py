from __future__ import annotations

# Modules
from .args import args
from .utils import utils
from .dialogs import Dialog


class Delete:
    def delete_items(
        self,
        number: str | None = None,
        tab_id: str | None = None,
        mode: str = "normal",
        force: bool = False,
    ) -> None:
        from .display import display
        from .session import session

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        if tabconvo.convo.id.startswith("ignore"):
            return

        if (mode == "above") or (mode == "below") or (mode == "others"):
            if len(tabconvo.convo.items) <= 1:
                return

        def check_index(index: int) -> bool:
            if not tabconvo:
                return False

            if index < 0:
                return False

            return index < len(tabconvo.convo.items)

        if not number:
            number = "last"

        index = utils.get_index(number, tabconvo.convo.items)

        if not check_index(index):
            return

        def action() -> None:
            if not tabconvo:
                return

            if not tabconvo.tab.tab_id:
                return

            if mode == "normal":
                tabconvo.convo.items.pop(index)
            elif mode == "above":
                tabconvo.convo.items = tabconvo.convo.items[index:]
            elif mode == "below":
                tabconvo.convo.items = tabconvo.convo.items[: index + 1]
            elif mode == "others":
                tabconvo.convo.items = [tabconvo.convo.items[index]]

            session.save()
            display.reset_tab(tabconvo.tab)

            if tabconvo.convo.items:
                tabconvo.convo.print()

        if not args.confirm_delete:
            force = True

        if force:
            action()
            return

        if mode == "normal":
            n = 1
        elif mode == "above":
            n = index
        elif mode == "below":
            n = len(tabconvo.convo.items) - index - 1
        elif mode == "others":
            n = len(tabconvo.convo.items) - 1
        else:
            return

        Dialog.show_confirm(f"Delete items ({n}) ?", lambda: action())


delete = Delete()
