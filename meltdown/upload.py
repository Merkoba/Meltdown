from __future__ import annotations

# Modules
from .utils import utils
from .config import config
from .display import display
from .rentry import Rentry


class Upload:
    def upload(self, tab_id: str | None = None, mode: str = "") -> None:
        from .dialogs import Dialog
        from .app import app

        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        if mode in ["last", "all"]:
            self.do_upload(tab_id, mode)
            return

        def action(mode: str) -> None:
            Dialog.hide_all()
            app.update()
            self.do_upload(tab_id, mode)

        cmds = []
        cmds.append(Dialog.cmd("Last Item", lambda a: action("last")))
        cmds.append(Dialog.cmd("All Of It", lambda a: action("all")))

        Dialog.show_dialog(
            f"Upload conversation to\n{config.rentry_site}", commands=cmds
        )

    def do_upload(self, tab_id: str | None = None, mode: str = "all") -> None:
        from .args import args
        from .display import display
        from .formats import get_markdown

        if not tab_id:
            tab_id = display.current_tab

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        text = get_markdown(tabconvo.convo, mode=mode)

        if args.upload_password:
            password = args.upload_password
        else:
            password = utils.random_word()

        try:
            Rentry(text=text, password=password, tab_id=tab_id)
        except Exception as e:
            utils.error(e)


upload = Upload()
