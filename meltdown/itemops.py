from __future__ import annotations

# Standard
from typing import TYPE_CHECKING

# Modules
from .app import app
from .args import args
from .utils import utils
from .dialogs import Dialog, Commands
from .memory import memory


if TYPE_CHECKING:
    from .session import Item


class ItemOps:
    def action(
        self,
        mode: str,
        number: str,
        tab_id: str | None = None,
        history_mode: str = "normal",
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
        no_history = history_mode == "no_history"
        history_cutoff = index if history_mode == "normal" else -1

        if mode == "repeat":
            if user_text:
                prompt = {
                    "text": user_text,
                    "file": file,
                    "no_history": no_history,
                    "history_cutoff": history_cutoff,
                }

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
                        text += display.get_prompt("user", put_colons=False)
                        text += f": {user_text}"

                        if file:
                            text += f"\n\nFile: {file}"

                        texts.append(text)

                    if ai_text:
                        text = ""
                        text += display.get_prompt("ai", put_colons=False)
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

    def repeat(self, number: str, history_mode: str = "normal") -> None:
        if not number:
            number = "last"

        self.action("repeat", number, history_mode=history_mode)

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
        from .formats import formats

        def action(mode: str) -> None:
            formats.do_open(mode, text=text)

        cmds = Commands()
        cmds.add("Program", lambda a: self.run_program(text))
        cmds.add("Markdown", lambda a: action("markdown"))
        cmds.add("Text", lambda a: action("text"))

        Dialog.show_dialog("Use Item", cmds)

    def run_program(
        self, text: str | None = None, program: str | None = None, auto: bool = False
    ) -> None:
        if not text:
            last_item = self.last_item()

            if last_item:
                text = last_item.ai

        if not text:
            return

        def run() -> None:
            if program:
                memory.set_value("last_program", program)
                app.run_program(program, text)

        if program:
            run()
            return

        if auto and memory.last_program:
            program = memory.last_program
            run()
            return

        def action(ans: str) -> None:
            nonlocal program

            if not ans:
                return

            program = ans
            run()

        if args.use_program:
            action(args.use_program)
            return

        Dialog.show_input("Run Program", lambda a: action(a), value=memory.last_program)

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

        if item.format:
            text += f"\nFormat: {item.format}"

        if item.date is not None:
            text += f"\n\n{utils.to_date(item.date, minimal=args.minimal_info)}\n"
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

        if item.tokens_per_second is not None:
            text += f"\nTPS: {item.tokens_per_second}"

        Dialog.show_msgbox("Information", text)

    def last_item(self) -> Item | None:
        from .display import display

        tabconvo = display.get_tab_convo()

        if not tabconvo:
            return None

        if not tabconvo.convo.items:
            return None

        return tabconvo.convo.items[-1]


itemops = ItemOps()
