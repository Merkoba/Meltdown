# Modules
from .args import args
from .commands import commands
from . import timeutils

# Standard
import re
import threading


def run(cmds: str) -> None:
    commands.exec(cmds)


def check(seconds: float, cmds: str, now: bool) -> None:
    first_run = False
    msg = f"Running a task every {seconds} seconds"
    print(msg)
    timeutils.sleep(1)

    while True:
        if not first_run:
            if now:
                run(cmds)

            first_run = True

        timeutils.sleep(seconds)
        run(cmds)


def start() -> None:
    for task in args.tasks:
        do_start(task)


def do_start(task: str) -> None:
    if not task:
        return

    match = re.match(r"^((?:\d.)?\d+)\s+(.*?)(\/now)?$", task)

    if not match:
        return

    try:
        seconds = float(match.group(1))
    except BaseException:
        return

    cmds = match.group(2)

    if match.group(3):
        now = True
    else:
        now = False

    thread = threading.Thread(target=lambda: check(seconds, cmds, now), args=())
    thread.daemon = True
    thread.start()
