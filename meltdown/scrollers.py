# Standard
from typing import TYPE_CHECKING

# Modules
from .args import args
from .tooltips import ToolTip
from .tips import tips
from .widgetutils import widgetutils


if TYPE_CHECKING:
    from .widgets import Widgets


class Scrollers:
    def setup(self) -> None:
        self.do_setup("system")
        self.do_setup("details_1")
        self.do_setup("details_2")
        self.check_all_buttons()

    def do_setup(self, name: str) -> None:
        from .widgets import widgets

        scroller = getattr(widgets, f"scroller_{name}")
        scroller.update_idletasks()
        canvas = getattr(widgets, f"scroller_canvas_{name}")
        canvas.update_idletasks()
        canvas.configure(width=scroller.winfo_reqwidth())
        canvas.configure(height=scroller.winfo_reqheight())
        left = getattr(widgets, f"scroller_button_left_{name}")
        right = getattr(widgets, f"scroller_button_right_{name}")

        left.set_bind("<Button-4>", lambda e: self.to_left(name))
        left.set_bind("<Button-5>", lambda e: self.to_right(name))
        left.set_bind("<Button-2>", lambda e: self.to_start(name))

        right.set_bind("<Button-4>", lambda e: self.to_left(name))
        right.set_bind("<Button-5>", lambda e: self.to_right(name))
        right.set_bind("<Button-2>", lambda e: self.to_end(name))

        scroller.bind("<Button-4>", lambda e: self.to_left(name))
        scroller.bind("<Button-5>", lambda e: self.to_right(name))

        for child in scroller.winfo_children():
            child.bind("<Button-4>", lambda e: self.to_left(name))
            child.bind("<Button-5>", lambda e: self.to_right(name))

    def to_left(self, name: str) -> None:
        from .widgets import widgets

        canvas = getattr(widgets, f"scroller_canvas_{name}")
        scroll_pos_left = canvas.xview()[0]

        if scroll_pos_left == 0.0:
            return

        canvas.xview_scroll(-widgets.canvas_scroll, "units")
        self.check_buttons(name)

    def to_right(self, name: str) -> None:
        from .widgets import widgets

        canvas = getattr(widgets, f"scroller_canvas_{name}")
        scroll_pos_right = canvas.xview()[1]

        if scroll_pos_right == 1.0:
            return

        canvas.xview_scroll(widgets.canvas_scroll, "units")
        self.check_buttons(name)

    def to_start(self, name: str) -> None:
        from .widgets import widgets

        canvas = getattr(widgets, f"scroller_canvas_{name}")
        canvas.xview_moveto(0)
        self.check_buttons(name)

    def to_end(self, name: str) -> None:
        from .widgets import widgets

        canvas = getattr(widgets, f"scroller_canvas_{name}")
        canvas.xview_moveto(1.0)
        self.check_buttons(name)

    def check_buttons(self, name: str) -> None:
        from .widgets import widgets
        from .tooltips import ToolTip

        canvas = getattr(widgets, f"scroller_canvas_{name}")
        scroll_pos_left = canvas.xview()[0]
        scroll_pos_right = canvas.xview()[1]
        ToolTip.hide_all()

        left = getattr(widgets, f"scroller_button_left_{name}")
        right = getattr(widgets, f"scroller_button_right_{name}")

        if scroll_pos_left == 0:
            left.set_style("disabled")
        else:
            left.set_style("alt")

        if scroll_pos_right == 1.0:
            right.set_style("disabled")
        else:
            right.set_style("alt")

    def check_all_buttons(self) -> None:
        self.check_buttons("system")
        self.check_buttons("details_1")
        self.check_buttons("details_2")

    def add(self, widgets: "Widgets", name: str) -> None:
        frame_data = widgetutils.make_frame()
        setattr(widgets, f"{name}_frame", frame_data.frame)
        left_frame = widgetutils.make_frame(frame_data.frame, col=0, row=0)
        left_frame.frame.grid_rowconfigure(0, weight=1)

        left_button = widgetutils.make_button(
            left_frame, "<", lambda: self.to_left(name), style="alt"
        )

        setattr(widgets, f"scroller_button_left_{name}", left_button)
        ToolTip(left_button, tips["scroller_button"])

        scroller_frame, canvas = widgetutils.make_scrollable_frame(frame_data.frame, 1)

        setattr(widgets, f"scroller_{name}", scroller_frame)
        setattr(widgets, f"scroller_canvas_{name}", canvas)
        right_frame = widgetutils.make_frame(frame_data.frame, col=2, row=0)
        right_frame.frame.grid_rowconfigure(0, weight=1)

        right_button = widgetutils.make_button(
            right_frame,
            ">",
            lambda: self.to_right(name),
            style="alt",
        )

        setattr(widgets, f"scroller_button_right_{name}", right_button)
        ToolTip(right_button, tips["scroller_button"])

        if not args.scroller_buttons:
            left_button.grid_remove()
            right_button.grid_remove()

        frame_data.frame.columnconfigure(1, weight=1)


scrollers = Scrollers()
