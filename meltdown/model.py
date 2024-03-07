# Modules
from .config import config
from .widgets import widgets
from . import timeutils
from . import state

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import threading
from pathlib import Path
from typing import List, Dict, Optional


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_stream_thread = threading.Event()
        self.stream_thread = threading.Thread()
        self.context_list: List[Dict[str, str]] = []
        self.streaming = False
        self.stream_loading = False
        self.model: Optional[Llama] = None
        self.model_loading = False
        self.stop_load_thread = threading.Event()
        self.load_thread = threading.Thread()
        self.stream_date = 0.0

    def unload(self) -> None:
        self.stop_stream()

        if self.model:
            self.model = None
            widgets.print("\n👻 Model unloaded")
            self.reset_context()

    def load(self, prompt: str = "") -> None:
        if not config.model:
            return

        if self.is_loading():
            print("(Load) Slow down!")
            return

        model_path = Path(config.model)

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.print("Error: Model not found. Check the path.")
            return

        def wrapper() -> None:
            self.do_load(config.model)

            if prompt:
                self.stream(prompt)

        self.unload()
        self.load_thread = threading.Thread(target=wrapper, args=())
        self.load_thread.daemon = True
        self.load_thread.start()

    def do_load(self, model: str) -> None:
        self.lock.acquire()
        self.model_loading = True

        now = timeutils.now()

        try:
            fmt = config.format if (config.format != "auto") else None
            name = Path(model).name
            widgets.print(f"\n🫠 Loading {name}")
            widgets.update()

            self.model = Llama(
                model_path=str(model),
                chat_format=fmt,
                verbose=False,
            )
        except BaseException as e:
            widgets.print("Error: Model failed to load.")
            self.model_loading = False
            print(e)
            return

        self.model_loading = False
        self.reset_context()
        msg, now = timeutils.check_time("Model loaded", now)
        widgets.print(msg)
        self.lock.release()
        return

    def reset_context(self) -> None:
        self.context_list = []

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=3)
            self.stop_stream_thread.clear()
            widgets.print("\n* Interrupted *")

    def stream(self, prompt: str) -> None:
        if self.is_loading():
            print("(Stream) Slow down!")
            return

        if not self.model:
            self.load(prompt)
            return

        def wrapper(prompt: str) -> None:
            self.streaming = True
            self.do_stream(prompt)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=wrapper, args=(prompt,))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def do_stream(self, prompt: str) -> None:
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

            return content

        widgets.prompt("user")
        widgets.insert(prompt)
        widgets.enable_stop_button()

        full_prompt = prompt

        if config.prepend:
            full_prompt = config.prepend + ". " + full_prompt

        if config.append:
            full_prompt = full_prompt + ". " + config.append

        print("Prompt:", full_prompt)

        if config.context > 0:
            context_dict = {"user": full_prompt}
        else:
            context_dict = None

        system = replace_content(config.system)
        messages = [{"role": "system", "content": system}]

        if self.context_list:
            for item in self.context_list:
                for key in item:
                    content = item[key]

                    if key == "user":
                        content = replace_content(content)

                    messages.append({"role": key, "content": content})

        content = full_prompt
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
        state.add_input(prompt)

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
            print("Stream Error:", e)
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
                        widgets.prompt("ai")
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
                    widgets.insert(token)
        except BaseException as e:
            print("Stream Read Error:", e)

        if context_dict and tokens:
            context_dict["assistant"] = "".join(tokens).strip()
            self.add_context(context_dict)

        self.lock.release()

    def add_context(self, context_dict: Dict[str, str]) -> None:
        self.context_list.append(context_dict)

        if len(self.context_list) > config.context:
            self.context_list.pop(0)


model = Model()
