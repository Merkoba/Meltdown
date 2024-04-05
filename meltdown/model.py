# Modules
from .config import config
from .widgets import widgets
from .display import display
from .session import session
from .app import app
from .args import args
from . import timeutils
from . import filemanager

# Libraries
from llama_cpp import Llama  # type: ignore
from openai import OpenAI  # type: ignore

# Standard
import threading
from pathlib import Path
from typing import Optional
from tkinter import filedialog
from typing import List, Tuple


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_stream_thread = threading.Event()
        self.stream_thread = threading.Thread()
        self.streaming = False
        self.stream_loading = False
        self.model: Optional[Llama] = None
        self.model_loading = False
        self.loaded_model = ""
        self.loaded_format = ""
        self.load_thread = threading.Thread()
        self.stream_date = 0.0
        self.gpt_client = None
        self.gpts: List[Tuple[str, str]] = [
            ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
            ("gpt-4-turbo", "GPT-4 Turbo"),
            ("gpt-4-turbo-preview", "GPT-4 Turbo Preview"),
        ]
        self.gpt_key = ""

    def setup(self) -> None:
        self.update_icon()

    def unload(self, announce: bool = False) -> None:
        if self.model_loading:
            return

        self.stop_stream()

        if self.model and announce:
            display.print("👻 Model unloaded")

        self.clear_model()

    def model_is_gpt(self, name: str) -> bool:
        return any(name == gpt[0] for gpt in self.gpts)

    def load(self, prompt: str = "", tab_id: str = "") -> None:
        if not config.model:
            display.print("You must configure a model first."
                          " It can be a local model which you can download"
                          " from the HuggingFace website (or elsewhere), or a remote ChatGPT model by"
                          " using your API key. Check the main menu on the top right.", tab_id=tab_id)
            return

        if self.loaded_model == config.model:
            if self.loaded_format == config.format:
                return

        if self.is_loading():
            print("(Load) Slow down!")
            return

        if self.model_is_gpt(config.model):
            self.unload()
            self.load_gpt(prompt, tab_id)
            return

        model_path = Path(config.model)

        if not tab_id:
            tab_id = display.current_tab

        if (not model_path.exists()) or (not model_path.is_file()):
            display.print("Error: Model not found. Check the path.", tab_id=tab_id)
            return

        def wrapper() -> None:
            self.load_local(config.model, tab_id)

            if prompt:
                self.stream(prompt, tab_id)

        self.unload()
        self.load_thread = threading.Thread(target=wrapper, args=())
        self.load_thread.daemon = True
        self.load_thread.start()

    def clear_model(self) -> None:
        self.model = None
        self.loaded_model = ""
        self.model_loading = False
        self.loaded_format = ""
        self.update_icon()

    def read_gpt_key(self) -> None:
        from .paths import paths

        try:
            with open(paths.apikey, "r", encoding="utf-8") as file:
                self.gpt_key = file.read().strip()
        except BaseException:
            self.gpt_key = ""

    def load_gpt(self, prompt: str, tab_id: str) -> None:
        try:
            self.read_gpt_key()

            if not self.gpt_key:
                display.print("Error: API key not found."
                              " You need to export it as OPENAI_API_KEY before running this program.")
                self.clear_model()
                return

            self.gpt_client = OpenAI(
                api_key=self.gpt_key
            )

            self.model = config.model
            self.model_loading = False
            self.loaded_model = config.model
            self.loaded_format = "gpt_remote"
            filemanager.add_model(config.model)
            display.print(f"🌐 {config.model} is ready to use")
            self.update_icon()

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException:
            display.print("Error: GPT model failed to load.")
            self.clear_model()

    def load_local(self, model: str, tab_id: str) -> None:
        from .app import app
        self.lock.acquire()
        self.model_loading = True

        now = timeutils.now()
        chat_format = config.format

        try:
            fmt = config.format if (chat_format != "auto") else None
            name = Path(model).name
            mlock = True if (config.mlock == "yes") else False
            display.to_bottom(tab_id)
            display.print(f"🫠 Loading {name}", tab_id=tab_id)
            app.update()

            self.model = Llama(
                model_path=str(model),
                chat_format=fmt,
                n_ctx=2048,
                use_mlock=mlock,
                n_threads=config.threads,
                verbose=False,
            )
        except BaseException as e:
            print(e)
            display.print("Error: Model failed to load.")
            self.clear_model()
            self.lock.release()
            return

        filemanager.add_model(model)
        self.model_loading = False
        self.loaded_model = model
        self.loaded_format = chat_format
        msg, now = timeutils.check_time("Model loaded", now)
        self.update_icon()
        display.print(msg)
        self.lock.release()

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stop_stream_thread.is_set():
            return

        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=3)
            display.print("< Interrupted >")

    def stream(self, prompt: str, tab_id: str) -> None:
        if self.is_loading():
            print("(Stream) Slow down!")
            return

        tab = display.get_tab(tab_id)

        if not tab:
            return

        if tab.mode == "ignore":
            return

        if not self.model:
            self.load(prompt, tab_id)
            return

        def wrapper(prompt: str, tab_id: str) -> None:
            self.stop_stream_thread.clear()
            self.streaming = True
            self.do_stream(prompt, tab_id)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=wrapper, args=(prompt, tab_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def do_stream(self, prompt: str, tab_id: str) -> None:
        self.lock.acquire()
        self.stream_loading = True

        widgets.show_model()
        prompt = prompt.strip()

        if not self.model:
            print("Model not loaded")
            return

        if not prompt:
            print("Empty prompt")
            return

        if config.prepend:
            prompt = self.check_dot(config.prepend) + prompt

        if config.append:
            prompt = self.check_dot(prompt) + config.append

        tab = display.get_tab(tab_id)

        if not tab:
            return

        if tab.mode == "ignore":
            return

        display.prompt("user", text=prompt, tab_id=tab_id)
        widgets.enable_stop_button()
        conversation = session.get_conversation(tab.conversation_id)

        if not conversation:
            return

        log_dict = {"user": prompt}
        system = self.replace_content(config.system)
        messages = [{"role": "system", "content": system}]

        if conversation.items:
            for item in conversation.items[-abs(config.context):]:
                for key in item:
                    content = item[key]

                    if key == "user":
                        content = self.replace_content(content)

                    messages.append({"role": key, "content": content})

        if config.printlogs:
            print("-----")
            print("prompt:", prompt)
            print("messages:", len(messages))
            print("context:", config.context)
            print("max_tokens:", config.max_tokens)
            print("temperature:", config.temperature)
            print("top_k:", config.top_k)
            print("top_p:", config.top_p)
            print("seed:", config.seed)

        content = prompt
        content = self.replace_content(content)
        messages.append({"role": "user", "content": content})

        added_name = False
        token_printed = False
        last_token = " "
        tokens = []

        filemanager.add_system(config.system)
        filemanager.add_prepends(config.prepend)
        filemanager.add_appends(config.append)

        now = timeutils.now()
        self.stream_date = now
        stream = args.stream

        if self.model_is_gpt(config.model):
            try:
                if not self.gpt_client:
                    return

                output = self.gpt_client.chat.completions.create(
                    stream=stream,
                    model=config.model,
                    messages=messages,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    top_p=config.top_p,
                    seed=config.seed,
                )
            except BaseException:
                display.print("Error: GPT model failed to stream."
                              " You might not have access to this particular model,"
                              " not enough credits, invalid API key,"
                              " or there is no internet connection.")
                self.stream_loading = False
                self.lock.release()
                return
        else:
            try:
                output = self.model.create_chat_completion_openai_v1(
                    stream=stream,
                    messages=messages,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    top_k=config.top_k,
                    top_p=config.top_p,
                    seed=config.seed,
                )
            except BaseException as e:
                print(e)
                self.stream_loading = False
                self.lock.release()
                return

        self.stream_loading = False

        if self.stream_date != now:
            return

        if self.stop_stream_thread.is_set():
            if self.lock.locked():
                self.lock.release()

            return

        if stream:
            try:
                for chunk in output:
                    if self.stop_stream_thread.is_set():
                        break

                    delta = chunk.choices[0].delta

                    if hasattr(delta, "content"):
                        if not added_name:
                            display.prompt("ai", tab_id=tab_id)
                            added_name = True

                        token = delta.content

                        if token == "\n":
                            if not token_printed:
                                continue
                        elif token == " ":
                            if last_token == " ":
                                continue

                        last_token = token

                        if token is not None:
                            if not token_printed:
                                token = token.lstrip()
                                token_printed = True

                            tokens.append(token)
                            display.insert(token, tab_id=tab_id)
            except BaseException as e:
                print(e)
        else:
            try:
                response = output.choices[0].message.content.strip()

                if response:
                    display.prompt("ai", tab_id=tab_id)
                    display.insert(response, tab_id=tab_id)
            except BaseException as e:
                print(e)

        if tokens:
            log_dict["assistant"] = "".join(tokens).strip()
            conversation.add(log_dict)

        self.lock.release()

    def browse_models(self) -> None:
        from .config import config

        if self.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=self.get_dir())

        if file:
            widgets.model.set_text(file)
            config.update("model")
            self.load()

    def load_or_unload(self) -> None:
        if self.model_loading:
            return

        if self.loaded_model:
            self.unload(True)
        else:
            self.load()

    def update_icon(self) -> None:
        if not app.exists():
            return

        icon = widgets.model_icon
        tooltip = widgets.model_icon_tooltip

        if not self.loaded_model:
            icon.configure(text="👻")
            tooltip.set_text("No model is loaded. Pick a local or GPT model to start chatting")
        elif self.model_is_gpt(self.loaded_model):
            icon.configure(text="🌐")
            tooltip.set_text("You are using a remote service."
                             " Its usage might cost money. Internet connection is required")
        else:
            icon.configure(text="🫠")
            tooltip.set_text("You are using a local model. No network requests are made")

    def set_api_key(self) -> None:
        from .dialogs import Dialog
        from .paths import paths

        def action(key: str) -> None:
            if not key:
                return

            path = Path(paths.apikey)

            if (not path.exists()) or not (path.is_file()):
                path.parent.mkdir(parents=True, exist_ok=True)
                Path.touch(paths.apikey, exist_ok=True)

            with open(path, "w", encoding="utf-8") as file:
                file.write(key)

        Dialog.show_input("OpenAI API Key", lambda text: action(text))

    def replace_content(self, content: str) -> str:
        if config.name_user:
            content = content.replace("@name_user", config.name_user)

        if config.name_ai:
            content = content.replace("@name_ai", config.name_ai)

        content = content.replace("@date", timeutils.today())
        return content

    def check_dot(self, text: str) -> str:
        if not text:
            return ""

        chars = [".", ",", ";", "!", "?"]

        if text[-1] in chars:
            return text + " "
        else:
            return text + ". "

    def get_dir(self) -> Optional[str]:
        models = [config.model] + config.models

        for model in models:
            path = Path(model)

            if path.exists() and path.is_file():
                return str(path.parent)

        return None

    def check_config(self, save: bool = True) -> None:
        if (not config.model) and config.models:
            config.model = config.models[0]

            if save:
                config.save()


model = Model()
