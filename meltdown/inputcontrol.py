# Standard
from typing import Any, Optional, List, Dict

# Libraries
from tkinterdnd2 import DND_TEXT  # type: ignore

# Modules
from .tooltips import ToolTip
from .commands import commands
from .config import config
from .entrybox import EntryBox
from .args import args
from .paths import paths
from .dialogs import Dialog
from .tips import tips
from .utils import utils
from .files import files
from .menus import Menu
from . import widgetutils


class InputControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.input: EntryBox
        self.autocomplete: List[str] = []

    def fill(self) -> None:
        from .widgets import widgets

        frame_data = widgets.frame_data_input
        self.input_label = widgetutils.make_label(frame_data, "Input")

        self.input = widgetutils.make_entry(frame_data)
        frame_data.expand()
        widgets.input = self.input
        widgets.input_frame = frame_data.frame
        ToolTip(self.input_label, tips["input"])
        ToolTip(self.input, tips["input"])

        if args.drag_and_drop:
            self.input.drop_target_register(DND_TEXT)  # type: ignore
            self.input.dnd_bind("<<Drop>>", lambda e: self.on_text_dropped(e))  # type: ignore

        prev_button = widgetutils.make_button(
            frame_data, "< Prev", lambda: self.history_up()
        )

        prev_button.set_bind("<Button-2>", lambda e: self.clear())
        ToolTip(prev_button, tips["prev_button"])

        next_button = widgetutils.make_button(
            frame_data, "Next >", lambda: self.history_down()
        )

        next_button.set_bind("<Button-2>", lambda e: self.clear())
        ToolTip(next_button, tips["next_button"])

        if args.write_button:
            write_button = widgetutils.make_button(
                frame_data, "Write", lambda: self.show_textbox()
            )

            write_button.set_bind("<Button-2>", lambda e: self.show_textbox(True))
            ToolTip(write_button, tips["write_button"])

        submit_button = widgetutils.make_button(
            frame_data, "Submit", lambda: self.submit(scroll=False)
        )

        submit_button.set_bind(
            "<Button-2>", lambda e: self.submit(scroll=False, no_history=True)
        )

        ToolTip(submit_button, tips["submit_button"])

        if not args.show_prevnext:
            prev_button.grid_remove()
            next_button.grid_remove()

        self.input.bind_mousewheel()

    def bind(self) -> None:
        self.input.bind("<Button-3>", lambda e: self.show_menu(e))

    def show_menu(self, event: Optional[Any] = None) -> None:
        from .widgets import widgets

        def action(text: str) -> None:
            if "\n" in text:
                self.show_textbox(text=text)
            else:
                self.set(text)

        widgets.show_menu_items("input", "inputs", lambda s: action(s), event)

    def focus(self) -> None:
        self.input.focus_set()
        self.input.on_focus_change("in")

    def apply_history(self, inputs: List[str]) -> None:
        text = inputs[self.history_index]
        self.set(text)
        self.input.focus_end()

    def get_history_list(
        self, force_no_cmds: bool = False, no_multi: bool = False
    ) -> List[str]:
        inputs = files.get_list("inputs")

        if no_multi:
            inputs = [i for i in inputs if (not "\n" in i)]

        if force_no_cmds or (not args.command_history):
            inputs = [i for i in inputs if (not commands.is_command(i))]

        return inputs

    def history_up(self) -> None:
        inputs = self.get_history_list(no_multi=True)

        if not inputs:
            return

        if self.history_index == -1:
            self.history_index = 0
        else:
            if self.history_index == len(inputs) - 1:
                self.clear()
                return

            self.history_index = (self.history_index + 1) % len(inputs)

        self.apply_history(inputs)

    def history_down(self) -> None:
        inputs = self.get_history_list(no_multi=True)

        if not inputs:
            return

        if self.history_index == -1:
            self.history_index = len(inputs) - 1
        else:
            if self.history_index == 0:
                self.clear()
                return

            self.history_index = (self.history_index - 1) % len(inputs)

        self.apply_history(inputs)

    def set(self, text: str) -> None:
        self.input.set_text(text)
        self.focus()

    def clear(self) -> None:
        self.input.clear()
        self.reset_history_index()

    def reset_history_index(self) -> None:
        self.history_index = -1

    def insert_name(self, who: str) -> None:
        name = getattr(config, f"name_{who}")
        text = self.input.get()

        if (not text) or text.endswith(" "):
            self.input.insert_text(name)
        else:
            self.input.insert_text(f" {name}")

        self.input.focus_end()

    def submit(
        self,
        tab_id: Optional[str] = None,
        text: Optional[str] = None,
        scroll: bool = True,
        file: Optional[str] = None,
        no_history: bool = False,
    ) -> None:
        from .model import model
        from .display import display
        from .widgets import widgets

        if not text:
            text = self.input.get().strip()

        if not tab_id:
            tab_id = display.current_tab

        tab = display.get_tab(tab_id)

        if not tab:
            return

        if not file:
            file = widgets.file.get().strip()

        if text or file:
            self.clear()
            widgets.file.clear(False)

            if not text:
                if args.fill_prompt:
                    if config.mode == "image":
                        text = args.image_prompt

            if text:
                if args.commands:
                    if commands.exec(text):
                        if args.command_history:
                            files.add_input(text)

                        self.add_words(text)

                        return

                files.add_input(text)
                self.add_words(text)

            if tab.mode == "ignore":
                return

            display.to_bottom()

            if model.model_loading:
                return

            prompt = {"text": text, "file": file, "no_history": no_history}

            files.add_system(config.system)
            files.add_model(config.model)

            if file:
                files.add_file(file)

            widgets.show_model()
            model.stream(prompt, tab.tab_id)
        elif scroll:
            display.toggle_scroll()

    def setup(self) -> None:
        path = paths.autocomplete

        if path.exists() and path.is_file():
            try:
                self.autocomplete = files.load(path)
            except BaseException as e:
                utils.error(e)
                self.autocomplete = []
        else:
            self.autocomplete = []

        self.check()

    def check(self) -> None:
        from .display import display

        text = args.input.strip()
        file = args.file.strip()

        if (not text) and (not file):
            return

        tab_id = display.current_tab

        if args.clean_slate:
            is_command = text and commands.is_command(text)

            if not is_command:
                if not display.tab_is_empty(tab_id):
                    tab_id = display.make_tab()

        if not tab_id:
            return

        self.submit(tab_id=tab_id, text=text, file=file)

    def add_words(self, text: str) -> None:
        from . import terminal

        if not args.input_memory:
            return

        words = text.split()
        added = False

        for word in words:
            clean_word = utils.clean_text(word)
            len_words = len(clean_word)

            if len_words < args.input_memory_min:
                continue

            if len_words > args.input_memory_max:
                continue

            if commands.is_command(clean_word):
                continue

            if clean_word not in self.autocomplete:
                self.autocomplete.append(clean_word)
                terminal.add_word(clean_word)
                added = True

            n = args.input_memory_max_items
            self.autocomplete = self.autocomplete[-n:]

        if added:
            files.save(paths.autocomplete, self.autocomplete)

    def show_textbox(self, maxed: bool = False, text: Optional[str] = None) -> None:
        from .textbox import TextBox

        def on_right_click(event: Any, textbox: TextBox) -> None:
            menu = Menu()

            text = textbox.get_text()
            menu.add(text="Copy", command=lambda e: textbox.copy())
            menu.add(text="Paste", command=lambda e: textbox.paste())

            if text:
                menu.add(text="Clear", command=lambda e: textbox.clear())

            inputs = self.get_history_list()
            items = inputs[: args.max_list_items]

            if items:
                menu.add(text="--- Recent ---", disabled=True)

            def add_item(item: str) -> None:
                def proc() -> None:
                    textbox.set_text(item)
                    textbox.focus_end()

                f_text = utils.bullet_points(item[: args.list_item_width])
                f_text = utils.replace_linebreaks(f_text)
                menu.add(text=f_text, command=lambda e: proc())

            for item in items:
                add_item(item)

            menu.show(event)

        def action(ans: Dict[str, Any]) -> None:
            self.submit(text=ans["text"], scroll=False)

        if not text:
            text = self.input.get().strip()

        self.clear()

        Dialog.show_textbox(
            "input",
            "Write an input",
            lambda a: action(a),
            on_right_click=on_right_click,
            value=text,
            start_maximized=maxed,
        )

    def input_command(self, arg: Optional[str] = None, maxed: bool = False) -> None:
        if arg:
            self.submit(text=arg)
        else:
            self.show_textbox(maxed=maxed)

    def paste(self) -> None:
        utils.paste(self.input)

    def on_text_dropped(self, event: Any) -> None:
        self.set(event.data)


inputcontrol = InputControl()
