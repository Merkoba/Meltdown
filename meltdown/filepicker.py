from __future__ import annotations

# Standard
from typing import Any
import tkinter as tk
from tkinter import ttk
from pathlib import Path


class FilePicker:
    @staticmethod
    def create(title: str, initial_dir: str | Path | None) -> str:
        from .app import app
        from .tooltips import ToolTip

        if initial_dir:
            initdir = Path(initial_dir)
        else:
            initdir = None

        ToolTip.hide_all()
        browser = FilePicker(app.root, title=title, initial_dir=initdir)
        return str(browser.show() or "")

    def __init__(
        self, parent: Any, title: str = "Select File", initial_dir: Path | None = None
    ) -> None:
        self.result = None
        self.selected_path = str(initial_dir or Path("~").expanduser())
        self.width = 600
        self.height = 600

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{self.width}x{self.height}")
        self.dialog.minsize(self.width, self.height)
        self.dialog.grab_set()  # Make dialog modal
        self.dialog.transient(parent)

        # Center the dialog on the parent window, not the entire screen
        self.dialog.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate center position relative to parent
        x = parent_x + (parent_width // 2) - (self.width // 2)
        y = parent_y + (parent_height // 2) - (self.height // 2)

        # Ensure the dialog stays within screen bounds
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()

        x = max(0, min(x, screen_width - self.width))
        y = max(0, min(y, screen_height - self.height))

        self.dialog.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Track last key pressed for cycling
        self.last_key = None
        self.last_key_time = 0.0
        self.current_match_index = -1

        self.setup_ui()
        self.populate_tree(self.selected_path)

        # Set focus to tree after everything is set up
        self.tree.focus_set()

    def setup_ui(self) -> None:
        # Path display
        path_frame = ttk.Frame(self.dialog)
        path_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(path_frame, text="Path:").pack(side="left")
        self.path_var = tk.StringVar(value=self.selected_path)
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.path_entry.bind("<Return>", self.on_path_entry_change)

        # Directory tree
        tree_frame = ttk.Frame(self.dialog)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, show="tree")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind events
        self.tree.bind("<Button-1>", self.on_single_click)
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        self.tree.bind("<KeyPress>", self.on_key_press)
        self.tree.bind("<Return>", self.on_double_click)
        self.tree.bind("<BackSpace>", self.on_backspace)

        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(
            side="right", padx=(5, 0)
        )

        ttk.Button(button_frame, text="Close", command=self.cancel_clicked).pack(
            side="right"
        )

    def populate_tree(self, path: str) -> None:
        # Clear existing items
        for citem in self.tree.get_children():
            self.tree.delete(citem)

        self.last_key = None
        self.current_match_index = -1

        ppath = Path(path)

        try:
            parent_dir = ppath.parent

            if parent_dir != ppath:  # Not root directory
                self.tree.insert(
                    "", "end", values=(parent_dir,), text="📁 ..", tags=("parent",)
                )

            # List directories in current path
            items = []

            for item in ppath.iterdir():
                item_path = ppath / item
                s_item = item.name

                if Path(item_path).is_dir():
                    # Show hidden directories but mark them differently
                    if s_item.startswith("."):
                        items.append((s_item, item_path, "🔒"))  # Hidden folder icon
                    else:
                        items.append((s_item, item_path, "📁"))  # Regular folder icon
                elif s_item.startswith("."):
                    items.append((s_item, item_path, "🔒"))  # Hidden file icon
                else:
                    items.append((s_item, item_path, "📑"))  # Regular file icon

            # Sort items (hidden folders first, then regular)
            items.sort(key=lambda x: (not x[0].startswith("."), x[0].lower()))

            # Add directories to tree
            for item_name, item_path, icon in items:
                self.tree.insert(
                    "", "end", values=(item_path,), text=f"{icon} {item_name}"
                )

        except PermissionError:
            self.tree.insert("", "end", text="❌ Permission denied")
        except Exception as e:
            self.tree.insert("", "end", text=f"❌ Error: {e}")

        children = self.tree.get_children()

        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            values = self.tree.item(first_item, "values")

            if values:
                self.selected_path = values[0]
                self.path_var.set(self.selected_path)

    def on_single_click(self, event: Any) -> None:
        # Get the item that was clicked
        item = self.tree.identify("item", event.x, event.y)  # type: ignore

        if item:
            # Select the item
            self.tree.selection_set(item)
            values = self.tree.item(item, "values")

            if values:
                self.selected_path = values[0]
                self.path_var.set(self.selected_path)

    def on_double_click(self, event: Any) -> None:
        item = None

        if getattr(event, "keysym", "") == "Return":
            item = self.tree.focus()
        else:
            item = self.tree.identify("item", event.x, event.y)  # type: ignore

        if item:
            self.tree.selection_set(item)
            values = self.tree.item(item, "values")

            if values:
                new_path = values[0]

                if Path(new_path).is_dir():
                    self.selected_path = new_path
                    self.path_var.set(self.selected_path)
                    self.populate_tree(new_path)
                else:
                    self.result = new_path
                    self.dialog.destroy()

    def ok_clicked(self) -> None:
        self.result = self.selected_path
        self.dialog.destroy()

    def cancel_clicked(self) -> None:
        self.result = None
        self.dialog.destroy()

    def show(self) -> Any | None:
        self.dialog.wait_window()
        return self.result

    def on_path_entry_change(self, event: Any) -> None:
        new_path = self.path_var.get()

        if Path(new_path).is_dir():
            self.selected_path = new_path
            self.populate_tree(new_path)
        else:
            # Maybe show an error or just revert to the last valid path
            self.path_var.set(self.selected_path)

    def on_key_press(self, event: Any) -> None:
        import time

        char = event.char.lower()

        if not char.isalnum():
            return

        current_time = time.time()

        # Reset cycling if different key or timeout (1 second)
        if char != self.last_key or (current_time - self.last_key_time) > 1.0:
            self.last_key = char
            self.current_match_index = -1

        self.last_key_time = current_time

        # Find all matching items
        matching_items = []

        for item_id in self.tree.get_children():
            item_text = self.tree.item(item_id, "text")

            # Extract the name from "📁 name" or "🔒 name"
            if " " in item_text:
                name = item_text.split(" ", 1)[1]

                if name.lower().startswith(char):
                    matching_items.append(item_id)

        if not matching_items:
            return

        # Cycle through matches
        self.current_match_index = (self.current_match_index + 1) % len(matching_items)
        selected_item = matching_items[self.current_match_index]
        self.tree.selection_set(selected_item)
        self.tree.focus(selected_item)
        self.tree.see(selected_item)

        # Update selected path for consistency (but not for "..")
        item_text = self.tree.item(selected_item, "text")

        if ".." not in item_text:
            values = self.tree.item(selected_item, "values")

            if values:
                self.selected_path = values[0]
                self.path_var.set(self.selected_path)

    def on_backspace(self, event: Any) -> None:
        parent_path = None

        for child_id in self.tree.get_children():
            item_tags = self.tree.item(child_id, "tags")

            if "parent" in item_tags:
                values = self.tree.item(child_id, "values")

                if values:
                    parent_path = values[0]

                break

        if parent_path:
            self.selected_path = parent_path
            self.path_var.set(self.selected_path)
            self.populate_tree(self.selected_path)
