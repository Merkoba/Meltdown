# Standard
from typing import TYPE_CHECKING, Optional, List, Tuple

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


def make_label(
    widgets: "Widgets",
    data: "FrameData",
    key: str,
    label: str,
    padx: Optional[Tuple[int, int]] = None,
) -> None:
    label_wid = widgetutils.make_label(data, label, padx=padx)
    setattr(widgets, f"{key}_label", label_wid)
    ToolTip(label_wid, tips[key])


def make_entry(
    widgets: "Widgets",
    data: "FrameData",
    key: str,
    width: Optional[int] = None,
) -> None:
    width = width or app.theme.entry_width_small
    entry_wid = widgetutils.make_entry(data, width=width)
    setattr(widgets, key, entry_wid)
    ToolTip(entry_wid, tips[key])


def make_combobox(
    widgets: "Widgets",
    data: "FrameData",
    key: str,
    values: List[str],
    width: Optional[int] = None,
) -> None:
    width = width or 15
    combo_wid = widgetutils.make_combobox(data, values=values, width=width)
    setattr(widgets, key, combo_wid)
    ToolTip(combo_wid, tips[key])


width_1 = 10


def add_users(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "user", "User", padx=(0, 0))
    make_entry(widgets, data, "avatar_user", width=4)
    make_entry(widgets, data, "name_user", width=width_1)

    make_label(widgets, data, "ai", "AI")
    make_entry(widgets, data, "avatar_ai", width=4)
    make_entry(widgets, data, "name_ai", width=width_1)


def add_history(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "history", "History")
    make_entry(widgets, data, "history")


def add_context(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "context", "Context")
    make_entry(widgets, data, "context")


def add_max_tokens(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "max_tokens", "Max Tokens")
    make_entry(widgets, data, "max_tokens")


def add_threads(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "threads", "Threads")
    make_entry(widgets, data, "threads")


def add_gpu_layers(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "gpu_layers", "GPU Layers")
    make_entry(widgets, data, "gpu_layers")


def add_format(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "format", "Format", padx=(0, 0))
    values = ["auto"]
    fmts = sorted(formats._chat_handlers)
    values.extend(fmts)
    make_combobox(widgets, data, "format", values, width=13)


def add_temperature(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "temperature", "Temperature")
    make_entry(widgets, data, "temperature")


def add_logits(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "logits", "Logits")
    make_combobox(widgets, data, "logits", ["normal", "all"], width=8)


def add_seed(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "seed", "Seed")
    make_entry(widgets, data, "seed")


def add_top_p(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "top_p", "Top P")
    make_entry(widgets, data, "top_p")


def add_top_k(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "top_k", "Top K")
    make_entry(widgets, data, "top_k")


def add_before(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "before", "Before")
    make_entry(widgets, data, "before", width=width_1)


def add_after(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "after", "After")
    make_entry(widgets, data, "after", width=width_1)


def add_stop(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "stop", "Stop")
    make_entry(widgets, data, "stop", width=width_1)


def add_mlock(widgets: "Widgets", data: "FrameData") -> None:
    make_label(widgets, data, "mlock", "M-Lock")
    make_combobox(widgets, data, "mlock", ["yes", "no"], width=7)


def add_items() -> None:
    from .framedata import FrameData
    from .widgets import widgets

    # Details 1 Items
    data = FrameData(widgets.scroller_details_1)
    add_users(widgets, data)
    add_history(widgets, data)
    add_context(widgets, data)
    add_max_tokens(widgets, data)
    add_threads(widgets, data)
    add_gpu_layers(widgets, data)
    add_temperature(widgets, data)

    # Details 2 Items
    data = FrameData(widgets.scroller_details_2)
    add_format(widgets, data)
    add_before(widgets, data)
    add_after(widgets, data)
    add_stop(widgets, data)
    add_seed(widgets, data)
    add_top_p(widgets, data)
    add_top_k(widgets, data)
    add_mlock(widgets, data)
    add_logits(widgets, data)
