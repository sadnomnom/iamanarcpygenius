import arcpy
from pathlib import Path
from typing import Dict, List, Optional
from scripts.helpers.logging_utils import get_logger
from scripts.helpers.config_utils import load_config

logger = get_logger(__name__)

class VegetationProcessor:
    """Handles vegetation management data processing."""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.config = load_config()
        arcpy.env.workspace = str(workspace)
        arcpy.env.overwriteOutput = True
        
    def process_vegetation_data(self, source_sub: str, expression: str) -> bool:
        """Process vegetation management data for a given substation."""
        try:
            # Create feature layers
            in_xfmr_lyr = arcpy.MakeFeatureLayer_management(
                "XFMR_MCD",
                f"XFMR_MCD_{source_sub}",
                expression
            )
            
            in_pricond_lyr = arcpy.MakeFeatureLayer_management(
                "PriCond_MCD",
                f"PriCond_MCD_{source_sub}",
                expression
            )
            
            # Process statistics
            self._process_statistics(in_pricond_lyr, in_xfmr_lyr, source_sub)
            
            # Update fields
            self._update_fields(source_sub)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing vegetation data: {e}")
            return False
    
    def _process_statistics(self, pricond_lyr: str, xfmr_lyr: str, source_sub: str):
        """Process statistics for primary conductor and transformer layers."""
        # Process primary conductor statistics
        arcpy.Statistics_analysis(
            pricond_lyr,
            f"PriCond_{source_sub}_MCD_Sum",
            [["SHAPE_Length", "SUM"]],
            ["CIRCUIT1", "MCD_CODE", "MCD_NAME"]
        )
        
        # Process transformer statistics
        arcpy.Statistics_analysis(
            xfmr_lyr,
            f"XFMR_{source_sub}_MCD_Sum",
            [["CUSTOMER_COUNT", "SUM"]],
            ["CIRCUIT1", "MCD_CODE", "MCD_NAME"]
        )
    
    def _update_fields(self, source_sub: str):
        """Update fields with calculated values."""
        pricond_sum = f"PriCond_{source_sub}_MCD_Sum"
        xfmr_sum = f"XFMR_{source_sub}_MCD_Sum"
        
        # Add fields if they don't exist
        field_definitions = [
            ("Circuit_MCD", "TEXT", 150),
            ("Miles", "DOUBLE"),
            ("SUB", "TEXT", 20)
        ]
        
        for table in [pricond_sum, xfmr_sum]:
            for field_name, field_type, field_length in field_definitions:
                if not arcpy.ListFields(table, field_name):
                    arcpy.AddField_management(table, field_name, field_type, 
                                           field_length=field_length)
        
        # Update primary conductor fields
        with arcpy.da.UpdateCursor(pricond_sum, 
            ['Circuit_MCD', 'CIRCUIT1', 'MCD_NAME', 'Miles', 'SUM_SHAPE_Length', 'SUB']) as cursor:
            for row in cursor:
                row[0] = f"{row[1]}_{row[2]}"  # Circuit_MCD
                row[3] = round(row[4] / 5280, 2)  # Convert to miles
                row[5] = source_sub
                cursor.updateRow(row)
        
        # Update transformer fields
        with arcpy.da.UpdateCursor(xfmr_sum, 
            ['Circuit_MCD', 'CIRCUIT1', 'MCD_NAME', 'SUB']) as cursor:
            for row in cursor:
                row[0] = f"{row[1]}_{row[2]}"
                row[3] = source_sub
                cursor.updateRow(row)
