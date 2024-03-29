# Modules
from .app import app
from .buttonbox import ButtonBox
from .entrybox import EntryBox
from .output import Output
from .tooltips import ToolTip

# Standard
import re
import tkinter as tk
from typing import Optional


class Find:
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        self.parent = parent
        self.tab_id = tab_id
        self.root = tk.Frame(parent)
        self.inner = tk.Frame(self.root)
        self.root.configure(background=app.theme.find_background)
        self.inner.configure(background=app.theme.find_background)
        w = app.theme.find_entry_width
        self.entry = EntryBox(self.inner, style="Normal.TEntry", font=app.theme.font, width=w)
        self.entry.set_name("find")
        ToolTip(self.entry, "Enter some text and hit Enter")
        self.entry.grid(row=0, column=0, sticky="ew", padx=4)
        self.entry.placeholder = "Find..."
        self.entry.check_placeholder()
        self.current_match: Optional[str] = None
        self.widget: Optional[tk.Text] = None
        self.visible = False

        padx_button = 4

        self.next_i_button = ButtonBox(self.inner, "Next (i)", lambda: self.find_next())
        ToolTip(self.next_i_button, "Find next match (case insensitive)")
        self.next_i_button.grid(row=0, column=1, sticky="ew", padx=padx_button)

        self.next_ci_button = ButtonBox(self.inner, "Next", lambda: self.find_next(False))
        ToolTip(self.next_ci_button, "Find next match (case sensitive)")
        self.next_ci_button.grid(row=0, column=2, sticky="ew", padx=padx_button)

        self.bound_ci_button = ButtonBox(self.inner, "Bound (i)", lambda: self.find_next(bound=True))
        ToolTip(self.bound_ci_button, "Find next word-bound match (case insensitive)")
        self.bound_ci_button.grid(row=0, column=3, sticky="ew", padx=padx_button)

        self.bound_i_button = ButtonBox(self.inner, "Bound", lambda: self.find_next(False, bound=True))
        ToolTip(self.bound_i_button, "Find next word-bound match (case sensitive)")
        self.bound_i_button.grid(row=0, column=4, sticky="ew", padx=padx_button)

        self.hide_button = ButtonBox(self.inner, "Hide", lambda: self.hide())
        ToolTip(self.hide_button, "Hide the find bar (Esc)")
        self.hide_button.grid(row=0, column=5, sticky="ew", padx=padx_button)

        self.inner.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        self.root.grid(row=0, column=0, sticky="ew")
        self.root.grid_remove()

    def find_next(self, case_insensitive: bool = True,
                  bound: bool = False, no_match: bool = False) -> None:
        if not self.visible:
            return

        if not self.widget:
            return

        self.clear()
        self.entry.focus_set()
        query = self.entry.get().strip()
        self.entry.set_text(query)

        if not query:
            return

        widget = self.widget

        if not widget:
            return

        if self.current_match is not None:
            start_pos = widget.index(f"{self.current_match}+1c")
        else:
            start_pos = "1.0"

        if not start_pos:
            return

        if query.startswith("/") and query.endswith("/"):
            query = query[1:-1]
        else:
            query = re.escape(query)

        if bound:
            query = r"\y" + query + r"\y"

        if case_insensitive:
            nocase = True
        else:
            nocase = False

        match = self.widget.search(query, start_pos, tk.END, regexp=True, nocase=nocase)

        if match:
            start_index = widget.index(match)
            end_index = widget.index(f"{start_index} wordend")
            widget.tag_add("find", start_index, end_index)
            widget.tag_config("find", background=app.theme.find_match_background)
            widget.tag_config("find", foreground=app.theme.find_match_foreground)
            end_bbox = widget.bbox(end_index)

            if end_bbox is None:
                widget.see(end_index)
            else:
                widget.see(start_index)

            self.current_match = end_index
        else:
            self.current_match = None

            if no_match:
                return

            self.find_next(case_insensitive, bound=bound, no_match=True)

    def clear(self) -> None:
        if self.widget:
            self.widget.tag_remove("find", "1.0", "end")

    def show(self, widget: Optional[tk.Text]) -> None:
        from .display import display

        if self.widget:
            self.clear()

        self.root.grid()
        self.entry.set_text("")
        self.entry.focus_set()

        if widget:
            self.widget = widget
        else:
            self.widget = display.get_output(self.tab_id)

        self.visible = True

    def hide(self) -> None:
        from .inputcontrol import inputcontrol

        self.clear()
        self.root.grid_remove()
        inputcontrol.focus()
        self.visible = False
        self.widget = None

    def on_esc(self) -> None:
        if self.entry.get():
            self.entry.clear()
        else:
            self.hide()
