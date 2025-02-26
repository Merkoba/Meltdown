from __future__ import annotations

# Standard
import re
import tkinter as tk

# Modules
from .app import app
from .buttonbox import ButtonBox
from .entrybox import EntryBox
from .tooltips import ToolTip
from .output import Output
from .tips import tips


class Find:
    def __init__(self, parent: tk.Frame, tab_id: str) -> None:
        self.parent = parent
        self.tab_id = tab_id
        self.root = tk.Frame(parent)
        self.inner = tk.Frame(self.root)
        self.root.configure(background=app.theme.find_background)
        self.inner.configure(background=app.theme.find_background)
        w = app.theme.find_entry_width

        self.entry = EntryBox(
            self.inner, style="Normal.TEntry", font=app.theme.font(), width=w
        )

        self.entry.set_name("find")
        ToolTip(self.entry, "Enter some text and hit Enter")
        self.entry.grid(row=0, column=0, sticky="ew", padx=4)
        self.entry.placeholder = "Find..."
        self.entry.check_placeholder()
        self.current_match: str | None = None
        self.current_match_reverse: str | None = None
        self.widget: tk.Text | None = None
        self.visible = False
        self.snippet = -1
        self.snippet_focused = False
        self.snippet_index = "1.0"

        padx_button = 4

        self.next_i_button = ButtonBox(self.inner, "Next (i)", lambda: self.find_next())

        self.next_i_button.set_bind(
            "<Button-2>", lambda _: self.find_next(reverse=True)
        )

        ToolTip(self.next_i_button, tips["find_next_i"])
        self.next_i_button.grid(row=0, column=1, sticky="ew", padx=padx_button)

        self.next_button = ButtonBox(self.inner, "Next", lambda: self.find_next(False))

        self.next_button.set_bind(
            "<Button-2>", lambda _: self.find_next(False, reverse=True)
        )

        ToolTip(self.next_button, tips["find_next"])
        self.next_button.grid(row=0, column=2, sticky="ew", padx=padx_button)

        self.bound_i_button = ButtonBox(
            self.inner, "Bound (i)", lambda: self.find_next(bound=True)
        )

        self.bound_i_button.set_bind(
            "<Button-2>", lambda _: self.find_next(bound=True, reverse=True)
        )

        ToolTip(self.bound_i_button, tips["find_bound_i"])
        self.bound_i_button.grid(row=0, column=3, sticky="ew", padx=padx_button)

        self.bound_button = ButtonBox(
            self.inner, "Bound", lambda: self.find_next(False, bound=True)
        )

        self.bound_button.set_bind(
            "<Button-2>", lambda _: self.find_next(False, bound=True, reverse=True)
        )

        ToolTip(self.bound_button, tips["find_bound"])
        self.bound_button.grid(row=0, column=4, sticky="ew", padx=padx_button)

        self.hide_button = ButtonBox(self.inner, "Hide", lambda: self.hide())
        ToolTip(self.hide_button, tips["find_hide"])
        self.hide_button.grid(row=0, column=5, sticky="ew", padx=padx_button)

        self.inner.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        self.root.grid(row=0, column=0, sticky="ew")
        self.root.grid_remove()

    def get_output(self) -> Output | None:
        from .display import display

        return display.get_output(self.tab_id)

    def find_next(
        self,
        case_insensitive: bool = True,
        bound: bool = False,
        no_match: bool = False,
        switch: bool = False,
        first_widget: tk.Widget | None = None,
        reverse: bool = False,
    ) -> None:
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

        if not first_widget:
            first_widget = self.widget

        if reverse and (self.current_match_reverse is not None):
            start_pos = widget.index(f"{self.current_match_reverse}+1c")
        elif self.current_match is not None:
            start_pos = widget.index(f"{self.current_match}+1c")
        elif reverse:
            start_pos = "end"
        else:
            start_pos = "1.0"

        if reverse:
            end_pos = "1.0"
        else:
            end_pos = "end"

        if not start_pos:
            return

        full_query = query

        if full_query.startswith("/") and full_query.endswith("/"):
            full_query = full_query[1:-1]
        else:
            full_query = re.escape(full_query)

        if bound:
            full_query = r"\y" + full_query + r"\y"

        if case_insensitive:
            nocase = True
        else:
            nocase = False

        match_ = self.widget.search(
            full_query,
            start_pos,
            end_pos,
            regexp=True,
            nocase=nocase,
            backwards=reverse,
        )

        output = self.get_output()

        if not output:
            return

        if match_:
            start_index = widget.index(match_)
            end_index = widget.index(f"{start_index}+{len(query)}c")
            widget.tag_add("find", start_index, end_index)
            widget.tag_configure("find", background=app.theme.find_match_background)
            widget.tag_configure("find", foreground=app.theme.find_match_foreground)
            end_bbox = widget.bbox(end_index)

            if end_bbox is None:
                widget.see(end_index)
            else:
                widget.see(start_index)

            if (self.widget != output) and (not self.snippet_focused):
                if self.snippet == -1:
                    pos, index = output.get_snippet_index_2(self.widget)
                    self.snippet_index = pos
                    self.snippet = index

                output.see(self.snippet_index)
                self.snippet_focused = True

            self.current_match_reverse = widget.index(f"{start_index}-1c")
            self.current_match = end_index
        else:
            self.current_match = None
            self.current_match_reverse = None

            if no_match:
                return

            if switch and (self.widget == first_widget):
                return

            self.change_widget()

            self.find_next(
                case_insensitive,
                bound=bound,
                no_match=False,
                switch=True,
                first_widget=first_widget,
                reverse=reverse,
            )

    def next_snippet(self) -> bool:
        self.snippet += 1
        output = self.get_output()

        if not output:
            return False

        if self.snippet >= len(output.snippets):
            return False

        snippets = list(reversed(output.snippets))
        self.widget = snippets[self.snippet].text
        self.snippet_index = output.get_snippet_index(self.snippet)
        self.snippet_focused = False
        return True

    def change_widget(self) -> None:
        if not self.next_snippet():
            self.widget = self.get_output()

            if not self.widget:
                return

            self.snippet = -1
            self.snippet_focused = False
            self.snippet_index = "1.0"

    def clear(self) -> None:
        if self.widget:
            self.widget.tag_remove("find", "1.0", "end")

    def show(
        self,
        widget: tk.Text | None = None,
        query: str | None = None,
    ) -> None:
        if self.widget:
            self.clear()

        self.root.grid()
        self.entry.set_text("")
        self.entry.focus_set()
        self.reset()

        if widget:
            self.widget = widget
        else:
            self.widget = self.get_output()

            if not self.widget:
                return

        self.visible = True

        if query:
            self.entry.set_text(query)
            self.find_next()

    def hide(self) -> None:
        from .inputcontrol import inputcontrol

        self.clear()
        self.root.grid_remove()
        inputcontrol.focus()
        self.visible = False
        self.widget = None
        self.snippet = -1
        self.snippet_focused = False
        self.snippet_index = "1.0"

    def toggle(self) -> None:
        if self.visible:
            self.hide()
        else:
            self.show()

    def reset(self) -> None:
        self.current_match = None
        self.current_match_reverse = None
        self.snippet = -1
        self.snippet_focused = False
        self.snippet_index = "1.0"
