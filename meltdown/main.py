# Standard
import os
import sys
import fcntl
import tempfile

# Modules
from .app import app
from .widgets import widgets
from .display import display
from .model import model
from .session import session
from .args import args
from .commands import commands
from .keyboard import keyboard
from .inputcontrol import inputcontrol
from . import terminal
from . import filemanager
from . import system
from . import tasks
from . import utils
from . import listener
from . import timeutils


def main() -> None:
    now = timeutils.now()
    title = app.manifest["title"]
    program = app.manifest["program"]
    args.parse()

    pid_file = os.path.join(tempfile.gettempdir(), f"mlt_{program}.pid")
    fp = open(pid_file, "w", encoding="utf-8")

    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        if not args.force:
            utils.msg(
                f"{title} is already running.\nUse --force to launch multiple instances."
            )
            sys.exit(0)

    filemanager.load()
    app.prepare()
    widgets.make()
    model.setup()
    display.make()
    session.load()
    widgets.setup()
    app.start_checks()
    keyboard.setup()
    commands.setup()
    system.start()
    tasks.start_all()
    app.setup()
    inputcontrol.setup()
    terminal.start()
    listener.start()
    app.autorun()

    # Create singleton
    fp.write(str(os.getpid()))
    fp.flush()

    if args.time:
        msg, now = timeutils.check_time("Program loaded", now)
        utils.msg(msg)

    try:
        app.run()
    except KeyboardInterrupt:
        pass

    try:
        model.unload()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
