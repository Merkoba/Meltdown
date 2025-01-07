from __future__ import annotations

# Standard
from typing import TYPE_CHECKING

# Modules
from .app import app
from .config import config
from .args import args
from .utils import utils
from .dialogs import Dialog


if TYPE_CHECKING:
    from .session import Item


class ItemOps:
    def action(
        self,
        mode: str,
        number: str,
        tab_id: str | None = None,
        no_history: bool = False,
        who: str = "both",
    ) -> None:
        from .model import model
        from .display import display
        from .output import Output

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        index = utils.get_index(number, tabconvo.convo.items)

        if index < 0:
            return

        if index >= len(tabconvo.convo.items):
            return

        item = tabconvo.convo.items[index]

        if not item:
            return

        user_text = item.user
        ai_text = item.ai
        file = item.file

        both_text = f"User: {user_text}\n\nAI: {ai_text}"

        if mode == "repeat":
            if user_text:
                prompt = {"text": user_text, "file": file, "no_history": no_history}
                model.stream(prompt, tabconvo.tab.tab_id)
        elif mode == "copy":
            text = ""

            if who:
                if who == "user":
                    text = user_text
                elif who == "ai":
                    text = ai_text
                elif who == "both":
                    texts = []

                    if user_text:
                        text = ""
                        text += Output.get_prompt("user", put_colons=False)
                        text += f": {user_text}"

                        if file:
                            text += f"\n\nFile: {file}"

                        texts.append(text)

                    if ai_text:
                        text = ""
                        text += Output.get_prompt("ai", put_colons=False)
                        text += f": {ai_text}"
                        texts.append(text)

                    text = "\n\n".join(texts)

            if not text:
                return

            utils.copy(text, command=True)
        elif mode == "select":
            Output.select_item(index + 1)
        elif mode == "use":
            if who == "user":
                if user_text:
                    self.do_use_item(user_text)
            elif who == "ai":
                if ai_text:
                    self.do_use_item(ai_text)
            elif who == "both":
                if user_text and ai_text:
                    self.do_use_item(both_text)
        elif mode == "info":
            self.do_show_info(item)

    def repeat(self, number: str, no_history: bool = False) -> None:
        if not number:
            number = "last"

        self.action("repeat", number, no_history=no_history)

    def copy(self, number: str) -> None:
        if not number:
            number = "last"

        self.action("copy", number)

    def select(self, number: str) -> None:
        if not number:
            number = "last"

        self.action("select", number)

    def use_item(self, number: str) -> None:
        if not number:
            number = "last"

        who = "ai"

        if args.use_both:
            who = "both"

        self.action("use", number, who=who)

    def do_use_item(self, text: str) -> None:
        from . import formats

        def action(mode: str) -> None:
            formats.do_open(mode, text=text)

        cmds = []
        cmds.append(Dialog.cmd("Program", lambda a: self.run_program(text)))
        cmds.append(Dialog.cmd("Markdown", lambda a: action("markdown")))
        cmds.append(Dialog.cmd("Text", lambda a: action("text")))

        Dialog.show_dialog("Use Item", cmds)

    def run_program(self, text: str) -> None:
        def action(ans: str) -> None:
            if not ans:
                return

            config.set_value("last_program", ans)
            app.run_program(ans, text)

        if args.use_program:
            action(args.use_program)
            return

        Dialog.show_input("Run Program", lambda a: action(a), value=config.last_program)

    def show_info(self, number: str) -> None:
        if not number:
            number = "last"

        who = "ai"

        if args.use_both:
            who = "both"

        self.action("info", number, who=who)

    def do_show_info(self, item: Item) -> None:
        text = ""

        if item.model:
            text += utils.no_break(f"Model: {item.model}")

        if item.date is not None:
            text += f"\n\n{utils.to_date(item.date)}\n"
            text += utils.time_ago(item.date, utils.now())

        if item.duration is not None:
            text += f"\n\nDuration: {item.duration:.2f} seconds"

        if item.user:
            w_user = len(utils.get_words(item.user))
            words = utils.singular_or_plural(w_user, "word", "words")
            text += f"\n\nUser: {w_user} {words} ({len(item.user)} chars)"

        if item.ai:
            w_ai = len(utils.get_words(item.ai))
            words = utils.singular_or_plural(w_ai, "word", "words")
            text += f"\nAI: {w_ai} {words} ({len(item.ai)} chars)"

        if item.file:
            text += utils.no_break(f"\n\nFile: {item.file}")

        if item.seed is not None:
            text += f"\n\nSeed: {item.seed}"

        if item.history is not None:
            text += f"\nHistory: {item.history}"

        if item.max_tokens is not None:
            text += f"\nMax Tokens: {item.max_tokens}"

        if item.temperature is not None:
            text += f"\nTemperature: {item.temperature}"

        if item.top_k is not None:
            text += f"\nTop K: {item.top_k}"

        if item.top_p is not None:
            text += f"\nTop P: {item.top_p}"

        Dialog.show_msgbox("Information", text)


itemops = ItemOps()
