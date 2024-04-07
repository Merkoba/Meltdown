# Modules
from .inputcontrol import inputcontrol
from .args import args
from .commands import commands
from .app import app

# Standard
import threading
from typing import Any, Generator, List

# Libraries
from prompt_toolkit import prompt  # type:ignore
from prompt_toolkit.history import InMemoryHistory  # type:ignore
from prompt_toolkit.completion import Completer, Completion  # type:ignore
from prompt_toolkit.document import Document  # type:ignore


class SlashCompleter(Completer):  # type:ignore
    def __init__(self, words: List[str]) -> None:
        self.words = words

    def get_completions(self, document: Document, event: Any) -> Generator[Completion, None, None]:
        text = document.text_before_cursor

        if text.startswith(args.prefix):
            for word in self.words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))


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
            user_input = prompt("Input: ", history=history, completer=completer,
                                reserve_space_for_menu=args.terminal_height,
                                vi_mode=args.terminal_vi)

        except KeyboardInterrupt:
            app.exit()
            return

        if not user_input:
            continue

        inputcontrol.submit(text=user_input)


def start() -> None:
    if not args.terminal:
        return

    thread = threading.Thread(target=get_input, args=())
    thread.daemon = True
    thread.start()
