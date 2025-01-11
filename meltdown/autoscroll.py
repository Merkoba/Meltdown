from __future__ import annotations

# Modules
from .app import app
from .args import args


class AutoScroll:
    def __init__(self) -> None:
        self.enabled = False
        self.direction = "down"
        self.delay_diff = 100
        self.delay = 1000

    def setup(self) -> None:
        self.delay = args.auto_scroll_delay

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

    def stop(self) -> None:
        from .display import display

        if not self.enabled:
            return

        self.enabled = False

        tab = display.get_current_tab()

        if not tab:
            return

        tab.bottom.on_auto_scroll_disabled()

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

        self.schedule_auto_scroll()

    def schedule_auto_scroll(self) -> None:
        app.root.after(self.delay, lambda: self.check())

    def faster(self) -> None:
        delay = max(self.delay - self.delay_diff, 100)
        self.update_delay(delay)

    def slower(self) -> None:
        delay = min(self.delay + self.delay_diff, 3000)
        self.update_delay(delay)

    def update_delay(self, delay: int) -> None:
        from .display import display

        self.delay = delay
        tab = display.get_current_tab()

        if not tab:
            return

        tab.bottom.auto_scroll_button.set_text(self.get_text())

    def get_text(self) -> str:
        return f"Auto-Scroll ({self.delay})"


autoscroll = AutoScroll()
