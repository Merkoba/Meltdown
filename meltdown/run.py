from __future__ import annotations

# Standard
import subprocess
from typing import Any

# Modules
from .args import args
from .utils import utils
from .dialogs import Dialog, Commands
from .formats import formats


class Script:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path

    def run(self) -> None:
        if not self.path:
            utils.msg(f"Script '{self.name}' has no path defined.")
            return

        tempfile = formats.to_tempfile()

        utils.msg(
            f"Running script '{self.name}' with path '{self.path}' and tempfile '{tempfile}'."
        )

        subprocess.run([self.path, str(tempfile)], check=False)


class Run:
    def __init__(self) -> None:
        self.scripts: list[Script] = []

    def setup(self) -> None:
        for script in args.scripts:
            parts = script.split(" ", 1)

            if len(parts) != 2:
                utils.msg(
                    f"Invalid script format: {script}. Expected format is '[name] [path]'."
                )

            name, path = parts
            self.scripts.append(Script(name, path))

    def run_shell(self, command: str, shell: bool = True) -> None:
        user_shell = utils.get_shell()
        cmds = [user_shell, "-c", command]
        result = subprocess.run(cmds, capture_output=True, text=True, check=False)
        message = result.stdout if result.returncode == 0 else result.stderr
        message = message.strip()

        if not message:
            message = "Success"

        def cmd_ok(arg: Any) -> None:
            pass

        def cmd_cancel() -> None:
            pass

        def cmd_run(arg: Any) -> None:
            pass

        dcmds = Commands()
        dcmds.add("Run", cmd_run)

        Dialog.show_textbox(
            "shell_command", "Output", cmd_ok, cmd_cancel, message, commands=dcmds
        )

    def run_python(self, command: str) -> None:
        try:
            subprocess.run(
                ["python3", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            pcmd = "python3"
        except FileNotFoundError:
            pcmd = "python"

        cmds = [pcmd, "-c", command]
        result = subprocess.run(cmds, capture_output=True, text=True, check=False)
        message = result.stdout if result.returncode == 0 else result.stderr
        message = message.strip()

        if not message:
            message = "Success"

        def cmd_ok(arg: Any) -> None:
            pass

        def cmd_cancel() -> None:
            pass

        def cmd_run(arg: Any) -> None:
            pass

        dcmds = Commands()
        dcmds.add("Run", cmd_run)

        Dialog.show_textbox(
            "python_command", "Output", cmd_ok, cmd_cancel, message, commands=dcmds
        )

    def get_script(self, name: str) -> Script | None:
        for script in self.scripts:
            if script.name == name:
                return script

        return None

    def run_script(self, name: str) -> None:
        if not name:
            return

        script = self.get_script(name)

        if not script:
            utils.msg(f"Script '{name}' not found.")
            return

        script.run()


run = Run()
