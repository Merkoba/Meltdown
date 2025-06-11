# Standard
import re
import threading

# Modules
from .args import args
from .commands import commands
from .utils import utils


class Task:
    prefix = utils.escape_regex(args.command_prefix)
    pattern = rf"^((?P<time>\d+(?:\.\d+)?)(?P<unit>s|m|h|d)?\s+(?P<commands>.*?)(?:\s*(?P<now>{prefix}now))?$)"

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
                time = float(match.group("time"))
            except BaseException as e:
                utils.error(e)
                return

            unit = match.group("unit")

            if unit == "m":
                time *= 60
            elif unit == "h":
                time *= 60 * 60
            elif unit == "d":
                time *= 60 * 60 * 24

            cmds = match.group("commands")

            if match.group("now"):
                now = True
            else:
                now = False

            if time < 1:
                continue

            Task(int(time), cmds, now)


tasks = Tasks()
