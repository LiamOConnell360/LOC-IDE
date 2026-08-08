import sys
import os
# Add current directory to path so modules can find each other (works for both local and testing env)
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import subprocess
import threading
from typing import Callable

class ExecutionEngine:
    """
    Handles the execution of Python script in a separate thread
    to ensure the GUI remains responsive while code is running.
    """
    def __init__(self, output_callback: Callable[[str], None]):
        # This callback will be used to send strings (output) 
        # from the background thread to the UI text widget.
        self.output_callback = output_callback

    def run(self, script_path: str):
        """Runs a python script and streams its output."""
        # Start the execution in a new thread so it doesn't block Tkinter
        threading.Thread(target=self._execute, args=(script_path,), daemon=True).start()

    def _execute(self, script_path: str):
        try:
            # Use sys.executable to ensure we are using the same 
            # interpreter that is running the IDE.
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Read stdout and stderr as they come in
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_callback(output)

            # Capture stderr as well if there's anything left
            _, stderr = process.communicate()
            if stderr:
                self.output_callback(f"\n[STDERR_START]\n{stderr}\n[STDERR_END]")

        except Exception as e:
            self.output_callback(f"Error executing script: {str(e)}")
