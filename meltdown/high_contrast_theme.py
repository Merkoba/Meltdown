# Modules
from .theme import Theme


class HighContrastTheme(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.background_color = "black"
        self.foreground_color = "white"

        self.output_background = "black"
        self.output_foreground = "white"
