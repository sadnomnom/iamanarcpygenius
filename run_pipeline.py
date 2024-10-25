import click
from pathlib import Path
from scripts.file_handler import FileHandler
from scripts.table_builder import TableBuilder
from scripts.helpers.logging_utils import setup_file_logger
from scripts.helpers.config_utils import load_config
from config.fixed_paths import (
    MXD_INPUT_DIR,
    APRX_INPUT_DIR,
    PDF_OUTPUT_DIR,
    LOGS_DIR,
    ensure_directories
)

@click.command()
@click.option('--input-dir', type=click.Path(exists=True), help='Input directory containing map files')
@click.option('--output-dir', type=click.Path(), help='Output directory for PDFs')
@click.option('--resolution', default=300, help='PDF export resolution (DPI)')
def main(input_dir, output_dir, resolution):
    """Main entry point for the processing pipeline."""
    # Ensure directories exist
    ensure_directories()
    
    # Setup logging
    logger = setup_file_logger("pipeline", LOGS_DIR)
    logger.info("Starting processing pipeline")
    
    # Initialize handlers
    file_handler = FileHandler()
    table_builder = TableBuilder()
    
    # Load configuration
    config = load_config()
    
    # Set up directories
    input_dir = Path(input_dir) if input_dir else MXD_INPUT_DIR
    output_dir = Path(output_dir) if output_dir else PDF_OUTPUT_DIR
    
    # Process files
    for input_path in input_dir.glob('*.*'):
        if file_handler.validate_file(input_path):
            output_path = output_dir / f"{input_path.stem}.pdf"
            success = file_handler.process_file(input_path, output_path, resolution)
            status = "Success" if success else "Failed"
            logger.info(f"Processed {input_path}: {status}")
    
    logger.info("Pipeline completed")

if __name__ == "__main__":
    main()
