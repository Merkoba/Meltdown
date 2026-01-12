from .inputcontrol import inputcontrol


class Next:
    def __init__(self) -> None:
        self.items: list[str] = []

    def action(self, text: str | None) -> None:
        if text:
            self.add(text)
        else:
            self.use()

    def add(self, text: str) -> None:
        self.items.append(text)

    def use(self) -> None:
        if self.items:
            item = self.items.pop(0)
            inputcontrol.set(item)


next_fns = Next()