# Standard
import subprocess
from typing import Any

# Modules
from .dialogs import Dialog, Commands


class Run:
    @staticmethod
    def run_shell(command: str, shell: bool = True) -> None:
        cmds = ["fish", "-c", command]
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
        cmds = ["python", "-c", command]
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
