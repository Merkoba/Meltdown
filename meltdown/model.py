from __future__ import annotations

# Standard
import base64
import threading
from pathlib import Path
from typing import Any, Generator

# Libraries
import requests  # type: ignore
from llama_cpp import Llama, ChatCompletionChunk  # type: ignore
from llama_cpp.llama_chat_format import Llava15ChatHandler  # type: ignore
from openai import OpenAI  # type: ignore
from openai.types.chat.chat_completion import ChatCompletion  # type: ignore

# Modules
from .app import app
from .args import args
from .config import config
from .display import display
from .tips import tips
from .utils import utils
from .files import files


PromptArg = dict[str, Any]


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_stream_thread = threading.Event()
        self.stream_thread = threading.Thread()
        self.streaming = False
        self.stream_loading = False
        self.model: Llama | None = None
        self.model_loading = False
        self.loaded_model = ""
        self.loaded_format = ""
        self.load_thread = threading.Thread()
        self.stream_date = 0.0
        self.gpt_client = None
        self.last_response = ""

        self.gpts: list[tuple[str, str]] = [
            ("gpt-3.5-turbo", "GPT 3.5 Turbo"),
            ("gpt-4o", "GPT 4o"),
        ]

        self.gpt_key = ""

    def setup(self) -> None:
        self.update_icon()
        self.start_auto_unload()

    def unload(self, announce: bool = False) -> None:
        if self.model_loading:
            return

        self.stop_stream()

        if self.loaded_model and announce:
            msg = "Model unloaded"
            display.print(utils.emoji_text(msg, "unloaded"))

        self.clear_model()

    def model_is_gpt(self, name: str) -> bool:
        return any(name == gpt[0] for gpt in self.gpts)

    def load(self, prompt: PromptArg | None = None, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        if not config.model:
            display.print(
                "You must configure a model first."
                " It can be a local model which you can download"
                " from the HuggingFace website (or elsewhere), or a remote ChatGPT model by"
                " using your API key. Check the model menu on the top right.",
                tab_id=tab_id,
            )

            return

        if self.loaded_model == config.model:
            if self.loaded_format == config.format:
                return

        if self.is_loading():
            utils.msg("(Load) Slow down!")
            return

        if self.model_is_gpt(config.model):
            self.unload()
            self.load_gpt(tab_id, prompt)
            return

        model_path = Path(config.model)

        if (not model_path.exists()) or (not model_path.is_file()):
            display.print("Error: Model not found. Check the path.", tab_id=tab_id)
            return

        def wrapper() -> None:
            if not self.load_local(config.model, tab_id):
                return

            if prompt:
                self.stream(prompt, tab_id)

        self.unload()
        self.load_thread = threading.Thread(target=lambda: wrapper())
        self.load_thread.daemon = True
        self.load_thread.start()

    def clear_model(self) -> None:
        self.model = None
        self.loaded_model = ""
        self.model_loading = False
        self.loaded_format = ""
        self.stream_date = 0.0
        self.update_icon()

    def read_gpt_key(self) -> None:
        from .paths import paths

        try:
            self.gpt_key = files.read(paths.apikey)
        except BaseException as e:
            utils.error(e)
            self.gpt_key = ""

    def load_gpt(self, tab_id: str, prompt: PromptArg | None = None) -> None:
        try:
            self.read_gpt_key()

            if not self.gpt_key:
                display.print(
                    "Error: OpenAI API key not found. Use the model menu to set it."
                )

                self.clear_model()
                return

            self.gpt_client = OpenAI(api_key=self.gpt_key)
            self.model_loading = False
            self.loaded_model = config.model
            self.loaded_format = "gpt_remote"
            msg = f"{config.model} is ready to use"
            display.print(utils.emoji_text(msg, "remote"))
            self.update_icon()

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException as e:
            utils.error(e)
            display.print("Error: GPT model failed to load.")
            self.clear_model()

    def load_local(self, model: str, tab_id: str) -> bool:
        from .app import app

        self.model_loading = True
        now = utils.now()
        chat_format = config.format

        try:
            chat_handler = None

            if config.logits == "all":
                logits_all = True
            else:
                logits_all = False

            if config.mode == "image":
                mmproj = Path(Path(model).parent / "mmproj.gguf")

                if not mmproj.exists():
                    display.print(
                        "Error: mmproj.gguf not found."
                        " It must be in the same directory as the model.",
                    )

                    self.model_loading = False
                    return False

                chat_handler = Llava15ChatHandler(clip_model_path=str(mmproj))

            fmt = config.format if (chat_format != "auto") else None
            name = Path(model).name
            mlock = config.mlock == "yes"
            display.to_bottom(tab_id)

            if args.model_feedback and (not args.quiet):
                msg = f"Loading {name}"
                display.print(utils.emoji_text(msg, "loading"), tab_id=tab_id)

            app.update()
            self.lock.acquire()

            self.model = Llama(
                model_path=model,
                n_ctx=config.context,
                n_threads=config.threads,
                n_gpu_layers=config.gpu_layers,
                use_mlock=mlock,
                chat_format=fmt,
                chat_handler=chat_handler,
                logits_all=logits_all,
                verbose=args.verbose,
            )
        except BaseException as e:
            utils.error(e)
            display.print("Error: Model failed to load.")
            self.clear_model()
            self.release_lock()
            return False

        self.model_loading = False
        self.loaded_model = model
        self.loaded_format = chat_format
        self.update_icon()

        if args.model_feedback and (not args.quiet):
            text = utils.emoji_text("Model loaded", "local")
            msg, now = utils.check_time(text, now)
            display.print(msg)

        self.release_lock()
        return True

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stop_stream_thread.is_set():
            return

        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=3)

            if args.model_feedback and (not args.quiet):
                display.print("< Interrupted >")

    def stream(self, prompt: PromptArg, tab_id: str | None = None) -> None:
        if self.is_loading():
            utils.msg("(Stream) Slow down!")
            return

        if not tab_id:
            tab_id = display.current_tab

        tab = display.get_tab(tab_id)

        if not tab:
            return

        if tab.mode == "ignore":
            return

        if not self.loaded_model:
            self.load(prompt, tab_id)
            return

        def wrapper(prompt: dict[str, str], tab_id: str) -> None:
            self.stop_stream_thread.clear()
            self.streaming = True
            self.do_stream(prompt, tab_id)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=lambda: wrapper(prompt, tab_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def prepare_stream(
        self, prompt: dict[str, str], tab_id: str
    ) -> tuple[list[dict[str, str]], dict[str, str]] | None:
        prompt_text = prompt.get("text", "").strip()
        prompt_file = prompt.get("file", "").strip()
        prompt_user = prompt.get("user", "").strip()
        no_history = prompt.get("no_history", False)

        if prompt_file:
            if not utils.is_url(prompt_file) and (not Path(prompt_file).exists()):
                display.print("Error: File not found.")
                return None

        prompt_text = self.limit_tokens(prompt_text)
        original_text = prompt_text
        original_file = prompt_file

        if (not prompt_text) and (not prompt_file):
            return None

        if not self.loaded_model:
            utils.msg("Model not loaded")
            return None

        if config.before:
            prompt_text = self.check_dot(config.before) + prompt_text

        if config.after:
            prompt_text = self.check_dot(prompt_text) + config.after

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return None

        if tabconvo.tab.mode == "ignore":
            return None

        log_dict: dict[str, Any] = {}
        log_dict["date"] = utils.now()
        log_dict["user"] = prompt_user if prompt_user else prompt_text
        log_dict["file"] = original_file

        messages: list[dict[str, Any]] = []

        if config.system:
            system = utils.replace_keywords(config.system)
            messages.append({"role": "system", "content": system})

        if tabconvo.convo.items and (config.history > 0) and (not no_history):
            for item in tabconvo.convo.items[-abs(config.history) :]:
                for key in ["user", "ai"]:
                    content = getattr(item, key)

                    if key == "user":
                        content = utils.replace_keywords(content)
                        role = "user"
                    elif key == "ai":
                        role = "assistant"
                    else:
                        continue

                    messages.append({"role": role, "content": content})

        prompt_text = utils.replace_keywords(prompt_text)

        if (not prompt_text) and (not prompt_file):
            return None

        file_text = ""

        if prompt_file and (config.mode == "text"):
            file_text = self.read_file(prompt_file)
            file_text = self.limit_tokens(file_text)

            if file_text:
                messages.append({"role": "user", "content": file_text})

        if prompt_file and (config.mode == "image"):
            content_items = []

            if not utils.is_url(prompt_file):
                converted = self.image_to_base64(prompt_file)

                if not converted:
                    return None

                prompt_file = converted

            content_items.append(
                {"type": "image_url", "image_url": {"url": prompt_file}}
            )

            content_items.append({"type": "text", "text": prompt_text})
            messages.append({"role": "user", "content": content_items})
        else:
            messages.append({"role": "user", "content": prompt_text})

        o_text = prompt_user if prompt_user else original_text

        if not prompt_user:
            prompt_user = prompt_text

        display.prompt(
            "user", text=prompt_user, tab_id=tab_id, original=o_text, file=original_file
        )

        display.stream_started(tab_id)
        return messages, log_dict

    def do_stream(self, prompt: dict[str, str], tab_id: str) -> None:
        prepared = self.prepare_stream(prompt, tab_id)

        if not prepared:
            return

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        now = utils.now()
        self.stream_date = now
        messages, log_dict = prepared
        self.stream_loading = True
        self.lock.acquire()

        if self.model_is_gpt(config.model):
            try:
                if not self.gpt_client:
                    self.stream_loading = False
                    self.release_lock()
                    return

                output = self.gpt_client.chat.completions.create(
                    messages=messages,
                    stream=args.stream,
                    model=config.model,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    top_p=config.top_p,
                    seed=config.seed,
                    stop=self.get_stop_list(),
                )
            except BaseException as e:
                utils.error(e)

                display.print(
                    "Error: GPT model failed to stream."
                    " You might not have access to this particular model,"
                    " not enough credits, invalid API key,"
                    " or there is no internet connection."
                )

                self.stream_loading = False
                self.release_lock()
                return
        else:
            if not self.model:
                self.stream_loading = False
                self.release_lock()
                return

            try:
                output = self.model.create_chat_completion_openai_v1(
                    messages=messages,
                    stream=args.stream,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    top_k=config.top_k,
                    top_p=config.top_p,
                    seed=config.seed,
                    stop=self.get_stop_list(),
                )
            except BaseException as e:
                utils.error(e)
                self.stream_loading = False
                self.release_lock()
                return

        self.stream_loading = False

        if self.stream_date != now:
            self.release_lock()
            return

        if self.stop_stream_thread.is_set():
            self.release_lock()
            return

        if args.stream:
            ans = self.process_stream(output, tab_id)
        else:
            ans = self.process_instant(output, tab_id)

        res = ans.strip()

        if res:
            log_dict["ai"] = res
            self.last_response = res
            tabconvo.convo.add(log_dict)

            if args.show_duration:
                diff = utils.now() - now
                seconds = int(round(diff))
                word = utils.singular_or_plural(seconds, "second", "seconds")
                display.print(f"Duration: {seconds} {word}", tab_id=tab_id)

        self.release_lock()

    def process_stream(
        self,
        output: Generator[ChatCompletionChunk, None, None],
        tab_id: str,
    ) -> str:
        broken = False
        added_name = False
        token_printed = False
        last_token = " "
        buffer_date = 0.0
        tokens: list[str] = []
        buffer: list[str] = []

        def print_buffer() -> None:
            if not len(buffer):
                return

            display.insert("".join(buffer), tab_id=tab_id)
            buffer.clear()

        try:
            for chunk in output:
                if self.stop_stream_thread.is_set():
                    broken = True
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
                        buffer.append(token)
                        now = utils.now()

                        if (now - buffer_date) >= args.delay:
                            print_buffer()
                            buffer_date = now
        except BaseException as e:
            utils.error(e)

        if not broken:
            print_buffer()

        return "".join(tokens)

    def process_instant(self, output: ChatCompletion, tab_id: str) -> str:
        try:
            response = output.choices[0].message.content.strip()

            if response:
                display.prompt("ai", tab_id=tab_id)
                display.insert(response, tab_id=tab_id)
                return str(response)
        except BaseException as e:
            utils.error(e)

        return ""

    def load_or_unload(self) -> None:
        if self.model_loading:
            return

        if self.loaded_model:
            self.unload(True)
        else:
            self.load()

    def update_icon(self) -> None:
        from .widgets import widgets

        if not app.exists():
            return

        icon = widgets.model_icon
        tooltip = widgets.model_icon_tooltip

        if not self.loaded_model:
            if args.emojis:
                text = utils.get_emoji("unloaded")
            else:
                text = "Not Loaded"

            icon.configure(text=text)
            tooltip.set_text(tips["model_unloaded"])
        elif self.model_is_gpt(self.loaded_model):
            if args.emojis:
                text = utils.get_emoji("remote")
            else:
                text = "Remote"

            icon.configure(text=text)
            tooltip.set_text(tips["model_remote"])
        else:
            if args.emojis:
                text = utils.get_emoji("local")
            else:
                text = "Local"

            icon.configure(text=text)
            tooltip.set_text(tips["model_local"])

    def set_api_key(self) -> None:
        from .dialogs import Dialog
        from .paths import paths

        def action(key: str) -> None:
            path = Path(paths.apikey)

            if (not path.exists()) or not (path.is_file()):
                path.parent.mkdir(parents=True, exist_ok=True)
                Path.touch(paths.apikey, exist_ok=True)

            files.write(path, key)

        Dialog.show_input("OpenAI API Key", lambda text: action(text), mode="password")

    def check_dot(self, text: str) -> str:
        if not text:
            return ""

        chars = [".", ",", ";", "!", "?"]

        if text[-1] in chars:
            return text + " "

        return text + ". "

    def image_to_base64(self, path_str: str) -> str | None:
        path = Path(path_str)

        try:
            with path.open("rb") as img_file:
                base64_data = base64.b64encode(img_file.read()).decode("utf-8")
                return f"data:image/png;base64,{base64_data}"
        except BaseException as e:
            utils.error(e)
            return None

    def release_lock(self) -> None:
        if self.lock.locked():
            self.lock.release()

    def read_file(self, path: str) -> str:
        text = ""

        if utils.is_url(path):
            try:
                response = requests.get(path, timeout=5)

                if response.status_code == 200:
                    text = str(response.text)
            except BaseException as e:
                utils.error(e)
        else:
            try:
                text = files.read(Path(path))
            except BaseException as e:
                utils.error(e)

        return text

    def limit_tokens(self, text: str) -> str:
        if not args.limit_tokens:
            return text

        if not self.model:
            return text

        try:
            max_tokens = int(config.max_tokens * config.token_limit)
            encoded = text.encode("utf-8")
            tokens = self.model.tokenize(encoded)
            bytes = self.model.detokenize(tokens[:max_tokens])
            return str(bytes.decode("utf-8")).strip()
        except BaseException as e:
            utils.error(e)
            return text

    def show_name(self) -> None:
        from .widgets import widgets
        from .dialogs import Dialog

        model_ = self.loaded_model

        if not model_:
            model_ = widgets.model.get()

        if not model_:
            return

        Dialog.show_message(model_)

    def get_stop_list(self) -> list[str] | None:
        stop_list = config.stop.split(";;") if config.stop else None

        if stop_list:
            stop_list = [item.strip() for item in stop_list]

        return stop_list

    def start_auto_unload(self) -> None:
        if args.auto_unload < 1:
            return

        m = utils.singular_or_plural(args.auto_unload, "minute", "minutes")
        utils.msg(f"Auto-unload set to {args.auto_unload} {m}")
        thread = threading.Thread(target=lambda: self.auto_unload_loop())
        thread.daemon = True
        thread.start()

    def auto_unload_loop(self) -> None:
        utils.sleep(10)

        while True:
            if self.loaded_model and (self.stream_date > 0):
                seconds = utils.now() - self.stream_date
                minutes = seconds / 60

                if minutes >= args.auto_unload:
                    self.unload()

            utils.sleep(10)


model = Model()
