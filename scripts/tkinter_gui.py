import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional, Dict, List
from scripts.map_generator import MapGenerator
from scripts.helpers.config_utils import load_config
from scripts.helpers.logging_utils import get_logger
from scripts.helpers.progress_bar import ProgressBar
import traceback
from scripts.helpers.config_utils import ConfigurationError
from scripts.helpers.config_utils import validate_substation

logger = get_logger(__name__)

class MapProcessorGUI:
    """Main GUI for the map processing application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Map Processing Pipeline")
        self.config = load_config()
        
        # Initialize variables
        self.year_var = tk.StringVar(value=self.config.get('options', {}).get('default_year', '2024'))
        self.resolution_var = tk.StringVar(value='300')
        self.source_sub_var = tk.StringVar()
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Year selection
        year_frame = ttk.LabelFrame(self.root, text="Year Selection", padding=10)
        ttk.Label(year_frame, text="Processing Year:").pack(side=tk.LEFT)
        ttk.Entry(year_frame, textvariable=self.year_var, width=6).pack(side=tk.LEFT, padx=5)
        
        # Source substation selection
        sub_frame = ttk.LabelFrame(self.root, text="Source Substation", padding=10)
        ttk.Label(sub_frame, text="Substation:").pack(side=tk.LEFT)
        ttk.Entry(sub_frame, textvariable=self.source_sub_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # Resolution selection
        res_frame = ttk.LabelFrame(self.root, text="PDF Resolution", padding=10)
        ttk.Label(res_frame, text="DPI:").pack(side=tk.LEFT)
        ttk.Entry(res_frame, textvariable=self.resolution_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(self.root, text="Processing Options", padding=10)
        ttk.Checkbutton(options_frame, text="Process Internal Maps").pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Process External Maps").pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Generate Overview Maps").pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(self.root, padding=10)
        ttk.Button(button_frame, text="Process Maps", command=self.process_maps).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_frame = ttk.Frame(self.root)
        ttk.Label(status_frame, textvariable=self.status_var).pack(fill=tk.X)
        
        # Add progress bar
        self.progress = ProgressBar(self.root)
        
        # Store frames for layout
        self.frames = [year_frame, sub_frame, res_frame, options_frame, 
                      button_frame, self.progress.frame, status_frame]
    
    def _setup_layout(self):
        """Set up the GUI layout."""
        for frame in self.frames:
            frame.pack(fill=tk.X, padx=10, pady=5)
    
    def process_maps(self):
        """Process maps based on user input."""
        try:
            source_sub = self.source_sub_var.get().strip()
            year = self.year_var.get().strip()
            
            config = load_config()
            if not validate_substation(source_sub, config):
                self.show_error("Invalid substation")
                return
            
            workspace = Path(config['paths']['workspace'])
            generator = MapGenerator(workspace)
            
            # Process intersections first
            if not generator.process_intersections():
                raise Exception("Failed to process intersections")
                
            # Then generate maps
            if not generator.generate_maps(source_sub, year):
                raise Exception("Failed to generate maps")
                
            self.show_success("Maps generated successfully!")
            
        except Exception as e:
            logger.error(f"Error in GUI processing: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            self.show_error(f"Error: {str(e)}")
    
    def _validate_inputs(self) -> bool:
        """Validate user inputs."""
        try:
            year = self.year_var.get().strip()
            source_sub = self.source_sub_var.get().strip()
            
            if not year:
                messagebox.showerror("Error", "Please enter a processing year")
                return False
            
            if not source_sub:
                messagebox.showerror("Error", "Please enter a source substation")
                return False
            
            # Validate substation
            if not validate_substation(source_sub, self.config):
                messagebox.showerror(
                    "Error", 
                    f"Invalid substation: {source_sub}\n\n"
                    f"Valid substations: {', '.join(sorted(self.config['substations']))}"
                )
                return False
            
            try:
                resolution = int(self.resolution_var.get())
                if resolution <= 0:
                    raise ValueError("Resolution must be positive")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid resolution (DPI)")
                return False
            
            return True
            
        except ConfigurationError as e:
            messagebox.showerror("Configuration Error", str(e))
            return False
        except Exception as e:
            logger.error(f"Error validating inputs: {e}")
            messagebox.showerror("Error", f"An error occurred while validating inputs: {e}")
            return False
    
    def _get_processing_params(self) -> Dict[str, str]:
        """Get processing parameters from GUI inputs."""
        return {
            'year': self.year_var.get().strip(),
            'source_sub': self.source_sub_var.get().strip(),
            'resolution': int(self.resolution_var.get())
        }
    
    def _handle_error(self, error: Exception):
        """Handle and log errors."""
        error_msg = str(error)
        logger.error(f"Error in GUI processing: {error_msg}")
        logger.error(traceback.format_exc())
        
        self.progress.update(0, "Error occurred")
        self.status_var.set("Error occurred")
        
        messagebox.showerror(
            "Error",
            f"An error occurred during processing:\n\n{error_msg}\n\n"
            "Check the logs for more details."
        )
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main entry point for the GUI."""
    try:
        app = MapProcessorGUI()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start GUI: {e}")
        raise

if __name__ == '__main__':
    main()
