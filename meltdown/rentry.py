from __future__ import annotations

# Standard
import threading
import urllib.parse
from pathlib import Path
from http import HTTPStatus
from typing import Callable

# Libraries
import requests  # type: ignore

# Modules
from .args import args


Action = Callable[[str, str, str], None]


class Rentry:
    def __init__(
        self,
        text: str,
        password: str,
        tab_id: str,
        after_upload: Action,
    ) -> None:
        self.text = text
        self.password = password
        self.tab_id = tab_id
        self.after_upload = after_upload
        self.timeout = 10

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Referer": args.rentry_site,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

        thread = threading.Thread(target=lambda: self.post())
        thread.daemon = True
        thread.start()

    def get_cookie(self, cookie_name: str) -> str:
        return str(self.session.cookies.get(cookie_name, default=""))

    def get_token(self) -> str:
        return self.get_cookie("csrftoken")

    def post(self) -> None:
        self.session = requests.session()
        self.session.get(args.rentry_site)

        res = self.session.post(
            args.rentry_site,
            headers=self.headers,
            timeout=self.timeout,
            data={
                "csrfmiddlewaretoken": self.get_token(),
                "text": (self.text if len(self.text) > 0 else "."),
                "edit_code": self.password,
            },
            allow_redirects=False,
        )

        if res.status_code != HTTPStatus.FOUND:
            return

        url = urllib.parse.urlparse(res.headers["Location"])
        url = Path(url.path).name
        full_url = f"{args.rentry_site}/{url}"
        self.after_upload(full_url, self.password, self.tab_id)
