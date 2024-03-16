# Modules
from .app import app
from .config import config


def check(text: str) -> bool:
    from .widgets import widgets
    from .session import session
    from .model import model
    from . import state

    prefix = "/"
    with_prefix = text.startswith(prefix)
    single_word = len(text.split()) == 1

    if (not with_prefix) or (not single_word):
        return False

    cmd = text[1:]

    if cmd == "clear":
        widgets.display.clear_output()
    elif cmd == "config":
        config.show_config()
    elif cmd == "exit" or cmd == "quit":
        app.exit()
    elif cmd == "session":
        widgets.display.print(session.to_json())
    elif cmd == "compact":
        app.toggle_compact()
    elif cmd == "log":
        state.save_log()
    elif cmd == "logs":
        state.open_logs_dir()
    elif cmd == "resize":
        app.resize()
    elif cmd == "stop":
        model.stop_stream()
    elif cmd == "sys":
        app.open_task_manager()
    elif cmd == "top":
        widgets.display.output_top()
    elif cmd == "bottom":
        widgets.display.output_bottom()
    elif cmd == "maximize" or cmd == "max":
        app.toggle_maximize()
    elif cmd == "unmaximize":
        app.unmaximize()

    return True
