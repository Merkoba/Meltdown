# Standard
import argparse
from typing import Any, Dict


class ArgParser:
    def __init__(self, title: str, argdefs: Dict[str, Any], obj: Any):
        parser = argparse.ArgumentParser(description=title)
        argdefs["string_arg"] = {"nargs": "*"}

        for key in argdefs:
            item = argdefs[key]

            if key == "string_arg":
                name = key
            else:
                name = ArgParser.under_to_dash(key)
                name = f"--{name}"

            tail = {key: value for key,
                    value in item.items() if value is not None}

            parser.add_argument(name, **tail)

        self.parser = parser
        self.args = parser.parse_args()
        self.obj = obj

    def string_arg(self) -> str:
        return " ".join(self.args.string_arg)

    def get_value(self, attr: str, key: str = "") -> None:
        value = getattr(self.args, attr)

        if value is not None:
            if key:
                self.set(key, value)
            else:
                self.set(attr, value)

    def get(self, attr: str) -> Any:
        return getattr(self.obj, attr)

    def set(self, attr: str, value: Any) -> None:
        setattr(self.obj, attr, value)

    @staticmethod
    def dash_to_under(s: str) -> str:
        return s.replace("-", "_")

    @staticmethod
    def under_to_dash(s: str) -> str:
        return s.replace("_", "-")
