# Standard
from typing import TYPE_CHECKING

# Libraries
from llama_cpp.llama_chat_format import LlamaChatCompletionHandlerRegistry as formats  # type: ignore

# Modules
from .app import app
from .tooltips import ToolTip
from .tips import tips
from . import widgetutils


if TYPE_CHECKING:
    from .widgets import Widgets
    from .framedata import FrameData


def add_users(widgets: "Widgets", data: "FrameData") -> None:
    avatar_width = 4
    widgets.user_label = widgetutils.make_label(data, "User", padx=0)
    ToolTip(widgets.user_label, tips["user_label"])

    widgets.avatar_user = widgetutils.make_entry(data, width=avatar_width)
    ToolTip(widgets.avatar_user, tips["avatar_user"])

    widgets.name_user = widgetutils.make_entry(data)
    ToolTip(widgets.name_user, tips["name_user"])

    widgets.ai_label = widgetutils.make_label(data, "AI")
    ToolTip(widgets.ai_label, tips["ai_label"])

    widgets.avatar_ai = widgetutils.make_entry(data, width=avatar_width)
    ToolTip(widgets.avatar_ai, tips["avatar_ai"])

    widgets.name_ai = widgetutils.make_entry(data)
    ToolTip(widgets.name_ai, tips["name_ai"])


def add_history(widgets: "Widgets", data: "FrameData") -> None:
    widgets.history_label = widgetutils.make_label(data, "History")
    widgets.history = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.history_label, tips["history"])
    ToolTip(widgets.history, tips["history"])


def add_context(widgets: "Widgets", data: "FrameData") -> None:
    widgets.context_label = widgetutils.make_label(data, "Context")
    widgets.context = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.context_label, tips["context"])
    ToolTip(widgets.context, tips["context"])


def add_max_tokens(widgets: "Widgets", data: "FrameData") -> None:
    widgets.max_tokens_label = widgetutils.make_label(data, "Max Tokens")
    widgets.max_tokens = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.max_tokens_label, tips["max_tokens"])
    ToolTip(widgets.max_tokens, tips["max_tokens"])


def add_threads(widgets: "Widgets", data: "FrameData") -> None:
    widgets.threads_label = widgetutils.make_label(data, "Threads")
    widgets.threads = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.threads_label, tips["threads"])
    ToolTip(widgets.threads, tips["threads"])


def add_gpu_layers(widgets: "Widgets", data: "FrameData") -> None:
    widgets.gpu_layers_label = widgetutils.make_label(data, "GPU Layers")
    widgets.gpu_layers = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.gpu_layers_label, tips["gpu_layers"])
    ToolTip(widgets.gpu_layers, tips["gpu_layers"])


def add_format(widgets: "Widgets", data: "FrameData") -> None:
    widgets.format_label = widgetutils.make_label(data, "Format", padx=0)
    values = ["auto"]
    fmts = sorted([item for item in formats._chat_handlers])
    values.extend(fmts)
    widgets.format = widgetutils.make_combobox(data, values=values, width=15)
    ToolTip(widgets.format_label, tips["format"])
    ToolTip(widgets.format, tips["format"])


def add_temperature(widgets: "Widgets", data: "FrameData") -> None:
    widgets.temperature_label = widgetutils.make_label(data, "Temp")

    widgets.temperature = widgetutils.make_entry(
        data, width=app.theme.entry_width_small
    )

    ToolTip(widgets.temperature_label, tips["temperature"])
    ToolTip(widgets.temperature, tips["temperature"])


def add_seed(widgets: "Widgets", data: "FrameData") -> None:
    widgets.seed_label = widgetutils.make_label(data, "Seed")
    widgets.seed = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.seed_label, tips["seed"])
    ToolTip(widgets.seed, tips["seed"])


def add_top_p(widgets: "Widgets", data: "FrameData") -> None:
    widgets.top_p_label = widgetutils.make_label(data, "Top P")
    widgets.top_p = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.top_p_label, tips["top_p"])
    ToolTip(widgets.top_p, tips["top_p"])


def add_top_k(widgets: "Widgets", data: "FrameData") -> None:
    widgets.top_k_label = widgetutils.make_label(data, "Top K")
    widgets.top_k = widgetutils.make_entry(data, width=app.theme.entry_width_small)
    ToolTip(widgets.top_k_label, tips["top_k"])
    ToolTip(widgets.top_k, tips["top_k"])


def add_before(widgets: "Widgets", data: "FrameData") -> None:
    widgets.before_label = widgetutils.make_label(data, "Before")
    widgets.before = widgetutils.make_entry(data, width=11)
    ToolTip(widgets.before_label, tips["before"])
    ToolTip(widgets.before, tips["before"])


def add_after(widgets: "Widgets", data: "FrameData") -> None:
    widgets.after_label = widgetutils.make_label(data, "After")
    widgets.after = widgetutils.make_entry(data, width=11)
    ToolTip(widgets.after_label, tips["after"])
    ToolTip(widgets.after, tips["after"])


def add_stop(widgets: "Widgets", data: "FrameData") -> None:
    widgets.stop_label = widgetutils.make_label(data, "Stop")
    widgets.stop = widgetutils.make_entry(data, width=11)
    ToolTip(widgets.stop_label, tips["stop"])
    ToolTip(widgets.stop, tips["stop"])


def add_mlock(widgets: "Widgets", data: "FrameData") -> None:
    widgets.mlock_label = widgetutils.make_label(data, "M-Lock")

    widgets.mlock = widgetutils.make_combobox(
        data, width=app.theme.combobox_width_small, values=["yes", "no"]
    )

    ToolTip(widgets.mlock_label, tips["mlock"])
    ToolTip(widgets.mlock, tips["mlock"])
