from __future__ import annotations

# Standard
import threading
from typing import Any
from collections.abc import Generator

# Libraries
from prompt_toolkit import PromptSession  # type: ignore
from prompt_toolkit.history import InMemoryHistory  # type: ignore
from prompt_toolkit.completion import Completer, Completion  # type: ignore
from prompt_toolkit.document import Document  # type: ignore
from prompt_toolkit.key_binding import KeyBindings  # type: ignore

# Modules
from .args import args
from .app import app
from .commands import commands
from .inputcontrol import inputcontrol
from .utils import utils


completer: Completer
words: list[str] = []


class SlashCompleter(Completer):  # type: ignore
    def get_completions(
        self, document: Document, complete_event: Any
    ) -> Generator[Completion, None, None]:
        text = document.get_word_before_cursor(WORD=True).strip()

        if not text:
            return

        if text.startswith(args.command_prefix):
            for word in words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))
        else:
            for word in words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))


class Console:
    def __init__(self) -> None:
        self.session: PromptSession[Any] | None = None

    def add_word(self, word: str) -> None:
        if word not in words:
            words.append(word)

    def start(self) -> None:
        if not args.console:
            return

        thread = threading.Thread(target=lambda: self.do_start())
        thread.daemon = True
        thread.start()

    def do_start(self) -> None:
        kb = KeyBindings()

        @kb.add("c-v")  # type: ignore
        def _(event: Any) -> None:
            clipboard_data = utils.get_paste()

            if not clipboard_data:
                return

            event.current_buffer.insert_text(clipboard_data)

        history = InMemoryHistory()

        words.extend([f"/{key}" for key in commands.cmdkeys])
        words.extend(inputcontrol.autocomplete)

        completer = SlashCompleter()

        self.session = PromptSession(
            history=history,
            completer=completer,
            reserve_space_for_menu=args.console_height,
            vi_mode=args.console_vi,
            key_bindings=kb,
        )

        while True:
            try:
                text = self.session.prompt("Input: ")
            except KeyboardInterrupt:
                app.destroy()
                return
            except Exception:
                continue

            if not text:
                continue

            inputcontrol.submit(text=text)


console = Console()
