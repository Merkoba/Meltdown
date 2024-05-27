# Standard
from typing import Optional

# Modules
from .app import app
from .args import args


class AutoScroll:
    def __init__(self) -> None:
        self.enabled = False
        self.direction = "down"

    def enable(self, direction: Optional[str] = None) -> None:
        from .display import display

        if self.enabled:
            return

        tab = display.get_current_tab()

        if not tab:
            return

        if not direction:
            direction = "down"

        if direction == "up":
            if tab.output.yview()[0] <= 0.0001:
                return
        elif direction == "down":
            if tab.output.yview()[1] >= 0.9999:
                return
        else:
            return

        self.direction = direction
        self.enabled = True
        tab.bottom.on_auto_scroll_enabled()
        self.schedule_auto_scroll()

    def disable(self) -> None:
        from .display import display

        if not self.enabled:
            return

        self.enabled = False

        tab = display.get_current_tab()

        if not tab:
            return

        tab.bottom.on_auto_scroll_disabled()

    def toggle(self, direction: Optional[str] = None) -> None:
        if self.enabled:
            if direction:
                if direction != self.direction:
                    self.direction = direction
                    return

            self.disable()
        else:
            self.enable(direction=direction)

    def check(self) -> None:
        from .display import display

        if args.auto_scroll_delay < 100:
            return

        if not self.enabled:
            return

        if self.direction == "up":
            display.scroll_up()
        else:
            display.scroll_down()

        self.schedule_auto_scroll()

    def schedule_auto_scroll(self) -> None:
        app.root.after(args.auto_scroll_delay, lambda: self.check())


autoscroll = AutoScroll()
