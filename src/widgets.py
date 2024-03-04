# Modules
from config import config
import widgetutils
from framedata import FrameData
from app import app

# Standard
import tkinter as tk
from tkinter import ttk
from typing import Any
from tkinter import filedialog
from typing import Optional, Any, Tuple, List
from functools import partial


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = widgetutils.clean_string(text)
        self.tooltip: Optional[tk.Toplevel] = None
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.id = ""

    def schedule_tooltip(self, event: Any = None) -> None:
        self.id = self.widget.after(500, self.show_tooltip)  # 500ms delay

    def show_tooltip(self) -> None:
        if widgets.menu_open:
            return

        box: Optional[Tuple[int, int, int, int]] = None

        if isinstance(self.widget, ttk.Combobox):
            box = self.widget.bbox("insert")
        else:
            box = self.widget.bbox()

        if not box:
            return

        x, y, _, _ = box
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="white",
                         wraplength=250, justify=tk.LEFT)
        label.pack()

    def hide_tooltip(self, event: Any = None) -> None:
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = ""


class Widgets:
    def __init__(self) -> None:
        def get_d() -> FrameData:
            return FrameData(widgetutils.make_frame(), 0)

        # Model
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)

        widgetutils.make_label(d, "Model")
        self.model = widgetutils.make_input(d, sticky="ew")
        ToolTip(self.model, "Path to a model file. This should be a file that works with"
                " llama.cpp, like gguf files for instance.")

        self.stop_button = widgetutils.make_button(d, "Stop")
        ToolTip(self.stop_button, "Stop generating the current response")

        self.model_menu_button = widgetutils.make_button(d, "Models")
        ToolTip(self.model_menu_button, "Pick a model file from your file system")

        self.main_menu_button = widgetutils.make_button(d, "Menu")
        ToolTip(self.main_menu_button, "Open the main menu")

        # Settings
        d = get_d()

        widgetutils.make_label(d, "User")
        self.name_user = widgetutils.make_input(d)
        ToolTip(self.name_user, "The name of the user (you)")

        widgetutils.make_label(d, "AI")
        self.name_ai = widgetutils.make_input(d)
        ToolTip(self.name_ai, "The name of the assistant (AI)")

        widgetutils.make_label(d, "Tokens")
        self.max_tokens = widgetutils.make_input(d, width=config.input_width_small)
        ToolTip(self.max_tokens, "Maximum number of tokens to generate."
                " Higher values will result in longer output, but will"
                " also take longer to compute.")

        widgetutils.make_label(d, "Temp")
        self.temperature = widgetutils.make_input(d, width=config.input_width_small)
        ToolTip(self.temperature, "The temperature parameter is used to control"
                " the randomness of the output. A higher temperature (~1) results in more randomness"
                " and diversity in the generated text, as the model is more likely to"
                " explore a wider range of possible tokens. Conversely, a lower temperature"
                " (<1) produces more focused and deterministic output, emphasizing the"
                " most probable tokens.")

        widgetutils.make_label(d, "Top K")
        self.top_k = widgetutils.make_input(d, width=config.input_width_small)
        ToolTip(self.top_k, "The top-k parameter limits the model's \
                predictions to the top k most probable tokens at each step \
                of generation. By setting a value for k, you are instructing \
                the model to consider only the k most likely tokens. \
                This can help in fine-tuning the generated output and \
                ensuring it adheres to specific patterns or constraints.")

        widgetutils.make_label(d, "Top P")
        self.top_p = widgetutils.make_input(d, width=config.input_width_small)
        ToolTip(self.top_p, "Top-p, also known as nucleus sampling, controls"
                " the cumulative probability of the generated tokens."
                " The model generates tokens until the cumulative probability"
                " exceeds the chosen threshold (p). This approach allows for"
                " more dynamic control over the length of the generated text"
                " and encourages diversity in the output by including less"
                " probable tokens when necessary.")

        # System
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)

        widgetutils.make_label(d, "System")
        self.system = widgetutils.make_input(d, sticky="ew")
        ToolTip(self.system, "This sets the system message that instructs"
                " the AI how to respond, or how to act in general."
                " You could use this to make the AI take on a specific persona or role.")

        widgetutils.make_label(d, "Context")
        self.context = widgetutils.make_input(d, width=config.input_width_small)
        ToolTip(self.context, "The number of previous messages to include as the context."
                " The computation will take longer with more context."
                " 0 means context is not used at all.")

        # Output
        d = get_d()
        d.frame.grid_columnconfigure(0, weight=1)
        d.frame.grid_rowconfigure(0, weight=1)
        self.output = widgetutils.make_text(d, state="disabled", sticky="nsew")

        # Input
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)
        widgetutils.make_label(d, "Prompt")
        self.input = widgetutils.make_input(d, sticky="ew")

        clear_button = widgetutils.make_button(d, "Clear", lambda: self.clear_input())
        ToolTip(clear_button, "Clear the input field")

        input_history_up_button = widgetutils.make_button(d, "Prev", lambda: self.input_history_up())
        ToolTip(input_history_up_button, "Previous item in the input history")

        input_history_up_down = widgetutils.make_button(d, "Next", lambda: self.input_history_down())
        ToolTip(input_history_up_down, "Next item in the input history")

        submit_button = widgetutils.make_button(d, "Submit", lambda: self.submit())
        ToolTip(submit_button, "Use the input as the prompt for the AI")

        self.output_menu = widgetutils.make_menu()
        self.model_menu = widgetutils.make_menu()
        self.recent_models_menu = widgetutils.make_menu()
        self.main_menu = widgetutils.make_menu()
        self.menu_open: Optional[tk.Menu] = None

    def fill(self) -> None:
        for key in config.saved_configs:
            self.fill_widget(key, getattr(config, key))

    def fill_widget(self, key: str, value: Any) -> None:
        widget = getattr(self, key)

        if type(widget) == tk.Entry or type(widget) == tk.Text:
            widgetutils.set_text(widget, value)
        elif type(widget) == ttk.Combobox:
            widgetutils.set_select(widget, value)

    def setup(self) -> None:
        import state
        from model import model

        self.fill()

        self.output_menu.add_command(label="Clear", command=lambda: self.clear_output())
        self.output_menu.add_command(label="Select All", command=lambda: widgetutils.select_all(self.output))
        self.output_menu.add_command(label="Copy All", command=lambda: widgetutils.copy_all(self.output))

        self.model_menu.add_command(label="Recent Models", command=lambda: self.show_recent_models())
        self.model_menu.add_command(label="Browse Models", command=lambda: self.browse_model())
        self.model_menu.add_command(label="Reset Models", command=lambda: state.reset_models())

        self.main_menu.add_command(label="Reset Config", command=lambda: state.reset_config())
        self.main_menu.add_command(label="Save Log", command=lambda: state.save_log())
        self.main_menu.add_command(label="Exit", command=lambda: app.exit())

        self.output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        self.model_menu_button.bind("<Button-1>", lambda e: self.show_model_menu(e))
        self.main_menu_button.bind("<Button-1>", lambda e: self.show_main_menu(e))
        self.stop_button.bind("<Button-1>", lambda e: model.stop_stream())

        self.output.bind("<Button-1>", lambda e: self.hide_menu())
        self.input.bind("<Button-1>", lambda e: self.hide_menu())

        self.input.bind("<Return>", lambda e: self.submit())

        self.name_user.bind("<FocusOut>", lambda e: state.update_name_user())
        self.name_ai.bind("<FocusOut>", lambda e: state.update_name_ai())
        self.max_tokens.bind("<FocusOut>", lambda e: state.update_max_tokens())
        self.temperature.bind("<FocusOut>", lambda e: state.update_temperature())
        self.system.bind("<FocusOut>", lambda e: state.update_system())
        self.top_k.bind("<FocusOut>", lambda e: state.update_top_k())
        self.top_p.bind("<FocusOut>", lambda e: state.update_top_p())
        self.context.bind("<FocusOut>", lambda e: state.update_context())
        self.output.tag_config("name_user", foreground="#87CEEB")
        self.output.tag_config("name_ai", foreground="#98FB98")
        self.input_history: List[str] = []
        self.input_history_index = 0

        def on_key(event: Any) -> None:
            if event.widget == self.output:
                if event.char:
                    # Focus the input and insert char
                    self.input.focus_set()
                    self.input.insert(tk.END, event.char)
            elif event.widget == self.input:
                if event.keysym == "Up":
                    self.input_history_up()
                elif event.keysym == "Down":
                    self.input_history_down()

        app.root.bind("<KeyPress>", on_key)

        self.deactivate_stop()
        self.input.focus_set()
        self.add_reset_menus()

    def add_to_input_history(self, text: str) -> None:
        self.input_history.append(text)

        if len(self.input_history) > 100:
            self.input_history.pop(0)

    def apply_input_history(self) -> None:
        text = self.input_history[self.input_history_index]
        self.input.delete(0, tk.END)
        self.input.insert(0, text)

    def input_history_down(self) -> None:
        if self.input_history:
            self.input_history_index = (self.input_history_index + 1) % len(self.input_history)
            self.apply_input_history()

    def input_history_up(self) -> None:
        if self.input_history:
            self.input_history_index = (self.input_history_index - 1) % len(self.input_history)
            self.apply_input_history()

    def print(self, text: str, linebreak: bool = True) -> None:
        if not app.exists():
            return

        left = ""
        right = ""

        if widgetutils.text_length(self.output) and \
                (widgetutils.last_character(self.output) != "\n"):
            left = "\n"

        if linebreak:
            right = "\n"

        text = left + text + right
        widgetutils.insert_text(self.output, text, True)
        widgetutils.to_bottom(self.output)

    def insert(self, text: str) -> None:
        if not app.exists():
            return

        widgetutils.insert_text(self.output, text, True)
        widgetutils.to_bottom(self.output)

    def show_output_menu(self, event: Any) -> None:
        self.open_menu(self.output_menu, event)

    def show_recent_models(self) -> None:
        import state
        self.recent_models_menu.delete(0, tk.END)

        for model in config.models:
            def proc(model: str = model) -> None:
                self.set_model(model)

            self.recent_models_menu.add_command(label=model, command=proc)

        if not config.models:
            self.recent_models_menu.add_command(label="Empty", command=lambda: state.models_info())

        self.open_menu(self.recent_models_menu, self.last_menu_event)

    def open_menu(self, menu: tk.Menu, event: Optional[Any] = None) -> None:
        self.hide_menu()

        if event:
            menu_width = menu.winfo_reqwidth()
            x = event.x_root - menu_width if event.x_root - menu_width > 0 else event.x_root
            menu.post(x, event.y_root)
        else:
            widgetutils.show_menu_at_center(menu)

        self.last_menu_event = event
        self.menu_open = menu

    def hide_menu(self) -> None:
        if self.menu_open:
            self.menu_open.unpost()
            self.menu_open = None

    def browse_model(self) -> None:
        import state
        file = filedialog.askopenfilename(initialdir=state.get_models_dir())

        if file:
            widgetutils.set_text(self.model, file)
            state.update_model()

    def submit(self) -> None:
        from model import model
        text = self.input.get()

        if text:
            self.add_to_input_history(text)
            self.clear_input()
            model.stream(text)

    def clear_output(self) -> None:
        def clear() -> None:
            widgetutils.clear_text(self.output, True)

        widgetutils.show_confirm("Clear all output text?", clear, None)

    def clear_input(self) -> None:
        widgetutils.clear_text(self.input)

    def prompt(self, who: str) -> None:
        name = getattr(config, f"name_{who}")
        prompt = f"\n{name}: "
        self.print(prompt, False)
        start_index = self.output.index(f"end - {len(prompt)}c")
        end_index = self.output.index("end - 3c")
        self.output.tag_add(f"name_{who}", start_index, end_index)

    def set_model(self, model: str) -> None:
        import state
        widgetutils.set_text(self.model, model)
        state.update_model()

    def intro(self) -> None:
        for line in config.intro:
            self.print(line)

    def show_model(self) -> None:
        widgetutils.set_text(self.model, config.model)

    def update(self) -> None:
        app.root.update_idletasks()

    def show_main_menu(self, event: Any) -> None:
        self.open_menu(self.main_menu, event)

    def show_model_menu(self, event: Any) -> None:
        self.open_menu(self.model_menu, event)

    def add_reset_menus(self) -> None:
        import state

        def add_menu(key: str) -> None:
            widget = getattr(self, key)
            menu = widgetutils.make_menu()

            reset_func = partial(state.reset_one_config, key=key)
            menu.add_command(label=f"Reset", command=reset_func)

            if key != "model":
                show_func = partial(self.open_menu, menu=menu)
                widget.bind("<Button-3>", lambda e: show_func(event=e))

            widget.bind("<Button-1>", lambda e: self.hide_menu())

        for key in config.saved_configs:
            add_menu(key)

    def deactivate_stop(self) -> None:
        if app.exists():
            self.stop_button.configure(background=config.stop_background_disabled)
            self.stop_button.config(state="disabled")

    def activate_stop(self) -> None:
        if app.exists():
            self.stop_button.configure(background=config.stop_background)
            self.stop_button.config(state="normal")


widgets: Widgets = Widgets()
