import tkinter as tk
from tkinter import ttk
from editor_widget import CodeEditor
from file_manager import FileManager
from execution_engine import ExecutionEngine

class IDEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Python IDE")
        self.geometry("1000x700")

        # Configuration
        self.current_file = None

        # Create main layout containers
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        # Side Panes (File Manager)
        self.sidebar = tk.Frame(self.main_container, width=250, bg="#f0f0f0")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # The "File Manager" widget
        self.file_tree = FileManager(self.sidebar)
        self.file_tree.pack(fill="both", expand=True)
        self.file_tree.populate_tree(".") 
        
        # Bind the selection to a local function
        self.file_tree.bind("<Button-1>", self.on_file_select)

        # Right side container (Editor + Output)
        self.editor_container = tk.Frame(self.main_container)
        self.editor_container.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # The Code Editor widget
        self.editor = CodeEditor(self.editor_container)
        self.editor.pack(fill="both", expand=True)

        # Bottom Console (Output area)
        self.console = tk.Text(self.editor_container, height=10, bg="#1e1e1e", fg="white")
        self.console.pack(fill="x", pady=(5, 0))
        self.console.insert("1.0", "--- Terminal Output ---")

        # Initialize the backend engine
        self.engine = ExecutionEngine(self.on_output)

    def on_file_select(self, event):
        """Update editor when user clicks a file in the sidebar."""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            path = self.file_tree.item(item, "values")[0]
            
            if path:
                self.current_file = path
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert("1.0", content)
                    self.editor.apply_highlighting()
                except Exception as e:
                    self.console.insert(tk.END, f"Error opening file: {str(e)}")

    def on_output(self, text):
        """Callback from execution engine to display in the console."""
        self.console.insert(tk.END, text)
        self.console.see(tk.END)

    def execute_current_file(self):
        if self.current_file:
            self.console.delete("1.0", tk.END) # Clear console
            self.engine.run(self.current_file)
        else:
            self.console.insert(tk.END, "Error: No file selected.")

    def setup_toolbar(self):
        # This would be used if we wanted a permanent top toolbar
        pass

if __name__ == "__main__":
    app = IDEApp()
    # Adding a run button to the UI for easy access
    toolbar = tk.Frame(app)
    toolbar.pack(side="top", fill="x")
    run_btn = tk.Button(toolbar, text="▶ Run Code", command=app.execute_current_file)
    run_btn.pack(pady=5)
    
    app.mainloop()
