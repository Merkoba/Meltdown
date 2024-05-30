# Standard
from typing import Optional

# Modules
from .app import app
from .args import args
from .utils import utils
from .dialogs import Dialog


def action(
    mode: str, number: str, tab_id: Optional[str] = None, no_history: bool = False
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

    user_text = item.get("user")
    ai_text = item.get("ai")
    file = item.get("file", "")

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
    elif mode == "program":
        if ai_text:
            run_program(ai_text)


def repeat(number: str, no_history: bool = False) -> None:
    if not number:
        number = "last"

    action("repeat", number, no_history=no_history)


def copy(number: str) -> None:
    if not number:
        number = "last"

    action("copy", number)


def select(number: str) -> None:
    if not number:
        number = "last"

    action("select", number)


def prog(number: str) -> None:
    if not number:
        number = "last"

    action("prog", number)


def run_program(text: str) -> None:
    def action(ans: str) -> None:
        if not ans:
            return

        cmd = [ans, text]
        app.run_command(cmd)

    if args.item_program:
        action(args.item_program)
        return

    Dialog.show_input("Run program", lambda a: action(a))