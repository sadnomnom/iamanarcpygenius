from pathlib import Path
from typing import List, Dict
import pandas as pd
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class TableBuilder:
    """Builds summary tables from processed map files."""
    
    def __init__(self):
        self.data: List[Dict] = []
    
    def add_entry(self, input_file: Path, output_file: Path, status: str, processing_time: float):
        """Adds a processing entry to the table."""
        self.data.append({
            'Input File': str(input_file),
            'Output File': str(output_file),
            'Status': status,
            'Processing Time (s)': processing_time
        })
    
    def build_summary_table(self) -> pd.DataFrame:
        """Creates a summary DataFrame from the collected data."""
        return pd.DataFrame(self.data)
    
    def export_to_csv(self, output_path: Path):
        """Exports the summary table to a CSV file."""
        try:
            df = self.build_summary_table()
            df.to_csv(output_path, index=False)
            logger.info(f"Exported summary table to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to export summary table: {e}")
