import os

class FileManager:
    def __init__(self, root_path):
        """Initialize the manager with the base directory."""
        self.root_path = root_path

    def read_file(self, path):
        """Read the content of a file safely."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading file at {path}: {e}")

    def save_file(self, path, content):
        """Save the content of a string to a specified file."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file at {path}: {e}")
            return False
