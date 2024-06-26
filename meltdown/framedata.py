# Standard
import tkinter as tk


class FrameData:
    frame_number = 0

    def __init__(self, frame: tk.Frame) -> None:
        FrameData.frame_number += 1
        self.frame = frame
        self.col = 0

    def expand(self) -> None:
        self.frame.grid_columnconfigure(self.col - 1, weight=1)

    def do_expand(self, col: int) -> None:
        self.frame.grid_columnconfigure(col, weight=1)

    def do_unexpand(self, col: int) -> None:
        self.frame.grid_columnconfigure(col, weight=0)
