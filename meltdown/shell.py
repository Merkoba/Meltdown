# Standard
import subprocess

# Modules
from .dialogs import Dialog


class Shell:
    @staticmethod
    def run(command: str, shell: bool = True) -> str:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        message = result.stdout if result.returncode == 0 else result.stderr
        message = message.strip()

        if not message:
            message = "Success"

        def cmd_ok() -> None:
            Dialog.close()

        def cmd_cancel() -> None:
            Dialog.close()

        Dialog.show_textbox("shell_command", "Output", cmd_ok, cmd_cancel, message)


shell = Shell()
