# Standard
import threading
from typing import Any, Generator, List

# Libraries
from prompt_toolkit import PromptSession  # type:ignore
from prompt_toolkit.history import InMemoryHistory  # type:ignore
from prompt_toolkit.completion import Completer, Completion  # type:ignore
from prompt_toolkit.document import Document  # type:ignore
from prompt_toolkit.key_binding import KeyBindings  # type:ignore
import pyperclip  # type: ignore

# Modules
from .args import args
from .app import app
from .commands import commands
from .inputcontrol import inputcontrol


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


def start() -> None:
    if not args.terminal:
        return

    thread = threading.Thread(target=lambda: do_start())
    thread.daemon = True
    thread.start()


def do_start() -> None:
    kb = KeyBindings()

    @kb.add("c-v")  # type:ignore
    def _(event: Any) -> None:
        clipboard_data = pyperclip.paste().strip()
        event.current_buffer.insert_text(clipboard_data)

    history = InMemoryHistory()
    cmdlist = [f"/{key}" for key in commands.cmdkeys]
    completer = SlashCompleter(cmdlist)

    session = PromptSession(history=history, completer=completer,
                            reserve_space_for_menu=args.terminal_height,
                            vi_mode=args.terminal_vi, key_bindings=kb)

    while True:
        try:
            text = session.prompt("Input: ")

        except KeyboardInterrupt:
            app.exit()
            return
        except Exception:
            continue

        if not text:
            continue

        if args.terminal_memory:
            for word in text.split(" "):
                if len(word) >= args.terminal_memory_min:
                    completer.add_word(word)

        inputcontrol.submit(text=text)
