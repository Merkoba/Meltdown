# Standard
import tkinter as tk
from typing import List, Optional

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
        self.widget = None

    def check(self, widget: Optional[tk.Widget] = None) -> None:
        if not widget:
            self.widget = inputcontrol.input
        else:
            self.widget = widget

        text = self.widget.get_text()

        if "\n" in text:
            text = text.split("\n")[-1]

        if not self.matches:
            self.get_matches(text)

        def do_check() -> None:
            if self.index >= len(self.matches):
                self.index = 0

            match = self.matches[self.index]
            input_text = text[1:]

            if match == input_text:
                if len(self.matches) == 1:
                    return

                self.index += 1
                do_check()
                return

            missing = match[len(self.clean(self.word)) :]

            if self.match:
                self.widget.delete_text(self.pos, len(self.missing))

            self.widget.insert_text(missing, index=self.pos)

            self.index += 1
            self.match = match
            self.missing = missing

        if self.matches:
            do_check()

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
        caret_pos = self.widget.index(tk.INSERT)
        full_pos = caret_pos

        if "." in caret_pos:
            caret_pos = int(caret_pos.split(".")[1])

        text_to_caret = text[:caret_pos]
        last_space_pos = text_to_caret.rfind(" ")
        word = text_to_caret[last_space_pos + 1 : caret_pos]

        if not word:
            return

        self.word = word
        self.pos = self.widget.index(full_pos)

        if "." in self.pos:
            self.pos = int(self.pos.split(".")[1])

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
