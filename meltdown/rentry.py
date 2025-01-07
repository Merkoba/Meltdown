# Standard
import ast
import threading
import urllib.parse
from pathlib import Path
from http import HTTPStatus

# Libraries
import requests  # type: ignore

# Modules
from .config import config
from .display import display
from .dialogs import Dialog


class Rentry:
    def __init__(self, text: str = "", password: str = "", tab_id: str = "") -> None:
        self.text = text
        self.password = password
        self.tab_id = tab_id

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Referer": config.rentry_site,
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
        self.session.get(config.rentry_site)

        req = self.session.post(
            config.rentry_site,
            headers=self.headers,
            timeout=10,
            data={
                "csrfmiddlewaretoken": self.get_token(),
                "text": (self.text if len(self.text) > 0 else "."),
                "edit_code": self.password,
            },
            allow_redirects=False,
        )

        if req.status_code != HTTPStatus.FOUND:
            return

        messages = ast.literal_eval(self.get_cookie("messages"))
        messages = messages.split(",")
        url = urllib.parse.urlparse(req.headers["Location"])
        url = Path(url.path).name
        full_url = f"{config.rentry_site}/{url}"

        display.print(
            f"Uploaded: {full_url} ({self.password})",
            do_format=True,
            tab_id=self.tab_id,
        )

        Dialog.show_message(full_url)
