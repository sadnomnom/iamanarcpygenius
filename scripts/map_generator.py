import arcpy
from pathlib import Path
from typing import Dict, List, Optional
from scripts.helpers.logging_utils import get_logger
from scripts.file_handler import FileHandler
from scripts.vegetation_processor import VegetationProcessor
import traceback
from scripts.helpers.config_utils import load_config, ConfigurationError, validate_substation

logger = get_logger(__name__)

class MapGenerator:
    """Handles the complete map generation pipeline."""
    
    def __init__(self, workspace: Path):
        """Initialize the map generator with workspace path."""
        try:
            self.workspace = workspace
            self.config = load_config()
            self.file_handler = FileHandler()
            self.veg_processor = VegetationProcessor(workspace)
            arcpy.env.workspace = str(workspace)
            arcpy.env.overwriteOutput = True
            logger.info(f"Initialized MapGenerator with workspace: {self.workspace}")
            
        except Exception as e:
            logger.error(f"Failed to initialize MapGenerator: {e}")
            raise
    
    def generate_maps(self, source_sub: str, year: str) -> bool:
        """Generate all maps for a given substation with detailed logging."""
        logger.info(f"Starting map generation for {source_sub} (year: {year})")
        progress = ProgressTracker(total_steps=100, operation_name="Map Generation")
        
        try:
            # Process vegetation data (30%)
            progress.update(10, "Building SQL expression...")
            expression = self._build_expression(source_sub)
            logger.debug(f"SQL Expression: {expression}")
            
            progress.update(20, "Processing vegetation data...")
            if not self.veg_processor.process_vegetation_data(source_sub, expression):
                logger.error("Vegetation data processing failed")
                return False
            
            # Process maps (70%)
            map_types = ['Internal', 'External', 'InternalOverview', 'ExternalOverview']
            maps_per_type = 70 / len(map_types)
            
            for i, map_type in enumerate(map_types):
                current_progress = 30 + (i * maps_per_type)
                progress.update(current_progress, f"Processing {map_type} map...")
                
                if not self._process_map(source_sub, map_type, year):
                    logger.error(f"Failed to process {map_type} map")
                    return False
                    
                progress.update(current_progress + maps_per_type - 1, 
                              f"Completed {map_type} map")
            
            progress.complete(f"Map generation completed successfully for {source_sub}")
            return True
            
        except Exception as e:
            logger.error(f"Error in map generation pipeline: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def _build_expression(self, source_sub: str) -> str:
        """Build SQL expression for feature selection."""
        circuits = self._get_circuits(source_sub)
        return f"ORIENTATION <> 'UNDERGROUND CABLE' and CIRCUIT1 in ({','.join(repr(c) for c in circuits)})"
    
    def _get_circuits(self, source_sub: str) -> List[str]:
        """Get list of circuits for a substation."""
        circuits = []
        table = f"{self.workspace}/PriCond_MCD_{source_sub}_Sum"
        with arcpy.da.SearchCursor(table, ["CIRCUIT1"]) as cursor:
            for row in cursor:
                if row[0] not in circuits:
                    circuits.append(row[0])
        return circuits
    
    def _process_map(self, source_sub: str, map_type: str, year: str) -> bool:
        """Process a single map type."""
        try:
            template_path = self._get_template_path(map_type, year)
            output_path = self._get_output_path(source_sub, map_type, year)
            
            # Process the map
            return self.file_handler.process_file(
                template_path,
                output_path,
                resolution=300
            )
            
        except Exception as e:
            logger.error(f"Error processing {map_type} map: {e}")
            return False
    
    def _get_template_path(self, map_type: str, year: str) -> Path:
        """Get the template path for a map type."""
        template_dir = self.workspace.parent / "MXD" / year
        return template_dir / f"Template{map_type}_{year}_11x17.mxd"
    
    def _get_output_path(self, source_sub: str, map_type: str, year: str) -> Path:
        """Get the output path for a map."""
        output_dir = self.workspace.parent / "MXD" / year / "Export" / source_sub
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{source_sub}_{map_type}_{year}_11x17.pdf"

    def process_intersections(self) -> bool:
        """Process intersections for the workspace."""
        try:
            config = self.config['paths']['source_data']
            
            # Check if files are locked
            if arcpy.TestSchemaLock(config['xfmr']):
                logger.warning(f"Source file is locked: {config['xfmr']}")
                return False
            
            # Process with retry logic for concurrent access
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return self.file_handler.process_intersections(
                        config['xfmr'],
                        config['pricond'],
                        str(self.workspace)
                    )
                except arcpy.ExecuteError as e:
                    if "ERROR 000464" in str(e):  # Cannot acquire lock
                        if attempt < max_retries - 1:
                            logger.info("File locked, retrying...")
                            continue
                    raise
        except Exception as e:
            logger.error(f"Failed to process intersections: {e}")
            return False
