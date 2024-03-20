# Modules
from .theme import Theme


class DefaultTheme(Theme):
    def __init__(self) -> None:
        self.width = 784
        self.height = 752

        self.font_family = "sans"
        self.font = (self.font_family, 14)
        self.font_button = (self.font_family, 12)
        self.font_combobox = (self.font_family, 13)
        self.font_tab = (self.font_family, 12)
        self.font_menu = (self.font_family, 13)
        self.snippet_font_family = "monospace"

        self.syntax_style = "monokai"
        self.dialog_color = "#252933"
        self.background_color = "#212121"
        self.foreground_color = "white"
        self.red_color = "#FF6B6B"
        self.green_color = "#44B3A1"
        self.button_background = "#446CA1"
        self.button_background_alt = "#3D4555"
        self.button_background_hover = "#387ADF"
        self.button_background_hover_alt = "#494D62"
        self.green_button_background_hover = "#944E63"
        self.green_background = "#3F9687"
        self.background_disabled = "#2B303B"
        self.button_foreground = "white"
        self.entry_background = "#2B303B"
        self.entry_foreground = "white"
        self.placeholder_color = "#494D62"
        self.separator_color = "#2B303B"
        self.text_background = "#2B303B"
        self.text_foreground = "white"
        self.combobox_background = "#2B303B"
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
