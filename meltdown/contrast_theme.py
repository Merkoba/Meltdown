# Modules
from .theme import Theme


class ContrastTheme(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.background_color = "black"
        self.foreground_color = "white"

        self.output_background = "black"
        self.output_foreground = "white"

        self.entry_background = "black"
        self.entry_foreground = "white"
        self.entry_placeholder_color = "#494D62"
        self.entry_insert = "white"
        self.entry_border_width = 1

        self.entry_background_dialog = "black"
        self.entry_foreground_dialog = "white"
        self.entry_insert_dialog = "white"
        self.entry_selection_background_dialog = "white"
        self.entry_selection_foreground_dialog = "black"
        self.entry_border_width_dialog = 1

        self.combobox_background = "black"
        self.combobox_foreground = "white"
        self.combobox_border_width = 1

        self.button_background = "#1ae6e6"
        self.button_foreground = "black"
        self.button_hover_background = "#1ae6e6"

        self.button_alt_background = "#3fbebe"
        self.button_alt_hover_background = "#38f1f1"

        self.button_highlight_background = "#ffff00"
        self.button_highlight_hover_background = "#ffff00"

        self.button_active_background = "#ffff00"
        self.button_active_hover_background = "#ffff00"

        self.button_disabled_background = "#2B303B"

        self.tab_normal_background = "black"
        self.tab_normal_foreground = "white"
        self.tab_selected_background = "white"
        self.tab_selected_foreground = "black"
        self.tab_border = "white"
        self.tabs_container_color = "black"

        self.system_normal = "#1ae6e6"
        self.system_heavy = "#FF6B6B"

        self.dialog_background = "black"
        self.dialog_foreground = "white"
        self.dialog_border = "white"
        self.dialog_border_width = 3
        self.dialog_top_frame = "black"

        self.snippet_background = "black"
        self.snippet_foreground = "white"

        self.snippet_header_background = "white"
        self.snippet_header_foreground = "black"

        self.snippet_selection_background = "#C3C3C3"
        self.snippet_selection_foreground = "black"

        self.menu_background = "black"
        self.menu_foreground = "white"
        self.menu_hover_background = "white"
        self.menu_hover_foreground = "black"
        self.menu_disabled_background = "black"
        self.menu_disabled_foreground = "white"
        self.menu_border = "white"
        self.menu_canvas_background = "black"

        self.separator_color = "white"

        self.textbox_background = "black"
        self.textbox_foreground = "white"
        self.textbox_insert = "white"
