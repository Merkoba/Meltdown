# Standard
import threading
from pathlib import Path
import tempfile

# Modules
from .args import args
from .app import app
from .utils import utils
from .files import files
from .inputcontrol import inputcontrol


def start() -> None:
    if not args.listener:
        return

    if args.listener_delay < 1:
        return

    thread = threading.Thread(target=lambda: do_start())
    thread.daemon = True
    thread.start()


def do_start() -> None:
    program = app.manifest["program"]

    if args.listener_path:
        path = Path(args.listener_path)
    else:
        file_name = f"mlt_{program}.input"
        path = Path(tempfile.gettempdir(), file_name)

    if not args.quiet:
        m = utils.singular_or_plural(args.listener_delay, "sec", "secs")
        utils.msg(f"Listener active ({args.listener_delay} {m})")
        utils.msg(f"Write to: {path!s}")

    while True:
        if path.exists() and path.is_file():
            try:
                text = files.read(path)

                if text:
                    files.write(path, "")
                    inputcontrol.submit(text=text)
            except Exception as e:
                utils.msg(f"Listener error: {e!s}")

        utils.sleep(args.listener_delay)
