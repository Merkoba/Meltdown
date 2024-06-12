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
    file_name = f"mlt_{program}.input"

    if not args.quiet:
        m = utils.singular_or_plural(args.listener_delay, "sec", "secs")
        utils.msg(f"Listener active ({args.listener_delay} {m})")

    path = Path(tempfile.gettempdir(), file_name)

    while True:
        if path.exists() and path.is_file():
            text = files.read(path)

            if text:
                files.write(path, "")
                inputcontrol.submit(text=text)

        utils.sleep(args.listener_delay)
