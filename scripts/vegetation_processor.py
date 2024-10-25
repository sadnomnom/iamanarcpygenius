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
            logger.info(f"Processing vegetation data for {source_sub}")
            logger.debug(f"Using workspace: {self.workspace}")
            logger.debug(f"SQL Expression: {expression}")
            
            # Validate workspace
            if not self.workspace.exists():
                logger.error(f"Workspace does not exist: {self.workspace}")
                return False
                
            # Set workspace
            arcpy.env.workspace = str(self.workspace)
            
            # Create feature layers
            logger.info("Creating feature layers...")
            xfmr_layer = f"XFMR_MCD_{source_sub}"
            pricond_layer = f"PriCond_MCD_{source_sub}"
            
            try:
                in_xfmr_lyr = arcpy.MakeFeatureLayer_management(
                    "XFMR_MCD",
                    xfmr_layer,
                    expression
                )
                
                in_pricond_lyr = arcpy.MakeFeatureLayer_management(
                    "PriCond_MCD",
                    pricond_layer,
                    expression
                )
            except arcpy.ExecuteError:
                logger.error(f"Failed to create feature layers: {arcpy.GetMessages(2)}")
                return False
                
            # Process intersections
            logger.info("Processing intersections...")
            if not self.file_handler.process_intersections(
                xfmr_layer, 
                pricond_layer, 
                str(self.workspace)
            ):
                logger.error("Failed to process intersections")
                return False
                
            # Process statistics
            logger.info("Processing statistics...")
            self._process_statistics(in_pricond_lyr, in_xfmr_lyr, source_sub)
            
            # Update fields
            logger.info("Updating fields...")
            self._update_fields(source_sub)
            
            logger.info(f"Successfully processed vegetation data for {source_sub}")
            return True
                
        except Exception as e:
            logger.error(f"Error processing vegetation data: {e}")
            logger.error(f"Error details: {type(e).__name__}")
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
