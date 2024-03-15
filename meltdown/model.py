# Modules
from .config import config
from .widgets import widgets
from .session import session
from . import timeutils
from . import state

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import threading
from pathlib import Path
from typing import Optional
from tkinter import filedialog


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

    def unload(self, announce: bool = False) -> None:
        if self.model_loading:
            return

        self.stop_stream()

        if self.model:
            self.model = None
            self.loaded_model = ""
            self.loaded_format = ""

            if announce:
                widgets.display.print("\n👻 Model unloaded")

    def load(self, prompt: str = "", tab_id: str = "") -> None:
        if not config.model:
            return

        if self.is_loading():
            print("(Load) Slow down!")
            return

        model_path = Path(config.model)

        if not tab_id:
            tab_id = widgets.display.current_tab

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.display.print("Error: Model not found. Check the path.", tab_id=tab_id)
            return

        def wrapper() -> None:
            self.do_load(config.model)

            if prompt:
                self.stream(prompt, tab_id)

        self.unload()
        self.load_thread = threading.Thread(target=wrapper, args=())
        self.load_thread.daemon = True
        self.load_thread.start()

    def do_load(self, model: str) -> None:
        from .app import app
        self.lock.acquire()
        self.model_loading = True

        now = timeutils.now()
        cformat = config.format

        try:
            fmt = config.format if (cformat != "auto") else None
            name = Path(model).name
            widgets.display.print(f"\n🫠 Loading {name}")
            app.update()

            self.model = Llama(
                model_path=str(model),
                chat_format=fmt,
                n_ctx=2048,
                verbose=False,
            )
        except BaseException as e:
            widgets.display.print("Error: Model failed to load.")
            self.model_loading = False
            print(e)
            return

        self.model_loading = False
        self.loaded_model = model
        self.loaded_format = cformat
        msg, now = timeutils.check_time("Model loaded", now)
        widgets.display.print(msg)
        self.lock.release()
        return

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=3)
            widgets.display.print("\n* Interrupted *")

    def stream(self, prompt: str, tab_id: str) -> None:
        if self.is_loading():
            print("(Stream) Slow down!")
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

        def replace_content(content: str) -> str:
            if config.name_user:
                content = content.replace("@name_user", config.name_user)

            if config.name_ai:
                content = content.replace("@name_ai", config.name_ai)

            content = content.replace("@date", timeutils.today())
            return content

        def check_dot(text: str) -> str:
            if text.endswith(".") or text.endswith("!") or text.endswith("?"):
                return text + " "
            else:
                return text + ". "

        if config.prepend:
            prompt = check_dot(config.prepend) + prompt

        if config.append:
            prompt = check_dot(prompt) + config.append

        widgets.prompt("user", tab_id=tab_id)
        widgets.display.insert(prompt, tab_id=tab_id)
        widgets.enable_stop_button()

        tab = widgets.display.get_tab(tab_id)

        if not tab:
            return

        document = session.get_document(tab.document_id)

        if not document:
            return

        log_dict = {"user": prompt}
        system = replace_content(config.system)
        messages = [{"role": "system", "content": system}]

        if document.items:
            for item in document.items[-config.context:]:
                for key in item:
                    content = item[key]

                    if key == "user":
                        content = replace_content(content)

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
        content = replace_content(content)
        messages.append({"role": "user", "content": content})

        added_name = False
        token_printed = False
        last_token = " "
        tokens = []

        state.add_model(config.model)
        state.add_system(config.system)
        state.add_prepends(config.prepend)
        state.add_appends(config.append)

        now = timeutils.now()
        self.stream_date = now

        try:
            output = self.model.create_chat_completion(
                stream=True,
                messages=messages,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_k=config.top_k,
                top_p=config.top_p,
                seed=config.seed,
            )
        except BaseException as e:
            self.stream_loading = False
            return

        self.stream_loading = False

        if self.stream_date != now:
            return

        if self.stop_stream_thread.is_set():
            return

        try:
            for chunk in output:
                if self.stop_stream_thread.is_set():
                    break

                delta = chunk["choices"][0]["delta"]

                if "content" in delta:
                    if not added_name:
                        widgets.prompt("ai", tab_id=tab_id)
                        added_name = True

                    token = delta["content"]

                    if token == "\n":
                        if not token_printed:
                            continue
                    elif token == " ":
                        if last_token == " ":
                            continue

                    last_token = token

                    if not token_printed:
                        token = token.lstrip()
                        token_printed = True

                    tokens.append(token)
                    widgets.display.insert(token, tab_id=tab_id)
        except BaseException:
            pass

        if tokens:
            log_dict["assistant"] = "".join(tokens).strip()
            document.add(log_dict)

        self.lock.release()

    def browse_models(self) -> None:
        from . import state
        from . import widgetutils

        if self.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=state.get_models_dir())

        if file:
            widgetutils.set_text(widgets.model, file)
            state.update_config("model")
            self.load()

    def load_or_unload(self) -> None:
        if self.model_loading:
            return

        if self.loaded_model:
            self.unload(True)
        else:
            self.load()


model = Model()
