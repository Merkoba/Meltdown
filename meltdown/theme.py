# Modules
from .config import config

# Standard
from typing import Tuple


class Theme:
    def __init__(self) -> None:
        self.width: int
        self.height: int

        self.font_family: str
        self.font: Tuple[str, int]
        self.font_button: Tuple[str, int]
        self.font_combobox: Tuple[str, int]
        self.font_tab: Tuple[str, int]
        self.font_menu: Tuple[str, int]
        self.snippet_font_family: str

        self.syntax_style: str
        self.dialog_color: str
        self.background_color: str
        self.foreground_color: str
        self.red_color: str
        self.green_color: str
        self.button_background: str
        self.button_background_alt: str
        self.button_background_hover: str
        self.button_background_hover_alt: str
        self.green_button_background_hover: str
        self.green_background: str
        self.background_disabled: str
        self.button_foreground: str
        self.entry_background: str
        self.entry_foreground: str
        self.placeholder_color: str
        self.separator_color: str
        self.text_background: str
        self.text_foreground: str
        self.combobox_background: str
        self.dialog_background: str
        self.dialog_foreground: str
        self.dialog_border: str
        self.snippet_background: str
        self.snippet_foreground: str
        self.snippet_header_background: str
        self.snippet_header_foreground: str
        self.highlight_background: str
        self.highlight_foreground: str
        self.border_color: str
        self.menu_background: str
        self.menu_foreground: str
        self.menu_hover_background: str
        self.menu_hover_foreground: str
        self.menu_disabled_background: str
        self.menu_disabled_foreground: str

        self.padx: int
        self.pady: int
        self.frame_padx: int
        self.frame_pady: int
        self.entry_width: int
        self.entry_width_small: int
        self.combobox_width: int
        self.combobox_width_small: int
        self.border_width: int
        self.button_width: int
        self.snippet_header_minus: int

    def get_output_font(self) -> Tuple[str, int]:
        return (self.font_family, config.output_font_size)

    def get_snippet_font(self, smaller: bool = False) -> Tuple[str, int]:
        size = config.output_font_size

        if smaller:
            size -= self.snippet_header_minus

        return (self.snippet_font_family, size)

    def get_bold_font(self) -> Tuple[str, int, str]:
        return (self.font_family, config.output_font_size, "bold")

    def get_italic_font(self) -> Tuple[str, int, str]:
        return (self.font_family, config.output_font_size, "italic")
