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
import atexit
from typing import List, Dict


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_thread = threading.Event()
        self.thread = threading.Thread()
        self.context_list: List[Dict[str, str]] = []
        self.loaded_model = ""
        self.streaming = False
        atexit.register(self.stop_stream)

    def load(self, model: str) -> bool:
        if not model:
            return False

        model_path = Path(model)

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.print("Model not found.")
            return False

        self.stop_stream()
        now = timeutils.now()

        try:
            fmt = config.format if (config.format != "auto") else None

            widgets.print("\n🫠 Loading model...")
            widgets.update()

            self.model = Llama(
                model_path=str(model_path),
                chat_format=fmt,
                verbose=False,
            )
        except BaseException as e:
            widgets.print("Model failed to load.")
            return False

        self.loaded_model = model
        self.context_list = []
        msg, now = timeutils.check_time("Model loaded", now)
        widgets.print(msg)
        return True

    def reset_context(self) -> None:
        self.context_list = []

    def stream(self, prompt: str) -> None:
        if not self.loaded_model:
            if not self.load(config.model):
                return

        def wrapper(prompt: str) -> None:
            self.streaming = True
            self.do_stream(prompt)
            self.streaming = False

        self.stop_stream()
        self.thread = threading.Thread(target=wrapper, args=(prompt,))
        self.thread.start()

    def do_stream(self, prompt: str) -> None:
        self.lock.acquire()
        widgets.show_model()
        prompt = prompt.strip()

        if not prompt:
            return

        widgets.prompt("user")
        widgets.insert(prompt)
        widgets.enable_stop()

        if config.context > 0:
            context_dict = {"user": prompt}
        else:
            context_dict = None

        messages = [{"role": "system", "content": config.system}]

        if self.context_list:
            for item in self.context_list:
                for key in item:
                    messages.append({"role": key, "content": item[key]})

        messages.append({"role": "user", "content": prompt})

        added_name = False
        token_printed = False
        last_token = " "
        tokens = []

        state.add_model(config.model)
        state.add_system(config.system)
        state.add_input(prompt)

        output = self.model.create_chat_completion(
            stream=True,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_k=config.top_k,
            top_p=config.top_p,
            seed=config.seed,
        )

        for chunk in output:
            if self.stop_thread.is_set():
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

        if context_dict:
            context_dict["assistant"] = "".join(tokens).strip()
            self.add_context(context_dict)

        self.lock.release()

    def add_context(self, context_dict: Dict[str, str]) -> None:
        self.context_list.append(context_dict)

        if len(self.context_list) > config.context:
            self.context_list.pop(0)

    def stop_stream(self) -> None:
        if self.thread and self.thread.is_alive():
            self.stop_thread.set()
            self.thread.join()
            self.stop_thread.clear()
            widgets.print("\n* Interrupted *")


model = Model()
