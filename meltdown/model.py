# Standard
import threading
from pathlib import Path
from typing import Optional
from tkinter import filedialog
from typing import List, Tuple

# Libraries
from llama_cpp import Llama  # type: ignore
from openai import OpenAI  # type: ignore

# Modules
from .app import app
from .args import args
from .config import config
from .widgets import widgets
from .display import display
from .session import session
from .files import files
from .tips import tips
from .utils import utils
from . import timeutils
from . import emojis


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
            msg = "Model unloaded"
            display.print(emojis.text(msg, "unloaded"))

        self.clear_model()

    def model_is_gpt(self, name: str) -> bool:
        return any(name == gpt[0] for gpt in self.gpts)

    def load(self, prompt: str = "", tab_id: str = "") -> None:
        if not config.model:
            display.print(
                "You must configure a model first."
                " It can be a local model which you can download"
                " from the HuggingFace website (or elsewhere), or a remote ChatGPT model by"
                " using your API key. Check the main menu on the top right.",
                tab_id=tab_id,
            )
            return

        if self.loaded_model == config.model:
            if self.loaded_format == config.format:
                return

        if self.is_loading():
            utils.error("(Load) Slow down!")
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
        self.load_thread = threading.Thread(target=lambda: wrapper())
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
        except BaseException as e:
            utils.error(e)
            self.gpt_key = ""

    def load_gpt(self, prompt: str, tab_id: str) -> None:
        try:
            self.read_gpt_key()

            if not self.gpt_key:
                display.print(
                    "Error: OpenAI API key not found." " Use the main menu to set it."
                )
                self.clear_model()
                return

            self.gpt_client = OpenAI(api_key=self.gpt_key)

            self.model = config.model
            self.model_loading = False
            self.loaded_model = config.model
            self.loaded_format = "gpt_remote"
            files.add_model(config.model)
            msg = f"{config.model} is ready to use"
            display.print(emojis.text(msg, "remote"))
            self.update_icon()

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException as e:
            utils.error(e)
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

            if args.model_feedback and (not args.quiet):
                msg = f"Loading {name}"
                display.print(emojis.text(msg, "local"), tab_id=tab_id)

            app.update()

            self.model = Llama(
                model_path=str(model),
                n_ctx=config.context,
                n_threads=config.threads,
                n_gpu_layers=config.gpu_layers,
                use_mlock=mlock,
                chat_format=fmt,
                verbose=args.verbose,
            )
        except BaseException as e:
            utils.error(e)
            display.print("Error: Model failed to load.")
            self.clear_model()
            self.lock.release()
            return

        files.add_model(model)
        self.model_loading = False
        self.loaded_model = model
        self.loaded_format = chat_format
        self.update_icon()

        if args.model_feedback and (not args.quiet):
            msg, now = timeutils.check_time("Model loaded", now)
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

            if args.model_feedback and (not args.quiet):
                display.print("< Interrupted >")

    def stream(self, prompt: str, tab_id: str) -> None:
        if self.is_loading():
            utils.error("(Stream) Slow down!")
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
        self.stream_thread = threading.Thread(target=lambda: wrapper(prompt, tab_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def do_stream(self, prompt: str, tab_id: str) -> None:
        self.lock.acquire()
        self.stream_loading = True

        widgets.show_model()
        prompt = prompt.strip()

        if not self.model:
            utils.error("Model not loaded")
            return

        if not prompt:
            utils.error("Empty prompt")
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
            for item in conversation.items[-abs(config.history) :]:
                for key in item:
                    content = item[key]

                    if key == "user":
                        content = self.replace_content(content)

                    messages.append({"role": key, "content": content})

        if args.debug:
            utils.msg("-----")
            utils.msg(f"prompt: {prompt}")
            utils.msg(f"messages: {len(messages)}")
            utils.msg(f"history: {config.history}")
            utils.msg(f"max_tokens: {config.max_tokens}")
            utils.msg(f"temperature: {config.temperature}")
            utils.msg(f"top_k: {config.top_k}")
            utils.msg(f"top_p: {config.top_p}")
            utils.msg(f"seed: {config.seed}")

        content = prompt
        content = self.replace_content(content)
        messages.append({"role": "user", "content": content})

        files.add_system(config.system)
        files.add_prepends(config.prepend)
        files.add_appends(config.append)

        now = timeutils.now()
        self.stream_date = now
        stream = args.stream
        display.stream_started(tab_id)
        stop_list = config.stop.split(";;") if config.stop else None

        if stop_list:
            stop_list = [item.strip() for item in stop_list]

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
                    stop=stop_list,
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
                    stop=stop_list,
                )
            except BaseException as e:
                utils.error(e)
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

        added_name = False
        token_printed = False
        last_token = " "
        tokens: List[str] = []
        buffer: List[str] = []
        buffer_date = 0.0
        broken = False

        def print_buffer(force: bool = False) -> None:
            nonlocal buffer_date

            if not len(buffer):
                return

            datenow = timeutils.now()

            if not force:
                if (datenow - buffer_date) < args.delay:
                    return

            buffer_date = datenow
            display.insert("".join(buffer), tab_id=tab_id)
            buffer.clear()

        if stream:
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
                            print_buffer()
            except BaseException as e:
                utils.error(e)
        else:
            try:
                response = output.choices[0].message.content.strip()

                if response:
                    display.prompt("ai", tab_id=tab_id)
                    display.insert(response, tab_id=tab_id)
            except BaseException as e:
                utils.error(e)

        if not broken:
            print_buffer(True)

        if tokens:
            log_dict["assistant"] = "".join(tokens).strip()
            conversation.add(log_dict)

        self.lock.release()

    def set_model(self, m: str) -> None:
        from .widgets import widgets

        widgets.model.set_text(m)
        config.update("model")

    def browse_models(self) -> None:
        if self.model_loading:
            return

        file = filedialog.askopenfilename(initialdir=self.get_dir())

        if file:
            self.set_model(file)

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
            if args.emojis:
                text = emojis.get("unloaded")
            else:
                text = "Not Loaded"

            icon.configure(text=text)
            tooltip.set_text(tips["model_unloaded"])
        elif self.model_is_gpt(self.loaded_model):
            if args.emojis:
                text = emojis.get("remote")
            else:
                text = "Remote"

            icon.configure(text=text)
            tooltip.set_text(tips["model_remote"])
        else:
            if args.emojis:
                text = emojis.get("local")
            else:
                text = "Local"

            icon.configure(text=text)
            tooltip.set_text(tips["model_local"])

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
            content = content.replace(f"{args.keychar}name_user", config.name_user)

        if config.name_ai:
            content = content.replace(f"{args.keychar}name_ai", config.name_ai)

        content = content.replace(f"{args.keychar}date", timeutils.today())
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
        models = [config.model] + files.get_list("models")

        for model in models:
            path = Path(model)

            if path.exists() and path.is_file():
                return str(path.parent)

        return None

    def check_config(self, save: bool = True) -> None:
        models = files.get_list("models")

        if (not config.model) and models:
            config.model = models[0]

            if save:
                config.save()


model = Model()
