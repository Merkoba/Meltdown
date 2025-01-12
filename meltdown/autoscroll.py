from __future__ import annotations

# Modules
from .app import app
from .args import args
from .utils import utils


class AutoScroll:
    def __init__(self) -> None:
        self.enabled = False
        self.direction = "down"
        self.delay_diff = 100
        self.delay = 1000
        self.min_delay = 100
        self.max_delay = 2000

    def setup(self) -> None:
        self.delay = utils.clamp(args.autoscroll_delay, self.min_delay, self.max_delay)

    def start(self, direction: str | None = None) -> None:
        from .display import display

        if self.enabled:
            return

        tab = display.get_current_tab()

        if not tab:
            return

        if not direction:
            direction = "down"

        if direction == "up":
            if tab.get_output().yview()[0] <= 0.0001:
                return
        elif direction == "down":
            if tab.get_output().yview()[1] >= 0.9999:
                return
        else:
            return

        self.direction = direction
        self.enabled = True
        tab.get_bottom().on_autoscroll_enabled()
        self.schedule_autoscroll()

    def stop(self, check: bool = False) -> None:
        from .display import display

        if not self.enabled:
            return

        if check:
            if not args.autoscroll_interrupt:
                return

        self.enabled = False

        tab = display.get_current_tab()

        if not tab:
            return

        tab.get_bottom().on_autoscroll_disabled()

    def toggle(self, direction: str | None = None) -> None:
        if not direction:
            direction = "down"

        if self.enabled:
            if direction != self.direction:
                self.direction = direction
                return

            self.stop()
        else:
            self.start(direction=direction)

    def check(self) -> None:
        from .display import display

        if self.delay < 100:
            return

        if not self.enabled:
            return

        if self.direction == "up":
            display.scroll_up()
        else:
            display.scroll_down()

        self.schedule_autoscroll()

    def schedule_autoscroll(self) -> None:
        app.root.after(self.delay, lambda: self.check())

    def faster(self) -> None:
        delay = max(self.delay - self.delay_diff, self.min_delay)
        self.update_delay(delay)

    def slower(self) -> None:
        delay = min(self.delay + self.delay_diff, self.max_delay)
        self.update_delay(delay)

    def update_delay(self, delay: int) -> None:
        from .display import display

        self.delay = delay
        tab = display.get_current_tab()

        if not tab:
            return

        tab.get_bottom().autoscroll_button.set_text(self.get_text())

    def get_text(self) -> str:
        perc = 100 - int(
            ((self.delay - self.min_delay) / (self.max_delay - self.min_delay)) * 100
        )

        return f"Autoscroll ({perc})"


autoscroll = AutoScroll()
