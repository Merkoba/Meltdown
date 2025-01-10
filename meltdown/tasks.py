# Standard
import re
import threading

# Modules
from .args import args
from .commands import commands
from .utils import utils


class Task:
    prefix = utils.escape_regex(args.prefix)
    pattern = rf"^((?:\d.)?\d+)\s+(.*?)({prefix}now)?$"

    def __init__(self, seconds: int, cmds: str, now: bool) -> None:
        self.seconds = seconds
        self.cmds = cmds
        self.now = now
        self.first = False
        self.start()

    def start(self) -> None:
        thread = threading.Thread(target=lambda: self.check())
        thread.daemon = True
        thread.start()

    def run(self) -> None:
        commands.exec(self.cmds)

    def check(self) -> None:
        if not args.quiet:
            msg = f"Running a task every {self.seconds} seconds"
            utils.msg(msg)

        utils.sleep(1)

        while True:
            if not self.first:
                if self.now:
                    self.run()

                self.first = True

            utils.sleep(self.seconds)
            self.run()


class Tasks:
    def start_all(self) -> None:
        for task in args.tasks:
            if not task:
                continue

            match = re.match(Task.pattern, task)

            if not match:
                return

            try:
                seconds = int(match.group(1))
            except BaseException as e:
                utils.error(e)
                return

            cmds = match.group(2)

            if match.group(3):
                now = True
            else:
                now = False

            if seconds < 1:
                continue

            Task(seconds, cmds, now)


tasks = Tasks()
