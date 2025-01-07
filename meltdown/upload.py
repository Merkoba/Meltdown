from __future__ import annotations

# Libraries
import rentrylib  # type: ignore

# Modules
from .utils import utils


class Upload:
    def __init__(self) -> None:
        self.service = "https://rentry.org"

    def upload(self, tab_id: str | None = None) -> None:
        from .dialogs import Dialog
        from .app import app

        def action() -> None:
            Dialog.hide_all()
            app.update()
            self.do_upload(tab_id)

        Dialog.show_confirm(f"Upload conversation to\n{self.service}", lambda: action())

    def do_upload(self, tab_id: str | None = None) -> str:
        from .args import args
        from .display import display
        from .dialogs import Dialog
        from .formats import get_markdown

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        text = get_markdown(tabconvo.convo)

        if args.upload_password:
            password = args.upload_password
        else:
            password = utils.random_word()

        page = rentrylib.RentryPage(
            text=text,
            edit_code=password,
        )

        url = f"{self.service}/{page.site}"
        display.print(f"Uploaded: {url} ({page.code})", do_format=True)
        Dialog.show_message(url)


upload = Upload()
