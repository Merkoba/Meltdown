# Standard
import tkinter as tk
from typing import List

# Modules
from .inputcontrol import inputcontrol
from .commands import commands
from .args import args


class AutoComplete:
    def __init__(self) -> None:
        self.index = 0
        self.matches: List[str] = []
        self.match = ""
        self.word = ""
        self.pos = 0
        self.missing = ""

    def check(self) -> None:
        text = inputcontrol.input.get()

        if not self.matches:
            self.get_matches(text)

        def check() -> None:
            if self.index >= len(self.matches):
                self.index = 0

            match = self.matches[self.index]
            input_text = inputcontrol.input.get()[1:]

            if match == input_text:
                if len(self.matches) == 1:
                    return

                self.index += 1
                check()
                return

            missing = match[len(self.clean(self.word)) :]

            if self.match:
                inputcontrol.input.delete_text(self.pos, len(self.missing))

            inputcontrol.input.insert_text(missing, index=self.pos)

            self.index += 1
            self.match = match
            self.missing = missing

        if self.matches:
            check()

    def reset(self) -> None:
        self.matches = []
        self.match = ""
        self.missing = ""
        self.index = 0
        self.pos = 0

    def get_matches(self, text: str) -> None:
        from .inputcontrol import inputcontrol

        if not text:
            return

        self.reset()
        caret_pos = inputcontrol.input.index(tk.INSERT)
        text_to_caret = text[:caret_pos]
        last_space_pos = text_to_caret.rfind(" ")
        word = text_to_caret[last_space_pos + 1 : caret_pos]

        if not word:
            return

        self.word = word
        self.pos = inputcontrol.input.index(caret_pos)

        if commands.is_command(word):
            word = self.clean(word)

            for key in commands.cmdkeys:
                if key.startswith(word):
                    self.matches.append(key)
        else:
            for w in inputcontrol.autocomplete:
                if w.startswith(word):
                    self.matches.append(w)

    def clean(self, text: str) -> str:
        if text.startswith(args.prefix):
            return text[1:]

        return text


autocomplete = AutoComplete()
