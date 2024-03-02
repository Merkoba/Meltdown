# Modules
from config import config
from widgets import widgets
import timeutils

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import threading
from pathlib import Path
import atexit
from typing import List, Any


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_thread = threading.Event()
        self.thread = threading.Thread()
        self.context: List[Any] = []
        self.loaded_model = ""
        atexit.register(self.check_thread)

    def load(self, model: str) -> bool:
        if not model:
            return False

        model_path = Path(model)

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.print("Model not found.")
            return False

        if model == self.loaded_model:
            widgets.print("Model already loaded.")
            return False

        self.check_thread()
        now = timeutils.now()
        widgets.print("Loading model...")
        widgets.update()

        try:
            self.model = Llama(
                model_path=str(model_path),
                verbose=False,
            )
        except BaseException as e:
            widgets.print("Model failed to load.")
            return False

        self.loaded_model = model
        msg, now = timeutils.check_time("Model loaded.", now)
        widgets.print(msg)
        return True

    def check_thread(self) -> None:
        if self.thread and self.thread.is_alive():
            self.stop_thread.set()
            self.thread.join()
            self.stop_thread.clear()
            widgets.print("* Interrupted *")

    def stream(self, prompt: str) -> None:
        if not self.loaded_model:
            if not self.load(config.model):
                return

        self.check_thread()
        self.thread = threading.Thread(target=self.do_stream, args=(prompt,))
        self.thread.start()

    def do_stream(self, prompt: str) -> None:
        self.lock.acquire()
        widgets.show_model()
        prompt = prompt.strip()

        if not prompt:
            return

        widgets.prompt(1)
        widgets.insert(prompt)

        messages = [
            {"role": "system", "content": config.system},
            {
                "role": "user",
                "content": prompt,
            },
        ]

        added_name = False
        token_printed = False
        last_token = " "

        output = self.model.create_chat_completion(
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            stream=True,
            top_k=config.top_k,
            top_p=config.top_p,
        )

        for chunk in output:
            if self.stop_thread.is_set():
                break

            delta = chunk["choices"][0]["delta"]

            if "content" in delta:
                if not added_name:
                    widgets.prompt(2)
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

                widgets.insert(token)

        self.lock.release()


model = Model()
