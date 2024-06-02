from __future__ import annotations

# Standard
import tkinter as tk

# Modules
from .inputcontrol import inputcontrol
from .commands import commands
from .args import args
from .utils import utils
from .entrybox import EntryBox
from .textbox import TextBox


InputWidget = EntryBox | TextBox | None


class AutoComplete:
    def __init__(self) -> None:
        self.index = 0
        self.matches: list[str] = []
        self.match = ""
        self.word = ""
        self.pos = 0
        self.missing = ""
        self.widget: InputWidget

    def check(self, widget: InputWidget = None) -> None:
        try:
            self.do_check(widget=widget)
        except BaseException as e:
            utils.error(e)

    def do_check(self, widget: InputWidget = None) -> None:
        if not widget:
            self.widget = inputcontrol.input
        else:
            self.widget = widget

        if not self.widget:
            return

        text = self.widget.get_text()

        if "\n" in text:
            text = text.split("\n")[-1]

        if not self.matches:
            self.get_matches(text)

        def action() -> None:
            if not self.widget:
                return

            if not isinstance(self.widget, EntryBox):
                return

            if self.index >= len(self.matches):
                self.index = 0

            match = self.matches[self.index]
            input_text = text[1:]

            if match == input_text:
                if len(self.matches) == 1:
                    return

                self.index += 1
                action()
                return

            missing = match[len(self.clean(self.word)) :]

            if self.match:
                self.widget.delete_text(self.pos, len(self.missing))

            self.widget.insert_text(missing, index=self.pos, add_space=True)

            self.index += 1
            self.match = match
            self.missing = missing

        if self.matches:
            action()

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

        if not self.widget:
            return

        self.reset()
        s_caret_pos = str(self.widget.index(tk.INSERT))

        if "." in s_caret_pos:
            s_caret_pos = s_caret_pos.split(".")[1]

        self.pos = int(s_caret_pos)
        text_to_caret = text[: self.pos]
        last_space_pos = text_to_caret.rfind(" ")
        word = text_to_caret[last_space_pos + 1 : self.pos]

        if not word:
            return

        self.word = word

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
