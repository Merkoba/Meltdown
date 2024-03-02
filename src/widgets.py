# Modules
from config import config
import widgetutils
from framedata import FrameData

# Standard
import tkinter as tk
from typing import Any
from tkinter import filedialog
from typing import Optional, Any


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
        ToolTip(self.model, "Path to a model file. This should be a file that works with \
                llama.cpp, like gguf files for instance. Right click to see recently used models")

        browse_button = widgetutils.make_button(d, "Browse", lambda: self.browse_model())
        ToolTip(browse_button, "Pick a model file from your file system")

        main_menu_button = widgetutils.make_button(d, "Menu", lambda: self.show_main_menu())
        ToolTip(main_menu_button, "Open the main menu")

        # Settings
        d = get_d()

        widgetutils.make_label(d, "User")
        self.name_user = widgetutils.make_input(d)
        ToolTip(self.name_user, "The name of the user (you)")

        widgetutils.make_label(d, "AI")
        self.name_ai = widgetutils.make_input(d)
        ToolTip(self.name_ai, "The name of the assistant (AI)")

        widgetutils.make_label(d, "Tokens")
        self.max_tokens = widgetutils.make_input(d)
        ToolTip(self.max_tokens, "Maximum number of tokens to generate. \
                Higher values will result in longer output, but will \
                also take longer to compute")

        widgetutils.make_label(d, "Temp")
        self.temperature = widgetutils.make_input(d)
        ToolTip(self.temperature, "The temperature parameter is used to control \
                the randomness of the output. A higher temperature (~1) results in more randomness \
                and diversity in the generated text, as the model is more likely to \
                explore a wider range of possible tokens. Conversely, a lower temperature \
                (<1) produces more focused and deterministic output, emphasizing the \
                most probable tokens")

        # System
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)

        widgetutils.make_label(d, "System")
        self.system = widgetutils.make_input(d, sticky="ew")
        ToolTip(self.system, "This sets the system message that instructs \
                the AI how to respond, or how to act in general. \
                You could use this to make the AI take on a specific persona or role")

        widgetutils.make_label(d, "Top K")
        self.top_k = widgetutils.make_input(d)
        ToolTip(self.top_k, "The top-k parameter limits the model's \
                predictions to the top k most probable tokens at each step \
                of generation. By setting a value for k, you are instructing \
                the model to consider only the k most likely tokens. \
                This can help in fine-tuning the generated output and \
                ensuring it adheres to specific patterns or constraints")

        widgetutils.make_label(d, "Top P")
        self.top_p = widgetutils.make_input(d)
        ToolTip(self.top_p, "Top-p, also known as nucleus sampling, controls \
                the cumulative probability of the generated tokens. \
                The model generates tokens until the cumulative probability \
                exceeds the chosen threshold (p). This approach allows for \
                more dynamic control over the length of the generated text \
                and encourages diversity in the output by including less \
                probable tokens when necessary")

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

        widgetutils.make_label(d, "Context")
        values = [0, 1, 5, 10, 100]
        self.context = widgetutils.make_select(d, values)
        self.context.configure(width=5)
        ToolTip(self.context, "The number of previous messages to include as the context.\
                The computation will take longer with more context. \
                0 means context is not used at all")

        widgetutils.make_button(d, "Submit", lambda: self.submit())

        self.output_menu = tk.Menu(config.app, tearoff=0, font=config.font)
        self.model_menu = tk.Menu(config.app, tearoff=0, font=config.font)
        self.main_menu = tk.Menu(config.app, tearoff=0, font=config.font)

    def fill(self) -> None:
        widgetutils.set_text(self.model, config.model)
        widgetutils.set_text(self.name_user, config.name_user)
        widgetutils.set_text(self.name_ai, config.name_ai)
        widgetutils.set_text(self.max_tokens, config.max_tokens)
        widgetutils.set_text(self.temperature, config.temperature)
        widgetutils.set_text(self.system, config.system)
        widgetutils.set_text(self.top_k, config.top_k)
        widgetutils.set_text(self.top_p, config.top_p)
        widgetutils.set_select(self.context, config.context)

    def setup(self) -> None:
        import state

        self.fill()

        self.model.bind("<Button-3>", lambda e: self.show_model_menu(e))
        self.model.bind("<Button-1>", lambda e: self.hide_menus())
        self.model.bind("<Button-1>", lambda e: self.hide_menus())

        self.output_menu.add_command(label="Clear", command=lambda: self.clear_output())
        self.output_menu.add_command(label="Select All", command=lambda: widgetutils.select_all(self.output))
        self.output_menu.add_command(label="Copy All", command=lambda: widgetutils.copy_all(self.output))

        self.main_menu.add_command(label="Recent Models", command=lambda: self.show_model_menu(None))
        self.main_menu.add_command(label="Reset Config", command=lambda: state.reset_config())
        self.main_menu.add_command(label="Reset Models", command=lambda: state.reset_models())
        self.main_menu.add_command(label="Save Log", command=lambda: state.save_log())

        self.output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        self.output.bind("<Button-1>", lambda e: self.hide_menus())
        self.output.bind("<Button-1>", lambda e: self.hide_menus())

        self.input.bind("<Return>", lambda e: self.submit())

        self.name_user.bind("<FocusOut>", lambda e: state.update_name_user())
        self.name_ai.bind("<FocusOut>", lambda e: state.update_name_ai())
        self.max_tokens.bind("<FocusOut>", lambda e: state.update_max_tokens())
        self.temperature.bind("<FocusOut>", lambda e: state.update_temperature())
        self.system.bind("<FocusOut>", lambda e: state.update_system())
        self.model.bind("<FocusOut>", lambda e: state.update_model())
        self.top_k.bind("<FocusOut>", lambda e: state.update_top_k())
        self.top_p.bind("<FocusOut>", lambda e: state.update_top_p())
        self.context.bind("<<ComboboxSelected>>", lambda e: state.update_context())

        def on_key(event: Any) -> None:
            if event.widget == self.output:
                if event.char:
                    # Focus the input and insert char
                    self.input.focus_set()
                    self.input.insert(tk.END, event.char)

        config.app.bind("<KeyPress>", on_key)

        self.input.focus_set()

    def print(self, text: str, linebreak: bool = True) -> None:
        if not widgetutils.exists():
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
        if not widgetutils.exists():
            return

        widgetutils.insert_text(self.output, text, True)
        widgetutils.to_bottom(self.output)

    def show_output_menu(self, event: Any) -> None:
        self.output_menu.post(event.x_root, event.y_root)

    def hide_output_menu(self) -> None:
        self.output_menu.unpost()

    def show_model_menu(self, event: Any) -> None:
        import state

        self.model_menu.delete(0, tk.END)

        for model in config.models:
            def proc(model: str = model) -> None:
                self.set_model(model)

            self.model_menu.add_command(label=model, command=proc)

        if len(config.models):
            self.model_menu.add_separator()
            self.model_menu.add_command(label="Reset", command=lambda: state.reset_models())
        else:
            self.model_menu.add_command(label="Empty", command=lambda: state.models_info())

        if event:
            self.model_menu.post(event.x_root, event.y_root)
        else:
            widgetutils.show_menu_at_center(self.model_menu)

    def hide_model_menu(self) -> None:
        self.model_menu.unpost()

    def hide_menus(self) -> None:
        self.hide_output_menu()
        self.hide_model_menu()
        self.hide_main_menu()

    def browse_model(self) -> None:
        import state
        file = filedialog.askopenfilename(initialdir=state.get_models_dir())
        widgetutils.set_text(self.model, file)
        state.update_model()

    def submit(self) -> None:
        from model import model
        text = self.input.get()

        if text:
            self.clear_input()
            model.stream(text)

    def clear_output(self) -> None:
        widgetutils.clear_text(self.output, True)

    def clear_input(self) -> None:
        widgetutils.clear_text(self.input)

    def prompt(self, who: str) -> None:
        name = getattr(config, f"name_{who}")
        prompt = f"{name}: "
        self.print(prompt, False)

    def set_model(self, model: str) -> None:
        import state
        widgetutils.set_text(self.model, model)
        state.update_model()

    def intro(self) -> None:
        self.print("Welcome to Meltdown")
        self.print("Type a prompt and press Enter to continue")
        self.print("The specified model will load automatically")

    def show_model(self) -> None:
        widgetutils.set_text(self.model, config.model)

    def update(self) -> None:
        config.app.update_idletasks()

    def show_main_menu(self) -> None:
        widgetutils.show_menu_at_center(self.main_menu)

    def hide_main_menu(self) -> None:
        self.main_menu.unpost()


widgets: Widgets = Widgets()
