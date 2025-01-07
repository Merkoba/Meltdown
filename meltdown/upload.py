from __future__ import annotations

# Modules
from .utils import utils
from .config import config
from .rentry import RentryPage


class Upload:
    def upload(self, tab_id: str | None = None, mode: str = "") -> None:
        from .dialogs import Dialog
        from .app import app

        if mode in ["last", "all"]:
            self.do_upload(tab_id, mode)
            return

        def action(mode: str) -> None:
            Dialog.hide_all()
            app.update()
            self.do_upload(tab_id, mode)

        cmds = []
        cmds.append(("Last Item", lambda a: action("last")))
        cmds.append(("All Of It", lambda a: action("all")))

        Dialog.show_dialog(
            f"Upload conversation to\n{config.rentry_site}", commands=cmds
        )

    def do_upload(self, tab_id: str | None = None, mode: str = "all") -> str:
        from .args import args
        from .display import display
        from .dialogs import Dialog
        from .formats import get_markdown

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = get_markdown(tabconvo.convo, mode=mode)

        if args.upload_password:
            password = args.upload_password
        else:
            password = utils.random_word()

        try:
            page = RentryPage(text=text, edit_code=password)
        except Exception as e:
            utils.error(e)

        url = f"{config.rentry_site}/{page.site}"
        display.print(f"Uploaded: {url} ({page.code})", do_format=True)
        Dialog.show_message(url)


upload = Upload()
