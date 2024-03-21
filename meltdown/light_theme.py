# Modules
from .theme import Theme


class LightTheme(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.background_color = "white"
        self.foreground_color = "black"
        self.output_background = "#C5C5C5"
        self.output_foreground = "black"
        self.entry_background = "#C5C5C5"
        self.entry_foreground = "black"
        self.entry_placeholder_color = "grey"
        self.name_user = "black"
        self.name_ai = "#0000FF"
        self.tab_selected_background = "grey",
        self.tab_normal_background = "#AEAEAE",
        self.tab_selected_foreground = "white",
        self.tab_normal_foreground = "black",
        self.button_foreground = "white"

        self.button_background = "#6A7B83"
        self.button_hover_background = "#A7BABC"

        self.button_alt_background = "#B1BBBC"
        self.button_alt_hover_background = "#A8BCBE"

        self.button_highlight_hover_background = "#944E63"
        self.button_highlight_background = "#3F9687"

        self.button_disabled_background = "#C5C5C5"

        self.combobox_background = "#C5C5C5"
        self.combobox_foreground = "black"

        self.snippet_background = "#E7E7E7"
        self.snippet_foreground = "black"
        self.snippet_header_background = "#7B7B7B"
        self.snippet_header_foreground = "white"
        self.syntax_style = "sas"

        self.scrollbar_1 = "silver"
        self.scrollbar_2 = "#C5C5C5"