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


def add_items() -> None:
    from .widgets import widgets
    from .framedata import FrameData
    from .system import system
    from . import details

    # Details 1 Items
    system.add_monitors(FrameData(widgets.scroller_system))

    # Details 2 Items
    sd1 = FrameData(widgets.scroller_details_1)
    details.add_users(widgets, sd1)
    details.add_history(widgets, sd1)
    details.add_context(widgets, sd1)
    details.add_max_tokens(widgets, sd1)
    details.add_threads(widgets, sd1)
    details.add_gpu_layers(widgets, sd1)
    details.add_temperature(widgets, sd1)

    # Details 3 Items
    sd2 = FrameData(widgets.scroller_details_2)
    details.add_format(widgets, sd2)
    details.add_before(widgets, sd2)
    details.add_after(widgets, sd2)
    details.add_stop(widgets, sd2)
    details.add_seed(widgets, sd2)
    details.add_top_p(widgets, sd2)
    details.add_top_k(widgets, sd2)
    details.add_mlock(widgets, sd2)


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
