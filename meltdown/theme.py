# Standard
from typing import Tuple


class Theme:
    width = 784
    height = 752

    font_family = "sans"
    font = (font_family, 14)
    font_button = (font_family, 12)
    font_combobox = (font_family, 13)
    font_tab = (font_family, 12)
    font_menu = (font_family, 13)
    snippet_font_family = "monospace"

    syntax_style = "monokai"
    dialog_color = "#252933"
    background_color = "#212121"
    foreground_color = "white"
    red_color = "#FF6B6B"
    green_color = "#44B3A1"
    button_background = "#446CA1"
    button_background_alt = "#3D4555"
    button_background_hover = "#387ADF"
    button_background_hover_alt = "#494D62"
    green_button_background_hover = "#944E63"
    green_background = "#3F9687"
    background_disabled = "#2B303B"
    button_foreground = "white"
    entry_background = "#2B303B"
    entry_foreground = "white"
    placeholder_color = "#494D62"
    separator_color = "#2B303B"
    text_background = "#2B303B"
    text_foreground = "white"
    combobox_background = "#2B303B"
    dialog_background = "white"
    dialog_foreground = "black"
    dialog_border = "#446CA1"
    snippet_background = "#3D4555"
    snippet_foreground = "white"
    snippet_header_background = "#A9C3CA"
    snippet_header_foreground = "#2B303B"
    highlight_background = "#3D4555"
    highlight_foreground = "white"
    border_color = "#959595"
    menu_background = "white"
    menu_foreground = "black"
    menu_hover_background = "#6693C3"
    menu_hover_foreground = "white"
    menu_disabled_background = "#E0E0E0"
    menu_disabled_foreground = "#3D4555"

    padx = 10
    pady = 10
    frame_padx = 0
    frame_pady = 0
    entry_width = 10
    entry_width_small = 6
    combobox_width = 11
    combobox_width_small = 7
    border_width = 4
    button_width = 8
    snippet_header_minus = 1

    @staticmethod
    def get_output_font() -> Tuple[str, int]:
        from .config import config
        return (Theme.font_family, config.output_font_size)

    @staticmethod
    def get_snippet_font(smaller: bool = False) -> Tuple[str, int]:
        from .config import config
        size = config.output_font_size

        if smaller:
            size -= Theme.snippet_header_minus

        return (Theme.snippet_font_family, size)

    @staticmethod
    def get_bold_font() -> Tuple[str, int, str]:
        from .config import config
        return (Theme.font_family, config.output_font_size, "bold")

    @staticmethod
    def get_italic_font() -> Tuple[str, int, str]:
        from .config import config
        return (Theme.font_family, config.output_font_size, "italic")
