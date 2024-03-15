# Modules
from .config import config
from .app import app
from .display import Display
from .tooltips import ToolTip
from .enums import Fill
from .menus import Menu
from .entrybox import EntryBox
from . import widgetutils
from . import commands

# Libraries
from llama_cpp.llama_chat_format import LlamaChatCompletionHandlerRegistry as formats  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any
from tkinter import filedialog
from typing import Optional, Any, Callable


right_padding = 11


class Widgets:
    def __init__(self) -> None:
        self.input_history_index = -1

        def get_frame(bottom_padding: Optional[int] = None) -> tk.Frame:
            return widgetutils.make_frame(bottom_padding=bottom_padding)

        # Model
        frame = get_frame()
        self.model_frame = frame

        widgetutils.make_label(frame, "Model")
        self.model = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)
        ToolTip(self.model, "Path to a model file. This should be a file that works with"
                " llama.cpp, like gguf files for instance.")

        self.load_button = widgetutils.make_button(frame, "Load", lambda: self.load_or_unload())
        ToolTip(self.load_button, "Load or unload the model")

        self.main_menu_button = widgetutils.make_button(frame, "Menu", right_padding=right_padding)
        ToolTip(self.main_menu_button, "Open the main menu")

        # System
        frame = get_frame()
        self.system_frame = frame

        widgetutils.make_label(frame, "System")
        self.system = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)
        ToolTip(self.system, "This sets the system prompt. You can use keywords like @name_user, @name_ai, and @date")

        self.cpu_label = widgetutils.make_label(frame, "CPU")
        self.cpu = tk.StringVar()
        self.cpu_text = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.cpu_text.configure(textvariable=self.cpu)
        ToolTip(self.cpu_text, "Current CPU usage")
        self.cpu.set("000%")

        self.ram_label = widgetutils.make_label(frame, "RAM")
        self.ram = tk.StringVar()
        self.ram_text = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.ram_text.configure(textvariable=self.ram)
        ToolTip(self.ram_text, "Current RAM usage")
        self.ram.set("000%")

        self.temp_label = widgetutils.make_label(frame, "TMP")
        self.temp = tk.StringVar()
        self.temp_text = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.temp_text.configure(textvariable=self.temp)
        ToolTip(self.temp_text, "Current CPU temperature")
        self.temp.set("000°C")

        # Details
        frame = get_frame()
        self.details_frame = frame

        widgetutils.make_label(frame, "User")
        self.name_user = widgetutils.make_entry(frame)
        ToolTip(self.name_user, "The name of the user (you)")

        widgetutils.make_label(frame, "AI")
        self.name_ai = widgetutils.make_entry(frame)
        ToolTip(self.name_ai, "The name of the assistant (AI)")

        widgetutils.make_label(frame, "Temp")
        self.temperature = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.temperature, "The temperature parameter is used to control"
                " the randomness of the output. A higher temperature (~1) results in more randomness"
                " and diversity in the generated text, as the model is more likely to"
                " explore a wider range of possible tokens. Conversely, a lower temperature"
                " (<1) produces more focused and deterministic output, emphasizing the"
                " most probable tokens.")

        widgetutils.make_label(frame, "Format")
        values = ["auto"]
        fmts = [item for item in formats._chat_handlers]
        fmts.sort()
        values.extend(fmts)
        self.format = widgetutils.make_combobox(frame, values=values, width=17, right_padding=right_padding)
        ToolTip(self.format, "That will format the prompt according to how model expects it."
                " Auto is supposed to work with newer models that include the format in the metadata."
                " Check llama-cpp-python to find all the available formats.")

        # Tuning
        frame = get_frame()
        self.tuning_frame = frame

        widgetutils.make_label(frame, "Tokens")
        self.max_tokens = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.max_tokens, "Maximum number of tokens to generate."
                " Higher values will result in longer output, but will"
                " also take longer to compute.")

        widgetutils.make_label(frame, "Context")
        self.context = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.context, "The number of previous messages to include as the context."
                " The computation will take longer with more context."
                " 0 means context is not used at all.")

        widgetutils.make_label(frame, "Seed")
        self.seed = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.seed, "The seed to use for sampling."
                " The same seed should generate the same or similar results."
                " -1 means no seed is used.")

        widgetutils.make_label(frame, "Top K")
        self.top_k = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.top_k, "The top-k parameter limits the model's"
                " predictions to the top k most probable tokens at each step"
                " of generation. By setting a value for k, you are instructing"
                " the model to consider only the k most likely tokens."
                " This can help in fine-tuning the generated output and"
                " ensuring it adheres to specific patterns or constraints.")

        widgetutils.make_label(frame, "Top P")
        self.top_p = widgetutils.make_entry(frame, width=config.entry_width_small)
        ToolTip(self.top_p, "Top-p, also known as nucleus sampling, controls"
                " the cumulative probability of the generated tokens."
                " The model generates tokens until the cumulative probability"
                " exceeds the chosen threshold (p). This approach allows for"
                " more dynamic control over the length of the generated text"
                " and encourages diversity in the output by including less"
                " probable tokens when necessary.")

        # Buttons
        frame = get_frame()

        self.stop_button = widgetutils.make_button(frame, "Stop", lambda: self.stop(), fill=Fill.HORIZONTAL)
        ToolTip(self.stop_button, "Stop generating the current response")

        self.new_button = widgetutils.make_button(frame, "New", lambda: self.display.make_tab(), fill=Fill.HORIZONTAL)
        ToolTip(self.new_button, "Add a new tab")

        self.clear_button = widgetutils.make_button(frame, "Clear",
                                                    lambda: self.display.clear_output(), fill=Fill.HORIZONTAL)
        ToolTip(self.clear_button, "Clear the output of the current tab")

        self.close_button = widgetutils.make_button(
            frame, "Close", lambda: self.display.close_tab(
                show_close_all=True), fill=Fill.HORIZONTAL)
        ToolTip(self.close_button, "Close the current tab")

        self.log_button = widgetutils.make_button(frame, "Log",
                                                  lambda: self.display.save_log(), fill=Fill.HORIZONTAL)
        ToolTip(self.log_button, "Save the output to a log file")

        self.top_button = widgetutils.make_button(frame, "Top", lambda: self.display.output_top(),
                                                  fill=Fill.HORIZONTAL, right_padding=right_padding)
        ToolTip(self.top_button, "Scroll to the top of the output")

        # Output
        app.root.grid_rowconfigure(widgetutils.frame_number, weight=1)

        frame = get_frame()

        notebook = widgetutils.make_notebook(frame, fill=Fill.BOTH, right_padding=right_padding)
        self.display = Display(notebook)

        # Bottom
        frame = get_frame()

        self.bottom_button = widgetutils.make_button(frame, "Go To Bottom",
                                                     lambda: self.display.output_bottom(), fill=Fill.HORIZONTAL,
                                                            right_padding=right_padding, pady=2)
        ToolTip(self.bottom_button, "Scroll to the bottom of the output")

        # Addons
        frame = get_frame()
        self.addons_frame = frame

        widgetutils.make_label(frame, "Prepend")
        self.prepend = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)
        ToolTip(self.prepend, "Add this to the beginning of the prompt")

        widgetutils.make_label(frame, "Append")
        self.append = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL, right_padding=right_padding)
        ToolTip(self.append, "Add this to the end of the prompt")

        # Input
        frame = get_frame(bottom_padding=10)
        widgetutils.make_label(frame, "Input")
        self.input = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)
        ToolTip(self.input, "The prompt for the AI. The prompt is a message that the AI will respond to.")

        input_history_up_button = widgetutils.make_button(frame, "< Prev", lambda: self.input_history_up())
        ToolTip(input_history_up_button, "Previous item in the input history")

        input_history_up_down = widgetutils.make_button(frame, "Next >", lambda: self.input_history_down())
        ToolTip(input_history_up_down, "Next item in the input history")

        submit_button = widgetutils.make_button(frame, "Submit", lambda: self.submit(), right_padding=right_padding)
        ToolTip(submit_button, "Send the prompt to the AI")

        self.main_menu = Menu()
        self.models_menu = Menu()
        self.systems_menu = Menu()
        self.prepends_menu = Menu()
        self.appends_menu = Menu()
        self.inputs_menu = Menu()
        self.stop_button_enabled = True
        self.load_button_enabled = True
        self.format_select_enabled = True
        self.bottom_button_enabled = True
        self.top_button_enabled = True

    def get_widget(self, key: str) -> Optional[tk.Widget]:
        if hasattr(self, key):
            widget = getattr(self, key)
            assert isinstance(widget, tk.Widget)
            return widget
        else:
            return None

    def fill(self) -> None:
        for key in config.defaults():
            self.fill_widget(key, getattr(config, key))

    def fill_widget(self, key: str, value: Any, focus: bool = False) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if type(widget) == EntryBox:
            widgetutils.set_text(widget, value)

            if focus:
                widget.focus_set()
        elif type(widget) == ttk.Combobox:
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        from . import keyboard

        if self.display.num_tabs() == 0:
            self.display.make_tab()

        self.fill()
        self.setup_main_menu()
        self.setup_binds()
        self.setup_widgets()
        self.focus_input()
        self.add_generic_menus()
        self.disable_bottom_button()
        self.setup_monitors()
        self.start_checks()

        keyboard.setup()

    def setup_monitors(self) -> None:
        self.cpu_label.bind("<Button-1>", lambda e: app.open_task_manager())
        self.cpu_text.bind("<Button-1>", lambda e: app.open_task_manager())
        self.ram_label.bind("<Button-1>", lambda e: app.open_task_manager())
        self.ram_text.bind("<Button-1>", lambda e: app.open_task_manager())
        self.temp_label.bind("<Button-1>", lambda e: app.open_task_manager())
        self.temp_text.bind("<Button-1>", lambda e: app.open_task_manager())

    def setup_widgets(self) -> None:
        from . import state

        def setup_entrybox(key: str, placeholder: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            if type(widget) != EntryBox:
                return

            widget.key = key
            widget.placeholder = placeholder
            widget.check_placeholder()

        def setup_combobox(key: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            widget.bind("<<ComboboxSelected>>", lambda e: state.update_config(key))

        setup_entrybox("input", "Ask something to the AI")
        setup_entrybox("name_user", "Name")
        setup_entrybox("name_ai", "Name")
        setup_entrybox("context", "Int")
        setup_entrybox("system", "Instructions to the AI")
        setup_entrybox("max_tokens", "Int")
        setup_entrybox("temperature", "Float")
        setup_entrybox("seed", "Int")
        setup_entrybox("top_k", "Int")
        setup_entrybox("top_p", "Float")
        setup_entrybox("model", "Path to a model file")
        setup_entrybox("prepend", "Add before")
        setup_entrybox("append", "Add after")
        setup_combobox("format")

    def setup_binds(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_model_menu(e))
        self.system.bind("<Button-3>", lambda e: self.show_system_menu(e))
        self.prepend.bind("<Return>", lambda e: self.submit())
        self.prepend.bind("<Button-3>", lambda e: self.show_prepend_menu(e))
        self.append.bind("<Return>", lambda e: self.submit())
        self.append.bind("<Button-3>", lambda e: self.show_append_menu(e))
        self.input.bind("<Button-3>", lambda e: self.show_input_menu(e))
        self.input.bind("<Return>", lambda e: self.submit())

    def setup_main_menu(self) -> None:
        from .session import session
        from . import state

        self.main_menu.add(text="Recent Models", command=lambda: self.show_model_menu())
        self.main_menu.add(text="Browse Models", command=lambda: self.browse_models())
        self.main_menu.separator()
        self.main_menu.add(text="Save Config", command=lambda: state.save_config_state())
        self.main_menu.add(text="Load Config", command=lambda: state.load_config_state())
        self.main_menu.add(text="Reset Config", command=lambda: state.reset_config())
        self.main_menu.separator()
        self.main_menu.add(text="Save Session", command=lambda: session.save_state())
        self.main_menu.add(text="Load Session", command=lambda: session.load_state())
        self.main_menu.separator()
        self.main_menu.add(text="Open Logs", command=lambda: state.open_logs_dir())
        self.main_menu.separator()
        self.main_menu.add(text="Compact", command=lambda: app.toggle_compact())
        self.main_menu.add(text="Resize", command=lambda: app.resize())
        self.main_menu.add(text="About", command=lambda: app.show_about())
        self.main_menu.separator()
        self.main_menu.add(text="Exit", command=lambda: app.exit())
        self.main_menu_button.set_bind("<ButtonRelease-1>", self.show_main_menu)

    def focus_input(self) -> None:
        self.input.focus_set()

    def apply_input_history(self) -> None:
        text = config.inputs[self.input_history_index]
        self.set_input(text)

    def input_history_up(self) -> None:
        if not self.input.get():
            self.reset_history_index()

        if not config.inputs:
            return

        if self.input_history_index == -1:
            self.input_history_index = 0
        else:
            if self.input_history_index == len(config.inputs) - 1:
                self.clear_input()
                return
            else:
                self.input_history_index = (self.input_history_index + 1) % len(config.inputs)

        self.apply_input_history()

    def input_history_down(self) -> None:
        if not config.inputs:
            return

        if self.input_history_index == -1:
            self.input_history_index = len(config.inputs) - 1
        else:
            if self.input_history_index == 0:
                self.clear_input()
                return
            else:
                self.input_history_index = (self.input_history_index - 1) % len(config.inputs)

        self.apply_input_history()

    def add_common_commands(self, menu: Menu, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if not widget:
            return

        if (type(widget) == EntryBox) or (type(widget) == tk.Text):
            menu.add(text="Copy", command=lambda: self.copy(key))
            menu.add(text="Paste", command=lambda: self.paste(key))

            if key in config.clearables:
                menu.add(text="Clear", command=lambda: self.clear(key))

        if config.get_default(key):
            menu.add(text="Reset", command=lambda: state.reset_one_config(key))

    def show_menu_items(self, key_config: str, key_list: str, command: Callable[..., Any],
                        event: Optional[Any] = None) -> None:
        menu = getattr(self, f"{key_list}_menu")
        menu.clear()
        items = getattr(config, key_list)[:config.max_list_items]
        self.add_common_commands(menu, key_config)

        if items:
            menu.add(text="--- Recent ---", disabled=True)

            for item in items:
                def proc(item: str = item) -> None:
                    command(item)

                menu.add(text=item[:80], command=proc)

        if event:
            menu.show(event)
        else:
            widget = self.get_widget(key_config)

            if widget:
                menu.show(widget=widget)

                if items:
                    menu.select_item(4)

    def show_model_menu(self, event: Optional[Any] = None) -> None:
        from .model import model

        if model.model_loading:
            return

        self.show_menu_items("model", "models", lambda m: self.set_model(m), event)

    def show_system_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("system", "systems", lambda s: self.set_system(s), event)

    def show_prepend_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("prepend", "prepends", lambda s: self.set_prepend(s), event)

    def show_append_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("append", "appends", lambda s: self.set_append(s), event)

    def show_input_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("input", "inputs", lambda s: self.set_input(s), event)

    def browse_models(self) -> None:
        from . import state
        from .model import model

        if model.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=state.get_models_dir())

        if file:
            widgetutils.set_text(self.model, file)
            state.update_config("model")
            model.load()

    def submit(self) -> None:
        from .model import model
        from . import state
        text = self.input.get()

        if text:
            self.display.output_bottom()
            self.clear_input()
            state.add_input(text)

            if commands.check(text):
                return

            if model.model_loading:
                return

            model.stream(text, self.display.current_tab)
        else:
            self.display.output_bottom()

    def clear_input(self) -> None:
        self.input.clear()
        self.reset_history_index()

    def reset_history_index(self) -> None:
        self.input_history_index = -1

    def prompt(self, who: str, tab_id: str = "") -> None:
        avatar = getattr(config, f"avatar_{who}")
        name = getattr(config, f"name_{who}")

        if name:
            prompt = f"\n{avatar} {name} : "
        else:
            prompt = f"\n{avatar} : "

        if not tab_id:
            tab_id = self.display.current_tab

        self.display.print(prompt, False, tab_id=tab_id)
        output = self.display.get_output(tab_id)

        if not output:
            return

        start_index = output.index(f"end - {len(prompt)}c")
        end_index = output.index("end - 3c")
        output.tag_add(f"name_{who}", start_index, end_index)

    def set_model(self, m: str) -> None:
        from . import state
        from .model import model

        widgetutils.set_text(self.model, m)

        if state.update_config("model"):
            model.load()

    def show_intro(self, tab_id: str = "") -> None:
        for line in config.intro:
            self.display.print(line, tab_id=tab_id)

    def show_model(self) -> None:
        widgetutils.set_text(self.model, config.model)

    def show_main_menu(self, event: Optional[Any] = None) -> None:
        if event:
            self.main_menu.show(event)
        else:
            self.main_menu.show(widget=self.main_menu_button)

    def add_generic_menus(self) -> None:
        def add_menu(key: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            menu = Menu()
            self.add_common_commands(menu, key)

            if key not in ["model", "system", "prepend", "append", "input"]:
                widget.bind("<Button-3>", lambda e: menu.show(e))

        for key in config.defaults():
            add_menu(key)
            add_menu("input")

    def enable_stop_button(self) -> None:
        if (not self.stop_button_enabled) and app.exists():
            self.stop_button.style("green")
            self.stop_button_enabled = True

    def disable_stop_button(self) -> None:
        if self.stop_button_enabled and app.exists():
            self.stop_button.style("disabled")
            self.stop_button_enabled = False

    def enable_load_button(self) -> None:
        if (not self.load_button_enabled) and app.exists():
            self.load_button.style("normal")
            self.load_button_enabled = True

    def disable_load_button(self) -> None:
        if self.load_button_enabled and app.exists():
            self.load_button.style("disabled")
            self.load_button_enabled = False

    def enable_format_select(self) -> None:
        if (not self.format_select_enabled) and app.exists():
            self.format.configure(style="Normal.TCombobox")
            self.enable_widget(self.format)
            self.format_select_enabled = True

    def disable_format_select(self) -> None:
        if self.format_select_enabled and app.exists():
            self.format.configure(style="Disabled.TCombobox")
            self.disable_widget(self.format)
            self.format_select_enabled = False

    def enable_bottom_button(self) -> None:
        if (not self.bottom_button_enabled) and app.exists():
            self.bottom_button.style("normal")
            self.bottom_button_enabled = True

    def disable_bottom_button(self) -> None:
        if self.bottom_button_enabled and app.exists():
            self.bottom_button.style("disabled")
            self.bottom_button_enabled = False

    def enable_top_button(self) -> None:
        if (not self.top_button_enabled) and app.exists():
            self.top_button.style("normal")
            self.top_button_enabled = True

    def disable_top_button(self) -> None:
        if self.top_button_enabled and app.exists():
            self.top_button.style("disabled")
            self.top_button_enabled = False

    def enable_widget(self, widget: ttk.Widget) -> None:
        widget.state(["!disabled"])

    def disable_widget(self, widget: ttk.Widget) -> None:
        widget.state(["disabled"])

    def do_checks(self) -> None:
        from .model import model

        if model.streaming:
            self.enable_stop_button()
        else:
            self.disable_stop_button()

        if model.model_loading:
            self.disable_load_button()
            self.disable_format_select()
        else:
            self.enable_load_button()
            self.enable_format_select()

        if model.loaded_model:
            self.load_button.set_text("Unload")
        else:
            self.load_button.set_text("Load")

        self.display.check_scroll_buttons()

    def start_checks(self) -> None:
        self.do_checks()
        app.root.after(200, self.start_checks)

    def set_input(self, text: str) -> None:
        widgetutils.set_text(self.input, text, move=True)

    def set_system(self, text: str) -> None:
        from . import state
        widgetutils.set_text(self.system, text)
        state.update_config("system")

    def set_prepend(self, text: str) -> None:
        from . import state
        widgetutils.set_text(self.prepend, text)
        state.update_config("prepend")

    def set_append(self, text: str) -> None:
        from . import state
        widgetutils.set_text(self.append, text)
        state.update_config("append")

    def stop(self) -> None:
        from .model import model
        model.stop_stream()

    def load(self) -> None:
        from .model import model

        if model.model_loading:
            return

        self.focus_input()
        model.load()

    def unload(self) -> None:
        from .model import model

        if model.model_loading:
            return

        self.focus_input()
        model.unload(True)

    def load_or_unload(self) -> None:
        from .model import model

        if model.loaded_format:
            self.unload()
        else:
            self.load()

    def copy(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if not widget:
            return

        if type(widget) == EntryBox:
            widgetutils.copy(widget.get())
            widget.focus_set()
            state.update_config(key)

    def paste(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or (type(widget) != EntryBox):
            return

        widgetutils.paste(widget)
        widget.focus_set()
        state.update_config(key)

    def clear(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or ((type(widget) != EntryBox)
                            and (type(widget) != tk.Text)):
            return

        widgetutils.clear_text(widget)
        widget.focus_set()
        state.update_config(key)

    def esckey(self) -> None:
        from .model import model
        widget = self.get_widget("input")
        assert isinstance(widget, EntryBox)

        if widget.get():
            self.clear_input()
        elif model.streaming:
            self.stop()
        else:
            self.display.output_bottom()

    def show_context(self) -> None:
        widget = app.root.focus_get()

        if widget == self.input:
            self.show_input_menu()
        elif widget == self.prepend:
            self.show_prepend_menu()
        elif widget == self.append:
            self.show_append_menu()
        elif widget == self.model:
            self.show_model_menu()
        elif widget == self.system:
            self.show_system_menu()


widgets: Widgets = Widgets()
