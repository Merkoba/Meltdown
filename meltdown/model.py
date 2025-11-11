from __future__ import annotations

# Standard
import os
import json
import base64
import threading
from pathlib import Path
from typing import Any

# Libraries
import requests  # type: ignore
import litellm  # type: ignore
from litellm import completion
from litellm import image_generation
from litellm.types.utils import ModelResponse  # type: ignore
from litellm.litellm_core_utils.streaming_handler import CustomStreamWrapper  # type: ignore

# Modules
from .app import app
from .args import args
from .config import config
from .display import display
from .tips import tips
from .utils import utils
from .search import search
from .files import files
from .session import Item
from .variables import variables

litellm.drop_params = True

# Try Import
llama_cpp = utils.try_import("llama_cpp")

if llama_cpp:
    LlamaCPP = llama_cpp.Llama
    Llava15ChatHandler = llama_cpp.llama_chat_format.Llava15ChatHandler
else:
    LlamaCPP = None
    Llava15ChatHandler = None


PromptArg = dict[str, Any]
ToolCallsBuffer = dict[str, dict[str, Any]]


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_stream_thread = threading.Event()
        self.stream_thread = threading.Thread()
        self.streaming = False
        self.stream_loading = False
        self.model: LlamaCPP | None = None  # type: ignore
        self.model_loading = False
        self.loaded_model = ""
        self.loaded_format = ""
        self.loaded_provider = ""
        self.loaded_type = ""
        self.load_thread = threading.Thread()
        self.stream_date = 0.0
        self.last_response = ""
        self.icon_text = ""
        self.stream_timeout = 20
        self.tools_timeout = 20
        self.read_file_timeout = 10
        self.stop_stream_timeout = 5

        kerr = "Use the model menu to set it."
        self.openai_key_error = f"Error: OpenAI API key not found. {kerr}"
        self.google_key_error = f"Error: Google API key not found. {kerr}"
        self.anthropic_key_error = f"Error: Anthropic API key not found. {kerr}"

        self.gpts: list[tuple[str, str]] = [
            ("gpt-4o", "GPT 4o"),
            ("gpt-4o-mini", "GPT 4o Mini"),
            ("gpt-3.5-turbo", "GPT 3.5 Turbo"),
        ]

        self.geminis: list[tuple[str, str]] = [
            ("gemini-2.5-pro", "Gemini 2.5 Pro"),
            ("gemini-2.5-flash", "Gemini 2.5 Flash"),
        ]

        self.claudes: list[tuple[str, str]] = [
            ("claude-opus-4", "Claude 4 Opus"),
            ("claude-4-sonnet", "Claude 4 Sonnet"),
            ("claude-3-7-sonnet", "Claude 3.7 Sonnet"),
        ]

        self.openai_key = ""
        self.google_key = ""
        self.anthropic_key = ""

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the internet for current information, recent events, news, facts, or any information that might not be in the training data. This tool searches multiple sources including DuckDuckGo, Wikipedia, and Google to find accurate, up-to-date information. Use this when the user asks about: recent events, current information, specific facts that need verification, geographical information (like capitals of countries), current statistics, news, or anything happening after the model's training cutoff date. The tool returns structured search results with titles, URLs, and content snippets that provide comprehensive and factual information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to use. Should be specific and keyword-focused for best results. For factual questions like 'capital of Zimbabwe', use clear, direct queries. Include relevant keywords that would help find the information the user is looking for.",
                            }
                        },
                        "required": ["query"],
                    },
                },
            }
        ]

        # Map tool names to actual callable functions
        self.toolfuncs = {
            "web_search": self.web_search,
        }

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
        return name.startswith("gpt-")

    def model_is_gemini(self, name: str) -> bool:
        return name.startswith("gemini-")

    def model_is_claude(self, name: str) -> bool:
        return name.startswith("claude-")

    def load(self, prompt: PromptArg | None = None, tab_id: str | None = None) -> None:
        if not tab_id:
            tab_id = display.current_tab

        if not self.get_model():
            display.print(
                "You must configure a model first."
                " It can be a local model which you can download"
                " from the HuggingFace website (or elsewhere), or a remote ChatGPT model by"
                " using your API key. Check the model menu on the top right.",
                tab_id=tab_id,
            )

            return

        if self.loaded_model == self.get_model():
            if self.loaded_format == config.format:
                return

        if self.is_loading():
            utils.msg("(Load) Slow down!")
            return

        if self.model_is_gpt(self.get_model()):
            self.unload()
            self.load_openai(tab_id, prompt)
            return

        if self.model_is_gemini(self.get_model()):
            self.unload()
            self.load_google(tab_id, prompt)
            return

        if self.model_is_claude(self.get_model()):
            self.unload()
            self.load_anthropic(tab_id, prompt)
            return

        model_path = Path(self.get_model())

        if (not model_path.exists()) or (not model_path.is_file()):
            display.print("Error: Model not found. Check the path.", tab_id=tab_id)
            return

        def wrapper() -> None:
            if not self.load_local(self.get_model(), tab_id):
                return

            if prompt:
                self.stream(prompt, tab_id)

        self.unload()
        self.stream_date = utils.now()
        self.load_thread = threading.Thread(target=lambda: wrapper())
        self.load_thread.daemon = True
        self.load_thread.start()

    def clear_model(self) -> None:
        self.model = None
        self.loaded_model = ""
        self.loaded_type = ""
        self.model_loading = False
        self.loaded_format = ""
        self.loaded_provider = ""
        self.stream_date = 0.0
        self.update_icon()

    def read_openai_key(self) -> None:
        from .paths import paths

        try:
            self.openai_key = files.read(paths.openai_key)
        except BaseException:
            self.openai_key = ""

    def read_google_key(self) -> None:
        from .paths import paths

        try:
            self.google_key = files.read(paths.google_key)
        except BaseException:
            self.google_key = ""

    def read_anthropic_key(self) -> None:
        from .paths import paths

        try:
            self.anthropic_key = files.read(paths.anthropic_key)
        except BaseException:
            self.anthropic_key = ""

    def load_openai(
        self, tab_id: str, prompt: PromptArg | None = None, quiet: bool = False
    ) -> bool:
        self.read_openai_key()

        if not self.openai_key:
            display.print(self.openai_key_error)
            self.clear_model()
            return False

        try:
            now = utils.now()
            os.environ["OPENAI_API_KEY"] = self.openai_key
            self.model_loading = False
            self.loaded_model = self.get_model()
            self.loaded_format = "openai"
            self.loaded_provider = "openai"
            self.loaded_type = "remote"
            self.after_load(now, quiet=quiet)

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException as e:
            utils.error(e)
            display.print("Error: OpenAI failed to load.")
            self.clear_model()

        return True

    def load_google(
        self, tab_id: str, prompt: PromptArg | None = None, quiet: bool = False
    ) -> bool:
        self.read_google_key()

        if not self.google_key:
            display.print(self.google_key_error)
            self.clear_model()
            return False

        try:
            now = utils.now()
            os.environ["GOOGLE_API_KEY"] = self.google_key
            self.model_loading = False
            self.loaded_model = self.get_model()
            self.loaded_format = "google"
            self.loaded_provider = "gemini"
            self.loaded_type = "remote"
            self.after_load(now, quiet=quiet)

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException as e:
            utils.error(e)
            display.print("Error: Google failed to load.")
            self.clear_model()

        return True

    def load_anthropic(
        self, tab_id: str, prompt: PromptArg | None = None, quiet: bool = False
    ) -> bool:
        self.read_anthropic_key()

        if not self.anthropic_key:
            display.print(self.anthropic_key_error)
            self.clear_model()
            return False

        try:
            now = utils.now()
            os.environ["ANTHROPIC_API_KEY"] = self.anthropic_key
            self.model_loading = False
            self.loaded_model = self.get_model()
            self.loaded_format = "anthropic"
            self.loaded_provider = "anthropic"
            self.loaded_type = "remote"
            self.after_load(now, quiet=quiet)

            if prompt:
                self.stream(prompt, tab_id)
        except BaseException as e:
            utils.error(e)
            display.print("Error: Anthropic failed to load.")
            self.clear_model()

        return True

    def load_local(self, model: str, tab_id: str, quiet: bool = False) -> bool:
        from .app import app

        if not llama_cpp:
            self.no_llama_error()
            return False

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

                if Llava15ChatHandler:
                    chat_handler = Llava15ChatHandler(clip_model_path=str(mmproj))
                else:
                    self.model_loading = False
                    return False

            if not LlamaCPP:
                self.model_loading = False
                return False

            fmt = config.format if (chat_format != "auto") else None
            name = Path(model).name
            mlock = config.mlock == "yes"
            display.to_bottom(tab_id)

            if args.model_feedback and (not args.quiet):
                msg = f"Loading {name}"
                display.print(utils.emoji_text(msg, "loading"), tab_id=tab_id)

            app.update()
            self.lock.acquire()

            self.model = LlamaCPP(
                model_path=model,
                n_ctx=config.context,
                n_batch=config.batch_size,
                n_ubatch=config.ubatch_size,
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
        self.loaded_provider = "local"
        self.loaded_type = "local"
        self.after_load(now, quiet=quiet)
        self.release_lock()
        return True

    def after_load(self, start_date: float, quiet: bool = False) -> None:
        from .system import system

        self.update_icon()

        if args.model_feedback and (not args.quiet) and (not quiet):
            if self.loaded_type == "local":
                text = utils.emoji_text("Model loaded", "local")
                msg, _ = utils.check_time(text, start_date)
                display.print(msg)
            elif self.loaded_type == "remote":
                msg = f"{self.get_model()} is ready to use"
                display.print(utils.emoji_text(msg, "remote"))

        if args.system_auto_hide:
            system.check_auto_hide()

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stop_stream_thread.is_set():
            return

        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=self.stop_stream_timeout)

            if args.model_feedback and (not args.quiet):
                display.print("< Interrupted >")

    def stream(self, prompt: PromptArg, tab_id: str | None = None) -> None:
        if self.is_loading():
            utils.msg("(Stream) Slow down!")
            return

        if not tab_id:
            tab_id = display.current_tab

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if tabconvo.tab.mode == "ignore":
            return

        num_items = len(tabconvo.convo.items)

        if num_items >= args.max_items:
            display.print(
                "Limit: Max items reached. Make a new tab or clear the conversation.",
                tab_id=tab_id,
            )

            return

        if not self.loaded_model:
            self.load(prompt, tab_id)
            return

        def wrapper(prompt: PromptArg, tab_id: str) -> None:
            self.stop_stream_thread.clear()
            self.streaming = True
            app.do_checks()
            self.do_stream(prompt, tab_id)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=lambda: wrapper(prompt, tab_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def prepare_stream(
        self,
        prompt: PromptArg,
        tab_id: str,
    ) -> tuple[list[dict[str, str]], Item] | None:
        prompt_text = prompt.get("text", "").strip()
        prompt_file = prompt.get("file", "").strip()
        prompt_user = prompt.get("user", "").strip()
        no_history = prompt.get("no_history", False)
        internal = prompt.get("internal", None)

        if prompt_file:
            prompt_file = files.clean_path(prompt_file)

            if (not utils.is_url(prompt_file)) and (not Path(prompt_file).exists()):
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
        log_dict["model"] = utils.last_slash(self.loaded_model)
        log_dict["seed"] = config.seed
        log_dict["history"] = config.history
        log_dict["max_tokens"] = config.max_tokens
        log_dict["temperature"] = config.temperature
        log_dict["top_k"] = config.top_k
        log_dict["top_p"] = config.top_p
        log_dict["format"] = config.format
        log_dict["internal"] = internal

        # Temporary
        log_dict["ai"] = "Empty"
        log_dict["duration"] = 0

        messages: list[dict[str, Any]] = []

        if config.system:
            system = utils.replace_keywords(config.system)
            messages.append({"role": "system", "content": system})

        if tabconvo.convo.items and config.history and (not no_history):
            for item in tabconvo.convo.items[-abs(config.history) :]:
                user_value = getattr(item, "user", "")
                ai_value = getattr(item, "ai", "")

                if (not user_value) or (not ai_value):
                    continue

                if self.long_url(user_value) or self.long_url(ai_value):
                    continue

                for key in ["user", "ai"]:
                    if key == "user":
                        content = user_value
                    elif key == "ai":
                        content = ai_value
                    else:
                        continue

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
            ptext = prompt_text

            if internal:
                ptext = f"{internal}\n{ptext}"

            messages.append({"role": "user", "content": ptext})

        o_text = prompt_user if prompt_user else original_text

        if not prompt_user:
            prompt_user = prompt_text

        display.prompt(
            "user",
            text=prompt_user,
            tab_id=tab_id,
            original=o_text,
            file=original_file,
        )

        display.prompt("ai", text=args.thinking_text, tab_id=tab_id)
        convo_item = tabconvo.convo.add(log_dict)
        display.stream_started(tab_id)
        return messages, convo_item

    def do_stream(self, prompt: PromptArg, tab_id: str) -> None:
        prepared = self.prepare_stream(prompt, tab_id)

        if not prepared:
            return

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        now = utils.now()
        self.stream_date = now
        messages, convo_item = prepared
        self.stream_loading = True
        self.lock.acquire()
        gen_config = self.get_gen_config(messages)
        output: ModelResponse | CustomStreamWrapper | Any | None = None

        if self.is_remote_model():
            try:
                output = completion(**gen_config, timeout=self.stream_timeout)
            except BaseException as e:
                utils.error(e)

                display.print(
                    "Error: Remote model failed to stream."
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
                output = self.model.create_chat_completion_openai_v1(**gen_config)
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

        if not output:
            self.release_lock()
            return

        try:
            if config.stream == "yes":
                ans = self.process_stream(output, tab_id)
            else:
                ans = self.process_instant(output, tab_id)
        except BaseException as e:
            utils.error(e)
            self.release_lock()
            return

        res = ans.strip()
        now_2 = utils.now()

        if res:
            duration = now_2 - now
            convo_item.ai = res
            convo_item.duration = duration
            tabconvo.convo.update()
            self.last_response = res

            if args.durations:
                word = utils.singular_or_plural(duration, "second", "seconds")
                display.print(f"Duration: {duration:.2f} {word}", tab_id=tab_id)

        self.stream_date = now_2
        self.release_lock()

    def process_stream(
        self,
        output: ModelResponse | CustomStreamWrapper,
        tab_id: str,
    ) -> str:
        broken = False
        first_content = False
        token_printed = False
        last_token = " "
        buffer_date = 0.0
        tokens: list[str] = []
        buffer: list[str] = []
        tool_calls_buffer: ToolCallsBuffer = {}
        has_tool_calls = False

        def print_buffer() -> None:
            if not len(buffer):
                return

            display.insert("".join(buffer), tab_id=tab_id)
            buffer.clear()

        def is_whitespace_only(token: str) -> bool:
            return (token != "\n") and (not token.strip())

        def add_token(new_token: str) -> None:
            if (new_token == "\n") and (len(tokens) >= 2):
                if (tokens[-2] == "\n") and is_whitespace_only(tokens[-1]):
                    tokens.pop()

            if (new_token == "\n") and (len(tokens) >= 2):
                if (tokens[-1] == "\n") and (tokens[-2] == "\n"):
                    return

            tokens.append(new_token)

        try:
            for chunk in output:
                if self.stop_stream_thread.is_set():
                    broken = True
                    break

                if not chunk:
                    continue

                token = None
                choices = getattr(chunk, "choices", None)

                if choices:
                    delta = choices[0].delta

                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            index = getattr(tool_call, "index", None)

                            if index is not None:
                                str_index = str(index)
                            else:
                                str_index = "0"

                            has_tool_calls = True

                            if str_index not in tool_calls_buffer:
                                tool_calls_buffer[str_index] = {
                                    "id": "",
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""},
                                }

                            if hasattr(tool_call, "id") and tool_call.id:
                                tool_calls_buffer[str_index]["id"] = tool_call.id

                            if hasattr(tool_call, "function") and tool_call.function:
                                if (
                                    hasattr(tool_call.function, "name")
                                    and tool_call.function.name
                                ):
                                    tool_calls_buffer[str_index]["function"]["name"] = (
                                        tool_call.function.name
                                    )
                                if (
                                    hasattr(tool_call.function, "arguments")
                                    and tool_call.function.arguments
                                ):
                                    tool_calls_buffer[str_index]["function"][
                                        "arguments"
                                    ] += tool_call.function.arguments
                    elif hasattr(delta, "content") and delta.content:
                        token = delta.content
                else:
                    continue

                if token:
                    if not first_content:
                        display.remove_last_ai(tab_id)
                        display.prompt("ai", tab_id=tab_id)
                        first_content = True

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

                    add_token(token)
                    buffer.append(token)
                    now = utils.now()

                    if (now - buffer_date) >= args.delay:
                        print_buffer()
                        buffer_date = now

            if tool_calls_buffer and has_tool_calls:
                if not broken:
                    print_buffer()

                if not first_content:
                    display.remove_last_ai(tab_id)
                    display.prompt("ai", text="Using tools...", tab_id=tab_id)

                tool_response = self.handle_tool_calls(tool_calls_buffer, tab_id)

                if tool_response:
                    if not first_content:
                        display.remove_last_ai(tab_id)
                        display.prompt("ai", tab_id=tab_id)

                    tokens.append(tool_response)
                    display.insert(tool_response, tab_id=tab_id)
        except BaseException as e:
            utils.error(e)

        if not broken:
            print_buffer()

        return "".join(tokens)

    def process_instant(
        self, output: ModelResponse | Any | CustomStreamWrapper, tab_id: str
    ) -> str:
        try:
            choices = getattr(output, "choices", None)

            if not choices or not choices[0]:
                return ""

            message = choices[0].message

            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_messages = []
                assistant_tool_calls = []

                for tool_call in message.tool_calls:
                    fn_name = getattr(tool_call.function, "name", "")
                    fn_args_raw = getattr(tool_call.function, "arguments", None)
                    tool_call_id = getattr(tool_call, "id", "")
                    toolfunc = self.toolfuncs.get(fn_name)
                    exec_args: dict[str, Any] = {}
                    args_str_for_assistant = "{}"

                    try:
                        if isinstance(fn_args_raw, str):
                            fn_args_raw_str = fn_args_raw.strip()

                            exec_args = (
                                json.loads(fn_args_raw_str) if fn_args_raw_str else {}
                            )

                            args_str_for_assistant = fn_args_raw_str or "{}"
                        elif isinstance(fn_args_raw, dict):
                            exec_args = fn_args_raw
                            args_str_for_assistant = json.dumps(fn_args_raw)
                        else:
                            exec_args = {}
                            args_str_for_assistant = "{}"
                    except Exception:
                        exec_args = {}

                        try:
                            args_str_for_assistant = (
                                fn_args_raw
                                if isinstance(fn_args_raw, str)
                                else json.dumps({})
                            )
                        except Exception:
                            args_str_for_assistant = "{}"

                    assistant_tool_calls.append(
                        {
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": fn_name,
                                "arguments": args_str_for_assistant,
                            },
                        }
                    )

                    if not toolfunc:
                        continue

                    try:
                        result = toolfunc(**exec_args)

                        tool_messages.append(
                            {
                                "tool_call_id": tool_call_id,
                                "role": "tool",
                                "name": fn_name,
                                "content": str(result),
                            }
                        )
                    except Exception as e:
                        tool_messages.append(
                            {
                                "tool_call_id": tool_call_id,
                                "role": "tool",
                                "name": fn_name,
                                "content": f"Error executing function: {e}",
                            }
                        )

                if tool_messages:
                    tabconvo = display.get_tab_convo(tab_id)

                    if tabconvo and tabconvo.convo.items:
                        messages: list[dict[str, Any]] = []

                        if config.system:
                            system = utils.replace_keywords(config.system)
                            messages.append({"role": "system", "content": system})

                        last_item = tabconvo.convo.items[-1]
                        user_content = getattr(last_item, "user", "")

                        if user_content:
                            messages.append({"role": "user", "content": user_content})

                        messages.append(
                            {"role": "assistant", "tool_calls": assistant_tool_calls}
                        )

                        messages.extend(tool_messages)

                        original_question = (
                            user_content if user_content else "the user's question"
                        )

                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    f"Based on the web search results provided above, please provide a comprehensive and detailed "
                                    f'answer to this question: "{original_question}"\n\nUse the specific information, facts, '
                                    f"and details from the search results to give an accurate, informative, and up-to-date response. "
                                    f"Include relevant details, dates, numbers, and context from the search results in your answer."
                                ),
                            }
                        )

                        gen_config = self.get_gen_config(messages)

                        if self.is_remote_model():
                            follow_up = completion(
                                **gen_config, timeout=self.tools_timeout
                            )
                        elif self.model:
                            local_gen_config = gen_config.copy()

                            if "model" in local_gen_config:
                                del local_gen_config["model"]

                            follow_up = self.model.create_chat_completion_openai_v1(
                                **local_gen_config
                            )
                        else:
                            return ""

                        choices = getattr(follow_up, "choices", None)

                        if not choices or not choices[0]:
                            return ""

                        if choices and choices[0].message.content:
                            response = choices[0].message.content.strip()
                            display.remove_last_ai(tab_id)
                            display.prompt("ai", tab_id=tab_id)
                            display.insert(response, tab_id=tab_id)
                            return str(response)

                return ""

            response = message.content.strip()
            response = utils.clean_lines(response)

            if response:
                display.remove_last_ai(tab_id)
                display.prompt("ai", tab_id=tab_id)
                display.insert(response, tab_id=tab_id)
                return str(response)
        except BaseException as e:
            utils.error(e)

        return ""

    def generate_image(self, prompt: str | None, tab_id: str | None = None) -> None:
        if not prompt:
            return

        if not prompt.strip():
            return

        if not tab_id:
            tab_id = display.current_tab

        if not self.load_openai(tab_id, quiet=True):
            return

        def wrapper(prompt: str, tab_id: str) -> None:
            self.stop_stream_thread.clear()
            self.streaming = True
            app.do_checks()
            self.do_generate_image(prompt, tab_id)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=lambda: wrapper(prompt, tab_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def do_generate_image(self, prompt: str, tab_id: str) -> None:
        prompt = prompt[: args.image_prompt_max].strip()

        try:
            display.stream_started(tab_id)
            display.prompt("user", text=prompt, tab_id=tab_id, original=prompt)
            display.prompt("ai", text=args.generating_text, tab_id=tab_id)
            time_start = utils.now()
            self.lock.acquire()

            response = image_generation(
                n=1,
                prompt=prompt,
                size=args.image_size,
                model=args.image_model,
            )

            if (not response) or (not response.data) or (not response.data[0]):
                return

            url = response.data[0].url

            if not url:
                return

            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                return

            time_end = utils.now()
            time_diff = time_end - time_start
            link_text = utils.time_in("Image generated", time_start, time_end)
            link = f"[{link_text}]({url})"

            display.remove_last_ai(tab_id)
            display.prompt("ai", text=link, tab_id=tab_id)

            log_dict: dict[str, Any] = {}
            log_dict["user"] = prompt
            log_dict["ai"] = link
            log_dict["date"] = time_end
            log_dict["duration"] = time_diff
            log_dict["model"] = args.image_model
            log_dict["seed"] = config.seed
            log_dict["history"] = config.history
            log_dict["max_tokens"] = config.max_tokens
            log_dict["temperature"] = config.temperature
            log_dict["top_k"] = config.top_k
            log_dict["top_p"] = config.top_p
            log_dict["format"] = config.format
            log_dict["file"] = ""

            tabconvo.convo.add(log_dict)
            tabconvo.convo.update()
        except BaseException as e:
            display.print("Error generating the image.")
            utils.error(e)

        self.release_lock()

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
        text = ""

        if not self.loaded_model:
            if args.emojis:
                text = utils.get_emoji("unloaded")
            else:
                text = "Not Loaded"

            self.icon_text = tips["model_unloaded"]
        elif (
            self.model_is_gpt(self.loaded_model)
            or self.model_is_gemini(self.loaded_model)
            or self.model_is_claude(self.loaded_model)
        ):
            if args.emojis:
                text = utils.get_emoji("remote")
            else:
                text = "Remote"

            self.icon_text = tips["model_remote"]
        else:
            if args.emojis:
                text = utils.get_emoji("local")
            else:
                text = "Local"

            self.icon_text = tips["model_local"]

        icon.configure(text=text)
        tooltip.set_text(self.icon_text)

    def set_openai_key(self) -> None:
        from .dialogs import Dialog
        from .paths import paths

        def action(key: str) -> None:
            path = Path(paths.openai_key)

            if (not path.exists()) or not (path.is_file()):
                path.parent.mkdir(parents=True, exist_ok=True)
                Path.touch(paths.openai_key, exist_ok=True)

            files.write(path, key)
            self.read_openai_key()

        self.read_openai_key()

        Dialog.show_input(
            "OpenAI API Key",
            lambda text: action(text),
            mode="password",
            value=self.openai_key,
        )

    def set_google_key(self) -> None:
        from .dialogs import Dialog
        from .paths import paths

        def action(key: str) -> None:
            path = Path(paths.google_key)

            if (not path.exists()) or not (path.is_file()):
                path.parent.mkdir(parents=True, exist_ok=True)
                Path.touch(paths.google_key, exist_ok=True)

            files.write(path, key)
            self.read_google_key()

        self.read_google_key()

        Dialog.show_input(
            "Google API Key",
            lambda text: action(text),
            mode="password",
            value=self.google_key,
        )

    def set_anthropic_key(self) -> None:
        from .dialogs import Dialog
        from .paths import paths

        def action(key: str) -> None:
            path = Path(paths.anthropic_key)

            if (not path.exists()) or not (path.is_file()):
                path.parent.mkdir(parents=True, exist_ok=True)
                Path.touch(paths.anthropic_key, exist_ok=True)

            files.write(path, key)
            self.read_anthropic_key()

        self.read_anthropic_key()

        Dialog.show_input(
            "Anthropic API Key",
            lambda text: action(text),
            mode="password",
            value=self.anthropic_key,
        )

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
                response = requests.get(path, timeout=self.read_file_timeout)

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

        if config.max_tokens <= 0:
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

        model_ = utils.split_long(model_)
        Dialog.show_message(model_)

    def get_stop_list(self) -> list[str] | None:
        stop_list = config.stop.split(";;") if config.stop else None

        if stop_list:
            stop_list = [item.strip() for item in stop_list]

        return stop_list

    def start_auto_unload(self) -> None:
        if args.auto_unload < 1:
            return

        m = utils.singular_or_plural(args.auto_unload, "min", "mins")

        if not args.quiet:
            utils.msg(f"Model will auto-unload in {args.auto_unload} {m}")

        thread = threading.Thread(target=lambda: self.auto_unload_loop())
        thread.daemon = True
        thread.start()

    def auto_unload_loop(self) -> None:
        utils.sleep(10)

        while True:
            if self.loaded_model and self.stream_date:
                seconds = utils.now() - self.stream_date
                minutes = seconds / 60

                if minutes >= args.auto_unload:
                    self.unload()

            utils.sleep(10)

    def no_llama_error(self) -> None:
        msg = "Error: llama.cpp support is not enabled. A library must be installed to use local models. Check the documentation."
        display.print(msg)

    def long_url(self, text: str) -> bool:
        if " " in text:
            return False

        if utils.is_url(text):
            if len(text) > 100:
                return True

        return False

    def get_model(self) -> str:
        return variables.replace_variables(config.model)

    def web_search(self, query: str) -> str:
        try:
            return search.web_search(query)
        except Exception as e:
            error_msg = f"Error performing web search: {e}"
            utils.error(error_msg)
            return error_msg

    def handle_tool_calls(self, tool_calls_buffer: ToolCallsBuffer, tab_id: str) -> str:
        try:
            tool_calls = []
            tool_messages = []

            for tool_call_data in tool_calls_buffer.values():
                if not tool_call_data["function"]["name"]:
                    continue

                fn_name = tool_call_data["function"]["name"]
                fn_args_str = tool_call_data["function"]["arguments"]
                tool_call_id = tool_call_data["id"]

                toolfunc = self.toolfuncs.get(fn_name)

                if not toolfunc:
                    continue

                try:
                    fn_args = json.loads(fn_args_str) if fn_args_str else {}
                    result = toolfunc(**fn_args)

                    tool_messages.append(
                        {
                            "tool_call_id": tool_call_id,
                            "role": "tool",
                            "name": fn_name,
                            "content": str(result),
                        }
                    )

                    tool_calls.append(
                        {
                            "id": tool_call_id,
                            "type": "function",
                            "function": {"name": fn_name, "arguments": fn_args_str},
                        }
                    )
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    tool_messages.append(
                        {
                            "tool_call_id": tool_call_id,
                            "role": "tool",
                            "name": fn_name,
                            "content": f"Error executing function: {e}",
                        }
                    )

            if not tool_messages:
                return ""

            tabconvo = display.get_tab_convo(tab_id)
            if not tabconvo or not tabconvo.convo.items:
                return ""

            messages: list[dict[str, Any]] = []

            if config.system:
                system = utils.replace_keywords(config.system)
                messages.append({"role": "system", "content": system})

            last_item = tabconvo.convo.items[-1]
            user_content = getattr(last_item, "user", "")

            if user_content:
                messages.append({"role": "user", "content": user_content})

            messages.append({"role": "assistant", "tool_calls": tool_calls})
            messages.extend(tool_messages)
            original_question = user_content if user_content else "the user's question"

            messages.append(
                {
                    "role": "user",
                    "content": f'Based on the web search results provided above, please provide a comprehensive and detailed answer to this question: "{original_question}"\n\nUse the specific information, facts, and details from the search results to give an accurate, informative, and up-to-date response. Include relevant details, dates, numbers, and context from the search results in your answer.',
                }
            )

            gen_config = self.get_gen_config(messages)
            gen_config["stream"] = False

            if self.is_remote_model():
                response = completion(**gen_config, timeout=self.tools_timeout)
            elif self.model:
                local_gen_config = gen_config.copy()
                del local_gen_config["model"]

                response = self.model.create_chat_completion_openai_v1(
                    **local_gen_config
                )
            else:
                return "\n\nError: No model available"

            choices = getattr(response, "choices", None)

            if not choices or not choices[0]:
                return "\n\nError: No choices in response"

            content = choices[0].message.content

            if choices and content:
                return f"\n\n{content}"

            return ""
        except Exception as e:
            utils.error(e)
            return f"\n\nError handling tool calls: {e}"

    def is_remote_model(self) -> bool:
        return (
            self.model_is_gpt(self.get_model())
            or self.model_is_gemini(self.get_model())
            or self.model_is_claude(self.get_model())
        )

    def get_gen_config(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        gen_config = {
            "messages": messages,
            "stream": config.stream == "yes",
            "temperature": config.temperature,
            "top_p": config.top_p,
            "seed": config.seed,
            "stop": self.get_stop_list(),
        }

        if config.search == "yes":
            gen_config["tools"] = self.tools
            gen_config["tool_choice"] = "auto"

        if self.is_remote_model():
            gen_config["model"] = f"{self.loaded_provider}/{self.get_model()}"
        else:
            gen_config["model"] = self.get_model()

        return gen_config

    def prompt(self, text: str, tab_id: str | None = None) -> None:
        self.stream({"text": text}, tab_id=tab_id)


model = Model()
