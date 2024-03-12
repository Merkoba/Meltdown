# Modules
from .config import config
from . import widgetutils
from .app import app
from .display import Display
from .tooltips import ToolTip
from .enums import Fill
from .menus import Menu

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

        widgetutils.make_label(frame, "CPU")
        self.cpu = tk.StringVar()
        self.cpu_label = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.cpu_label.configure(textvariable=self.cpu)
        self.cpu.set("000%")

        widgetutils.make_label(frame, "RAM")
        self.ram = tk.StringVar()
        self.ram_label = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.ram_label.configure(textvariable=self.ram)
        self.ram.set("000%")

        widgetutils.make_label(frame, "TMP")
        self.temp = tk.StringVar()
        self.temp_label = widgetutils.make_label(frame, "", right_padding=right_padding)
        self.temp_label.configure(textvariable=self.temp)
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

        self.bottom_button = widgetutils.make_button(frame, "Go To Bottom", lambda: self.display.output_bottom(), fill=Fill.HORIZONTAL)
        ToolTip(self.bottom_button, "Scroll to the bottom of the output")

        # Addons
        frame = get_frame()
        self.addons_frame = frame

        widgetutils.make_label(frame, "Prepend")
        self.prepend = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)

        widgetutils.make_label(frame, "Append")
        self.append = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL, right_padding=right_padding)

        # Input
        frame = get_frame(bottom_padding=10)
        widgetutils.make_label(frame, "Input")
        self.input = widgetutils.make_entry(frame, fill=Fill.HORIZONTAL)

        input_history_up_button = widgetutils.make_button(frame, "< Prev", lambda: self.input_history_up())
        ToolTip(input_history_up_button, "Previous item in the input history")

        input_history_up_down = widgetutils.make_button(frame, "Next >", lambda: self.input_history_down())
        ToolTip(input_history_up_down, "Next item in the input history")

        submit_button = widgetutils.make_button(frame, "Submit", lambda: self.submit(), right_padding=right_padding)
        ToolTip(submit_button, "Use the input as the prompt for the AI")

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

    def fill_widget(self, key: str, value: Any) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if type(widget) == ttk.Entry or type(widget) == tk.Text:
            widgetutils.set_text(widget, value)
        elif type(widget) == ttk.Combobox:
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        from . import state
        from .session import session

        if self.display.num_tabs() == 0:
            self.display.make_tab()

        self.fill()

        self.main_menu.add(text="Recent Models", command=lambda: self.show_recent_models())
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
        self.main_menu_button.bind("<ButtonRelease-1>", lambda e: self.show_main_menu(e))

        self.model.bind("<Button-3>", lambda e: self.show_recent_models(e))
        self.system.bind("<Button-3>", lambda e: self.show_recent_systems(e))
        self.prepend.bind("<Return>", lambda e: self.submit())
        self.prepend.bind("<Button-3>", lambda e: self.show_recent_prepends(e))
        self.append.bind("<Return>", lambda e: self.submit())
        self.append.bind("<Button-3>", lambda e: self.show_recent_appends(e))
        self.input.bind("<Button-3>", lambda e: self.show_recent_inputs(e))

        self.input.bind("<Return>", lambda e: self.submit())
        self.input.bind("<Escape>", lambda e: self.esckey())

        def bind(key: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            if type(widget) == ttk.Entry or type(widget) == tk.Text:
                on = "<FocusOut>"
            elif type(widget) == ttk.Combobox:
                on = "<<ComboboxSelected>>"

            widget.bind(on, lambda e: state.update_config(key))

        bind("name_user")
        bind("name_ai")
        bind("context")
        bind("system")
        bind("max_tokens")
        bind("temperature")
        bind("seed")
        bind("top_k")
        bind("top_p")
        bind("format")
        bind("model")
        bind("prepend")
        bind("append")

        self.input_history_index: int
        self.reset_history_index()

        def on_key(event: Any) -> None:
            # Focus the input and insert char
            ftypes = [ttk.Combobox, ttk.Notebook, ttk.Button, tk.Text]

            if type(event.widget) in ftypes:
                if (len(event.keysym.strip()) == 1) or (event.keysym == "slash"):
                    self.focus_input()
                    self.input.insert(tk.END, event.char)
            # Input history Up or Down
            elif event.widget == self.input:
                if event.keysym == "Up":
                    self.input_history_up()
                elif event.keysym == "Down":
                    self.input_history_down()

        app.root.bind("<KeyPress>", on_key)

        self.focus_input()
        self.add_generic_menus()
        self.disable_bottom_button()
        self.start_checks()

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

        if (type(widget) == ttk.Entry) or (type(widget) == tk.Text):
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
        menu.add(text="--- Recent ---", disabled=True)

        for item in items:
            def proc(item: str = item) -> None:
                command(item)

            menu.add(text=item[:80], command=proc)

        menu.show(event)

    def show_recent_models(self, event: Optional[Any] = None) -> None:
        from .model import model

        if model.model_loading:
            return

        self.show_menu_items("model", "models", lambda m: self.set_model(m), event)

    def show_recent_systems(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("system", "systems", lambda s: self.set_system(s), event)

    def show_recent_prepends(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("prepend", "prepends", lambda s: self.set_prepend(s), event)

    def show_recent_appends(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("append", "appends", lambda s: self.set_append(s), event)

    def show_recent_inputs(self, event: Optional[Any] = None) -> None:
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

            if self.check_command(text):
                return

            if model.model_loading:
                return

            model.stream(text, self.display.current_tab)

    def check_command(self, text: str) -> bool:
        if not text.startswith("/"):
            return False

        if text == "/clear":
            self.display.clear_output()
            return True
        elif text == "/config":
            config.show_config()
            return True
        elif text == "/exit" or text == "/quit":
            app.exit()
            return True
        elif text == "/session":
            from .session import session
            self.display.print(session.to_json())
            return True

        return False

    def clear_input(self) -> None:
        widgetutils.clear_text(self.input)
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

    def update(self) -> None:
        app.root.update_idletasks()

    def show_main_menu(self, event: Any) -> None:
        self.main_menu.show(event)

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
            self.stop_button.configure(style="Green.TButton")
            self.enable_widget(self.stop_button)
            self.stop_button_enabled = True

    def disable_stop_button(self) -> None:
        if self.stop_button_enabled and app.exists():
            self.stop_button.configure(style="Disabled.TButton")
            self.disable_widget(self.stop_button)
            self.stop_button_enabled = False

    def enable_load_button(self) -> None:
        if (not self.load_button_enabled) and app.exists():
            self.load_button.configure(style="Normal.TButton")
            self.enable_widget(self.load_button)
            self.load_button_enabled = True

    def disable_load_button(self) -> None:
        if self.load_button_enabled and app.exists():
            self.load_button.configure(style="Disabled.TButton")
            self.disable_widget(self.load_button)
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
            self.bottom_button.configure(style="Normal.TButton")
            self.enable_widget(self.bottom_button)
            self.bottom_button_enabled = True

    def disable_bottom_button(self) -> None:
        if self.bottom_button_enabled and app.exists():
            self.bottom_button.configure(style="Disabled.TButton")
            self.disable_widget(self.bottom_button)
            self.bottom_button_enabled = False

    def enable_top_button(self) -> None:
        if (not self.top_button_enabled) and app.exists():
            self.top_button.configure(style="Normal.TButton")
            self.enable_widget(self.top_button)
            self.top_button_enabled = True

    def disable_top_button(self) -> None:
        if self.top_button_enabled and app.exists():
            self.top_button.configure(style="Disabled.TButton")
            self.disable_widget(self.top_button)
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
            self.load_button.configure(text="Unload")
        else:
            self.load_button.configure(text="Load")

        self.display.output_scroll()

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

        model.load()

    def unload(self) -> None:
        from .model import model

        if model.model_loading:
            return

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

        if type(widget) == ttk.Entry:
            widgetutils.copy(widget.get())
            state.update_config(key)

    def paste(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or (type(widget) != ttk.Entry):
            return

        widgetutils.paste(widget)
        state.update_config(key)

    def clear(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or ((type(widget) != ttk.Entry)
                            and (type(widget) != tk.Text)):
            return

        widgetutils.clear_text(widget)
        state.update_config(key)

    def esckey(self) -> None:
        widget = self.get_widget("input")
        assert isinstance(widget, ttk.Entry)

        if widget.get():
            self.clear_input()
        else:
            self.stop()


widgets: Widgets = Widgets()
