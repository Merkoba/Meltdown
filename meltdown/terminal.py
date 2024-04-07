# Modules
from .inputcontrol import inputcontrol
from .args import args
from .commands import commands
from .app import app
from . import timeutils
from . import utils

# Standard
import threading
from typing import Any, Generator, List
from pathlib import Path

# Libraries
from prompt_toolkit import prompt  # type:ignore
from prompt_toolkit.history import InMemoryHistory  # type:ignore
from prompt_toolkit.completion import Completer, Completion  # type:ignore
from prompt_toolkit.document import Document  # type:ignore
import tempfile


class SlashCompleter(Completer):  # type:ignore
    def __init__(self, words: List[str]) -> None:
        self.words = words

    def get_completions(self, document: Document, event: Any) -> Generator[Completion, None, None]:
        text = document.get_word_before_cursor(WORD=True).strip()

        if not text:
            return

        if text.startswith(args.prefix):
            for word in self.words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))
        else:
            for word in self.words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))

    def add_word(self, name: str) -> None:
        if name not in self.words:
            self.words.append(name)


def get_input() -> None:
    history = InMemoryHistory()
    cmdkeys = commands.commands.keys()
    names = []

    for key in cmdkeys:
        cmd = commands.commands[key]
        names.append(key)
        names.extend(cmd["aliases"])

    cmdlist = [f"/{name}" for name in names]
    completer = SlashCompleter(cmdlist)

    while True:
        try:
            text = prompt("Input: ", history=history, completer=completer,
                          reserve_space_for_menu=args.terminal_height,
                          vi_mode=args.terminal_vi)

        except KeyboardInterrupt:
            app.exit()
            return

        if not text:
            continue

        if args.terminal_memory:
            for word in text.split(" "):
                if len(word) >= args.terminal_memory_min:
                    completer.add_word(word)

        inputcontrol.submit(text=text)


def start() -> None:
    if args.terminal:
        thread = threading.Thread(target=get_input, args=())
        thread.daemon = True
        thread.start()

    if args.listener:
        start_listener()


def start_listener() -> None:
    if args.listener_delay < 0.1:
        return

    thread = threading.Thread(target=lambda: listener())
    thread.daemon = True
    thread.start()


def listener() -> None:
    program = app.manifest["program"]
    file_name = f"mlt_{program}.input"

    if not args.quiet:
        utils.msg(f"Listening to {file_name}")

    path = Path(tempfile.gettempdir(), file_name)

    while True:
        if path.exists() and path.is_file():
            with open(path, "r") as file:
                text = file.read().strip()

                if text:
                    with open(path, "w") as file:
                        file.write("")

                    inputcontrol.submit(text=text)

        timeutils.sleep(args.listener_delay)
