# Standard
import re
import sys
import argparse
from typing import List, Any, Dict, Union
from pathlib import Path


class ArgParser:
    # Generic class to get arguments from the terminal
    def __init__(self, title: str, argdefs: Dict[str, Any], aliases: Dict[str, List[str]], obj: Any):
        parser = argparse.ArgumentParser(description=title)
        argdefs["string_arg"] = {"nargs": "*"}

        for key in argdefs:
            item = argdefs[key]

            if key == "string_arg":
                names = [key]
            else:
                name = ArgParser.under_to_dash(key)

                # Add -- and - formats
                names = [f"--{name}", f"-{name}"]
                name2 = key.replace("-", "")

                # Check without dashes
                if name2 != name:
                    names.extend([f"--{name2}", f"-{name2}"])

            if key in aliases:
                names += aliases[key]

            tail = {key: value for key,
                    value in item.items() if value is not None}
            parser.add_argument(*names, **tail)

        self.args = parser.parse_args()
        self.obj = obj

    def string_arg(self) -> str:
        return " ".join(self.args.string_arg)

    def get_list(self, attr: str, value: str, vtype: Any, separator: str) -> List[Any]:
        try:
            lst = list(map(vtype, map(str.strip, value.split(separator))))
        except BaseException:
            sys.exit(f"Failed to parse '--{attr}'")

        return lst

    def normal(self, attr: str, value: Any = None) -> None:
        if not value:
            value = getattr(self.args, attr)

        if value is not None:
            self.set(attr, value)

    def commas(self, attr: str, vtype: Any, allow_string: bool = False,
               is_tuple: bool = False, value: Any = None) -> None:
        if not value:
            value = getattr(self.args, attr)

        if value is not None:
            if "," in value:
                lst = self.get_list(attr, value, vtype, ",")

                if is_tuple:
                    self.set(attr, tuple(lst))
                else:
                    self.set(attr, lst)

            elif allow_string:
                self.set(attr, value)

    def path(self, attr: str, value: Any = None) -> None:
        if not value:
            value = getattr(self.args, attr)

        if value is not None:
            self.set(attr, ArgParser.resolve_path(value))

    # Allow p1 and m1 formats
    def number(self, attr: str, vtype: Any, allow_zero: bool = False,
               duration: bool = False, value: Any = None) -> None:
        if not value:
            value = getattr(self.args, attr)

        if value is None:
            return

        value = str(value)
        num = value
        op = ""

        if value.startswith("p") or value.startswith("m"):
            op = value[0]
            num = value[1:]

        if duration:
            num = self.parse_duration(num)

        try:
            if vtype == int:
                num = int(num)
            elif vtype == float:
                num = float(num)
        except BaseException:
            sys.exit(f"Failed to parse '{attr}'")

        default = self.get(attr)

        if op == "p":
            num = default + num
        elif op == "m":
            num = default - num

        err = f"Value for '{attr}' is too low"

        if num == 0:
            if not allow_zero:
                sys.exit(err)
        elif num < 0:
            sys.exit(err)

        self.set(attr, num)

    def get(self, attr: str) -> Any:
        return getattr(self.obj, attr)

    def set(self, attr: str, value: Any) -> None:
        setattr(self.obj, attr, value)

    def parse_duration(self, time_string: str) -> str:
        match = re.match(r"(\d+(\.\d+)?)([smh]+)", time_string)

        if match:
            value, _, unit = match.groups()
            value = float(value)

            if unit == "ms":
                time_string = str(int(value))
            elif unit == "s":
                time_string = str(int(value * 1000))
            elif unit == "m":
                time_string = str(int(value * 60 * 1000))
            elif unit == "h":
                time_string = str(int(value * 60 * 60 * 1000))

        return time_string

    @staticmethod
    def dash_to_under(s: str) -> str:
        return s.replace("-", "_")

    @staticmethod
    def under_to_dash(s: str) -> str:
        return s.replace("_", "-")

    @staticmethod
    def full_path(path: Union[Path, str]) -> Path:
        return Path(path).expanduser().resolve()

    @staticmethod
    def resolve_path(path: Union[Path, str]) -> Path:
        path = ArgParser.full_path(path)

        if path.is_absolute():
            return ArgParser.full_path(path)
        else:
            return ArgParser.full_path(Path(Path.cwd(), path))
