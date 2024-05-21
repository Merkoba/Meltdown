# Standard
from typing import TYPE_CHECKING

# Modules
from .args import args
from .tooltips import ToolTip
from .tips import tips
from . import widgetutils


if TYPE_CHECKING:
    from .widgets import Widgets


def setup() -> None:
    do_setup("system")
    do_setup("details_1")
    do_setup("details_2")

    check_all_buttons()


def do_setup(name: str) -> None:
    from .widgets import widgets

    scroller = getattr(widgets, f"scroller_{name}")
    scroller.update_idletasks()
    canvas = getattr(widgets, f"scroller_canvas_{name}")
    canvas.update_idletasks()
    canvas.configure(width=scroller.winfo_reqwidth())
    canvas.configure(height=scroller.winfo_reqheight())
    left = getattr(widgets, f"scroller_button_left_{name}")
    right = getattr(widgets, f"scroller_button_right_{name}")

    left.set_bind("<Button-4>", lambda e: to_left(name))
    left.set_bind("<Button-5>", lambda e: to_right(name))
    left.set_bind("<Button-2>", lambda e: to_start(name))

    right.set_bind("<Button-4>", lambda e: to_left(name))
    right.set_bind("<Button-5>", lambda e: to_right(name))
    right.set_bind("<Button-2>", lambda e: to_end(name))

    scroller.bind("<Button-4>", lambda e: to_left(name))
    scroller.bind("<Button-5>", lambda e: to_right(name))

    for child in scroller.winfo_children():
        child.bind("<Button-4>", lambda e: to_left(name))
        child.bind("<Button-5>", lambda e: to_right(name))


def to_left(name: str) -> None:
    from .widgets import widgets

    canvas = getattr(widgets, f"scroller_canvas_{name}")
    scroll_pos_left = canvas.xview()[0]

    if scroll_pos_left == 0.0:
        return

    canvas.xview_scroll(-widgets.canvas_scroll, "units")
    check_buttons(name)


def to_right(name: str) -> None:
    from .widgets import widgets

    canvas = getattr(widgets, f"scroller_canvas_{name}")
    scroll_pos_right = canvas.xview()[1]

    if scroll_pos_right == 1.0:
        return

    canvas.xview_scroll(widgets.canvas_scroll, "units")
    check_buttons(name)


def to_start(name: str) -> None:
    from .widgets import widgets

    canvas = getattr(widgets, f"scroller_canvas_{name}")
    canvas.xview_moveto(0)
    check_buttons(name)


def to_end(name: str) -> None:
    from .widgets import widgets

    canvas = getattr(widgets, f"scroller_canvas_{name}")
    canvas.xview_moveto(1.0)
    check_buttons(name)


def check_buttons(name: str) -> None:
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
        left.set_text("-")
    else:
        left.set_style("alt")
        left.set_text("<")

    if scroll_pos_right == 1.0:
        right.set_style("disabled")
        right.set_text("-")
    else:
        right.set_style("alt")
        right.set_text(">")


def check_all_buttons() -> None:
    check_buttons("system")
    check_buttons("details_1")
    check_buttons("details_2")


def add(widgets: "Widgets", name: str) -> None:
    frame_data = widgetutils.make_frame()
    setattr(widgets, f"{name}_frame", frame_data.frame)
    left_frame = widgetutils.make_frame(frame_data.frame, col=0, row=0)
    left_frame.frame.grid_rowconfigure(0, weight=1)

    left_button = widgetutils.make_button(
        left_frame, "<", lambda: to_left(name), style="alt"
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
        lambda: to_right(name),
        style="alt",
    )

    setattr(widgets, f"scroller_button_right_{name}", right_button)
    ToolTip(right_button, tips["scroller_button"])

    if not args.scroller_buttons:
        left_button.grid_remove()
        right_button.grid_remove()

    frame_data.frame.columnconfigure(1, weight=1)
