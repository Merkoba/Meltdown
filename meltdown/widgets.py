# Standard
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Optional, Any, Callable, Dict
from pathlib import Path

# Libraries
from llama_cpp.llama_chat_format import LlamaChatCompletionHandlerRegistry as formats  # type: ignore

# Modules
from .args import args
from .app import app
from .config import config
from .tooltips import ToolTip
from .menus import Menu
from .dialogs import Dialog
from .entrybox import EntryBox
from .inputcontrol import inputcontrol
from .display import display
from .commands import commands
from .framedata import FrameData
from .tips import tips
from .files import files
from .utils import utils
from . import widgetutils


class Widgets:
    def __init__(self) -> None:
        self.input: EntryBox
        self.canvas_scroll = 1
        self.url_enabled = True

        self.cpu: tk.StringVar
        self.ram: tk.StringVar
        self.temp: tk.StringVar
        self.gpu: tk.StringVar
        self.gpu_ram: tk.StringVar
        self.gpu_temp: tk.StringVar

        self.cpu_text: tk.Label
        self.ram_text: tk.Label
        self.temp_text: tk.Label
        self.gpu_text: tk.Label
        self.gpu_ram_text: tk.Label
        self.gpu_temp_text: tk.Label

    def make(self) -> None:
        # Model
        app.main_frame.grid_columnconfigure(FrameData.frame_number, weight=1)
        frame_data_model = widgetutils.make_frame()
        self.model_frame = frame_data_model.frame

        self.model_label = widgetutils.make_label(frame_data_model, "Model")
        self.model = widgetutils.make_entry(frame_data_model)
        frame_data_model.expand()
        self.model.bind_mousewheel()
        ToolTip(self.model_label, tips["model"])
        ToolTip(self.model, tips["model"])

        self.model_icon = widgetutils.make_label(frame_data_model, "", colons=False)
        self.model_icon_tooltip = ToolTip(self.model_icon, "")

        if not args.model_icon:
            self.model_icon.grid_remove()

        self.load_button = widgetutils.make_button(
            frame_data_model, "Load", lambda: self.load_or_unload()
        )

        ToolTip(self.load_button, tips["load_button"])

        self.model_menu_button = widgetutils.make_button(
            frame_data_model,
            "Model",
            lambda e: self.show_model_menu(e),
        )

        ToolTip(self.model_menu_button, tips["model_menu"])

        self.main_menu_button = widgetutils.make_button(
            frame_data_model, "Menu", lambda e: self.show_main_menu(e)
        )

        ToolTip(self.main_menu_button, tips["main_menu"])

        # System
        frame_data_system = widgetutils.make_frame()
        self.system_frame = frame_data_system.frame

        monitor_args = [
            args.system_cpu,
            args.system_ram,
            args.system_temp,
            args.system_gpu,
            args.system_gpu_ram,
            args.system_gpu_temp,
        ]

        self.system_disabled = (not args.system) or (not any(monitor_args))

        if not self.system_disabled:
            monitors = []

            if args.system_cpu:
                monitors.append("cpu")

            if args.system_ram:
                monitors.append("ram")

            if args.system_temp:
                monitors.append("temp")

            if args.system_gpu:
                monitors.append("gpu")

            if args.system_gpu_ram:
                monitors.append("gpu_ram")

            if args.system_gpu_temp:
                monitors.append("gpu_temp")

            def make_monitor(name: str, label_text: str) -> None:
                label = widgetutils.make_label(frame_data_system, label_text)
                label.configure(cursor="hand2")
                setattr(self, name, tk.StringVar())
                monitor_text = widgetutils.make_label(frame_data_system, "", padx=0)
                monitor_text.configure(textvariable=getattr(self, name))
                monitor_text.configure(cursor="hand2")
                setattr(self, f"{name}_text", monitor_text)
                tip = tips[f"system_{name}"]
                ToolTip(label, tip)
                ToolTip(monitor_text, tip)
                getattr(self, name).set("000%")

                label.bind("<Button-1>", lambda e: app.open_task_manager())
                monitor_text.bind("<Button-1>", lambda e: app.open_task_manager())

            if args.system_cpu:
                make_monitor("cpu", "CPU")

            if args.system_ram:
                make_monitor("ram", "RAM")

            if args.system_temp:
                make_monitor("temp", "TMP")

            if args.system_gpu:
                make_monitor("gpu", "GPU")

            if args.system_gpu_ram:
                make_monitor("gpu_ram", "GPU RAM")

            if args.system_gpu_temp:
                make_monitor("gpu_temp", "GPU TMP")

        # Details Container
        frame_data_details = widgetutils.make_frame()
        self.details_frame = frame_data_details.frame

        left_frame = widgetutils.make_frame(self.details_frame, col=0, row=0)
        left_frame.frame.grid_rowconfigure(0, weight=1)

        self.details_button_left = widgetutils.make_button(
            left_frame, "<", lambda: widgets.details_left(), style="alt"
        )

        ToolTip(self.details_button_left, tips["details_button"])

        self.details, self.details_canvas = widgetutils.make_scrollable_frame(
            self.details_frame, 1
        )

        right_frame = widgetutils.make_frame(self.details_frame, col=2, row=0)
        right_frame.frame.grid_rowconfigure(0, weight=1)

        self.details_button_right = widgetutils.make_button(
            right_frame,
            ">",
            lambda: widgets.details_right(),
            style="alt",
        )

        ToolTip(self.details_button_right, tips["details_button"])

        self.details_frame.columnconfigure(1, weight=1)

        # Details Widgets
        details_data = FrameData(self.details)

        avatar_width = 4
        self.user_label = widgetutils.make_label(details_data, "User", padx=0)
        ToolTip(self.user_label, tips["user_label"])

        self.avatar_user = widgetutils.make_entry(details_data, width=avatar_width)
        ToolTip(self.avatar_user, tips["avatar_user"])

        self.name_user = widgetutils.make_entry(details_data)
        ToolTip(self.name_user, tips["name_user"])

        self.ai_label = widgetutils.make_label(details_data, "AI")
        ToolTip(self.ai_label, tips["ai_label"])

        self.avatar_ai = widgetutils.make_entry(details_data, width=avatar_width)
        ToolTip(self.avatar_ai, tips["avatar_ai"])

        self.name_ai = widgetutils.make_entry(details_data)
        ToolTip(self.name_ai, tips["name_ai"])

        self.history_label = widgetutils.make_label(details_data, "History")

        self.history = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.history_label, tips["history"])
        ToolTip(self.history, tips["history"])

        self.context_label = widgetutils.make_label(details_data, "Context")

        self.context = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.context_label, tips["context"])
        ToolTip(self.context, tips["context"])

        self.max_tokens_label = widgetutils.make_label(details_data, "Max Tokens")

        self.max_tokens = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.max_tokens_label, tips["max_tokens"])
        ToolTip(self.max_tokens, tips["max_tokens"])

        self.threads_label = widgetutils.make_label(details_data, "Threads")

        self.threads = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.threads_label, tips["threads"])
        ToolTip(self.threads, tips["threads"])

        self.gpu_layers_label = widgetutils.make_label(details_data, "GPU Layers")

        self.gpu_layers = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.gpu_layers_label, tips["gpu_layers"])
        ToolTip(self.gpu_layers, tips["gpu_layers"])

        self.format_label = widgetutils.make_label(details_data, "Format")
        values = ["auto"]
        fmts = sorted([item for item in formats._chat_handlers])
        values.extend(fmts)
        self.format = widgetutils.make_combobox(details_data, values=values, width=17)
        ToolTip(self.format_label, tips["format"])
        ToolTip(self.format, tips["format"])

        self.mode_label = widgetutils.make_label(details_data, "Mode")

        self.mode = widgetutils.make_combobox(
            details_data,
            width=app.theme.combobox_width_small,
            values=["text", "image"],
        )

        ToolTip(self.mode_label, tips["mode"])
        ToolTip(self.mode, tips["mode"])

        self.temperature_label = widgetutils.make_label(details_data, "Temp")

        self.temperature = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.temperature_label, tips["temperature"])
        ToolTip(self.temperature, tips["temperature"])

        self.seed_label = widgetutils.make_label(details_data, "Seed")

        self.seed = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.seed_label, tips["seed"])
        ToolTip(self.seed, tips["seed"])

        self.top_p_label = widgetutils.make_label(details_data, "Top-P")

        self.top_p = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.top_p_label, tips["top_p"])
        ToolTip(self.top_p, tips["top_p"])

        self.top_k_label = widgetutils.make_label(details_data, "Top-K")

        self.top_k = widgetutils.make_entry(
            details_data, width=app.theme.entry_width_small
        )

        ToolTip(self.top_k_label, tips["top_k"])
        ToolTip(self.top_k, tips["top_k"])

        self.before_label = widgetutils.make_label(details_data, "Before")
        self.before = widgetutils.make_entry(details_data, width=11)
        self.before.bind_mousewheel()
        ToolTip(self.before_label, tips["before"])
        ToolTip(self.before, tips["before"])

        self.after_label = widgetutils.make_label(details_data, "After")
        self.after = widgetutils.make_entry(details_data, width=11)
        self.after.bind_mousewheel()
        ToolTip(self.after_label, tips["after"])
        ToolTip(self.after, tips["after"])

        self.stop_label = widgetutils.make_label(details_data, "Stop")
        self.stop = widgetutils.make_entry(details_data, width=11)
        ToolTip(self.stop_label, tips["stop"])
        ToolTip(self.stop, tips["stop"])

        self.mlock_label = widgetutils.make_label(details_data, "M-Lock")

        self.mlock = widgetutils.make_combobox(
            details_data, width=app.theme.combobox_width_small, values=["yes", "no"]
        )

        ToolTip(self.mlock_label, tips["mlock"])
        ToolTip(self.mlock, tips["mlock"])

        # Buttons
        frame_data_buttons = widgetutils.make_frame()
        self.buttons_frame = frame_data_buttons.frame

        self.stop_button = widgetutils.make_button(
            frame_data_buttons, "Stop", lambda: self.stop_stream()
        )

        frame_data_buttons.expand()
        ToolTip(self.stop_button, tips["stop_button"])

        self.new_button = widgetutils.make_button(
            frame_data_buttons, "New", lambda: display.make_tab()
        )

        frame_data_buttons.expand()
        ToolTip(self.new_button, tips["new_button"])

        self.close_button = widgetutils.make_button(
            frame_data_buttons, "Close", lambda: display.close_tab()
        )

        frame_data_buttons.expand()
        ToolTip(self.close_button, tips["close_button"])

        self.clear_button = widgetutils.make_button(
            frame_data_buttons, "Clear", lambda: display.clear()
        )

        frame_data_buttons.expand()
        ToolTip(self.clear_button, tips["clear_button"])

        self.top_button = widgetutils.make_button(
            frame_data_buttons, "Top", lambda: display.to_top()
        )

        frame_data_buttons.expand()
        ToolTip(self.top_button, tips["top_button"])

        self.more_menu_button = widgetutils.make_button(
            frame_data_buttons,
            "More",
            lambda e: self.show_more_menu(e),
        )

        ToolTip(self.more_menu_button, tips["more_menu"])

        if not args.more_button:
            self.more_menu_button.grid_remove()
        else:
            frame_data_buttons.expand()

        # Display
        app.main_frame.grid_rowconfigure(FrameData.frame_number, weight=1)
        frame_data_display = widgetutils.make_frame()
        self.display_frame = frame_data_display.frame
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        # URL
        frame_data_url = widgetutils.make_frame()
        self.url_frame = frame_data_url.frame
        self.url_label = widgetutils.make_label(frame_data_url, "URL")
        self.url = widgetutils.make_entry(frame_data_url)
        frame_data_url.expand()
        self.url.bind_mousewheel()
        ToolTip(self.url_label, tips["url"])
        ToolTip(self.url, tips["url"])

        self.browse_file_button = widgetutils.make_button(
            frame_data_url, "Browse", lambda: self.browse_file()
        )

        ToolTip(self.browse_file_button, tips["browse_file_button"])

        # Input
        self.frame_data_input = widgetutils.make_frame()
        self.input_frame = self.frame_data_input.frame

        self.models_menu = Menu()
        self.systems_menu = Menu()
        self.urls_menu = Menu()
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
            self.check_move_to_end(key)

            if focus:
                widget.focus_set()
        elif isinstance(widget, ttk.Combobox):
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        from .display import display

        inputcontrol.fill()

        self.fill()
        self.setup_details()
        self.setup_binds()
        self.setup_widgets()
        self.add_generic_menus()
        self.check_details_buttons()
        self.setup_tooltips()
        self.disable_stop_button()
        self.check_mode()

        inputcontrol.focus()

        if display.num_tabs() == 0:
            display.make_tab()
        else:
            display.select_last_tab()

    def append_tooltip(self, widget: tk.Widget, text: str) -> None:
        tooltip = ToolTip.get_tooltip(widget)

        if not tooltip:
            return

        tooltip.append_text(f"({text})")

    def setup_tooltips(self) -> None:
        for key in config.defaults():
            widget = self.get_widget(key)

            if widget:
                self.append_tooltip(widget, key)

            label = self.get_widget(f"{key}_label")

            if label:
                self.append_tooltip(label, key)

    def setup_details(self) -> None:
        app.root.update_idletasks()
        self.details.update_idletasks()
        self.details_canvas.update_idletasks()
        self.details_canvas.configure(width=self.details.winfo_reqwidth())
        self.details_canvas.configure(height=self.details.winfo_reqheight())

        self.details_button_left.set_bind(
            "<Button-4>", lambda e: widgets.details_left()
        )
        self.details_button_left.set_bind(
            "<Button-5>", lambda e: widgets.details_right()
        )
        self.details_button_left.set_bind(
            "<Button-2>", lambda e: widgets.details_start()
        )

        self.details_button_right.set_bind(
            "<Button-4>", lambda e: widgets.details_left()
        )
        self.details_button_right.set_bind(
            "<Button-5>", lambda e: widgets.details_right()
        )
        self.details_button_right.set_bind(
            "<Button-2>", lambda e: widgets.details_end()
        )

        self.details.bind("<Button-4>", lambda e: widgets.details_left())
        self.details.bind("<Button-5>", lambda e: widgets.details_right())

        for child in self.details.winfo_children():
            child.bind("<Button-4>", lambda e: widgets.details_left())
            child.bind("<Button-5>", lambda e: widgets.details_right())

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
            self.check_move_to_end(key)

        def setup_combobox(key: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            widget.bind("<<ComboboxSelected>>", lambda e: config.update(key))

        setup_entrybox("input", "Ask something to the AI")
        setup_entrybox("avatar_user", "")
        setup_entrybox("name_user", "Name")
        setup_entrybox("avatar_ai", "")
        setup_entrybox("name_ai", "Name")
        setup_entrybox("history", "Int")
        setup_entrybox("context", "Int")
        setup_entrybox("max_tokens", "Int")
        setup_entrybox("temperature", "Float")
        setup_entrybox("seed", "Int")
        setup_entrybox("top_k", "Int")
        setup_entrybox("top_p", "Float")
        setup_entrybox("model", "Path to a model file")
        setup_entrybox("before", "Text")
        setup_entrybox("after", "Text")
        setup_entrybox("url", "URL to a remote image or a local path")
        setup_entrybox("threads", "Int")
        setup_entrybox("gpu_layers", "Int")

        setup_combobox("format")
        setup_combobox("mlock")
        setup_combobox("mode")

    def setup_binds(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_model_context(e))
        self.url.bind("<Button-3>", lambda e: self.show_url_menu(e))
        self.model_icon.bind("<Button-1>", lambda e: self.model_icon_click())
        self.main_menu_button.set_bind("<Button-2>", lambda e: app.show_about())
        self.main_menu_button.set_bind("<Button-3>", lambda e: commands.show_palette())
        inputcontrol.bind()

    def add_common_commands(self, menu: Menu, key: str) -> None:
        config.update(key)
        widget = self.get_widget(key)

        if not widget:
            return

        if (isinstance(widget, EntryBox)) or (isinstance(widget, tk.Text)):
            menu.add(text="Copy", command=lambda e: self.copy(key))
            menu.add(text="Paste", command=lambda e: self.paste(key))

            if key in config.clearables:
                menu.add(text="Clear", command=lambda e: self.clear(key))

        value = config.get(key)
        defvalue = config.get_default(key)

        if (defvalue is not None) and (value != defvalue) and (defvalue != ""):
            menu.add(text="Reset", command=lambda e: config.reset_one(key))

    def show_menu_items(
        self,
        key_config: str,
        key_list: str,
        command: Callable[..., Any],
        event: Optional[Any] = None,
        only_items: bool = False,
    ) -> None:
        menu = getattr(self, f"{key_list}_menu")
        items = files.get_list(key_list)[: args.max_list_items]
        menu.clear()

        if only_items:
            if not items:
                Dialog.show_message("No items yet")
                return
        else:
            self.add_common_commands(menu, key_config)

        if items:
            if not only_items:
                menu.add(text="--- Recent ---", disabled=True)

            def add_item(item: str) -> None:
                def proc() -> None:
                    command(item)

                menu.add(
                    text=item[: args.list_item_width],
                    command=lambda e: proc(),
                )

            for item in items:
                add_item(item)

        if event:
            menu.show(event)
        else:
            widget = self.get_widget(key_config)

            if widget:
                menu.show(widget=widget)

    def show_model_context(
        self, event: Optional[Any] = None, only_items: bool = False
    ) -> None:
        from .model import model

        if model.model_loading:
            return

        self.show_menu_items(
            "model",
            "models",
            lambda m: self.set_model(m),
            event,
            only_items=only_items,
        )

    def show_url_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("url", "urls", lambda s: self.set_url(s), event)

    def show_model(self) -> None:
        self.model.set_text(config.model)
        self.model.move_to_end()

    def add_generic_menus(self) -> None:
        def show_menu(key: str, event: Any) -> None:
            menu = Menu()
            self.add_common_commands(menu, key)
            menu.show(event)

        def bind_menu(key: str) -> None:
            widget = self.get_widget(key)

            if not widget:
                return

            if key not in ["model", "url", "input", "system"]:
                widget.bind("<Button-3>", lambda e: show_menu(key, e))

        for key in config.defaults():
            bind_menu(key)

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

    def set_url(self, text: str) -> None:
        self.url.set_text(text)
        config.update("url")

    def set_model(self, m: str) -> None:
        widgets.model.set_text(m)
        config.update("model")

    def stop_stream(self) -> None:
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
            utils.copy(widget.get())
            widget.focus_set()
            config.update(key)

    def paste(self, key: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        utils.paste(widget)
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
            return

        if display.select_active_tab():
            return

        if model.streaming:
            self.stop_stream()
            return

        display.to_bottom()

    def show_context(self) -> None:
        widget = app.root.focus_get()

        if widget == self.input:
            inputcontrol.show_menu()
        elif widget == self.url:
            self.show_url_menu()
        elif widget == self.model:
            self.show_model_context()

    def details_left(self) -> None:
        self.details_canvas.xview_scroll(-self.canvas_scroll, "units")
        self.check_details_buttons()

    def details_right(self) -> None:
        self.details_canvas.xview_scroll(self.canvas_scroll, "units")
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
            self.details_button_left.set_text("-")
        else:
            self.details_button_left.set_style("alt")
            self.details_button_left.set_text("<")

        if scroll_pos_right == 1.0:
            self.details_button_right.set_style("disabled")
            self.details_button_right.set_text("-")
        else:
            self.details_button_right.set_style("alt")
            self.details_button_right.set_text(">")

    def use_gpt(self, name: str) -> None:
        config.set("model", name)

    def model_icon_click(self) -> None:
        app.hide_all()

    def show_recent_models(self) -> None:
        self.show_model_context(only_items=True)

    def write_system_prompt(
        self, text: Optional[str] = None, max: bool = False
    ) -> None:
        from .textbox import TextBox

        def action(ans: Dict[str, Any]) -> None:
            config.set("system", ans["text"])

        def copy(textbox: TextBox) -> None:
            utils.copy(textbox.get_text())

        def paste(textbox: TextBox) -> None:
            utils.paste(textbox)

        def clear(textbox: TextBox) -> None:
            textbox.set_text("")

        def reset(textbox: TextBox) -> None:
            value = config.get_default("system")

            if value:
                textbox.set_text(value)

        def on_right_click(event: Any, textbox: TextBox) -> None:
            menu = Menu()
            text = textbox.get_text()

            menu.add(text="Copy", command=lambda e: copy(textbox))
            menu.add(text="Paste", command=lambda e: paste(textbox))

            if text:
                menu.add(text="Clear", command=lambda e: clear(textbox))

            if text != config.get_default("system"):
                menu.add(text="Reset", command=lambda e: reset(textbox))

            items = files.get_list("systems")[: args.max_list_items]

            if items:
                menu.add(text="--- Recent ---", disabled=True)

            def add_item(item: str) -> None:
                def proc() -> None:
                    config.set("system", item)
                    textbox.set_text(item)
                    textbox.dialog.focus()

                menu.add(text=item[: args.list_item_width], command=lambda e: proc())

            for item in items:
                add_item(item)

            menu.show(event)

        if text:
            config.set("system", text)
            return

        Dialog.show_textbox(
            "System Prompt",
            lambda a: action(a),
            value=config.system,
            start_maximized=max,
            on_right_click=on_right_click,
        )

    def check_move_to_end(self, key: str) -> None:
        if key in ["model", "url"]:
            widget = widgets.get_widget(key)

            if not widget:
                return

            if not isinstance(widget, EntryBox):
                return

            widget.move_to_end()

    def show_main_menu(self, event: Any = None) -> None:
        from .menumanager import main_menu

        main_menu.show(event)

    def show_model_menu(self, event: Any = None) -> None:
        from .menumanager import model_menu

        model_menu.show(event)

    def show_more_menu(self, event: Any = None) -> None:
        from .menumanager import more_menu

        more_menu.show(event)

    def get_dir(self, what: str, list: str) -> Optional[str]:
        items = [getattr(config, what)] + files.get_list(list)

        for item in items:
            path = Path(item)

            if path.exists() and path.is_file():
                return str(path.parent)

        return None

    def browse_models(self) -> None:
        from .model import model

        if model.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=self.get_dir("model", "models"))

        if file:
            self.set_model(file)

    def browse_file(self) -> None:
        file = filedialog.askopenfilename(initialdir=self.get_dir("url", "urls"))

        if file:
            self.set_url(file)

    def show_url(self) -> None:
        self.url_frame.grid()
        widgets.url_enabled = True

    def hide_url(self) -> None:
        self.url_frame.grid_remove()
        widgets.url_enabled = False

    def check_mode(self) -> None:
        if config.mode == "image":
            self.show_url()
        else:
            self.hide_url()


widgets: Widgets = Widgets()
