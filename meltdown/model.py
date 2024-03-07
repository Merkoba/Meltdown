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
from typing import List, Dict, Optional


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_thread = threading.Event()
        self.thread = threading.Thread()
        self.context_list: List[Dict[str, str]] = []
        self.streaming = False
        self.model: Optional[Llama] = None
        atexit.register(self.stop_stream)

    def unload(self) -> None:
        self.stop_stream()
        self.model = None
        self.reset_context()

    def load(self, model: str) -> bool:
        if not model:
            return False

        model_path = Path(model)

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.print("Model not found.")
            return False

        self.unload()
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

        self.reset_context()
        msg, now = timeutils.check_time("Model loaded", now)
        widgets.print(msg)
        return True

    def reset_context(self) -> None:
        self.context_list = []

    def stream(self, prompt: str) -> None:
        if not self.model:
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

        def replace_content(content: str) -> str:
            content = content.replace("@name_user", config.name_user)
            content = content.replace("@name_ai", config.name_ai)
            return content

        widgets.prompt("user")
        widgets.insert(prompt)
        widgets.enable_stop()

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

        output = self.model.create_chat_completion(
            stream=True,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_k=config.top_k,
            top_p=config.top_p,
            seed=config.seed,
        )

        try:
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
        except BaseException as e:
            print("Stream Error:", e)

        if context_dict and tokens:
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
            self.thread.join(timeout=3)
            self.stop_thread.clear()
            widgets.print("\n* Interrupted *")


model = Model()
