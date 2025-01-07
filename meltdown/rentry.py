# Standard
import ast
import os.path
import re
import requests
import urllib.parse
from http import HTTPStatus

# Libraries
import requests  # type: ignore

# Modules
from .config import config


class Rentry:
    def __init__(self):
        self.session = requests.session()
        self.session.get(config.rentry_site)

    def get_cookie(self, cookie_name: str) -> str:
        return self.session.cookies.get(cookie_name, default="")

    def get_token(self):
        return self.get_cookie("csrftoken")

    def post(self, page: str, *args, **kwargs) -> requests.Response:
        url = urllib.parse.urljoin(config.rentry_site, page)

        return self.session.post(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
                "Referer": url,
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
            },
            *args,
            **kwargs,
        )


class RentryPage:
    rentry = None

    def __init__(self, text: str = "", custom_url: str = "", edit_code: str = ""):
        self.code = edit_code
        self.site = custom_url

        if self.rentry is None:
            self.rentry = Rentry()

        r_create = self.rentry.post(
            "/",
            data={
                "csrfmiddlewaretoken": self.rentry.get_token(),
                "text": (text if len(text) > 0 else "."),
                "edit_code": self.code,
                "url": self.site,
            },
            allow_redirects=False,
        )

        if r_create.status_code != HTTPStatus.FOUND:
            raise Exception("Failed to create page.")

        ck_messages = ast.literal_eval(self.rentry.get_cookie("messages"))
        ck_messages = ck_messages.split(",")

        if len(ck_messages) <= 1 or "Your edit code: " not in ck_messages:
            raise Exception("Failed to get a `messages` cookie.")

        self.code = ck_messages[ck_messages.index("Your edit code: ") + 1]
        self.code = re.sub("[\\W_]+", "", self.code)
        self.site = urllib.parse.urlparse(r_create.headers["Location"])
        self.site = os.path.basename(self.site.path)
