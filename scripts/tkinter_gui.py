import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from scripts.file_handler import FileHandler
from scripts.helpers.config_utils import load_config

class MapProcessorGUI:
    """GUI interface for the map processing pipeline."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Map Processor")
        self.file_handler = FileHandler()
        self.config = load_config()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Sets up the GUI elements."""
        # File selection frame
        file_frame = ttk.LabelFrame(self.root, text="File Selection", padding=10)
        file_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Button(file_frame, text="Select Input File", command=self.select_input_file).grid(row=0, column=0, pady=5)
        ttk.Button(file_frame, text="Select Output Directory", command=self.select_output_dir).grid(row=1, column=0, pady=5)
        
        # Processing options frame
        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(options_frame, text="Resolution (DPI):").grid(row=0, column=0, pady=5)
        self.resolution_var = tk.StringVar(value="300")
        ttk.Entry(options_frame, textvariable=self.resolution_var).grid(row=0, column=1, pady=5)
        
        # Process button
        ttk.Button(self.root, text="Process", command=self.process_file).grid(row=2, column=0, pady=10)
    
    def select_input_file(self):
        """Opens file dialog for input file selection."""
        filetypes = [("Map files", "*.mxd;*.aprx"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path = Path(filename)
    
    def select_output_dir(self):
        """Opens directory dialog for output selection."""
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir = Path(dirname)
    
    def process_file(self):
        """Processes the selected file."""
        if not hasattr(self, 'input_path') or not hasattr(self, 'output_dir'):
            messagebox.showerror("Error", "Please select input file and output directory")
            return
        
        try:
            resolution = int(self.resolution_var.get())
            output_path = self.output_dir / f"{self.input_path.stem}.pdf"
            
            if self.file_handler.process_file(self.input_path, output_path, resolution):
                messagebox.showinfo("Success", "File processed successfully!")
            else:
                messagebox.showerror("Error", "Failed to process file")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid resolution value")
    
    def run(self):
        """Starts the GUI application."""
        self.root.mainloop()
