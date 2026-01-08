from __future__ import annotations

# Standard
from typing import TYPE_CHECKING

# Modules
from .app import app
from .tooltips import ToolTip
from .tips import tips
from .utils import utils
from .widgetutils import widgetutils

# Try Import
llama_cpp = utils.try_import("llama_cpp")

if llama_cpp:
    Formats = llama_cpp.llama_chat_format.LlamaChatCompletionHandlerRegistry


if TYPE_CHECKING:
    from .widgets import Widgets
    from .framedata import FrameData


class Details:
    def __init__(self) -> None:
        self.width_1 = 10
        self.width_2 = 7

    def make_label(
        self,
        widgets: Widgets,
        data: FrameData,
        key: str,
        label: str,
        padx: tuple[int, int] | None = None,
    ) -> None:
        label_wid = widgetutils.make_label(data, label, padx=padx)
        setattr(widgets, f"{key}_label", label_wid)
        ToolTip(label_wid, tips[key])

    def make_entry(
        self,
        widgets: Widgets,
        data: FrameData,
        key: str,
        width: int | None = None,
    ) -> None:
        width = width or app.theme.entry_width_small
        entry_wid = widgetutils.make_entry(data, width=width)
        setattr(widgets, key, entry_wid)
        ToolTip(entry_wid, tips[key])

    def make_combobox(
        self,
        widgets: Widgets,
        data: FrameData,
        key: str,
        values: list[str],
        width: int | None = None,
    ) -> None:
        width = width or 15
        combo_wid = widgetutils.make_combobox(data, values=values, width=width)
        setattr(widgets, key, combo_wid)
        ToolTip(combo_wid, tips[key])

    def add_users(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "user", "User", padx=(0, app.theme.padx))
        self.make_entry(widgets, data, "avatar_user", width=4)
        self.make_entry(widgets, data, "name_user", width=self.width_1)

        self.make_label(widgets, data, "ai", "AI")
        self.make_entry(widgets, data, "avatar_ai", width=4)
        self.make_entry(widgets, data, "name_ai", width=self.width_1)

    def add_history(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "history", "History")
        self.make_entry(widgets, data, "history")

    def add_context(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "context", "Context")
        self.make_entry(widgets, data, "context")

    def add_max_tokens(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "max_tokens", "Tokens")
        self.make_entry(widgets, data, "max_tokens")

    def add_threads(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "threads", "Threads")
        self.make_entry(widgets, data, "threads")

    def add_gpu_layers(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "gpu_layers", "GPU")
        self.make_entry(widgets, data, "gpu_layers")

    def add_batch_size(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "batch_size", "n-batch")
        self.make_entry(widgets, data, "batch_size")

    def add_ubatch_size(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "ubatch_size", "u-batch")
        self.make_entry(widgets, data, "ubatch_size")

    def add_search(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "search", "Search", padx=(0, app.theme.padx))
        self.make_combobox(widgets, data, "search", ["yes", "no"], width=self.width_2)

    def add_memory(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "memory", "Memory", padx=(0, app.theme.padx))
        self.make_combobox(widgets, data, "memory", ["yes", "no"], width=self.width_2)

    def add_stream(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "stream", "Stream", padx=(0, app.theme.padx))
        self.make_combobox(widgets, data, "stream", ["yes", "no"], width=self.width_2)

    def add_format(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "format", "Format")
        values = ["auto"]

        if llama_cpp:
            fmts = sorted(Formats._chat_handlers)
            values.extend(fmts)

        self.make_combobox(widgets, data, "format", values, width=13)

    def add_temperature(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "temperature", "Temp")
        self.make_entry(widgets, data, "temperature")

    def add_logits(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "logits", "Logits")
        self.make_combobox(widgets, data, "logits", ["normal", "all"], width=8)

    def add_seed(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "seed", "Seed")
        self.make_entry(widgets, data, "seed")

    def add_top_p(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "top_p", "Top P")
        self.make_entry(widgets, data, "top_p")

    def add_top_k(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "top_k", "Top K")
        self.make_entry(widgets, data, "top_k")

    def add_before(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "before", "Before")
        self.make_entry(widgets, data, "before", width=self.width_1)

    def add_after(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "after", "After")
        self.make_entry(widgets, data, "after", width=self.width_1)

    def add_stop(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "stop", "Stop")
        self.make_entry(widgets, data, "stop", width=self.width_1)

    def add_mlock(self, widgets: Widgets, data: FrameData) -> None:
        self.make_label(widgets, data, "mlock", "M-Lock")
        self.make_combobox(widgets, data, "mlock", ["yes", "no"], width=self.width_2)

    def add_items(self) -> None:
        from .framedata import FrameData
        from .widgets import widgets

        # Details 1 Items
        data = FrameData(widgets.scroller_details_1)
        self.add_users(widgets, data)
        self.add_history(widgets, data)
        self.add_context(widgets, data)
        self.add_max_tokens(widgets, data)
        self.add_temperature(widgets, data)
        self.add_threads(widgets, data)
        self.add_gpu_layers(widgets, data)
        self.add_batch_size(widgets, data)
        self.add_ubatch_size(widgets, data)
        self.add_top_p(widgets, data)
        self.add_top_k(widgets, data)

        # Details 2 Items
        data = FrameData(widgets.scroller_details_2)
        self.add_stream(widgets, data)
        self.add_search(widgets, data)
        self.add_memory(widgets, data)
        self.add_format(widgets, data)
        self.add_seed(widgets, data)
        self.add_before(widgets, data)
        self.add_after(widgets, data)
        self.add_stop(widgets, data)
        self.add_mlock(widgets, data)
        self.add_logits(widgets, data)


details = Details()
