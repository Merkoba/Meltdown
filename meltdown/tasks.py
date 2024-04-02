# Modules
from .args import args
from . import timeutils

# Standard
import threading


def run(num: int) -> None:
    from .commands import commands
    task = getattr(args, f"task_{num}")
    commands.check(task)


def check(num: int, seconds: int) -> None:
    first_run = False
    instant = getattr(args, f"task_{num}_instant")
    msg = f"Running task {num} every {seconds} seconds"

    if instant:
        msg += " (instant)"

    print(msg)
    timeutils.sleep(1)

    while True:
        if not first_run:
            if instant:
                run(num)

            first_run = True

        timeutils.sleep(seconds)
        run(num)


def start() -> None:
    for num in range(1, 4):
        do_start(num)


def do_start(num: int) -> None:
    task = getattr(args, f"task_{num}")

    if not task:
        return

    seconds = 0
    secs = getattr(args, f"task_{num}_seconds")
    mins = getattr(args, f"task_{num}_minutes")
    hrs = getattr(args, f"task_{num}_hours")

    if secs:
        seconds = secs
    elif mins:
        seconds = mins * 60
    elif hrs:
        seconds = hrs * 60 * 60

    if not seconds:
        return

    thread = threading.Thread(target=lambda: check(num, seconds), args=())
    thread.daemon = True
    thread.start()
