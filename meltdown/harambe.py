from __future__ import annotations

# Standard
import threading
from http import HTTPStatus
from typing import Callable

# Libraries
import requests  # type: ignore

# Modules
from .args import args


Action = Callable[[str, str, str], None]


class Harambe:
    def __init__(
        self,
        text: str,
        username: str,
        password: str,
        tab_id: str,
        after_upload: Action,
        format_: str = "text",
        public: bool = False,
    ) -> None:
        self.text = text
        self.username = username
        self.password = password
        self.tab_id = tab_id
        self.after_upload = after_upload
        self.public = public
        self.timeout = 10

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Referer": args.harambe_site,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

        thread = threading.Thread(target=lambda: self.post(format_))
        thread.daemon = True
        thread.start()

    def post(self, format_: str) -> None:
        self.session = requests.session()
        self.session.get(args.harambe_site)
        content = self.text.strip() if len(self.text) > 0 else "."
        url = f"{args.harambe_site}/{args.harambe_endpoint}".strip()
        ext = "txt"

        if format_ == "markdown":
            ext = "md"
        elif format_ == "json":
            ext = "json"

        files = {
            "title": (None, "Meltdown Upload"),
            "pastebin": (None, content),
            "pastebin_filename": (None, f"harambe.{ext}"),
            "username": (None, args.harambe_username),
            "password": (None, args.harambe_password),
            "privacy": (None, "public" if self.public else "private"),
        }

        res = self.session.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            allow_redirects=False,
            files=files,
        )

        if res.status_code != HTTPStatus.OK:
            return

        response = res.content.decode("utf-8", errors="ignore")
        full_url = f"{args.harambe_site}/post/{response}".strip()
        self.after_upload(full_url, "", self.tab_id)
