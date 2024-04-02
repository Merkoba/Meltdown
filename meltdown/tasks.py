# Modules
from .args import args
from . import timeutils

# Standard
import threading


def setup() -> None:
    if args.task:
        start()


def run() -> None:
    from .commands import commands
    commands.check(args.task)


def check(seconds: int) -> None:
    first_run = False
    timeutils.sleep(1)

    while True:
        if not first_run:
            if args.task_instant:
                run()

            first_run = True

        timeutils.sleep(seconds)
        run()


def start() -> None:
    seconds = 0

    if args.task_seconds:
        seconds = args.task_seconds
    elif args.task_minutes:
        seconds = args.task_minutes * 60
    elif args.task_hours:
        seconds = args.task_hours * 60 * 60

    if not seconds:
        return

    thread = threading.Thread(target=lambda: check(seconds), args=())
    thread.daemon = True
    thread.start()
