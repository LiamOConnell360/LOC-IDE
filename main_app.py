import tkinter as tk
from tkinter import messagebox, filedialog
import os
import re
from file_manager import FileManager

# Configuration for colors and syntax rules
COLORS = {
    "keyword": "#1a73e8",     # Blue
    "string": "#009639",      # Green
    "comment": "#8e8e8e",     # Grey
    "builtin": "#9333ea",      # Purple (print, int, list, etc.)
}

# Regex patterns for Python syntax
RULES = [
    (r'\b(def|class|if|elif|else|while|for|import|from|as|try|except|finally|with|lambda|return|pass|break|continue|None|True|False)\b', "keyword"),
    (r'(\".*?\"|\'.*?\')', "string"),
    (r'(\#.*)', "comment"),
    (r'\b(print|int|float|list|dict|set|range|len|type|str|bool|input)\b', "builtin")
]

class IDEApp:
    def __init__(self):
        # Setup main window
        self.root = tk.Tk()
        self.root.title("Python IDE - Editor")
        self.root.geometry("1000x700")

        # Initialize File Manager
        self.file_manager = FileManager(root_path=os.getcwd())

        self.current_file_path = None

        # UI Setup
        self._setup_menu()
        self._setup_ui()
        self._update_status("Ready")

        self.root.mainloop()

    def _set_styles(self):
        """Configures the color tags for syntax highlighting."""
        self.text_area.tag_config("keyword", foreground=COLORS["keyword"], font=("Consolas", 12, "bold"))
        self.text_area.tag_config("string", foreground=COLORS["string"])
        self.text_area.tag_config("comment", foreground=COLORS["comment"])
        self.text_area.tag_config("builtin", foreground=COLORS["builtin"])

    def apply_highlighting(self):
        """Scans the text and applies styles based on predefined rules."""
        # Reset all tags first
        for tag in ["keyword", "string", "comment", "builtin"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)

        content = self.text_area.get("1.0", tk.END)

        # Use a simpler overlapping scan to apply tags safely
        for pattern, tag in RULES:
            for match in re.finditer(pattern, content):
                start = f"1.0 + {match.start()}c"
                end = f"1.0 + {match.end()}c"
                self.text_area.tag_add(tag, start, end)

    def _setup_menu(self):
        """Creates the top navigation menu."""
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # FIX: Changed add_cascade_submenu to add_cascade for cross-platform reliability
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: None)
        edit_menu.add_command(label="Redo", command=lambda: None)

        # FIX: Changed add_cascade_submenu to add_cascade for cross-platform reliability
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    def _setup_ui(self):
        """Builds the main editing area and status bar."""
        # Main text editor widget
        self.text_area = tk.Text(self.root, font=("Consolas", 12), wrap="none")
        self.text_area.pack(expand=True, fill="both", side="top")

        # Style Configuration
        self._set_styles()

        # Scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=lambda *args: scrollbar.set(*args))

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side="bottom", fill="x")

    def _update_status(self, message):
        self.status_bar.config(text=message)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file_path = None
        self._update_status("New File - Untitled")
        self.apply_highlighting()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*"))
        )
        if file_path:
            self.current_file_path = file_path
            content = self.file_manager.read_file(file_path)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, content)
            # Trigger highlighting immediately after loading the file
            self.apply_highlighting()
            self._update_status(f"Opened: {os.path.basename(file_path)}")

    def save_file(self):
        if self.current_file_path:
            self.file_manager.save_file(self.current_file_path, self.text_area.get(1.0, tk.END))
            self._update_status("File Saved")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".py")
            if file_path:
                self.current_file_path = file_path
                self.file_manager.save_file(self.current_file_path, self.text_area.get(1.0, tk.END))
                self._update_status("File Saved")

if __name__ == "__main__":
    app = IDEApp()
