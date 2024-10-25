import arcpy
from pathlib import Path
from typing import Optional, Union
from scripts.helpers.logging_utils import get_logger
from scripts.process_mxd import MXDProcessor
from scripts.process_aprx import APRXProcessor

logger = get_logger(__name__)

class FileHandler:
    """Handles processing of both .mxd and .aprx files."""
    
    def __init__(self):
        self.supported_extensions = {'.mxd', '.aprx'}
    
    def validate_file(self, file_path: Union[str, Path]) -> bool:
        """Validates if the file exists and has a supported extension."""
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return False
        if file_path.suffix.lower() not in self.supported_extensions:
            logger.error(f"Unsupported file type: {file_path.suffix}")
            return False
        return True

    def process_file(self, input_path: Union[str, Path], output_path: Union[str, Path], 
                    resolution: int = 300) -> bool:
        """Process a single map file (.mxd or .aprx)."""
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        if not self.validate_file(input_path):
            return False
            
        try:
            if input_path.suffix.lower() == '.mxd':
                processor = MXDProcessor(input_path)
            else:  # .aprx
                processor = APRXProcessor(input_path)
            
            # Process the file
            processor.open_file()
            result = processor.export_to_pdf(output_path, resolution)
            processor.close()
            
            return result is not None
            
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return False

    def process_intersections(self, in_xfmr: str, in_pricond: str, source_gdb: str) -> bool:
        """Process intersections between transformer and primary conductor layers."""
        try:
            # Create Transformer_MCD intersection
            arcpy.Intersect_analysis(
                [in_xfmr, r"\\exelonds\exutilshare\GDVA\PECO\GDB\BaseFeatures.gdb\PECO_MCD_ServiceType"],
                f"{source_gdb}\\Transformer_MCD",
                output_type="POINT"
            )
            logger.info("Created Transformer_MCD intersection")

            # Copy primary conductor
            arcpy.Copy_management(in_pricond, "PriCondSGB_MergeMCD")
            arcpy.Copy_management(in_pricond, "PriCondSGB_MergeMCD_2025")
            logger.info("Copied primary conductor layers")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in process_intersections: {e}")
            return False

    def process_veg(self, in_pricond: str, in_xfmr: str, expression: str, 
                   source_sub: str, source_gdb: str) -> bool:
        """Process vegetation management data."""
        try:
            # Create output names
            out_pricond_sum = f"{source_gdb}\\PriCond_MCD_{source_sub}_Sum"
            out_xfmr_sum = f"{source_gdb}\\XFMR_MCD_{source_sub}_Sum"
            
            # Process primary conductor statistics
            arcpy.Statistics_analysis(
                in_pricond,
                out_pricond_sum,
                "SHAPE_Length SUM",
                "CIRCUIT1;MCD_CODE;MCD_NAME"
            )
            
            # Process transformer statistics
            arcpy.Statistics_analysis(
                in_xfmr,
                out_xfmr_sum,
                "CUSTOMER_COUNT SUM",
                "CIRCUIT1;MCD_CODE;MCD_NAME"
            )
            
            # Add and calculate fields
            self._add_and_calculate_fields(out_pricond_sum, out_xfmr_sum, source_sub)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in process_veg: {e}")
            return False

    def _add_and_calculate_fields(self, pricond_sum: str, xfmr_sum: str, source_sub: str):
        """Helper method to add and calculate fields for vegetation processing."""
        # Add fields to primary conductor summary
        field_definitions = [
            ("Circuit_MCD", "TEXT", 150),
            ("Miles", "DOUBLE"),
            ("SUB", "TEXT", 20)
        ]
        
        for table in [pricond_sum, xfmr_sum]:
            for field_name, field_type, *field_length in field_definitions:
                if not arcpy.ListFields(table, field_name):
                    if field_length:
                        arcpy.AddField_management(table, field_name, field_type, 
                                               field_length=field_length[0])
                    else:
                        arcpy.AddField_management(table, field_name, field_type)
        
        # Calculate fields for primary conductor
        with arcpy.da.UpdateCursor(pricond_sum, 
            ['Circuit_MCD', 'CIRCUIT1', 'MCD_NAME', 'Miles', 'SUM_SHAPE_Length', 'SUB']) as cursor:
            for row in cursor:
                row[0] = f"{row[1]}_{row[2]}"  # Circuit_MCD
                row[3] = round(row[4] / 5280, 2)  # Miles
                row[5] = source_sub  # SUB
                cursor.updateRow(row)
        
        # Calculate fields for transformer
        with arcpy.da.UpdateCursor(xfmr_sum, 
            ['Circuit_MCD', 'CIRCUIT1', 'MCD_NAME', 'SUB']) as cursor:
            for row in cursor:
                row[0] = f"{row[1]}_{row[2]}"  # Circuit_MCD
                row[3] = source_sub  # SUB
                cursor.updateRow(row)
