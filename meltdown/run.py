# Standard
import subprocess
from typing import Any

# Modules
from .utils import utils
from .dialogs import Dialog, Commands


class Run:
    @staticmethod
    def run_shell(command: str, shell: bool = True) -> None:
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

    @staticmethod
    def run_python(command: str) -> None:
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


run = Run()
