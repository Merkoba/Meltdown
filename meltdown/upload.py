from __future__ import annotations

# Modules
from .app import app
from .utils import utils
from .display import display
from .harambe import Harambe
from .rentry import Rentry
from .dialogs import Dialog, Commands
from .args import args
from .formats import formats


class Upload:
    service: str = "harambe"
    full: bool = False

    def service_picker(
        self,
        tab_id: str | None = None,
        mode: str = "",
        full: bool = False,
        service: str = "",
    ) -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        self.full = full
        self.service = service

        def action(srv: str) -> None:
            self.service = srv
            self.upload_picker(tab_id=tab_id, mode=mode)


        if self.service:
            action(self.service)
            return

        if not self.full:
            if args.upload_service == "harambe":
                action("harambe")
                return

            if args.upload_service == "rentry":
                action("rentry")
                return

        cmds = Commands()
        cmds.add("Harambe", lambda a: action("harambe"))
        cmds.add("Rentry", lambda a: action("rentry"))
        Dialog.show_dialog("Pick upload service", commands=cmds)

    def privacy_picker(
        self, tab_id: str | None = None, mode: str = "", format_: str = "text"
    ) -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        def action(priv: bool) -> None:
            self.do_upload(tab_id=tab_id, mode=mode, format_=format_, public=priv)

        if not self.full:
            if args.upload_privacy == "public":
                action(True)
                return

            if args.upload_privacy == "private":
                action(False)
                return

        cmds = Commands()
        cmds.add("Public", lambda a: action(True))
        cmds.add("Private", lambda a: action(False))
        Dialog.show_dialog("Pick privacy", commands=cmds)

    def upload_picker(self, tab_id: str | None = None, mode: str = "") -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        def action(fmt: str) -> None:
            self.upload(tab_id=tab_id, mode=mode, format_=fmt)

        if not self.full:
            if args.upload_format == "text":
                action("text")
                return

            if args.upload_format == "json":
                action("json")
                return

            if args.upload_format == "markdown":
                action("markdown")
                return

        cmds = Commands()
        cmds.add("Text", lambda a: action("text"))
        cmds.add("JSON", lambda a: action("json"))
        cmds.add("Markdown", lambda a: action("markdown"))
        Dialog.show_dialog("Pick upload format", commands=cmds)

    def upload(
        self, tab_id: str | None = None, mode: str = "", format_: str = "markdown"
    ) -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        def procedure() -> None:
            if self.service == "harambe":
                self.privacy_picker(tab_id, mode, format_)
            else:
                self.do_upload(tab_id, mode, format_=format_)

        if mode in ["last", "all"]:
            procedure()
            return

        def action(mode: str) -> None:
            Dialog.hide_all()
            procedure()

        cmds = Commands()
        cmds.add("Last Item", lambda a: action("last"))
        cmds.add("All Of It", lambda a: action("all"))
        fmt = formats.get_name(format_, True)
        text = "Upload conversation to\n"

        if self.service == "harambe":
            text += args.harambe_site
        elif self.service == "rentry":
            text += args.rentry_site
        else:
            return

        text += f"\nFormat: {fmt}"

        Dialog.show_dialog(
            text,
            commands=cmds,
        )

    def after_upload(self, url: str, password: str, tab_id: str) -> None:
        if password:
            m = f"{url}({password})"
        else:
            m = url

        display.print(
            f"🌐 Uploaded: {m}",
            do_format=True,
            tab_id=tab_id,
        )

        def open_url() -> None:
            app.open_url(url)

        def copy_url() -> None:
            utils.copy(url)

        def copy_all() -> None:
            utils.copy(f"{url} ({password})")

        cmds = Commands()
        cmds.add("Open", lambda a: open_url())

        if password:
            cmds.add("Copy All", lambda a: copy_all())

        cmds.add("Copy URL", lambda a: copy_url())

        if password:
            msg = f"Uploaded ({password})"
        else:
            msg = "Uploaded"

        Dialog.show_dialog(msg, commands=cmds)

    def do_upload(
        self,
        tab_id: str | None = None,
        mode: str = "all",
        format_: str = "markdown",
        public: bool = False,
    ) -> None:
        if not tab_id:
            tab_id = display.current_tab

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        if format_ == "markdown":
            text = formats.get_markdown(tabconvo.convo, mode=mode, name_mode="upload")
        elif format_ == "json":
            text = formats.get_json(tabconvo.convo, mode=mode, name_mode="upload")
        else:
            text = formats.get_text(tabconvo.convo, mode=mode, name_mode="upload")

        if self.service == "harambe":
            try:
                Harambe(
                    text=text,
                    tab_id=tab_id,
                    username=args.harambe_username,
                    password=args.harambe_password,
                    after_upload=self.after_upload,
                    public=public,
                    format_=format_,
                )
            except Exception as e:
                utils.error(e)
        elif self.service == "rentry":
            if args.upload_password:
                password = args.upload_password
            else:
                password = utils.random_word()

            try:
                Rentry(
                    text=text,
                    tab_id=tab_id,
                    password=password,
                    after_upload=self.after_upload,
                )
            except Exception as e:
                utils.error(e)


upload = Upload()
