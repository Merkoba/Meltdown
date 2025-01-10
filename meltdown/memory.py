from __future__ import annotations

# Standard
from typing import Any


class Memory:
    def __init__(self) -> None:
        self.last_log = ""
        self.last_program = ""
        self.last_config = ""
        self.last_session = ""

    def load(self) -> None:
        from .paths import paths
        from .files import files

        try:
            mem = files.load(paths.memory)
        except BaseException:
            return

        for key in mem:
            if hasattr(self, key):
                setattr(self, key, mem[key])

    def save(self) -> None:
        from .paths import paths
        from .files import files

        mem = {}

        for key in self.__dict__:
            if key.startswith("last_"):
                mem[key] = getattr(self, key)

        files.save(paths.memory, mem)

    def set_value(self, key: str, value: Any) -> None:
        if getattr(self, key) == value:
            return

        setattr(self, key, value)
        self.save()


memory = Memory()
