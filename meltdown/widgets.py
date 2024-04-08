# Standard
import tkinter as tk
from tkinter import ttk
from typing import Optional, Any, Callable

# Libraries
from llama_cpp.llama_chat_format import LlamaChatCompletionHandlerRegistry as formats  # type: ignore

# Modules
from .args import args
from .app import app
from .config import config
from .tooltips import ToolTip
from .enums import Fill
from .menus import Menu
from .dialogs import Dialog
from .entrybox import EntryBox
from .inputcontrol import inputcontrol
from .display import display
from .commands import commands
from .logs import logs
from .framedata import FrameData
from . import widgetutils


class Widgets:
    def __init__(self) -> None:
        self.input: EntryBox
        pass

    def make(self) -> None:
        right_padding = app.theme.right_padding

        # Model
        app.main_frame.grid_columnconfigure(FrameData.frame_number, weight=1)
        frame_data_model = widgetutils.make_frame()
        self.model_frame = frame_data_model.frame

        self.model_label = widgetutils.make_label(frame_data_model, "Model")
        self.model = widgetutils.make_entry(frame_data_model)
        frame_data_model.expand()
        self.model.bind_mousewheel()
        tip = "Path to a model file. This should be a file that works with" \
            " llama.cpp, like gguf files for instance. It can also be a specific ChatGPT model." \
            " Check the main menu on the right to load the available models"
        ToolTip(self.model_label, tip)
        ToolTip(self.model, tip)

        self.model_icon = widgetutils.make_label(frame_data_model, "", colons=False)
        self.model_icon_tooltip = ToolTip(self.model_icon, "")

        if not args.model_icon:
            self.model_icon.grid_remove()

        self.load_button = widgetutils.make_button(frame_data_model, "Load", lambda: self.load_or_unload())
        ToolTip(self.load_button, "Load or unload the model")

        self.main_menu_button = widgetutils.make_button(frame_data_model, "Menu",
                                                        lambda e: self.show_main_menu(e),
                                                        right_padding=right_padding)
        ToolTip(self.main_menu_button, "Open the main menu")

        # System
        frame_data_system = widgetutils.make_frame()
        self.system_frame = frame_data_system.frame

        self.system_label = widgetutils.make_label(frame_data_system, "System")

        self.system_disabled = (not args.system) or \
            ((not args.system_cpu) and (not args.system_ram) and (not args.system_temp))

        if self.system_disabled:
            rpadding = right_padding
        else:
            rpadding = 0

        kc = args.keychar
        self.system = widgetutils.make_entry(frame_data_system, right_padding=rpadding)
        frame_data_system.expand()
        self.system.bind_mousewheel()
        tip = f"This sets the system prompt. You can use keywords like {kc}name_user, {kc}name_ai, and {kc}date"
        ToolTip(self.system_label, tip)
        ToolTip(self.system, tip)

        if not self.system_disabled:
            monitors = []

            if args.system_cpu:
                monitors.append("cpu")

            if args.system_ram:
                monitors.append("ram")

            if args.system_temp:
                monitors.append("tmp")

            if args.system_cpu:
                if "cpu" == monitors[-1]:
                    rightpad = right_padding
                else:
                    rightpad = None

                self.cpu_label = widgetutils.make_label(frame_data_system, "CPU")
                self.cpu_label.configure(cursor="hand2")
                self.cpu = tk.StringVar()
                self.cpu_text = widgetutils.make_label(frame_data_system, "", padx=0, right_padding=rightpad)
                self.cpu_text.configure(textvariable=self.cpu)
                self.cpu_text.configure(cursor="hand2")
                tip = "Current CPU usage"
                ToolTip(self.cpu_label, tip)
                ToolTip(self.cpu_text, tip)
                self.cpu.set("000%")

            if args.system_ram:
                if "ram" == monitors[-1]:
                    rightpad = right_padding
                else:
                    rightpad = None

                self.ram_label = widgetutils.make_label(frame_data_system, "RAM")
                self.ram_label.configure(cursor="hand2")
                self.ram = tk.StringVar()
                self.ram_text = widgetutils.make_label(frame_data_system, "", padx=0, right_padding=rightpad)
                self.ram_text.configure(textvariable=self.ram)
                self.ram_text.configure(cursor="hand2")
                tip = "Current RAM usage"
                ToolTip(self.ram_label, tip)
                ToolTip(self.ram_text, tip)
                self.ram.set("000%")

            if args.system_temp:
                if "tmp" == monitors[-1]:
                    rightpad = right_padding
                else:
                    rightpad = None

                self.temp_label = widgetutils.make_label(frame_data_system, "TMP")
                self.temp_label.configure(cursor="hand2")
                self.temp = tk.StringVar()
                self.temp_text = widgetutils.make_label(frame_data_system, "", padx=0, right_padding=rightpad)
                self.temp_text.configure(textvariable=self.temp)
                self.temp_text.configure(cursor="hand2")
                tip = "Current CPU temperature"
                ToolTip(self.temp_label, tip)
                ToolTip(self.temp_text, tip)
                self.temp.set("000°")

        # Details Container
        frame_data_details = widgetutils.make_frame()
        self.details_frame = frame_data_details.frame
        detail_button_info = "Scroll this row. Middle click for instant"

        frame_1 = widgetutils.make_frame(self.details_frame, col=0, row=0)
        self.details_button_left = widgetutils.make_button(frame_1, "<", lambda: widgets.details_left(), style="alt")
        ToolTip(self.details_button_left, detail_button_info)

        self.details, self.details_canvas = widgetutils.make_scrollable_frame(self.details_frame, 1)

        frame_3 = widgetutils.make_frame(self.details_frame, col=2, row=0)
        self.details_button_right = widgetutils.make_button(frame_3, ">",
                                                            lambda: widgets.details_right(), right_padding=right_padding, style="alt")
        ToolTip(self.details_button_right, detail_button_info)

        self.details_frame.columnconfigure(1, weight=1)

        # Details Widgets
        details_data = FrameData(self.details)
        self.name_user_label = widgetutils.make_label(details_data, "User", padx=0)
        self.name_user = widgetutils.make_entry(details_data)
        tip = "The name of the user (You)"
        ToolTip(self.name_user_label, tip)
        ToolTip(self.name_user, tip)

        self.name_ai_label = widgetutils.make_label(details_data, "AI")
        self.name_ai = widgetutils.make_entry(details_data)
        tip = "The name of the assistant (AI)"
        ToolTip(self.name_ai_label, tip)
        ToolTip(self.name_ai, tip)

        self.context_label = widgetutils.make_label(details_data, "Context")
        self.context = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "The number of previous messages to include as the context." \
            " The computation will take longer with more context." \
            " 0 means context is not used at all"
        ToolTip(self.context_label, tip)
        ToolTip(self.context, tip)

        self.max_tokens_label = widgetutils.make_label(details_data, "Tokens")
        self.max_tokens = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "Maximum number of tokens to generate." \
            " Higher values will result in longer output, but will" \
            " also take longer to compute"
        ToolTip(self.max_tokens_label, tip)
        ToolTip(self.max_tokens, tip)

        self.temperature_label = widgetutils.make_label(details_data, "Temp")
        self.temperature = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "The temperature parameter is used to control" \
            " the randomness of the output. A higher temperature (~1) results in more randomness" \
            " and diversity in the generated text, as the model is more likely to" \
            " explore a wider range of possible tokens. Conversely, a lower temperature" \
            " (<1) produces more focused and deterministic output, emphasizing the" \
            " most probable tokens"
        ToolTip(self.temperature_label, tip)
        ToolTip(self.temperature, tip)

        self.seed_label = widgetutils.make_label(details_data, "Seed")
        self.seed = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "The seed to use for sampling." \
            " The same seed should generate the same or similar results." \
            " -1 means no seed is used"
        ToolTip(self.seed_label, tip)
        ToolTip(self.seed, tip)

        self.top_p_label = widgetutils.make_label(details_data, "Top-P")
        self.top_p = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "Top-p, also known as nucleus sampling, controls" \
            " the cumulative probability of the generated tokens." \
            " The model generates tokens until the cumulative probability" \
            " exceeds the chosen threshold (p). This approach allows for" \
            " more dynamic control over the length of the generated text" \
            " and encourages diversity in the output by including less" \
            " probable tokens when necessary"
        ToolTip(self.top_p_label, tip)
        ToolTip(self.top_p, tip)

        self.top_k_label = widgetutils.make_label(details_data, "Top-K")
        self.top_k = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "(Not applied to GPT) The Top-k parameter limits the model's" \
            " predictions to the top k most probable tokens at each step" \
            " of generation. By setting a value for k, you are instructing" \
            " the model to consider only the k most likely tokens." \
            " This can help in fine-tuning the generated output and" \
            " ensuring it adheres to specific patterns or constraints"
        ToolTip(self.top_k_label, tip)
        ToolTip(self.top_k, tip)

        self.threads_label = widgetutils.make_label(details_data, "Threads")
        self.threads = widgetutils.make_entry(details_data, width=app.theme.entry_width_small)
        tip = "The number of CPU threads to use"
        ToolTip(self.threads_label, tip)
        ToolTip(self.threads, tip)

        self.format_label = widgetutils.make_label(details_data, "Format")
        values = ["auto"]
        fmts = sorted([item for item in formats._chat_handlers])
        values.extend(fmts)
        self.format = widgetutils.make_combobox(details_data, values=values, width=17)
        tip = "That will format the prompt according to how model expects it." \
            " Auto is supposed to work with newer models that include the format in the metadata." \
            " Check llama-cpp-python to find all the available formats"
        ToolTip(self.format_label, tip)
        ToolTip(self.format, tip)

        self.mlock_label = widgetutils.make_label(details_data, "M-Lock")
        self.mlock = widgetutils.make_combobox(details_data, width=app.theme.combobox_width_small, values=["yes", "no"])
        tip = "Keep the model in memory"
        ToolTip(self.mlock_label, tip)
        ToolTip(self.mlock, tip)

        # Buttons
        frame_data_buttons = widgetutils.make_frame()
        self.buttons_frame = frame_data_buttons.frame

        self.stop_button = widgetutils.make_button(frame_data_buttons, "Stop", lambda: self.stop())
        frame_data_buttons.expand()
        ToolTip(self.stop_button, "Stop generating the current response")

        self.new_button = widgetutils.make_button(frame_data_buttons, "New", lambda: display.make_tab())
        frame_data_buttons.expand()
        ToolTip(self.new_button, "Make a new tab")

        self.close_button = widgetutils.make_button(
            frame_data_buttons, "Close", lambda: display.close_tab())
        frame_data_buttons.expand()
        ToolTip(self.close_button, "Close the current tab")

        self.clear_button = widgetutils.make_button(frame_data_buttons, "Clear",
                                                    lambda: display.clear())
        frame_data_buttons.expand()
        ToolTip(self.clear_button, "Clear the conversation")

        self.top_button = widgetutils.make_button(frame_data_buttons, "Top", lambda: display.to_top())
        frame_data_buttons.expand()
        ToolTip(self.top_button, "Scroll to the top")

        self.output_menu = widgetutils.make_button(frame_data_buttons, "More", lambda e: display.show_output_menu(e),
                                                   right_padding=right_padding)
        frame_data_buttons.expand()
        ToolTip(self.output_menu, "Show more options")

        if not args.more_button:
            self.output_menu.grid_remove()

        # Display
        app.main_frame.grid_rowconfigure(FrameData.frame_number, weight=1)
        frame_data_display = widgetutils.make_frame()
        self.display_frame = frame_data_display.frame
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        # Addons
        frame_data_addons = widgetutils.make_frame()
        self.addons_frame = frame_data_addons.frame

        self.prepend_label = widgetutils.make_label(frame_data_addons, "Prepend")
        self.prepend = widgetutils.make_entry(frame_data_addons)
        frame_data_addons.expand()
        tip = "Add this to the beginning of the prompt"
        ToolTip(self.prepend_label, tip)
        ToolTip(self.prepend, tip)

        self.append_label = widgetutils.make_label(frame_data_addons, "Append")
        self.append = widgetutils.make_entry(frame_data_addons, right_padding=right_padding)
        frame_data_addons.expand()
        tip = "Add this to the end of the prompt"
        ToolTip(self.append_label, tip)
        ToolTip(self.append, tip)

        # Input
        self.frame_data_input = widgetutils.make_frame(bottom_padding=10)
        self.input_frame = self.frame_data_input.frame

        self.main_menu = Menu()
        self.models_menu = Menu()
        self.gpt_menu = Menu()
        self.systems_menu = Menu()
        self.prepends_menu = Menu()
        self.appends_menu = Menu()
        self.inputs_menu = Menu()
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
        inputcontrol.fill()

        self.fill()
        self.setup_details()
        self.setup_main_menu()
        self.setup_gpt_menu()
        self.setup_binds()
        self.setup_widgets()
        self.add_generic_menus()
        self.setup_system()
        self.check_details_buttons()
        self.setup_tooltips()

        inputcontrol.focus()

        if display.num_tabs() == 0:
            display.make_tab()
        else:
            display.select_last_tab()

    def setup_tooltips(self) -> None:
        for key in config.defaults():
            widget = self.get_widget(key)

            if not widget:
                continue

            tooltip = ToolTip.get_tooltip(widget)

            if not tooltip:
                continue

            tooltip.append_text(f"({key})")

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

    def setup_system(self) -> None:
        if self.system_disabled:
            return

        if args.system_cpu:
            self.cpu_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.cpu_text.bind("<Button-1>", lambda e: app.open_task_manager())

        if args.system_ram:
            self.ram_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.ram_text.bind("<Button-1>", lambda e: app.open_task_manager())

        if args.system_temp:
            self.temp_label.bind("<Button-1>", lambda e: app.open_task_manager())
            self.temp_text.bind("<Button-1>", lambda e: app.open_task_manager())

    def setup_widgets(self) -> None:
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

            widget.bind("<<ComboboxSelected>>", lambda e: config.update(key))

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
        self.model_icon.bind("<Button-1>", lambda e: self.model_icon_click())
        self.main_menu_button.set_bind("<Button-2>", lambda e: app.show_about())
        self.main_menu_button.set_bind("<Button-3>", lambda e: commands.show_palette())
        inputcontrol.bind()

    def setup_main_menu(self) -> None:
        from .model import model
        from .config import config
        from .session import session

        self.main_menu.add(text="Recent Models", command=lambda: self.show_model_menu(require_items=True))
        self.main_menu.add(text="Browse Models", command=lambda: model.browse_models())
        self.main_menu.separator()
        self.main_menu.add(text="Use GPT Model", command=lambda: self.show_gpt_menu())
        self.main_menu.add(text="Set API Key", command=lambda: model.set_api_key())
        self.main_menu.separator()
        self.main_menu.add(text="Configs", command=lambda: config.menu())
        self.main_menu.add(text="Sessions", command=lambda: session.menu())
        self.main_menu.add(text="Logs", command=lambda: logs.menu())
        self.main_menu.separator()
        self.main_menu.add(text="Commands", command=lambda: commands.show_palette())
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
        widget = self.get_widget(key)

        if not widget:
            return

        if (isinstance(widget, EntryBox)) or (isinstance(widget, tk.Text)):
            menu.add(text="Copy", command=lambda: self.copy(key))
            menu.add(text="Paste", command=lambda: self.paste(key))

            if key in config.clearables:
                menu.add(text="Clear", command=lambda: self.clear(key))

        if config.get_default(key):
            menu.add(text="Reset", command=lambda: config.reset_one(key))

    def show_menu_items(self, key_config: str, key_list: str, command: Callable[..., Any],
                        event: Optional[Any] = None, require_items: bool = False) -> None:

        menu = getattr(self, f"{key_list}_menu")
        menu.clear()
        items = getattr(config, key_list)[:args.max_list_items]

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

                menu.add(text=item[:args.list_item_width], command=proc)

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
        from .model import model
        self.model.set_text(m)
        config.update("model")
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
        if app.exists():
            self.stop_button.set_style("active")

    def disable_stop_button(self) -> None:
        if app.exists():
            self.stop_button.set_style("disabled")

    def enable_load_button(self) -> None:
        if app.exists():
            self.load_button.set_style("normal")

    def disable_load_button(self) -> None:
        if app.exists():
            self.load_button.set_style("disabled")

    def enable_format_select(self) -> None:
        if app.exists():
            self.format.configure(style="Normal.TCombobox")
            self.enable_widget(self.format)

    def disable_format_select(self) -> None:
        if app.exists():
            self.format.configure(style="Disabled.TCombobox")
            self.disable_widget(self.format)

    def enable_top_button(self) -> None:
        if app.exists():
            self.top_button.set_style("normal")

    def disable_top_button(self) -> None:
        if app.exists():
            self.top_button.set_style("disabled")

    def enable_widget(self, widget: ttk.Widget) -> None:
        widget.state(["!disabled"])

    def disable_widget(self, widget: ttk.Widget) -> None:
        widget.state(["disabled"])

    def set_system(self, text: str) -> None:
        self.system.set_text(text)
        config.update("system")

    def set_prepend(self, text: str) -> None:
        self.prepend.set_text(text)
        config.update("prepend")

    def set_append(self, text: str) -> None:
        self.append.set_text(text)
        config.update("append")

    def stop(self) -> None:
        from .model import model
        from .display import display
        display.to_bottom()
        model.stop_stream()

    def load_or_unload(self) -> None:
        from .model import model
        model.load_or_unload()

    def copy(self, key: str) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if isinstance(widget, EntryBox):
            widgetutils.copy(widget.get())
            widget.focus_set()
            config.update(key)

    def paste(self, key: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        widgetutils.paste(widget)
        widget.focus_set()
        config.update(key)

    def clear(self, key: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        widget.clear()
        widget.focus_set()
        config.update(key)

    def find_focused(self) -> bool:
        focused = app.root.focus_get()

        if isinstance(focused, EntryBox):
            if focused.name == "find":
                return True

        return False

    def model_focused(self) -> bool:
        focused = app.root.focus_get()
        return focused == self.model

    def esckey(self) -> None:
        from .model import model
        from .display import display

        if Dialog.current_dialog or Menu.current_menu:
            return

        if self.find_focused():
            return

        if self.input.get():
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
        config.set("model", name)
        model.load()

    def show_gpt_menu(self) -> None:
        self.gpt_menu.show(widget=self.main_menu_button)

    def model_icon_click(self) -> None:
        app.hide_all()


widgets: Widgets = Widgets()
