from __future__ import annotations

# Standard
import sys
from tkinter import ttk

# Modules
from .config import config


class Theme:
    def __init__(self) -> None:
        self.width = 780
        self.height = 860

        self.serif_family = "serif"
        self.font_family = "sans-serif"
        self.monospace_family = "monospace"

        self.font_size = 14
        self.font_entry_size = 14
        self.font_menu_size = 13
        self.font_textbox_size = 13
        self.font_combobox_size = 13
        self.font_tab_size = 12
        self.font_tab_highlight_size = 12
        self.font_button_size = 12
        self.font_tooltips_size = 12

        self.user_color = "#87CEEB"
        self.ai_color = "#98FB98"

        self.syntax_style = "monokai"

        self.background_color = "#212121"
        self.foreground_color = "white"

        self.system_normal = "#44B3A1"
        self.system_heavy = "#FF6B6B"

        self.button_background = "#446CA1"
        self.button_foreground = "white"
        self.button_hover_background = "#387ADF"

        self.button_alt_background = "#3D4555"
        self.button_alt_hover_background = "#494D62"

        self.button_highlight_background = "#3F9687"
        self.button_highlight_hover_background = "#5FA086"

        self.button_active_background = "#3F9687"
        self.button_active_hover_background = "#944E63"

        self.button_disabled_background = "#2B303B"

        self.button_padx = 10
        self.button_width = 8

        self.entry_background = "#2B303B"
        self.entry_foreground = "white"
        self.entry_placeholder_color = "#494D62"
        self.entry_insert = "white"
        self.entry_selection_background = "#C3C3C3"
        self.entry_selection_foreground = "black"
        self.entry_width = 10
        self.entry_width_small = 6
        self.entry_border_width = 0

        # Dialog entries use light style (white background, black text)
        self.entry_background_dialog = "white"
        self.entry_foreground_dialog = "black"
        self.entry_insert_dialog = "black"
        self.entry_selection_background_dialog = "#C3C3C3"
        self.entry_selection_foreground_dialog = "black"
        self.entry_border_width_dialog = 0

        self.separator_color = "#2B303B"

        self.output_background = "#2B303B"
        self.output_foreground = "white"

        self.output_selection_background = "#C3C3C3"
        self.output_selection_foreground = "black"

        self.combobox_background = "#2B303B"
        self.combobox_foreground = "white"
        self.combobox_border_width = 0

        self.dialog_background = "white"
        self.dialog_foreground = "black"
        self.dialog_border = "#4cc2af"
        self.dialog_border_width = 4
        self.dialog_top_frame = "#F5F5F5"

        self.snippet_background = "#3D4555"
        self.snippet_foreground = "white"

        self.snippet_header_background = "#A9C3CA"
        self.snippet_header_foreground = "#2B303B"

        self.snippet_selection_background = "#C3C3C3"
        self.snippet_selection_foreground = "black"

        self.smaller_font = 1

        # Unified highlight used by menus/dialogs/hover states
        # Use the same blue as menu hover to ensure visibility and contrast
        self.highlight_background = "#6693C3"
        self.highlight_foreground = "white"

        self.menu_background = "white"
        self.menu_foreground = "black"
        self.menu_hover_background = "#6693C3"
        self.menu_hover_foreground = "white"
        self.menu_disabled_background = "#E0E0E0"
        self.menu_disabled_foreground = "#7a7a7a"
        self.menu_border = "#959595"
        self.menu_border_width = 3
        self.menu_canvas_background = "white"
        self.menu_wrap_length = 480

        self.tab_normal_background = "#2B303B"
        self.tab_normal_foreground = "#C9C9C9"
        self.tab_selected_background = "#494D62"
        self.tab_selected_foreground = "white"
        self.tab_border = "#6A7B83"
        self.tabs_container_color = "#2B303B"
        self.tab_picked_border = "#4cc2af"
        self.tab_border_width = 1
        self.tab_padx = 10
        self.tab_pady = 0

        self.scrollbar_1 = "#333B4B"
        self.scrollbar_2 = "#98A1A3"

        self.scrollbar_dialog_2 = "#949494"
        self.scrollbar_dialog_1 = "#B0B0B0"

        self.tooltip_background = "white"
        self.tooltip_foreground = "black"
        self.tooltip_padding = 4
        self.tooltip_border = "#959595"
        self.tooltip_border_width = 3

        self.padx = 4
        self.pady = 4

        self.frame_padx = 0
        self.frame_pady = 0

        self.combobox_width = 11
        self.combobox_width_small = 7

        self.find_background = "#6A7B83"
        self.find_match_background = "#C3C3C3"
        self.find_match_foreground = "black"
        self.find_entry_width = 12

        self.textbox_background = "white"
        self.textbox_foreground = "black"
        self.textbox_insert = "black"
        self.textbox_border_width = 2
        self.textbox_border_color = "#6a7b83"
        self.textbox_border_focus_color = "#4cc2af"
        self.textbox_width = 38
        self.textbox_height = 7

        self.input_width = 25

        self.effect_color = "#0adeff"

        self.msgbox_width = 34
        self.msgbox_height = 10

    def get_monospace_family(self) -> str:
        if sys.platform == "darwin":
            return "Menlo"

        return self.monospace_family

    def get_serif_family(self) -> str:
        if sys.platform == "darwin":
            return "Times New Roman"

        return self.serif_family

    def get_sans_family(self) -> str:
        if sys.platform == "darwin":
            return "Helvetica"

        return self.font_family

    def get_font_family(self) -> str:
        from .args import args

        if config.font_family == "monospace":
            font = args.font_family_mono or self.get_monospace_family()
        elif config.font_family == "serif":
            font = args.font_family_serif or self.get_serif_family()
        else:
            font = args.font_family_sans or self.get_sans_family()

        return font

    def get_output_font(
        self, smaller: bool = False, underline: bool = False
    ) -> tuple[str, int, str]:
        ff = self.get_font_family()
        size = config.font_size

        if smaller:
            size -= self.smaller_font

        if underline:
            return (ff, size, "underline")

        return (ff, size, "normal")

    def get_snippet_font(self) -> tuple[str, int]:
        from .args import args

        return (args.snippets_font, config.font_size)

    def get_custom_font(
        self, font_family: str = "normal", effects: str = "", size: int | None = None
    ) -> tuple[str, int, str]:
        outfont = self.get_output_font()

        if font_family == "monospace":
            ff = self.get_monospace_family()
        else:
            ff = outfont[0]

        f_size = size if size else outfont[1]
        return (ff, f_size, effects)

    def get_header_size(self, num: int) -> int:
        return config.font_size + (4 - num)

    def get_separator_font(self) -> tuple[str, int]:
        ff = self.get_monospace_family()
        return (ff, config.font_size)

    def font(self, name: str = "font") -> tuple[str, int, str]:
        from .args import args

        diff = args.font_diff
        fam = self.font_family

        if name == "font":
            return (fam, self.font_size + diff, "normal")

        if name == "entry":
            return (fam, self.font_entry_size + diff, "normal")

        if name == "button":
            return (fam, self.font_button_size + diff, "normal")

        if name == "button_highlight":
            return (fam, self.font_button_size + diff, "underline")

        if name == "combobox":
            return (fam, self.font_combobox_size + diff, "normal")

        if name == "tab":
            return (fam, self.font_tab_size + diff, "normal")

        if name == "tab_alt":
            return (fam, self.font_tab_size + diff, "italic")

        if name == "tab_highlight":
            return (fam, self.font_tab_highlight_size + diff, "underline")

        if name == "menu":
            return (fam, self.font_menu_size + diff, "normal")

        if name == "menu_underline":
            return (fam, self.font_menu_size + diff, "underline")

        if name == "tooltips":
            return (fam, self.font_tooltips_size + diff, "normal")

        if name == "textbox":
            return (fam, self.font_textbox_size + diff, "normal")

        return (fam, self.font_size + diff, "normal")

    def setup(self) -> None:
        from .args import args
        from .app import app

        style = ttk.Style()

        abc = args.border_color
        bc = abc if abc else self.background_color
        app.root.configure(background=bc)
        app.main_frame.configure(background=self.background_color)

        # padding=[left, top, right, bottom])

        style.configure("Normal.TCombobox", foreground=self.combobox_foreground)

        style.map(
            "Normal.TCombobox",
            fieldbackground=[("readonly", self.combobox_background)],
            fieldforeground=[("readonly", self.combobox_foreground)],
        )

        style.map(
            "Normal.TCombobox",
            selectbackground=[("readonly", "transparent")],
            selectforeground=[("readonly", self.combobox_foreground)],
        )

        style.layout(
            "Normal.TCombobox",
            [
                (
                    "Combobox.field",
                    {
                        "children": [
                            (
                                "Combobox.padding",
                                {
                                    "children": [
                                        ("Combobox.textarea", {"sticky": "nswe"})
                                    ]
                                },
                            )
                        ]
                    },
                ),
            ],
        )

        style.layout(
            "Disabled.TCombobox",
            [
                (
                    "Combobox.field",
                    {
                        "children": [
                            (
                                "Combobox.padding",
                                {
                                    "children": [
                                        ("Combobox.textarea", {"sticky": "nswe"})
                                    ]
                                },
                            )
                        ]
                    },
                ),
            ],
        )

        style.configure("Normal.TCombobox", borderwidth=self.combobox_border_width)
        style.configure("Normal.TCombobox.Listbox", padding=0)
        style.configure("Normal.TCombobox", padding=[4, 0, 0, 0])
        app.root.option_add("*TCombobox*Listbox.font", ("sans-serif", 13))

        # Ensure visible hover/active highlights in classic Tk widgets used for menus/listboxes.
        # This avoids platform-specific branches by setting option database values globally.
        # Menus (classic Tk "Menu")
        app.root.option_add("*Menu.activeBackground", self.menu_hover_background)
        app.root.option_add("*Menu.activeForeground", self.menu_hover_foreground)

        # Listbox (used by some dropdowns/popups)
        app.root.option_add("*Listbox.selectBackground", self.highlight_background)
        app.root.option_add("*Listbox.selectForeground", self.highlight_foreground)

        # Combobox dropdown Listbox specifically
        app.root.option_add(
            "*TCombobox*Listbox.selectBackground", self.highlight_background
        )

        app.root.option_add(
            "*TCombobox*Listbox.selectForeground", self.highlight_foreground
        )

        # Ensure classic Tk Entry widgets follow our dark entry styling (not white)
        app.root.option_add("*Entry.background", self.entry_background)
        app.root.option_add("*Entry.foreground", self.entry_foreground)
        app.root.option_add("*Entry.insertBackground", self.entry_insert)
        app.root.option_add("*Entry.selectBackground", self.entry_selection_background)
        app.root.option_add("*Entry.selectForeground", self.entry_selection_foreground)
        app.root.option_add("*Entry.relief", "flat")
        app.root.option_add("*Entry.borderWidth", self.entry_border_width)

        # Configure default TEntry style to ensure all TTK entries use dark styling
        style.configure("TEntry", fieldbackground=self.entry_background)
        style.configure("TEntry", foreground=self.entry_foreground)
        style.configure("TEntry", borderwidth=self.entry_border_width)
        style.configure("TEntry", insertcolor=self.entry_insert)

        style.map(
            "TEntry",
            fieldbackground=[
                ("active", self.entry_background),
                ("disabled", self.entry_background),
                ("focus", self.entry_background),
                ("readonly", self.entry_background),
                ("!focus", self.entry_background),
            ],
            foreground=[
                ("active", self.entry_foreground),
                ("disabled", self.entry_foreground),
                ("focus", self.entry_foreground),
                ("readonly", self.entry_foreground),
                ("!focus", self.entry_foreground),
            ],
            readonlybackground=[
                ("!focus", self.entry_background),
                ("focus", self.entry_background),
            ],
        )

        style.map(
            "Disabled.TCombobox",
            fieldbackground=[("readonly", self.combobox_background)],
            fieldforeground=[("readonly", self.combobox_foreground)],
        )

        style.configure("Disabled.TCombobox", padding=[4, 2, 0, 2])
        style.configure("Disabled.TCombobox", borderwidth=self.combobox_border_width)

        # Normal Entry - keep dark background
        style.configure("Normal.TEntry", fieldbackground=self.entry_background)
        style.configure("Normal.TEntry", foreground=self.entry_foreground)
        style.configure("Normal.TEntry", borderwidth=self.entry_border_width)
        style.configure("Normal.TEntry", padding=[4, 0, 0, 0])
        style.configure("Normal.TEntry", insertcolor=self.entry_insert)

        style.configure(
            "Normal.TEntry", selectbackground=self.entry_selection_background
        )

        style.configure(
            "Normal.TEntry", selectforeground=self.entry_selection_foreground
        )

        style.map(
            "Normal.TEntry",
            fieldbackground=[
                ("active", self.entry_background),
                ("disabled", self.entry_background),
                ("focus", self.entry_background),
                ("readonly", self.entry_background),
                ("!focus", self.entry_background),
            ],
            foreground=[
                ("active", self.entry_foreground),
                ("disabled", self.entry_foreground),
                ("focus", self.entry_foreground),
                ("readonly", self.entry_foreground),
                ("!focus", self.entry_foreground),
            ],
            readonlybackground=[
                ("!focus", self.entry_background),
                ("focus", self.entry_background),
            ],
        )

        # Dialog Entry - keep white background
        style.configure("Dialog.TEntry", fieldbackground=self.entry_background_dialog)
        style.configure("Dialog.TEntry", foreground=self.entry_foreground_dialog)
        style.configure("Dialog.TEntry", borderwidth=self.entry_border_width_dialog)
        style.configure("Dialog.TEntry", padding=[4, 0, 0, 0])
        style.configure("Dialog.TEntry", insertcolor=self.entry_insert_dialog)

        style.configure(
            "Dialog.TEntry", selectbackground=self.entry_selection_background_dialog
        )

        style.configure(
            "Dialog.TEntry", selectforeground=self.entry_selection_foreground_dialog
        )

        style.map(
            "Dialog.TEntry",
            fieldbackground=[
                ("active", self.entry_background_dialog),
                ("disabled", self.entry_background_dialog),
                ("focus", self.entry_background_dialog),
                ("readonly", self.entry_background_dialog),
                ("!focus", self.entry_background_dialog),
            ],
            foreground=[
                ("active", self.entry_foreground_dialog),
                ("disabled", self.entry_foreground_dialog),
                ("focus", self.entry_foreground_dialog),
                ("readonly", self.entry_foreground_dialog),
                ("!focus", self.entry_foreground_dialog),
            ],
            readonlybackground=[
                ("!focus", self.entry_background_dialog),
                ("focus", self.entry_background_dialog),
            ],
        )

        style.configure(
            "Normal.Vertical.TScrollbar",
            gripcount=0,
            background=self.scrollbar_2,
            troughcolor=self.scrollbar_1,
            borderwidth=0,
        )

        style.map(
            "Normal.Vertical.TScrollbar",
            background=[("disabled", self.scrollbar_1)],
            troughcolor=[("disabled", self.scrollbar_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Normal.Horizontal.TScrollbar",
            gripcount=0,
            background=self.scrollbar_2,
            troughcolor=self.scrollbar_1,
            borderwidth=0,
        )

        style.map(
            "Normal.Horizontal.TScrollbar",
            background=[("disabled", self.scrollbar_1)],
            troughcolor=[("disabled", self.scrollbar_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Dialog.Vertical.TScrollbar",
            gripcount=0,
            background=self.scrollbar_dialog_2,
            troughcolor=self.scrollbar_dialog_1,
            borderwidth=0,
        )

        style.map(
            "Dialog.Vertical.TScrollbar",
            background=[("disabled", self.scrollbar_dialog_1)],
            troughcolor=[("disabled", self.scrollbar_dialog_1)],
            borderwidth=[("disabled", 0)],
        )

        style.configure(
            "Dialog.Horizontal.TScrollbar",
            gripcount=0,
            background=self.scrollbar_dialog_2,
            troughcolor=self.scrollbar_dialog_1,
            borderwidth=0,
        )

        style.map(
            "Dialog.Horizontal.TScrollbar",
            background=[("disabled", self.scrollbar_dialog_1)],
            troughcolor=[("disabled", self.scrollbar_dialog_1)],
            borderwidth=[("disabled", 0)],
        )

        # macOS-specific fixes for Tk styling issues
        if sys.platform == "darwin":
            # Combobox on macOS needs explicit styling on TCombobox (not just Normal.TCombobox)
            style.configure("TCombobox", fieldbackground=self.combobox_background)
            style.configure("TCombobox", background=self.combobox_background)

            style.map(
                "TCombobox",
                fieldbackground=[
                    ("active", self.combobox_background),
                    ("disabled", self.combobox_background),
                    ("focus", self.combobox_background),
                    ("readonly", self.combobox_background),
                    ("!focus", self.combobox_background),
                ],
                background=[
                    ("active", self.combobox_background),
                    ("disabled", self.combobox_background),
                    ("focus", self.combobox_background),
                    ("readonly", self.combobox_background),
                    ("!focus", self.combobox_background),
                ],
            )
