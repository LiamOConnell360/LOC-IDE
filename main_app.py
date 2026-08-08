import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# --- INTEGRATED CONFIGURATION ---
LANGUAGES = {
    "Python": {
        "extensions": [".py"],
        "rules": [
            (r"\b(def|class|import|from|if|elif|else|while|for|return|None|True|False)\b", "keyword"),
            (r"(\"[^\"]*\"|'[^']*')", "string"),
            (r"(#.*)", "comment"),
            (r"(\b(int|float|list|dict|str|bool|None)\b)", "builtin"),
            (r"(\b(def|class)\s+\w+\(.*\))", "type"),
        ]
    },
    "JavaScript": {
        "extensions": [".js", ".ts"],
        "rules": [
            (r"\b(const|let|var|function|if|else|for|while|return)\b", "keyword"),
            (r"(\"[^\"]*\"|'[^']*'|`[^`]*\`)", "string"),
            (r"(\/\/.*|\/\*.*?\*\/)", "comment"),
            (r"(\b(true|false|null|undefined)\b)", "builtin"),
        ]
    },
    "HTML": {
        "extensions": [".html", ".xml"],
        "rules": [
            (r"<!--.*?--\>", "comment"),
            (r"(<[^>]+>)", "tag"),
            (r"(\"[^\"]*\"|'[^']*')", "string")
        ]
    },
    "Java": {
        "extensions": [".java"],
        "rules": [
            (r"\b(public|private|protected|class|static|void|int|double|new|return|if|else|for|while)\b", "keyword"),
            (r"(\"[^\"]*\"|'[^']*')", "string"),
            (r"(\/\/.*|\/\*.*?\*\/)", "comment"),
            (r"(\b(System|String|Integer|Double|Boolean)\b)", "builtin")
        ]
    }
}

# --- INTEGRATED FILE MANAGER ---
class FileManager:
    def __init__(self, root_path):
        self.root_path = root_path
    def get_files(self):
        return [f for f in os.listdir(self.root_path) if os.path.isfile(os.path.join(self.root_path, f))]

# --- CORE APPLICATION ---
class IDEApp:
    def __init__(self):
        self.file_manager = FileManager(root_path=os.getcwd())
        self.current_file_path = None

        try:
            import tkinter as tk
            self.gui_available = True
        except (ImportError, OSError):
            self.gui_available = False

        print("\n" + "="*40)
        print("      CORE SYSTEM INITIALIZED")
        if self.gui_available:
            print("STATUS: Graphical Mode Active")
        else:
            print("STATUS: Terminal-Only Fallback")
        print(f"PATH:   {os.getcwd()}")
        print("="*40)

        if self.gui_available:
            self._run_gui_mode()
        else:
            self._run_terminal_mode()

    def _setup_gui_elements(self):
        import tkinter as tk
        # --- DARK THEME PALETTE ---
        bg_color = "#1e1e1e"      # Primary Background
        status_bar_color = "#333333"
        text_color = "#d4d4d4"    # Main Text Color

        style_map = {
            "keyword": "#cc78c0",      # Pink/Purple
            "string": "#e6db74",        # Yellow
            "comment": "#6a9955",       # Green
            "builtin": "#fd9711",       # Orange
            "type": "#d7ba7d",          # Mustard/Gold
            "preprocessor": "#c586c0",  # Muted Pink
            "tag": "#4ec9b0"            # Teal
        }

        default_font = ("Consolas", 13)
        try:
            tk.Tk().tkdefault_options["_root_font"] = default_font
        except: pass

        self.text_area = tk.Text(self.root, font=default_font, undo=True,
                                  wrap="none", bg=bg_color, fg=text_color,
                                  borderwidth=0, highlightthickness=0)
        self.text_area.pack(expand=True, fill="both")

        for tag, color in style_map.items():
            self.text_area.tag_config(tag, foreground=color)

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=lambda *args: scrollbar.set(*args))

        # --- SINGLE WINDOW FIX ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self._new_file)
        file_menu.add_command(label="Open", command=self._open_file)
        file_menu.add_command(label="Save", command=self._save_file)
        file_menu.add_command(label="Save As", command=self._save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        self.status_bar = tk.Label(self.root, text="System Ready", bd=1,
                                    relief=tk.SUNKEN, anchor=tk.W,
                                    bg=status_bar_color, fg="#cccccc")
        self.status_bar.pack(side="bottom", fill="x")

    def _new_file(self):
        self.current_file_path = None
        self.text_area.delete("1.0", "end")
        self._update_status("New file created.")

    def _open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_file_path = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", content)
            self.apply_highlighting()
            self._update_status(f"Opened: {os.path.basename(file_path)}")

    def _save_file(self):
        if self.current_file_path:
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self._update_status(f"Saved: {os.path.basename(self.current_file_path)}")
        else:
            self._save_as_file()

    def _save_as_file(self):
        path = filedialog.askdirectory()
        if path:
            name = input("Enter filename (e.g., main.py): ").strip()
            full_path = os.path.join(path, name) if name else os.path.join(path, "untitled.txt")
            self.current_file_path = full_path
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self._update_status(f"Saved as: {os.path.basename(full_path)}")

    def apply_highlighting(self):
        try:
            # Define the tags we want to highlight
            tags = ["keyword", "string", "comment", "builtin", "type", "preprocessor", "tag"]
            for tag in tags:
                self.text_area.tag_remove(tag, "1.0", tk.END)

            # Use "1.0" to "end" to capture the entire buffer
            content = self.text_area.get("1.0", "end")

            if len(content.strip()) > 0:
                for lang in LANGUAGES.values():
                    for pattern, tag_name in lang["rules"]:
                        try:
                            for match in re.finditer(pattern, content):
                                # Use 'c' suffix to indicate character count instead of line/column logic
                                start = f"1.0 + {match.start()}c"
                                end = f"1.0 + {match.end()}c"
                                self.text_area.tag_add(tag_name, start, end)
                        except: pass
        except Exception as e:
            pass

    def _run_gui_mode(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.title("Multi-Language IDE")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        self._setup_gui_elements()
        # Update highlighting on key release and paste events
        self.root.bind("<KeyRelease>", lambda e: self.apply_highlighting())
        try:
            self.root.bind("<Paste>", lambda e: self.apply_highlighting())
        except: pass

        self.root.mainloop()

    def _run_terminal_mode(self):
        print("\n" + "="*40)
        print("       CORE ENGINE - ONLINE")
        print("Note: Terminal mode active.")
        print("="*40)

        if sys.stdin.isatty():
            input("Press [Enter] to scan local files...")

        files = self.file_manager.get_files()
        for f in files:
            if not f.startswith("."):
                ext = os.path.splitext(f)[1].lower()
                lang = "Unknown"
                for name, d in LANGUAGES.items():
                    if ext in d["extensions"]:
                        lang = name
                        break
                print(f"FILE: {f[:25].ljust(25)} | TYPE: {lang}")

        if sys.stdin.isatty():
            input("\nProcess complete. Press [Enter] to exit.")

    def _update_status(self, msg):
        if hasattr(self.root, 'status_bar'):
            self.status_bar.config(text=msg)

if __name__ == "__main__":
    app = IDEApp()
