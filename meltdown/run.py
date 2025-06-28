# Standard
import subprocess
from typing import Any

# Modules
from .dialogs import Dialog, Commands


class Run:
    @staticmethod
    def run(command: str, shell: bool = True) -> None:
        cmds = ["fish", "-c"]
        parts = [p for p in command.split() if p]
        cmds.extend(parts)

        result = subprocess.run(
            cmds, capture_output=True, text=True, check=False
        )

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

        cmds = Commands()
        cmds.add("Run", cmd_run)

        Dialog.show_textbox(
            "shell_command", "Output", cmd_ok, cmd_cancel, message, commands=cmds
        )


run = Run()
