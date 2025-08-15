# Standard
import time
import threading
import tempfile
from typing import Any
from pathlib import Path

# Libraries
from watchdog.observers import Observer  # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore

# Modules
from .args import args
from .app import app
from .utils import utils
from .files import files
from .inputcontrol import inputcontrol


class FileChangeHandler(FileSystemEventHandler):  # type: ignore
    def __init__(self, path: Path) -> None:
        self.path = path

    def on_modified(self, event: Any) -> None:
        if event.src_path == str(self.path):
            try:
                text = files.read(self.path).strip()

                if text:
                    files.write(self.path, "")
                    inputcontrol.submit(text=text)
            except Exception as e:
                utils.msg(f"Listener error: {e!s}")


class Listener:
    def start(self) -> None:
        if not args.listen:
            return

        thread = threading.Thread(target=lambda: self.do_start())
        thread.daemon = True
        thread.start()

    def do_start(self) -> None:
        program = app.manifest["program"]

        if args.listen_file:
            path = Path(args.listen_file)
        else:
            file_name = f"mlt_{program}.input"
            path = Path(tempfile.gettempdir(), file_name)

        if not args.quiet:
            utils.msg(f"Listening: {path!s}")

        handler = FileChangeHandler(path)
        observer = Observer()
        observer.schedule(handler, str(path.parent), recursive=False)

        thread = threading.Thread(target=observer.start)
        thread.daemon = True
        thread.start()

        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()


listener = Listener()
