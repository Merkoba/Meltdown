# Modules
import tkinter as tk

# Standard
from enum import Enum
from typing import Literal


class Fill(Enum):
    NONE = tk.NONE
    HORIZONTAL = tk.X
    VERTICAL = tk.Y
    BOTH = tk.BOTH


FillLiteral = Literal[Fill.NONE, Fill.HORIZONTAL, Fill.VERTICAL, Fill.BOTH]
