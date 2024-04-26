# Standard
from typing import TYPE_CHECKING, Optional

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


def make_entry(
    widgets: "Widgets",
    data: "FrameData",
    key: str,
    label: str,
    width: Optional[int] = None,
) -> None:
    label_wid = widgetutils.make_label(data, label)
    setattr(widgets, f"{key}_label", label_wid)

    width = width or app.theme.entry_width_small
    entry_wid = widgetutils.make_entry(data, width=width)
    setattr(widgets, key, entry_wid)

    ToolTip(label_wid, tips[key])
    ToolTip(entry_wid, tips[key])


def make_combobox(
    widgets: "Widgets",
    data: "FrameData",
    key: str,
    label: str,
    values: list,
    padx: Optional[int] = None,
) -> None:
    label_wid = widgetutils.make_label(data, label, padx=padx)
    setattr(widgets, f"{key}_label", label_wid)

    combo_wid = widgetutils.make_combobox(data, values=values, width=15)
    setattr(widgets, key, combo_wid)

    ToolTip(label_wid, tips[key])
    ToolTip(combo_wid, tips[key])


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
    make_entry(widgets, data, "history", "History")


def add_context(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "context", "Context")


def add_max_tokens(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "max_tokens", "Max Tokens")


def add_threads(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "threads", "Threads")


def add_gpu_layers(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "gpu_layers", "GPU Layers")


def add_format(widgets: "Widgets", data: "FrameData") -> None:
    values = ["auto"]
    fmts = sorted([item for item in formats._chat_handlers])
    values.extend(fmts)
    make_combobox(widgets, data, "format", "Format", values)


def add_temperature(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "temperature", "Temperature")


def add_seed(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "seed", "Seed")


def add_top_p(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "top_p", "Top P")


def add_top_k(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "top_k", "Top K")


def add_before(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "before", "Before", width=11)


def add_after(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "after", "After", width=11)


def add_stop(widgets: "Widgets", data: "FrameData") -> None:
    make_entry(widgets, data, "stop", "Stop", width=11)


def add_mlock(widgets: "Widgets", data: "FrameData") -> None:
    values = ["yes", "no"]
    make_combobox(widgets, data, "mlock", "M-Lock", values)
