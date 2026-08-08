import tkinter as tk
from tkinter import font
import re

class CodeEditor(tk.Text):
    """
    A Tkinter Text widget specifically styled for coding,
    supporting syntax highlighting and various themes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define colors for different elements
        self.colors = {
            "keyword": "#107c10",     # Green
            "string": "#a31511",       # Red/Brownish
            "comment": "#0000ff",      # Blue
            "builtin": "#795e23",      # Olive/Gold
            "bg": "#ffffff",           # White background
            "fg": "#000000"            # Black text
        }

        # Fixed: Changed 'TkFont' to 'Font' as suggested by the interpreter.
        # This is the standard way to define font objects in tkinter.font.
        self.font = font.Font(family="Courier", size=12)
        self.configure(font=self.font, bg=self.colors["bg"], fg=self.colors["fg"])

        # Define tags for highlighting
        self.tag_config("keyword", foreground=self.colors["keyword"], font=self.font)
        self.tag_config("string", foreground=self.colors["string"], font=self.font)
        self.tag_config("comment", foreground=self.colors["comment"], font=self.font)
        self.tag_config("builtin", foreground=self.colors["builtin"], font=self.font)

        # Bind the key release to trigger highlighting as you type
        self.bind("<KeyRelease>", self.apply_highlighting)
        self.bind("<Shift-Tab>", self.apply_highlighting)

    def apply_highlighting(self, event=None):
        """Scans the text and applies tags based on regex patterns."""
        content = self.get("1.0", "end-1c")

        # Clear current highlights to re-apply logic from scratch
        for tag in ["keyword", "string", "comment", "builtin"]:
            self.tag_remove(tag, "1.0", "end")

        # Regex patterns for Python syntax
        patterns = [
            (r'\b(def|class|import|from|as|if|elif|else|while|for|in|try|except|finally|with|pass|None|True|False|and|or|not|lambda|yield)\b', "keyword"),
            (r'(\".*?\"|\'.*?\'|\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\')', "string"),
            (r'(#.*)', "comment"),
            (r'\b(print|int|str|list|dict|set|len|range|input|open)\b', "builtin")
        ]

        for pattern, tag in patterns:
            for match in re.finditer(pattern, content):
                start = f"1.0 + {match.start()}c"
                end = f"1.0 + {match.end()}c"
                self.tag_add(tag, start, end)

    def get_code(self):
        """Return the raw content of the editor."""
        return self.get("1.0", "end-1c")
