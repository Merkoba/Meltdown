# Standard
import threading
from typing import Any, Generator

# Libraries
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings

# Modules
from .args import args
from .app import app
from .commands import commands
from .inputcontrol import inputcontrol
from .utils import utils


completer: Completer
words: list[str] = []


class SlashCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: Any
    ) -> Generator[Completion, None, None]:
        text = document.get_word_before_cursor(WORD=True).strip()

        if not text:
            return

        if text.startswith(args.prefix):
            for word in words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))
        else:
            for word in words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))


def add_word(word: str) -> None:
    if word not in words:
        words.append(word)


def start() -> None:
    if not args.show_terminal:
        return

    thread = threading.Thread(target=lambda: do_start())
    thread.daemon = True
    thread.start()


def do_start() -> None:
    kb = KeyBindings()

    @kb.add("c-v")
    def _(event: Any) -> None:
        clipboard_data = utils.get_paste()

        if not clipboard_data:
            return

        event.current_buffer.insert_text(clipboard_data)

    history = InMemoryHistory()

    words.extend([f"/{key}" for key in commands.cmdkeys])
    words.extend(inputcontrol.autocomplete)

    completer = SlashCompleter()

    session: PromptSession[Any] = PromptSession(
        history=history,
        completer=completer,
        reserve_space_for_menu=args.terminal_height,
        vi_mode=args.terminal_vi,
        key_bindings=kb,
    )

    while True:
        try:
            text = session.prompt("Input: ")

        except KeyboardInterrupt:
            app.exit(force=True)
            return
        except Exception:
            continue

        if not text:
            continue

        inputcontrol.submit(text=text)
