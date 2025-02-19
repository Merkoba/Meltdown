# Standard
import re
from typing import Any

# Modules
from .dialogs import Dialog
from .utils import utils
from .args import args


class Variables:
    def __init__(self) -> None:
        self.variables: dict[str, str] = {}

    def setup(self) -> None:
        for variable in args.variables:
            self.set_variable(variable, False)

    def varname(self, name: str) -> str:
        prefix = args.variable_prefix
        return f"{prefix}{name}"

    def set_variable(self, cmd: str, feedback: bool = True) -> None:
        from .display import display

        def fmt() -> None:
            display.print("Format: [name] [value]")

        if " " not in cmd:
            fmt()
            return

        name, value = utils.cmd_value(cmd)

        if (not name) or (not value):
            fmt()
            return

        self.do_set_variable(name, value, feedback)

    def do_set_variable(self, name: str, value: str, feedback: bool = True) -> None:
        from .display import display

        self.variables[name] = value

        if feedback:
            v = self.varname(name)
            display.print(f"Set Var: `{v}` is now `{value}`", do_format=True)

    def unset_variable(self, name: str) -> None:
        from .display import display

        if name in self.variables:
            del self.variables[name]
            display.print(f"Unset Var: {name}")
        else:
            display.print(f"Variable not found: {name}")

    def read_variable(self, name: str) -> None:
        from .display import display

        if name in self.variables:
            display.print(f"Var: `{name}` is `{self.variables[name]}`", do_format=True)
        else:
            display.print(f"Variable not found: {name}")

    def read_variables(self) -> None:
        from .display import display

        items = []

        if self.variables:
            for name, value in self.variables.items():
                items.append(f"{name} = {value}")
        else:
            display.print("No variables set.")
            return

        Dialog.show_msgbox("Variables", "\n".join(items))

    def replace_variables(self, text: str) -> str:
        def replace(match: Any) -> str:
            name = str(match.group(2))
            key = name[1:]

            if key not in self.variables:
                return name

            return self.variables[key]

        prefix = re.escape(args.variable_prefix)
        pattern = re.compile(rf"(^|\s)({prefix}\w+)")
        return pattern.sub(lambda m: m.group(1) + replace(m), text)

    def is_variable(self, word: str) -> bool:
        return word.startswith(args.variable_prefix)


variables = Variables()
