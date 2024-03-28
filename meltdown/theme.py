# Modules
from .config import config

# Standard
from typing import Tuple


class Theme:
    def __init__(self) -> None:
        self.width = 784
        self.height = 752
        self.font_family = "sans"
        self.font = (self.font_family, 14)
        self.font_button = (self.font_family, 12)
        self.font_combobox = (self.font_family, 13)
        self.font_tab = (self.font_family, 12)
        self.font_menu = (self.font_family, 13)
        self.font_tooltips = (self.font_family, 12)
        self.snippet_font_family = "monospace"
        self.avatar_user = "👽"
        self.avatar_ai = "😎"
        self.name_user = "#87CEEB"
        self.name_ai = "#98FB98"
        self.syntax_style = "monokai"
        self.dialog_color = "#252933"
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.monitor_normal = "#44B3A1"
        self.monitor_heavy = "#FF6B6B"
        self.button_background = "#446CA1"
        self.button_alt_background = "#3D4555"
        self.button_hover_background = "#387ADF"
        self.button_alt_hover_background = "#494D62"
        self.button_highlight_hover_background = "#944E63"
        self.button_highlight_background = "#3F9687"
        self.button_disabled_background = "#2B303B"
        self.button_foreground = "white"
        self.button_padx = 10
        self.entry_background = "#2B303B"
        self.entry_foreground = "white"
        self.entry_placeholder_color = "#494D62"
        self.entry_insert = "white"
        self.separator_color = "#2B303B"
        self.output_background = "#2B303B"
        self.output_foreground = "white"
        self.combobox_background = "#2B303B"
        self.combobox_foreground = "white"
        self.dialog_background = "white"
        self.dialog_foreground = "black"
        self.dialog_border = "#446CA1"
        self.snippet_background = "#3D4555"
        self.snippet_foreground = "white"
        self.snippet_header_background = "#A9C3CA"
        self.snippet_header_foreground = "#2B303B"
        self.highlight_background = "#3D4555"
        self.highlight_foreground = "white"
        self.border_color = "#959595"
        self.menu_background = "white"
        self.menu_foreground = "black"
        self.menu_hover_background = "#6693C3"
        self.menu_hover_foreground = "white"
        self.menu_disabled_background = "#E0E0E0"
        self.menu_disabled_foreground = "#3D4555"
        self.output_selection_background = "#C3C3C3"
        self.output_selection_foreground = "black"
        self.snippet_selection_background = "#C3C3C3"
        self.snippet_selection_foreground = "black"
        self.entry_selection_background = "#C3C3C3"
        self.entry_selection_foreground = "black"
        self.tab_selected_background = "#494D62"
        self.tab_normal_background = "#2B303B"
        self.tab_selected_foreground = "white"
        self.tab_normal_foreground = "#C9C9C9"
        self.tab_border = "#6A7B83"
        self.tab_border_with = 1
        self.tabs_container_color = "#2B303B"
        self.tab_padx = 20
        self.tab_pady = 1
        self.scrollbar_1 = "#333B4B"
        self.scrollbar_2 = "#98A1A3"
        self.tooltip_background = "white"
        self.tooltip_foreground = "black"
        self.tooltip_padding = 4
        self.padx = 10
        self.pady = 10
        self.frame_padx = 0
        self.frame_pady = 0
        self.entry_width = 10
        self.entry_width_small = 6
        self.combobox_width = 11
        self.combobox_width_small = 7
        self.border_width = 4
        self.button_width = 8
        self.snippet_header_minus = 1
        self.right_padding = 11

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
