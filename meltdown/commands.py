# Modules
from .app import app
from .config import config


def check(text: str) -> bool:
    from .widgets import widgets
    from .session import session
    from .model import model
    from . import state

    if not text.startswith("/"):
        return False

    cmd = text[1:]

    if cmd == "clear":
        widgets.display.clear_output()
        return True
    elif cmd == "config":
        config.show_config()
        return True
    elif cmd == "exit" or cmd == "quit":
        app.exit()
        return True
    elif cmd == "session":
        widgets.display.print(session.to_json())
        return True
    elif cmd == "compact":
        app.toggle_compact()
        return True
    elif cmd == "log":
        state.save_log()
        return True
    elif cmd == "stop":
        model.stop_stream()
        return True

    return False
