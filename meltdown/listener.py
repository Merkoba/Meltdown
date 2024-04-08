# Standard
import threading
from pathlib import Path
import tempfile

# Modules
from .args import args
from .app import app
from .inputcontrol import inputcontrol
from . import timeutils
from . import utils


def start() -> None:
    if not args.listener:
        return

    if args.listener_delay < 0.1:
        return

    thread = threading.Thread(target=lambda: do_start())
    thread.daemon = True
    thread.start()


def do_start() -> None:
    program = app.manifest["program"]
    file_name = f"mlt_{program}.input"

    if not args.quiet:
        utils.msg(f"Listening to {file_name}")

    path = Path(tempfile.gettempdir(), file_name)

    while True:
        if path.exists() and path.is_file():
            with open(path, "r") as file:
                text = file.read().strip()

                if text:
                    with open(path, "w") as file:
                        file.write("")

                    inputcontrol.submit(text=text)

        timeutils.sleep(args.listener_delay)