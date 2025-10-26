from __future__ import annotations

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any
from collections.abc import Callable
from pathlib import Path

# Modules
from .args import args
from .app import app
from .config import config
from .tooltips import ToolTip
from .menus import Menu
from .dialogs import Dialog
from .entrybox import EntryBox
from .modelcontrol import modelcontrol
from .filecontrol import filecontrol
from .inputcontrol import inputcontrol
from .display import display
from .commands import commands
from .framedata import FrameData
from .tips import tips
from .files import files
from .logs import logs
from .utils import utils
from .model import model
from .autoscroll import autoscroll
from .close import close
from .scrollers import scrollers
from .widgetutils import widgetutils


Gettable = (EntryBox, ttk.Combobox)
TextWidget = (EntryBox, tk.Text)


class Widgets:
    def __init__(self) -> None:
        self.file: EntryBox
        self.input: EntryBox
        self.canvas_scroll = 1

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
        self.search_label: tk.Label
        self.search: ttk.Combobox
        self.stream_label: tk.Label
        self.stream: ttk.Combobox
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

        self.scroller_system: tk.Frame
        self.scroller_details_1: tk.Frame
        self.scroller_details_2: tk.Frame
        self.system_frame: tk.Frame

    def make(self) -> None:
        # Model
        app.main_frame.grid_columnconfigure(FrameData.frame_number, weight=1)
        frame_data_model = widgetutils.make_frame()
        self.model_frame = frame_data_model.frame

        self.model_menu_button = widgetutils.make_button(
            frame_data_model,
            "Model",
            lambda e: self.show_model_menu(e),
        )

        ToolTip(self.model_menu_button, tips["model_menu"])

        self.model = widgetutils.make_entry(frame_data_model)
        frame_data_model.expand()
        self.model.bind_mousewheel()
        ToolTip(self.model, tips["model"])

        self.model_icon = widgetutils.make_label(frame_data_model, "", colons=False)
        self.model_icon_tooltip = ToolTip(self.model_icon, "")
        self.model_icon.configure(cursor="hand2")

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

        self.main_menu_button = widgetutils.make_button(
            frame_data_model, "Menu", lambda e: self.show_main_menu(e)
        )

        ToolTip(self.main_menu_button, tips["main_menu"])

        # Scrollers
        scrollers.add(self, "system")
        scrollers.add(self, "details_1")
        scrollers.add(self, "details_2")

        # Buttons
        frame_data_buttons = widgetutils.make_frame()
        self.buttons_frame = frame_data_buttons.frame

        self.stop_button = widgetutils.make_button(
            frame_data_buttons, "Stop", lambda: self.stop_stream()
        )

        frame_data_buttons.expand()
        ToolTip(self.stop_button, tips["stop_button"])

        self.new_button = widgetutils.make_button(
            frame_data_buttons, "New", lambda: display.new_tab()
        )

        frame_data_buttons.expand()
        ToolTip(self.new_button, tips["new_button"])

        self.clear_button = widgetutils.make_button(
            frame_data_buttons, "Clear", lambda: display.clear()
        )

        frame_data_buttons.expand()
        ToolTip(self.clear_button, tips["clear_button"])

        self.close_button = widgetutils.make_button(
            frame_data_buttons, "Close", lambda: close.close()
        )

        frame_data_buttons.expand()
        ToolTip(self.close_button, tips["close_button"])

        self.top_button = widgetutils.make_button(
            frame_data_buttons, "Top", lambda: display.to_top()
        )

        frame_data_buttons.expand()
        ToolTip(self.top_button, tips["top_button"])

        self.tab_menu_button = self.more_menu_button = widgetutils.make_button(
            frame_data_buttons,
            "Tab",
            lambda e: self.show_tab_menu(e),
        )

        ToolTip(self.more_menu_button, tips["tab_menu"])
        frame_data_buttons.expand()

        self.save_button = widgetutils.make_button(
            frame_data_buttons,
            "Save",
            lambda: logs.to_text(),
        )

        ToolTip(self.save_button, "Save log as text")
        frame_data_buttons.expand()

        self.more_menu_button = widgetutils.make_button(
            frame_data_buttons,
            "More",
            lambda e: self.show_more_menu(e),
        )

        ToolTip(self.more_menu_button, tips["more_menu"])
        frame_data_buttons.expand()

        # Display
        app.main_frame.grid_rowconfigure(FrameData.frame_number, weight=1)
        frame_data_display = widgetutils.make_frame()
        self.display_frame = frame_data_display.frame
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        # File
        self.frame_data_file = widgetutils.make_frame()
        self.file_frame = self.frame_data_file.frame

        # Input
        self.frame_data_input = widgetutils.make_frame()
        self.input_frame = self.frame_data_input.frame

        self.models_menu = Menu()
        self.systems_menu = Menu()
        self.files_menu = Menu()
        self.inputs_menu = Menu()

    def get_widget(self, key: str) -> tk.Widget | None:
        if hasattr(self, key):
            widget = getattr(self, key)

            if not isinstance(widget, tk.Widget):
                return None

            return widget

        return None

    def fill(self) -> None:
        for key in config.defaults():
            self.fill_widget(key, getattr(config, key))

    def fill_widget(self, key: str, value: Any, focus: bool = False) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if isinstance(widget, EntryBox):
            if value not in [None, ""]:
                widget.set_text(str(value))
            else:
                widget.clear(focus=False)

            self.check_move_to_end(key)

            if focus:
                widget.focus_set()
        elif isinstance(widget, ttk.Combobox):
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        from .display import display
        from .system import system
        from .details import details

        modelcontrol.fill()
        filecontrol.fill()
        inputcontrol.fill()
        system.add_items()
        details.add_items()

        self.fill()
        self.setup_binds()
        self.setup_widgets()
        self.add_generic_menus()
        self.setup_tooltips()
        self.disable_stop_button()
        scrollers.setup()

        inputcontrol.focus()

        if display.num_tabs() == 0:
            display.make_tab()
        else:
            display.select_last_tab()

        files.load_list("files")

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
        setup_entrybox("model", "Local path or model name")
        setup_entrybox("before", "Text")
        setup_entrybox("after", "Text")
        setup_entrybox("stop", "Text")
        setup_entrybox("file", "Path to a remote or local file")
        setup_entrybox("threads", "Int")
        setup_entrybox("gpu_layers", "Int")

        setup_combobox("format")
        setup_combobox("mlock")
        setup_combobox("mode")
        setup_combobox("logits")
        setup_combobox("search")
        setup_combobox("stream")

    def setup_binds(self) -> None:
        self.model_icon.bind("<Button-1>", lambda e: self.model_icon_click())
        self.main_menu_button.set_bind("<Button-2>", lambda e: app.show_about())
        self.main_menu_button.set_bind("<Button-3>", lambda e: commands.show_palette())
        self.tab_menu_button.set_bind("<Button-2>", lambda e: self.show_tab_list(e))
        self.more_menu_button.set_bind("<Button-2>", lambda e: self.show_upload())
        self.top_button.set_bind("<Button-2>", lambda e: autoscroll.toggle("up"))
        self.top_button.set_bind("<ButtonRelease-3>", lambda e: self.scroll_up())
        self.top_button.set_bind("<Button-4>", lambda e: self.scroll_up())
        self.top_button.set_bind("<Button-5>", lambda e: self.scroll_down())
        self.close_button.set_bind("<Button-2>", lambda e: close.close_all())

        self.new_button.set_bind(
            "<Button-2>", lambda e: display.new_tab(position="start")
        )

        modelcontrol.bind()
        filecontrol.bind()
        inputcontrol.bind()

    def add_common_commands(self, menu: Menu, key: str) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        defvalue = config.get_default(key)

        if isinstance(widget, Gettable):
            value = widget.get()

            if value:
                selected = ""

                if isinstance(widget, EntryBox):
                    maybesel = widget.get_selected()

                    if maybesel:
                        selected = maybesel

                menu.add(text="Copy", command=lambda e: self.copy(key, text=selected))

            if isinstance(widget, TextWidget):
                menu.add(text="Paste", command=lambda e: self.paste(key))

            if value and (key in config.clearables):
                menu.add(text="Clear", command=lambda e: self.clear(key))

        conf_value = config.get(key)

        if defvalue is not None:
            if (conf_value != defvalue) and (defvalue != ""):
                menu.add(text="Reset", command=lambda e: config.reset_one(key))

            if isinstance(defvalue, (int, float)):
                menu.add(text="Half", command=lambda e: self.half_number(key))
                menu.add(text="Double", command=lambda e: self.double_number(key))

    def show_menu_items(
        self,
        key_config: str,
        key_list: str,
        cmd: Callable[..., Any],
        event: Any = None,
        only_items: bool = False,
        alt_cmd: Callable[..., Any] | None = None,
        target: tk.Widget | None = None,
    ) -> None:
        menu = getattr(self, f"{key_list}_menu")

        if not isinstance(menu, Menu):
            return

        if key_config == "input":
            items = inputcontrol.get_history_list()
        else:
            items = files.get_list(key_list)

        items = items[: args.max_list_items]
        widget = self.get_widget(key_config)
        value = ""

        if widget:
            if isinstance(widget, Gettable):
                value = widget.get()

        menu.clear()

        if only_items:
            if not items:
                Dialog.show_message("No items yet")
                return
        else:
            self.add_common_commands(menu, key_config)

        if items:
            short = key_config in ("model", "file")

            utils.fill_recent(
                menu,
                items,
                value,
                cmd=cmd,
                label=not only_items,
                short=short,
                alt_cmd=alt_cmd,
            )

        if event:
            menu.show(event)
        else:
            wid = target or widget

            if wid:
                menu.show(widget=wid)

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
            if model.loaded_model:
                self.load_button.set_style("active")
            else:
                self.load_button.set_style("normal")

    def disable_load_button(self) -> None:
        if app.exists():
            self.load_button.set_style("disabled")

    def enable_close_button(self) -> None:
        if app.exists():
            self.close_button.set_style("normal")

    def disable_close_button(self) -> None:
        if app.exists():
            self.close_button.set_style("disabled")

    def enable_clear_button(self) -> None:
        if app.exists():
            self.clear_button.set_style("normal")

    def disable_clear_button(self) -> None:
        if app.exists():
            self.clear_button.set_style("disabled")

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

    def stop_stream(self) -> None:
        from .display import display

        display.to_bottom()
        model.stop_stream()

    def load_or_unload(self) -> None:
        model.load_or_unload()

    def copy(self, key: str, text: str | None = None) -> None:
        widget = self.get_widget(key)

        if not widget:
            return

        if not isinstance(widget, Gettable):
            return

        if not text:
            text = widget.get()

        utils.copy(text)
        widget.focus_set()
        config.update(key)

    def paste(self, key: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        utils.paste(widget)
        config.update(key)
        widget.focus_end()

    def clear(self, key: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        widget.clear()
        widget.focus_set()
        config.update(key)

    def change_number(self, key: str, mode: str) -> None:
        widget = self.get_widget(key)

        if (not widget) or (not isinstance(widget, EntryBox)):
            return

        defvalue = config.get_default(key)
        current = config.get(key)

        if current is None:
            return

        if current == 0:
            return

        if mode == "half":
            num = current / 2
        else:
            num = current * 2

        if isinstance(defvalue, int):
            num = int(num)
        else:
            num = round(num, 2)

        config.set(key, num)

    def half_number(self, key: str) -> None:
        self.change_number(key, "half")

    def double_number(self, key: str) -> None:
        self.change_number(key, "double")

    def find_focused(self) -> bool:
        focused = app.focused()

        if not focused:
            return False

        if isinstance(focused, EntryBox):
            if focused.name == "find":
                return True

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
        widget = app.focused()

        if widget == self.input:
            inputcontrol.show_menu()
        elif widget == self.file:
            filecontrol.show_menu()
        elif widget == self.model:
            modelcontrol.show_context()

    def use_gpt(self, name: str) -> None:
        config.set("model", name)

    def use_gemini(self, name: str) -> None:
        config.set("model", name)

    def use_claude(self, name: str) -> None:
        config.set("model", name)

    def model_icon_click(self) -> None:
        Dialog.show_message(model.icon_text)

    def check_move_to_end(self, key: str) -> None:
        if key in ["model", "file"]:
            widget = widgets.get_widget(key)

            if not widget:
                return

            if not isinstance(widget, EntryBox):
                return

            widget.move_to_end()

    def show_main_menu(self, event: Any = None) -> None:
        from .menumanager import menumanager

        menumanager.main_menu.show(event)

    def show_model_menu(self, event: Any = None) -> None:
        from .menumanager import menumanager

        menumanager.model_menu.show(event)

    def show_tab_menu(self, event: Any = None) -> None:
        from .menumanager import menumanager

        menumanager.tab_menu.show(event)

    def show_more_menu(self, event: Any = None) -> None:
        from .menumanager import menumanager

        menumanager.more_menu.show(event)

    def show_tab_list(self, event: Any = None) -> None:
        from .display import display

        display.show_tab_list(event)

    def show_upload(self) -> None:
        from .upload import upload

        upload.upload_picker()

    def get_dir(self, what: str | None = None, list: str | None = None) -> str | None:
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

    def change_mode(self, what: str) -> None:
        if what not in config.modes:
            return

        config.set("mode", what)

    def scroll_up(self) -> None:
        ToolTip.hide_all()
        display.scroll_up(disable_autoscroll=True)

    def scroll_down(self) -> None:
        ToolTip.hide_all()
        display.scroll_down(disable_autoscroll=True)

    def window(self, widget: Any, start_line: int, win: Any) -> None:
        # Get current line count
        last_line = int(widget.index("end - 1c").split(".")[0])

        if start_line > last_line:
            # Add necessary newlines
            newlines_needed = start_line - last_line
            widget.insert("end", "\n" * newlines_needed)

        # Now insert the window at the position
        widget.window_create(f"{start_line}.0", window=win)


widgets: Widgets = Widgets()
