# Standard
import os
import fcntl
import tempfile
from pathlib import Path

# Modules
from .app import app
from .config import config
from .widgets import widgets
from .display import display
from .model import model
from .session import session
from .args import args
from .commands import commands
from .keyboard import keyboard
from .inputcontrol import inputcontrol
from .utils import utils
from .paths import paths
from .system import system
from .console import console
from .listener import listener
from .tasks import tasks
from .memory import memory
from .autoscroll import autoscroll
from .variables import variables
from .run import run


def main() -> None:
    now = utils.now()
    title = app.manifest["title"]
    program = app.manifest["program"]
    args.parse()

    if not paths.setup():
        return

    if args.profile:
        pid = f"mlt_{program}_{args.profile}.pid"
    else:
        pid = f"mlt_{program}.pid"

    pid_file = Path(tempfile.gettempdir(), pid)
    fp = pid_file.open("w", encoding="utf-8")

    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        if not args.force:
            utils.msg(
                f"{title} is already running.\nUse --force to launch multiple instances."
            )

            return

    memory.load()
    config.load()
    app.prepare()
    widgets.make()
    autoscroll.setup()
    model.setup()
    display.make()
    session.load()
    widgets.setup()
    keyboard.setup()
    commands.setup()
    variables.setup()
    inputcontrol.setup()
    run.setup()
    app.setup(now)
    system.start()
    console.start()
    listener.start()
    tasks.start_all()

    # Create singleton
    fp.write(str(os.getpid()))
    fp.flush()

    if args.time and (not args.quiet):
        msg, now = utils.check_time("Ready", now)
        utils.msg(msg)

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        utils.error(e)

    try:
        model.unload()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        utils.error(e)


if __name__ == "__main__":
    main()
