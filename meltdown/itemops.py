from __future__ import annotations

# Modules
from .app import app
from .config import config
from .args import args
from .utils import utils
from .dialogs import Dialog


class ItemOps:
    def action(
        self,
        mode: str,
        number: str,
        tab_id: str | None = None,
        no_history: bool = False,
        who: str | None = None,
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

        date = item.date
        user_text = item.user
        ai_text = item.ai
        file = item.file

        both_text = f"User: {user_text}\n\nAI: {ai_text}"

        if mode == "repeat":
            if user_text:
                prompt = {"text": user_text, "file": file, "no_history": no_history}
                model.stream(prompt, tabconvo.tab.tab_id)
        elif mode == "copy":
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
            if date:
                self.do_show_info(date)

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
        cmds.append(("Program", lambda a: self.run_program(text)))
        cmds.append(("Markdown", lambda a: action("markdown")))
        cmds.append(("Text", lambda a: action("text")))

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

    def do_show_info(self, date: float) -> None:
        n_date = utils.to_date(date)
        n_date += "\n"
        n_date += utils.time_ago(date, utils.now())

        Dialog.show_message(n_date)


itemops = ItemOps()
