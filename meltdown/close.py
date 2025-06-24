from __future__ import annotations

# Standard
from typing import TYPE_CHECKING

# Modules
from .args import args
from .display import display
from .dialogs import Dialog, Commands
from .utils import utils


if TYPE_CHECKING:
    from .display import Tab


class Close:
    def get_old_tabs(self) -> list[Tab]:
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

    def get_oldest_tab(self) -> Tab | None:
        ids = display.tab_ids()
        oldest_tab = None
        oldest_date = utils.now()

        for tab_id in ids:
            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                continue

            if tabconvo.convo.last_modified < oldest_date:
                oldest_tab = tabconvo.tab
                oldest_date = tabconvo.convo.last_modified

        return oldest_tab

    def get_empty_tabs(self) -> list[Tab]:
        ids = display.tab_ids()
        empty_tabs = []

        for tab_id in ids:
            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                continue

            if not tabconvo.convo.items:
                empty_tabs.append(tabconvo.tab)

        return empty_tabs

    def get_half_tabs(self) -> list[Tab]:
        ids = display.tab_ids()
        half_tabs: list[Tab] = []
        num_tabs = len(ids)

        if num_tabs <= 1:
            return half_tabs

        half_index = num_tabs // 2

        for i, tab_id in enumerate(ids):
            if i >= half_index:
                continue

            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                continue

            half_tabs.append(tabconvo.tab)

        return half_tabs

    def get_left_tabs(self, tab_id: str) -> list[str]:
        tab_ids = display.tab_ids()
        index = display.index(tab_id)
        return tab_ids[:index]

    def get_right_tabs(self, tab_id: str) -> list[str]:
        tab_ids = display.tab_ids()
        index = display.index(tab_id)
        return tab_ids[index + 1 :]

    def get_other_tabs(self, tab_id: str) -> list[str]:
        ids = display.tab_ids()
        return [tid for tid in ids if tid != tab_id]

    def get_pin_tabs(self) -> list[str]:
        return [tab.tab_id for tab in display.get_pins()]

    def get_normal_tabs(self) -> list[str]:
        return [tab.tab_id for tab in display.get_normal()]

    def close(
        self,
        tab_id: str | None = None,
        force: bool = False,
        make_empty: bool = True,
        force_empty: bool = False,
        full: bool = True,
    ) -> None:
        from .keyboard import keyboard

        num_tabs = display.num_tabs()

        if num_tabs == 0:
            return

        if not tab_id:
            tab_id = display.book.current()
            single = False
        else:
            single = True

        if not tab_id:
            return

        if not force:
            picked = display.get_picked()

            if picked:
                self.close_picked()
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

        empty_tabs = self.get_empty_tabs()
        old_tabs = self.get_old_tabs()

        if keyboard.shift:
            if empty_tabs:
                self.close_empty()

            return

        if keyboard.ctrl:
            if old_tabs:
                self.close_old()

            return

        cmds = Commands()

        if full and empty_tabs:
            cmds.add("Empty", lambda a: self.close_empty())

        if full and old_tabs:
            cmds.add("Old", lambda a: self.close_old())

        if full and (num_tabs > 1):
            cmds.add("Half", lambda a: self.close_half())

        if full and self.get_pin_tabs():
            cmds.add("Normal", lambda a: self.close_normal())

        if self.get_other_tabs(tab_id):
            cmds.add("Others", lambda a: self.close_others(tab_id=tab_id))

        if self.get_left_tabs(tab_id):
            cmds.add("Left", lambda a: self.close_left(tab_id=tab_id))

        if self.get_right_tabs(tab_id):
            cmds.add("Right", lambda a: self.close_right(tab_id=tab_id))

        if full:
            cmds.add("All", lambda a: self.close_all())

        if not cmds:
            return

        cmds.add("Ok" if single else "One", lambda a: action())
        msg = "Close tab ?" if single else "Close tabs ?"
        Dialog.show_dialog(msg, cmds)

    def close_all(self, force: bool = False, make_empty: bool = True) -> None:
        def action() -> None:
            for tab_id in display.tab_ids():
                self.close(tab_id=tab_id, force=True, make_empty=make_empty)

        if force or (not args.confirm_close):
            action()
            return

        n = display.num_tabs()
        Dialog.show_confirm(f"Close all tabs ({n}) ?", lambda: action())

    def close_old(self, force: bool = False) -> None:
        ids = display.tab_ids()

        if len(ids) <= 1:
            return

        tabs = self.get_old_tabs()

        if not tabs:
            return

        def action() -> None:
            for tab in tabs:
                self.close(tab_id=tab.tab_id, force=True, make_empty=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tabs)
        Dialog.show_confirm(f"Close old tabs ({n}) ?", lambda: action())

    def close_others(self, force: bool = False, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tab_ids = self.get_other_tabs(tab_id)

        def action() -> None:
            for tab_id in tab_ids:
                self.close(tab_id, force=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tab_ids)
        Dialog.show_confirm(f"Close other tabs ({n}) ?", lambda: action())

    def close_pins(self, force: bool = False, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tab_ids = self.get_pin_tabs()

        if not tab_ids:
            return

        def action() -> None:
            for tab_id in tab_ids:
                self.close(tab_id=tab_id, force=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tab_ids)
        Dialog.show_confirm(f"Close pinned tabs ({n}) ?", lambda: action())

    def close_normal(self, force: bool = False, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tab_ids = self.get_normal_tabs()

        if not tab_ids:
            return

        def action() -> None:
            for tab_id in tab_ids:
                self.close(tab_id=tab_id, force=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tab_ids)
        Dialog.show_confirm(f"Close normal tabs ({n}) ?", lambda: action())

    def close_left(self, force: bool = False, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tab_ids = self.get_left_tabs(tab_id)

        if not tab_ids:
            return

        def action() -> None:
            for tab_id in tab_ids:
                self.close(tab_id=tab_id, force=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tab_ids)
        Dialog.show_confirm(f"Close tabs to the left ({n}) ?", lambda: action())

    def close_right(self, force: bool = False, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tab_ids = self.get_right_tabs(tab_id)

        if not tab_ids:
            return

        def action() -> None:
            for tab_id in tab_ids:
                self.close(tab_id=tab_id, force=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tab_ids)
        Dialog.show_confirm(f"Close tabs to the right ({n}) ?", lambda: action())

    def close_empty(self, force: bool = False) -> None:
        ids = display.tab_ids()

        if len(ids) <= 1:
            return

        tabs = self.get_empty_tabs()

        if not tabs:
            return

        def action() -> None:
            for tab in tabs:
                self.close(tab_id=tab.tab_id, force=True, make_empty=True)

        if force or (not args.confirm_close):
            action()
            return

        n = len(tabs)
        Dialog.show_confirm(f"Close empty tabs ({n}) ?", lambda: action())

    def close_picked(self, force: bool = False) -> None:
        tabs = display.get_picked()

        if not tabs:
            return

        def action() -> None:
            for tab in tabs:
                self.close(tab_id=tab.tab_id, force=True, make_empty=True)

            display.unpick()

        if force or (not args.confirm_close):
            action()
            return

        n = len(tabs)
        Dialog.show_confirm(f"Close picked tabs ({n}) ?", lambda: action())

    def close_oldest(self, force: bool = False) -> None:
        tab = self.get_oldest_tab()

        if not tab:
            return

        def action() -> None:
            self.close(tab_id=tab.tab_id, force=True, make_empty=True)

        if force:
            action()
        else:
            Dialog.show_confirm("Close oldest tab ?", lambda: action())

    def close_half(self, force: bool = False) -> None:
        tabs = self.get_half_tabs()

        if not tabs:
            return

        def action() -> None:
            for tab in tabs:
                self.close(tab_id=tab.tab_id, force=True, make_empty=True)

        if force:
            action()
        else:
            n = len(tabs)
            Dialog.show_confirm(f"Close half of the tabs ({n}) ?", lambda: action())


close = Close()
