import os
from pathlib import Path

class FileManager:
    """Handles file system navigation, directory tree construction, and content management."""
    def __init__(self, root_path="."):
        self.root_path = Path(root_path).resolve()
        self.tree_data = {}

    def read_file(self, file_path):
        """Reads the content of a file and returns it as a string."""
        try:
            # Convert to path object if it's a string for consistent handling
            path = Path(file_path)
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def save_file(self, file_path, content):
        """Saves the provided string content to the given file path."""
        try:
            path = Path(file_path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file {file_path}: {e}")
            return False

    def get_project_structure(self):
        """Builds a dictionary representing the folder structure."""
        # Exclude internal folders like .git, __pycache__, etc.
        ignored_dirs = {'.git', '__pycache__', '.venv', 'env', '.vscode'}

        def walk(path):
            items = []
            for item in sorted(os.listdir(str(path))):
                # Skip hidden files/folders or those in ignore list
                if item.startswith('.') or item in ignored_dirs:
                    continue

                full_path = path / item
                if full_path.is_dir():
                    items.append((item, True))
                else:
                    items.append((item, False))
            return items

        # Simple representation for a treeview logic
        # Return the list instead of just the root to allow iterative building if needed
        return walk(self.root_path)

    def get_files(self):
        """Returns all files in the directory for search/indexing."""
        all_files = []
        for root, dirs, files in os.walk(str(self.root_path)):
            # Filter out ignored ones from walk
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'env'}]
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files

    def get_relative_path(self, absolute_path):
        """Converts an absolute path to a relative path from the root."""
        try:
            return os.path.relpath(absolute_path, self.root_path)
        except ValueError:
            return str(absolute_path)

    def is_file_in_project(self, file_path):
        """Checks if a path inside the project root."""
        p = Path(file_path).resolve()
        return str(self.root_path) in str(p)
