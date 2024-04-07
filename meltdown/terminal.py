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
    if not args.terminal:
        return

    thread = threading.Thread(target=get_input, args=())
    thread.daemon = True
    thread.start()
