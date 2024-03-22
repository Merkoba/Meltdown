# Modules
from .config import config
from .app import app
from .tooltips import ToolTip
from .enums import Fill
from .menus import Menu
from .entrybox import EntryBox
from .inputcontrol import inputcontrol
from .args import args
from . import widgetutils

# Libraries
from llama_cpp.llama_chat_format import LlamaChatCompletionHandlerRegistry as formats  # type: ignore

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any
from typing import Optional, Any, Callable


right_padding = config.right_padding


class Widgets:
    def __init__(self) -> None:
        self.input: EntryBox

    def make(self) -> None:
        from .display import display

        # Model
        self.model_frame = widgetutils.make_frame()

        widgetutils.make_label(self.model_frame, "Model")
        self.model = widgetutils.make_entry(self.model_frame, fill=Fill.HORIZONTAL)
        ToolTip(self.model, "Path to a model file. This should be a file that works with"
                " llama.cpp, like gguf files for instance. It can also be a specific ChatGPT model."
                " Check the main menu on the right to load the available models")

        self.model_icon = widgetutils.make_label(self.model_frame, "", colons=False)
        self.model_icon_tooltip = ToolTip(self.model_icon, "")

        self.load_button = widgetutils.make_button(self.model_frame, "Load", lambda: self.load_or_unload())
        ToolTip(self.load_button, "Load or unload the model")

        self.main_menu_button = widgetutils.make_button(self.model_frame, "Menu",
                                                        lambda e: self.show_main_menu(e),
                                                        right_padding=right_padding)
        ToolTip(self.main_menu_button, "Open the main menu")

        # System
        self.system_frame = widgetutils.make_frame()

        widgetutils.make_label(self.system_frame, "System")

        monitors_disabled = (not args.monitors) or \
            ((not args.monitor_cpu) and (not args.monitor_ram) and (not args.monitor_temp))

        if monitors_disabled:
            rpadding = right_padding
        else:
            rpadding = 0

        self.system = widgetutils.make_entry(self.system_frame, fill=Fill.HORIZONTAL, right_padding=rpadding)
        ToolTip(self.system, "This sets the system prompt. You can use keywords like @name_user, @name_ai, and @date")

        if not monitors_disabled:
            if args.monitor_cpu:
                self.cpu_label = widgetutils.make_label(self.system_frame, "CPU")
                self.cpu_label.configure(cursor="hand2")
                self.cpu = tk.StringVar()
                self.cpu_text = widgetutils.make_label(self.system_frame, "", padx=0)
                self.cpu_text.configure(textvariable=self.cpu)
                self.cpu_text.configure(cursor="hand2")
                ToolTip(self.cpu_text, "Current CPU usage")
                self.cpu.set("000%")

            if args.monitor_ram:
                self.ram_label = widgetutils.make_label(self.system_frame, "RAM")
                self.ram_label.configure(cursor="hand2")
                self.ram = tk.StringVar()
                self.ram_text = widgetutils.make_label(self.system_frame, "", padx=0)
                self.ram_text.configure(textvariable=self.ram)
                self.ram_text.configure(cursor="hand2")
                ToolTip(self.ram_text, "Current RAM usage")
                self.ram.set("000%")

            if args.monitor_temp:
                self.temp_label = widgetutils.make_label(self.system_frame, "TMP")
                self.temp_label.configure(cursor="hand2")
                self.temp = tk.StringVar()
                self.temp_text = widgetutils.make_label(self.system_frame, "", padx=0, right_padding=right_padding)
                self.temp_text.configure(textvariable=self.temp)
                self.temp_text.configure(cursor="hand2")
                ToolTip(self.temp_text, "Current CPU temperature")
                self.temp.set("000°")

        # Details Container
        self.details_frame = widgetutils.make_frame()
        detail_button_info = "Scroll this row. Middle click for instant"

        frame_1 = widgetutils.make_inner_frame(self.details_frame, 0)
        self.details_button_left = widgetutils.make_button(frame_1, "<", lambda: widgets.details_left(), style="alt", width=5)
        ToolTip(self.details_button_left, detail_button_info)

        self.details, self.details_canvas = widgetutils.make_scrollable_frame(self.details_frame, 1)

        frame_3 = widgetutils.make_inner_frame(self.details_frame, 2)
        self.details_button_right = widgetutils.make_button(frame_3, ">",
                                                            lambda: widgets.details_right(), right_padding=right_padding, style="alt", width=5)
        ToolTip(self.details_button_right, detail_button_info)

        self.details_frame.columnconfigure(1, weight=1)

        # Details Widgets
        widgetutils.make_label(self.details, "User", padx=0)
        self.name_user = widgetutils.make_entry(self.details)
        ToolTip(self.name_user, "The name of the user (you)")

        widgetutils.make_label(self.details, "AI")
        self.name_ai = widgetutils.make_entry(self.details)
        ToolTip(self.name_ai, "The name of the assistant (AI)")

        widgetutils.make_label(self.details, "Context")
        self.context = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.context, "The number of previous messages to include as the context."
                " The computation will take longer with more context"
                " 0 means context is not used at all")

        widgetutils.make_label(self.details, "Tokens")
        self.max_tokens = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.max_tokens, "Maximum number of tokens to generate."
                " Higher values will result in longer output, but will"
                " also take longer to compute")

        widgetutils.make_label(self.details, "Temp")
        self.temperature = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.temperature, "The temperature parameter is used to control"
                " the randomness of the output. A higher temperature (~1) results in more randomness"
                " and diversity in the generated text, as the model is more likely to"
                " explore a wider range of possible tokens. Conversely, a lower temperature"
                " (<1) produces more focused and deterministic output, emphasizing the"
                " most probable tokens")

        widgetutils.make_label(self.details, "Seed")
        self.seed = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.seed, "The seed to use for sampling."
                " The same seed should generate the same or similar results."
                " -1 means no seed is used")

        widgetutils.make_label(self.details, "Top K")
        self.top_k = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.top_k, "The top-k parameter limits the model's"
                " predictions to the top k most probable tokens at each step"
                " of generation. By setting a value for k, you are instructing"
                " the model to consider only the k most likely tokens."
                " This can help in fine-tuning the generated output and"
                " ensuring it adheres to specific patterns or constraints")

        widgetutils.make_label(self.details, "Top P")
        self.top_p = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.top_p, "Top-p, also known as nucleus sampling, controls"
                " the cumulative probability of the generated tokens."
                " The model generates tokens until the cumulative probability"
                " exceeds the chosen threshold (p). This approach allows for"
                " more dynamic control over the length of the generated text"
                " and encourages diversity in the output by including less"
                " probable tokens when necessary")

        widgetutils.make_label(self.details, "Threads")
        self.threads = widgetutils.make_entry(self.details, width=app.theme.entry_width_small)
        ToolTip(self.threads, "The number of CPU threads to use")

        widgetutils.make_label(self.details, "Format")
        values = ["auto"]
        fmts = sorted([item for item in formats._chat_handlers])
        values.extend(fmts)
        self.format = widgetutils.make_combobox(self.details, values=values, width=17)
        ToolTip(self.format, "That will format the prompt according to how model expects it."
                " Auto is supposed to work with newer models that include the format in the metadata."
                " Check llama-cpp-python to find all the available formats")

        widgetutils.make_label(self.details, "M-Lock")
        self.mlock = widgetutils.make_combobox(self.details, width=app.theme.combobox_width_small, values=["yes", "no"])
        ToolTip(self.mlock, "Keep the model in memory")

        # Buttons
        self.button_frame = widgetutils.make_frame()

        self.stop_button = widgetutils.make_button(self.button_frame, "Stop", lambda: self.stop(), fill=Fill.HORIZONTAL)
        ToolTip(self.stop_button, "Stop generating the current response")

        self.new_button = widgetutils.make_button(self.button_frame, "New", lambda: display.make_tab(), fill=Fill.HORIZONTAL)
        ToolTip(self.new_button, "Add a new tab")

        self.close_button = widgetutils.make_button(
            self.button_frame, "Close", lambda: display.close_tab(), fill=Fill.HORIZONTAL)
        ToolTip(self.close_button, "Close the current tab")

        self.clear_button = widgetutils.make_button(self.button_frame, "Clear",
                                                    lambda: display.clear(), fill=Fill.HORIZONTAL)
        ToolTip(self.clear_button, "Clear the output of the current tab")

        self.log_button = widgetutils.make_button(self.button_frame, "Log",
                                                  lambda: display.save_log(), fill=Fill.HORIZONTAL)
        ToolTip(self.log_button, "Save the output to a log file")

        self.top_button = widgetutils.make_button(self.button_frame, "Top", lambda: display.to_top(),
                                                  fill=Fill.HORIZONTAL)
        ToolTip(self.top_button, "Scroll to the top of the output")

        self.output_menu = widgetutils.make_button(self.button_frame, "#", lambda e: display.show_output_menu(e),
                                                   fill=Fill.HORIZONTAL, right_padding=right_padding, width=3)
        ToolTip(self.output_menu, "Open the output menu")

        # Output
        app.root.grid_rowconfigure(widgetutils.frame_number, weight=1)
        self.output_frame = widgetutils.make_frame()

        self.notebook = widgetutils.make_notebook(self.output_frame, fill=Fill.BOTH, right_padding=right_padding)

        # Addons
        self.addons_frame = widgetutils.make_frame()

        widgetutils.make_label(self.addons_frame, "Prepend")
        self.prepend = widgetutils.make_entry(self.addons_frame, fill=Fill.HORIZONTAL)
        ToolTip(self.prepend, "Add this to the beginning of the prompt")

        widgetutils.make_label(self.addons_frame, "Append")
        self.append = widgetutils.make_entry(self.addons_frame, fill=Fill.HORIZONTAL, right_padding=right_padding)
        ToolTip(self.append, "Add this to the end of the prompt")

        # Input
        self.input_frame = widgetutils.make_frame(bottom_padding=10)

        self.main_menu = Menu()
        self.models_menu = Menu()
        self.gpt_menu = Menu()
        self.systems_menu = Menu()
        self.prepends_menu = Menu()
        self.appends_menu = Menu()
        self.inputs_menu = Menu()
        self.stop_button_enabled = True
        self.load_button_enabled = True
        self.format_select_enabled = True
        self.top_button_enabled = True
        self.current_details = 1

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

        if isinstance(widget, EntryBox):
            widget.set_text(value)

            if focus:
                widget.focus_set()
        elif isinstance(widget, ttk.Combobox):
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        from .display import display

        if display.num_tabs() == 0:
            display.make_tab()

        inputcontrol.fill()

        self.fill()
        self.setup_details()
        self.setup_main_menu()
        self.setup_gpt_menu()
        self.setup_binds()
        self.setup_widgets()
        self.add_generic_menus()
        self.setup_monitors()
        self.start_checks()
        self.check_details_buttons()

        inputcontrol.focus()

    def setup_details(self) -> None:
        app.root.update_idletasks()
        self.details.update_idletasks()
        self.details_canvas.update_idletasks()
        self.details_canvas.configure(width=self.details.winfo_reqwidth())
        self.details_canvas.configure(height=self.details.winfo_reqheight())

        self.details_button_left.set_bind("<Button-4>", lambda e: widgets.details_left())
        self.details_button_left.set_bind("<Button-5>", lambda e: widgets.details_right())
        self.details_button_left.set_bind("<Button-2>", lambda e: widgets.details_start())

        self.details_button_right.set_bind("<Button-4>", lambda e: widgets.details_left())
        self.details_button_right.set_bind("<Button-5>", lambda e: widgets.details_right())
        self.details_button_right.set_bind("<Button-2>", lambda e: widgets.details_end())

        self.details.bind("<Button-4>", lambda e: widgets.details_left())
        self.details.bind("<Button-5>", lambda e: widgets.details_right())

        for child in self.details.winfo_children():
            child.bind("<Button-4>", lambda e: widgets.details_left())
            child.bind("<Button-5>", lambda e: widgets.details_right())

    def setup_monitors(self) -> None:
        if args.monitor_cpu:
            self.cpu_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.cpu_text.bind("<Button-1>", lambda e: app.open_task_manager())

        if args.monitor_ram:
            self.ram_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.ram_text.bind("<Button-1>", lambda e: app.open_task_manager())

        if args.monitor_temp:
            self.temp_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.temp_text.bind("<Button-1>", lambda e: app.open_task_manager())

    def setup_widgets(self) -> None:
        from . import state

        def setup_entrybox(key: str, placeholder: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            if not isinstance(widget, EntryBox):
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
        setup_entrybox("threads", "Int")

        setup_combobox("format")
        setup_combobox("mlock")

    def setup_binds(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_model_menu(e))
        self.system.bind("<Button-3>", lambda e: self.show_system_menu(e))
        self.prepend.bind("<Button-3>", lambda e: self.show_prepend_menu(e))
        self.append.bind("<Button-3>", lambda e: self.show_append_menu(e))
        inputcontrol.bind()

    def setup_main_menu(self) -> None:
        from .session import session
        from .model import model
        from . import state

        self.main_menu.add(text="Recent Models", command=lambda: self.show_model_menu(require_items=True))
        self.main_menu.add(text="Browse Models", command=lambda: model.browse_models())
        self.main_menu.add(text="Use GPT Model", command=lambda: self.show_gpt_menu())
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
        self.main_menu.add(text="Theme", command=lambda: app.toggle_theme())
        self.main_menu.add(text="About", command=lambda: app.show_about())
        self.main_menu.separator()
        self.main_menu.add(text="Exit", command=lambda: app.exit())

    def setup_gpt_menu(self) -> None:
        from .model import model

        for gpt in model.gpts:
            self.gpt_menu.add(text=gpt[1], command=lambda gpt=gpt: self.use_gpt(gpt[0]))

    def add_common_commands(self, menu: Menu, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if not widget:
            return

        if (isinstance(widget, EntryBox)) or (isinstance(widget, tk.Text)):
            menu.add(text="Copy", command=lambda: self.copy(key))
            menu.add(text="Paste", command=lambda: self.paste(key))

            if key in config.clearables:
                menu.add(text="Clear", command=lambda: self.clear(key))

        if config.get_default(key):
            menu.add(text="Reset", command=lambda: state.reset_one_config(key))

    def show_menu_items(self, key_config: str, key_list: str, command: Callable[..., Any],
                        event: Optional[Any] = None, require_items: bool = False) -> None:
        from .dialogs import Dialog
        menu = getattr(self, f"{key_list}_menu")
        menu.clear()
        items = getattr(config, key_list)[:config.max_list_items]

        if require_items:
            if not items:
                Dialog.show_message("No items yet")
                return

        self.add_common_commands(menu, key_config)
        num_common = len(menu.items)

        if items:
            menu.add(text="--- Recent ---", disabled=True)

            for item in items:
                def proc(item: str = item) -> None:
                    command(item)

                menu.add(text=item[:config.list_item_width], command=proc)

        if event:
            menu.show(event)
        else:
            widget = self.get_widget(key_config)

            if widget:
                menu.show(widget=widget)

                if items:
                    menu.select_item(num_common + 1)

    def show_model_menu(self, event: Optional[Any] = None, require_items: bool = False) -> None:
        from .model import model

        if model.model_loading:
            return

        self.show_menu_items("model", "models",
                             lambda m: self.set_model(m), event, require_items=require_items)

    def show_system_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("system", "systems", lambda s: self.set_system(s), event)

    def show_prepend_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("prepend", "prepends", lambda s: self.set_prepend(s), event)

    def show_append_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("append", "appends", lambda s: self.set_append(s), event)

    def set_model(self, m: str) -> None:
        from . import state
        from .model import model
        self.model.set_text(m)

        if state.update_config("model"):
            model.load()

    def show_model(self) -> None:
        self.model.set_text(config.model)

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
            self.stop_button.set_style("green")
            self.stop_button_enabled = True

    def disable_stop_button(self) -> None:
        if self.stop_button_enabled and app.exists():
            self.stop_button.set_style("disabled")
            self.stop_button_enabled = False

    def enable_load_button(self) -> None:
        if (not self.load_button_enabled) and app.exists():
            self.load_button.set_style("normal")
            self.load_button_enabled = True

    def disable_load_button(self) -> None:
        if self.load_button_enabled and app.exists():
            self.load_button.set_style("disabled")
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

    def enable_top_button(self) -> None:
        if (not self.top_button_enabled) and app.exists():
            self.top_button.set_style("normal")
            self.top_button_enabled = True

    def disable_top_button(self) -> None:
        if self.top_button_enabled and app.exists():
            self.top_button.set_style("disabled")
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

        model_empty = self.model.get() == ""

        if (model.loaded_format == "gpt_remote") or \
                model.model_loading or (model_empty and (not model.loaded_model)):
            self.disable_load_button()
            self.disable_format_select()
        else:
            self.enable_load_button()
            self.enable_format_select()

        if model.loaded_model:
            self.load_button.set_text("Unload")
        else:
            self.load_button.set_text("Load")

    def start_checks(self) -> None:
        self.do_checks()
        app.root.after(200, self.start_checks)

    def set_system(self, text: str) -> None:
        from . import state
        self.system.set_text(text)
        state.update_config("system")

    def set_prepend(self, text: str) -> None:
        from . import state
        self.prepend.set_text(text)
        state.update_config("prepend")

    def set_append(self, text: str) -> None:
        from . import state
        self.append.set_text(text)
        state.update_config("append")

    def stop(self) -> None:
        from .model import model
        from .display import display
        display.to_bottom()
        model.stop_stream()

    def load_or_unload(self) -> None:
        from .model import model
        model.load_or_unload()

    def copy(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if not widget:
            return

        if isinstance(widget, EntryBox):
            widgetutils.copy(widget.get())
            widget.focus_set()
            state.update_config(key)

    def paste(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        widgetutils.paste(widget)
        widget.focus_set()
        state.update_config(key)

    def clear(self, key: str) -> None:
        from . import state
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        widget.clear()
        widget.focus_set()
        state.update_config(key)

    def esckey(self) -> None:
        from .model import model
        from .display import display

        widget = self.get_widget("input")
        assert isinstance(widget, EntryBox)

        if widget.get():
            inputcontrol.clear()
        elif model.streaming:
            self.stop()
        else:
            display.to_bottom()

    def show_context(self) -> None:
        widget = app.root.focus_get()

        if widget == self.input:
            inputcontrol.show_menu()
        elif widget == self.prepend:
            self.show_prepend_menu()
        elif widget == self.append:
            self.show_append_menu()
        elif widget == self.model:
            self.show_model_menu()
        elif widget == self.system:
            self.show_system_menu()

    def details_left(self) -> None:
        self.details_canvas.xview_scroll(-2, "units")
        self.check_details_buttons()

    def details_right(self) -> None:
        self.details_canvas.xview_scroll(2, "units")
        self.check_details_buttons()

    def details_start(self) -> None:
        self.details_canvas.xview_moveto(0)
        self.check_details_buttons()

    def details_end(self) -> None:
        self.details_canvas.xview_moveto(1.0)
        self.check_details_buttons()

    def check_details_buttons(self) -> None:
        scroll_pos_left = self.details_canvas.xview()[0]
        scroll_pos_right = self.details_canvas.xview()[1]
        ToolTip.hide_all()

        if scroll_pos_left == 0:
            self.details_button_left.set_style("disabled")
        else:
            self.details_button_left.set_style("alt")

        if scroll_pos_right == 1.0:
            self.details_button_right.set_style("disabled")
        else:
            self.details_button_right.set_style("alt")

    def use_gpt(self, name: str) -> None:
        from .model import model
        from . import state
        state.set_config("model", name)

    def show_gpt_menu(self) -> None:
        self.gpt_menu.show(widget=self.main_menu_button)


widgets: Widgets = Widgets()
