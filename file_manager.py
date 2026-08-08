import tkinter as tk
from tkinter import ttk
import os

class FileManager(ttk.Treeview):
    """
    A tree view widget for navigating the project directory structure.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Internal reference to self (the tree widget)
        self.tree = self
        # Ensure standard browse mode is active
        self.configure(selectmode="browse")

    def populate_tree(self, root_dir):
        """
        Populates the tree with files and folders in the given directory.
        Fixes: Uses 'tags' for differentiation instead of ID position
        to prevent "Item already exists" errors from duplicate identifiers.
        """
        # Clear existing entries before repopulating to avoid duplicates on refresh
        self.delete(*self.get_children())

        # Use os.walk to traverse the directory tree
        for root, dirs, files in os.walk(root_dir):
            # Ensure we have a solid base for paths
            current_path = os.path.abspath(root)

            # Process Directories
            for d in dirs:
                full_path = os.path.abspath(os.path.join(root, d))
                # Logic Fix: 'dir_node' is passing as a tag, not an ID.
                # This allows multiple folders to share the same class/style.
                self.insert("", "end", text=d, values=(full_path,), tags=("dir_node",))

            # Process Files
            for f in files:
                full_path = os.path.abspath(os.path.join(root, f))
                # Logic Fix: 'file_node' is used as a tag so each file still
                # receives an automatically generated unique ID from Tkinter.
                self.insert("", "end", text=f, values=(full_path,), tags=("file_node",))

    def on_select(self, event):
        """
        Callback triggered when a user clicks/selects an item in the tree view.
        """
        selection = self.selection()
        if selection:
            item_id = selection[0]
            # Fetch the 'values' tuple (which contains the [full_path])
            values = self.item(item_id, "values")
            if values and len(values) > 0:
                selected_path = values[0]
                print(f"Selected Path: {selected_path}")
