# Modules
from .theme import Theme


class LightTheme(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.background_color = "white"
        self.foreground_color = "#343434"

        self.output_background = "white"
        self.output_foreground = "#343434"

        self.entry_background = "#C5C5C5"
        self.entry_foreground = "#343434"
        self.entry_placeholder_color = "grey"
        self.entry_insert = "#343434"

        self.name_user = "#343434"
        self.name_ai = "#343434"

        self.tab_normal_background = "#AEAEAE"
        self.tab_normal_foreground = "#343434"
        self.tab_selected_background = "#969696"
        self.tab_selected_foreground = "white"
        self.tabs_container_color = "#BABABA"
        self.tab_border = "#37373D"

        self.button_foreground = "white"
        self.button_background = "#6A7B83"
        self.button_hover_background = "#86A9AD"

        self.button_alt_background = "#B1BBBC"
        self.button_alt_hover_background = "#A8BCBE"

        self.button_highlight_background = "#3F9687"
        self.button_highlight_hover_background = "#5FA086"

        self.button_active_background = "#3F9687"
        self.button_active_hover_background = "#944E63"

        self.button_disabled_background = "#C5C5C5"

        self.combobox_background = "#C5C5C5"
        self.combobox_foreground = "#343434"

        self.snippet_background = "#CBCBCB"
        self.snippet_foreground = "#343434"
        self.snippet_header_background = "#7B7B7B"
        self.snippet_header_foreground = "white"
        self.syntax_style = "sas"

        self.scrollbar_1 = "#BABABA"
        self.scrollbar_2 = "#949494"

        self.menu_hover_background = "#6A7B83"

        self.button_highlight_background = "#44B3A1"

        self.output_selection_background = "#677577"
        self.output_selection_foreground = "white"
        self.snippet_selection_background = "#677577"
        self.snippet_selection_foreground = "white"
        self.entry_selection_background = "#677577"
        self.entry_selection_foreground = "white"

        self.tooltip_background = "#2B303B"
        self.tooltip_foreground = "white"

        self.find_background = "#8799C2"
        self.find_match_background = "#677577"
        self.find_match_foreground = "white"
