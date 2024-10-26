import tkinter as tk
from tkinter import ttk
from typing import Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class ProgressBar:
    """Progress bar widget with status updates."""
    
    def __init__(self, parent: Optional[tk.Widget] = None, total_steps: int = 100, operation_name: str = ""):
        self.total_steps = total_steps
        self.operation_name = operation_name
        
        if parent is not None:
            # GUI mode
            self.frame = ttk.Frame(parent)
            self.progress = ttk.Progressbar(
                self.frame,
                orient="horizontal",
                length=300,
                mode="determinate",
                maximum=total_steps
            )
            self.status_var = tk.StringVar(value="Ready")
            self.status_label = ttk.Label(self.frame, textvariable=self.status_var)
            self.progress.pack(fill=tk.X, padx=5, pady=2)
            self.status_label.pack(fill=tk.X, padx=5)
        else:
            # CLI mode
            self.frame = None
            self.progress = None
            self.status_var = None
            
    def pack(self, **kwargs):
        """Pack the progress bar frame if in GUI mode."""
        if self.frame:
            self.frame.pack(**kwargs)
        
    def update(self, step: int, status: Optional[str] = None):
        """Update progress bar and status."""
        try:
            if self.progress:
                # GUI mode
                self.progress["value"] = step
                if status:
                    self.status_var.set(status)
                if hasattr(self.frame, 'master'):
                    self.frame.master.update_idletasks()
            else:
                # CLI mode
                percent = (step / self.total_steps) * 100
                logger.info(f"{self.operation_name}: {percent:.0f}% - {status}")
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
    
    def reset(self):
        """Reset progress bar to initial state."""
        if self.progress:
            self.progress["value"] = 0
            self.status_var.set("Ready")
            if hasattr(self.frame, 'master'):
                self.frame.master.update_idletasks()
