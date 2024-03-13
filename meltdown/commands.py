# Modules
from .app import app
from .config import config


def check(text: str) -> bool:
    from .widgets import widgets

    if not text.startswith("/"):
        return False

    if text == "/clear":
        widgets.display.clear_output()
        return True
    elif text == "/config":
        config.show_config()
        return True
    elif text == "/exit" or text == "/quit":
        app.exit()
        return True
    elif text == "/session":
        from .session import session
        widgets.display.print(session.to_json())
        return True

    return False
