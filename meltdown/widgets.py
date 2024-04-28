# Standard
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Optional, Any, Callable, Dict
from pathlib import Path

# Libraries
from tkinterdnd2 import DND_FILES  # type: ignore

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
from .model import model
from . import widgetutils
from . import details


Gettable = (EntryBox, ttk.Combobox)
TextWidget = (EntryBox, tk.Text)


class Widgets:
    def __init__(self) -> None:
        self.input: EntryBox
        self.canvas_scroll = 1
        self.file_enabled = True

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

        self.user_label: tk.Label
        self.avatar_user: EntryBox
        self.name_user: EntryBox
        self.ai_label: tk.Label
        self.avatar_ai: EntryBox
        self.name_ai: EntryBox
        self.history_label: tk.Label
        self.history: EntryBox
        self.context_label: tk.Label
        self.context: EntryBox
        self.max_tokens_label: tk.Label
        self.max_tokens: EntryBox
        self.threads_label: tk.Label
        self.threads: EntryBox
        self.gpu_layers_label: tk.Label
        self.gpu_layers: EntryBox
        self.format_label: tk.Label
        self.format: ttk.Combobox
        self.temperature_label: tk.Label
        self.temperature: EntryBox
        self.seed_label: tk.Label
        self.seed: EntryBox
        self.top_p_label: tk.Label
        self.top_p: EntryBox
        self.top_k_label: tk.Label
        self.top_k: EntryBox
        self.before_label: tk.Label
        self.before: EntryBox
        self.after_label: tk.Label
        self.after: EntryBox
        self.stop_label: tk.Label
        self.stop: EntryBox
        self.mlock_label: tk.Label
        self.mlock: ttk.Combobox

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

        if args.drag_and_drop:
            self.model.drop_target_register(DND_FILES)  # type: ignore
            self.model.dnd_bind("<<Drop>>", lambda e: self.on_model_dropped(e))  # type: ignore

        self.model_icon = widgetutils.make_label(frame_data_model, "", colons=False)
        self.model_icon_tooltip = ToolTip(self.model_icon, "")

        if not args.model_icon:
            self.model_icon.grid_remove()

        self.mode = widgetutils.make_combobox(
            frame_data_model,
            width=app.theme.combobox_width_small,
            values=["text", "image"],
        )

        ToolTip(self.mode, tips["mode"])

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

        # Details Container 1
        frame_data_details_1 = widgetutils.make_frame()
        self.details_frame_1 = frame_data_details_1.frame
        left_frame_1 = widgetutils.make_frame(self.details_frame_1, col=0, row=0)
        left_frame_1.frame.grid_rowconfigure(0, weight=1)

        self.details_button_left_1 = widgetutils.make_button(
            left_frame_1, "<", lambda: widgets.details_left(1), style="alt"
        )

        ToolTip(self.details_button_left_1, tips["details_button"])

        self.details_1, self.details_canvas_1 = widgetutils.make_scrollable_frame(
            self.details_frame_1, 1
        )

        right_frame_1 = widgetutils.make_frame(self.details_frame_1, col=2, row=0)
        right_frame_1.frame.grid_rowconfigure(0, weight=1)

        self.details_button_right_1 = widgetutils.make_button(
            right_frame_1,
            ">",
            lambda: widgets.details_right(1),
            style="alt",
        )

        ToolTip(self.details_button_right_1, tips["details_button"])
        self.details_frame_1.columnconfigure(1, weight=1)

        # Details 1
        details_data = FrameData(self.details_1)
        details.add_users(self, details_data)
        details.add_history(self, details_data)
        details.add_context(self, details_data)
        details.add_max_tokens(self, details_data)
        details.add_threads(self, details_data)
        details.add_gpu_layers(self, details_data)
        details.add_temperature(self, details_data)

        # Details Container 2
        frame_data_details_2 = widgetutils.make_frame()
        self.details_frame_2 = frame_data_details_2.frame
        left_frame_2 = widgetutils.make_frame(self.details_frame_2, col=0, row=0)
        left_frame_2.frame.grid_rowconfigure(0, weight=1)

        self.details_button_left_2 = widgetutils.make_button(
            left_frame_2, "<", lambda: widgets.details_left(2), style="alt"
        )

        ToolTip(self.details_button_left_2, tips["details_button"])

        self.details_2, self.details_canvas_2 = widgetutils.make_scrollable_frame(
            self.details_frame_2, 1
        )

        right_frame_2 = widgetutils.make_frame(self.details_frame_2, col=2, row=0)
        right_frame_2.frame.grid_rowconfigure(0, weight=1)

        self.details_button_right_2 = widgetutils.make_button(
            right_frame_2,
            ">",
            lambda: widgets.details_right(2),
            style="alt",
        )

        ToolTip(self.details_button_right_2, tips["details_button"])
        self.details_frame_2.columnconfigure(1, weight=1)

        # Details 2
        details_data_2 = FrameData(self.details_2)
        details.add_format(self, details_data_2)
        details.add_before(self, details_data_2)
        details.add_after(self, details_data_2)
        details.add_stop(self, details_data_2)
        details.add_seed(self, details_data_2)
        details.add_top_p(self, details_data_2)
        details.add_top_k(self, details_data_2)
        details.add_mlock(self, details_data_2)

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

        # File
        frame_data_file = widgetutils.make_frame()
        self.file_frame = frame_data_file.frame
        self.file_label = widgetutils.make_label(frame_data_file, "File")
        self.file = widgetutils.make_entry(frame_data_file)
        frame_data_file.expand()
        self.file.bind_mousewheel()
        ToolTip(self.file_label, tips["file"])
        ToolTip(self.file, tips["file"])

        if args.drag_and_drop:
            self.file.drop_target_register(DND_FILES)  # type: ignore
            self.file.dnd_bind("<<Drop>>", lambda e: self.on_file_dropped(e))  # type: ignore

        self.recent_files_button = widgetutils.make_button(
            frame_data_file, "Recent", lambda: self.show_recent_files()
        )

        ToolTip(self.recent_files_button, tips["recent_files_button"])

        self.browse_file_button = widgetutils.make_button(
            frame_data_file, "Browse", lambda: self.browse_file()
        )

        ToolTip(self.browse_file_button, tips["browse_file_button"])

        # Input
        self.frame_data_input = widgetutils.make_frame()
        self.input_frame = self.frame_data_input.frame

        self.models_menu = Menu()
        self.systems_menu = Menu()
        self.files_menu = Menu()
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
        self.check_details_buttons(1)
        self.check_details_buttons(2)
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
        self.do_setup_details(1)
        self.do_setup_details(2)

    def do_setup_details(self, num: int) -> None:
        details = getattr(self, f"details_{num}")
        details.update_idletasks()
        canvas = getattr(self, f"details_canvas_{num}")
        canvas.update_idletasks()
        canvas.configure(width=details.winfo_reqwidth())
        canvas.configure(height=details.winfo_reqheight())
        left = getattr(self, f"details_button_left_{num}")
        right = getattr(self, f"details_button_right_{num}")

        left.set_bind("<Button-4>", lambda e: widgets.details_left(num))
        left.set_bind("<Button-5>", lambda e: widgets.details_right(num))
        left.set_bind("<Button-2>", lambda e: widgets.details_start(num))

        right.set_bind("<Button-4>", lambda e: widgets.details_left(num))
        right.set_bind("<Button-5>", lambda e: widgets.details_right(num))
        right.set_bind("<Button-2>", lambda e: widgets.details_end(num))

        details.bind("<Button-4>", lambda e: widgets.details_left(num))
        details.bind("<Button-5>", lambda e: widgets.details_right(num))

        for child in details.winfo_children():
            child.bind("<Button-4>", lambda e: widgets.details_left(num))
            child.bind("<Button-5>", lambda e: widgets.details_right(num))

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
        setup_entrybox("stop", "Text")
        setup_entrybox("file", "URL to a remote file or a local path")
        setup_entrybox("threads", "Int")
        setup_entrybox("gpu_layers", "Int")

        setup_combobox("format")
        setup_combobox("mlock")
        setup_combobox("mode")

    def setup_binds(self) -> None:
        self.model.bind("<Button-3>", lambda e: self.show_model_context(e))
        self.file.bind("<Button-3>", lambda e: self.show_file_menu(e))
        self.model_icon.bind("<Button-1>", lambda e: self.model_icon_click())
        self.main_menu_button.set_bind("<Button-2>", lambda e: app.show_about())
        self.main_menu_button.set_bind("<Button-3>", lambda e: commands.show_palette())
        self.top_button.set_bind("<Button-4>", lambda e: display.scroll_up())
        self.top_button.set_bind("<Button-5>", lambda e: display.scroll_down())
        inputcontrol.bind()

    def add_common_commands(self, menu: Menu, key: str) -> None:
        config.update(key)
        widget = self.get_widget(key)

        if not widget:
            return

        defvalue = config.get_default(key)

        if isinstance(widget, Gettable):
            value = widget.get()

            if value:
                menu.add(text="Copy", command=lambda e: self.copy(key))

            if isinstance(widget, TextWidget):
                menu.add(text="Paste", command=lambda e: self.paste(key))

            if value and (key in config.clearables):
                menu.add(text="Clear", command=lambda e: self.clear(key))

        conf_value = config.get(key)

        if (defvalue is not None) and (conf_value != defvalue) and (defvalue != ""):
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
        if model.model_loading:
            return

        self.show_menu_items(
            "model",
            "models",
            lambda m: self.set_model(m),
            event,
            only_items=only_items,
        )

    def show_file_context(
        self, event: Optional[Any] = None, only_items: bool = False
    ) -> None:
        self.show_menu_items(
            "file",
            "files",
            lambda m: self.set_file(m),
            event,
            only_items=only_items,
        )

    def show_file_menu(self, event: Optional[Any] = None) -> None:
        self.show_menu_items("file", "files", lambda s: self.set_file(s), event)

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

            if key not in ["model", "file", "input", "system"]:
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

    def set_file(self, text: str) -> None:
        self.file.set_text(text)

    def set_model(self, m: str) -> None:
        config.set("model", m)

    def stop_stream(self) -> None:
        from .display import display

        display.to_bottom()
        model.stop_stream()

    def load_or_unload(self) -> None:
        model.load_or_unload()

    def copy(self, key: str) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if isinstance(widget, Gettable):
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

        if isinstance(focused, EntryBox):
            return focused == self.model

        return False

    def esckey(self) -> None:
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
        elif widget == self.file:
            self.show_file_menu()
        elif widget == self.model:
            self.show_model_context()

    def details_left(self, num: int) -> None:
        canvas = getattr(self, f"details_canvas_{num}")
        scroll_pos_left = canvas.xview()[0]

        if scroll_pos_left == 0.0:
            return

        canvas.xview_scroll(-self.canvas_scroll, "units")
        self.check_details_buttons(num)

    def details_right(self, num: int) -> None:
        canvas = getattr(self, f"details_canvas_{num}")
        scroll_pos_right = canvas.xview()[1]

        if scroll_pos_right == 1.0:
            return

        canvas.xview_scroll(self.canvas_scroll, "units")
        self.check_details_buttons(num)

    def details_start(self, num: int) -> None:
        canvas = getattr(self, f"details_canvas_{num}")
        canvas.xview_moveto(0)
        self.check_details_buttons(num)

    def details_end(self, num: int) -> None:
        canvas = getattr(self, f"details_canvas_{num}")
        canvas.xview_moveto(1.0)
        self.check_details_buttons(num)

    def check_details_buttons(self, num: int) -> None:
        canvas = getattr(self, f"details_canvas_{num}")
        scroll_pos_left = canvas.xview()[0]
        scroll_pos_right = canvas.xview()[1]
        ToolTip.hide_all()

        left = getattr(self, f"details_button_left_{num}")
        right = getattr(self, f"details_button_right_{num}")

        if scroll_pos_left == 0:
            left.set_style("disabled")
            left.set_text("-")
        else:
            left.set_style("alt")
            left.set_text("<")

        if scroll_pos_right == 1.0:
            right.set_style("disabled")
            right.set_text("-")
        else:
            right.set_style("alt")
            right.set_text(">")

    def use_gpt(self, name: str) -> None:
        config.set("model", name)

    def model_icon_click(self) -> None:
        app.hide_all()

    def show_recent_models(self) -> None:
        self.show_model_context(only_items=True)

    def show_recent_files(self) -> None:
        self.show_file_context(only_items=True)

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

            if text:
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
            "system",
            "System Prompt",
            lambda a: action(a),
            value=config.system,
            start_maximized=max,
            on_right_click=on_right_click,
        )

    def check_move_to_end(self, key: str) -> None:
        if key in ["model", "file"]:
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

    def get_dir(self, what: Optional[str], list: Optional[str]) -> Optional[str]:
        items = []

        if what:
            items.append(getattr(config, what))

        if list:
            items.extend(files.get_list(list))

        for item in items:
            path = Path(item)

            if path.exists() and path.is_file():
                return str(path.parent)

        return None

    def browse_models(self) -> None:
        if model.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=self.get_dir("model", "models"))

        if file:
            self.set_model(file)

    def browse_file(self) -> None:
        file = filedialog.askopenfilename(initialdir=self.get_dir(None, "files"))

        if file:
            self.set_file(file)

    def show_file(self) -> None:
        self.file.clear(False)
        self.file_frame.grid()
        widgets.file_enabled = True

    def hide_file(self) -> None:
        self.file.clear(False)
        self.file_frame.grid_remove()
        widgets.file_enabled = False

    def check_mode(self) -> None:
        if config.mode == "image":
            self.show_file()
        else:
            self.hide_file()

    def change_model(self, name: str) -> None:
        if not name:
            return

        name = name.lower()
        list = files.get_list("models")

        if not list:
            return

        for item in list:
            if name in item.lower():
                self.set_model(item)
                return

    def change_mode(self, what: str) -> None:
        if what not in config.modes:
            return

        config.set("mode", what)

    def on_file_dropped(self, event: Any) -> None:
        if event.data:
            self.set_file(event.data)

    def on_model_dropped(self, event: Any) -> None:
        if event.data:
            self.set_model(event.data)


widgets: Widgets = Widgets()
