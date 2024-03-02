# Modules
from config import config
import timeutils
import action

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import threading
from pathlib import Path


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.stream_date = 0.0

    def load(self) -> bool:
        if not config.model:
            return False

        model_path = Path(config.model)

        if (not model_path.exists()) or (not model_path.is_file()):
            return False

        now = timeutils.now()

        self.model = Llama(
            model_path=str(model_path),
            verbose=False,
        )

        msg, now = timeutils.check_time("Model loaded", now)
        action.output(msg)
        config.model_loaded = True
        return True

    def stream(self, prompt: str) -> None:
        threading.Thread(target=self.do_stream, args=(prompt,)).start()

    def do_stream(self, prompt: str) -> None:
        if not config.model_loaded:
            action.output("Model is not loaded")
            return

        prompt = prompt.strip()

        if not prompt:
            return

        action.prompt(1)
        action.output(prompt)

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
        date = timeutils.now()
        self.stream_date = date

        output = self.model.create_chat_completion(  # type: ignore
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            stream=True,
        )

        for chunk in output:
            if date != self.stream_date:
                break

            delta = chunk["choices"][0]["delta"]

            if "content" in delta:
                if not added_name:
                    action.prompt(2)
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

                action.output(token, False)


model = Model()
