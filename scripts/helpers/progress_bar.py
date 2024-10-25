import tkinter as tk
from tkinter import ttk
from typing import Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class ProgressBar:
    """Progress bar widget with status updates."""
    
    def __init__(self, parent: tk.Widget, total_steps: int = 100):
        self.parent = parent
        self.total_steps = total_steps
        
        # Create frame
        self.frame = ttk.Frame(parent)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=300,
            mode="determinate",
            maximum=total_steps
        )
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.frame, textvariable=self.status_var)
        
        # Layout
        self.progress.pack(fill=tk.X, padx=5, pady=2)
        self.status_label.pack(fill=tk.X, padx=5)
        
    def pack(self, **kwargs):
        """Pack the progress bar frame."""
        self.frame.pack(**kwargs)
        
    def update(self, step: int, status: Optional[str] = None):
        """Update progress bar and status."""
        try:
            self.progress["value"] = step
            if status:
                self.status_var.set(status)
            self.parent.update_idletasks()
            logger.debug(f"Progress updated: {step}/{self.total_steps} - {status}")
        except Exception as e:
            logger.error(f"Error updating progress bar: {e}")
    
    def reset(self):
        """Reset progress bar to initial state."""
        self.progress["value"] = 0
        self.status_var.set("Ready")
        self.parent.update_idletasks()
