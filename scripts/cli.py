import click
from pathlib import Path
from scripts.file_handler import FileHandler
from scripts.helpers.config_utils import (
    load_config, 
    validate_substation, 
    ConfigurationError
)
from scripts.helpers.logging_utils import get_logger
import sys
from scripts.helpers.verify_setup import run_verification
from scripts.process_mxd import MXDProcessor
from scripts.process_aprx import APRXProcessor
from scripts.map_generator import MapGenerator

logger = get_logger(__name__)

@click.group()
def cli():
    """Command line interface for map processing pipeline."""
    pass

@cli.command()
def verify():
    """Verify the environment setup."""
    success = run_verification()
    if not success:
        click.echo("Environment verification failed. Check the logs for details.", err=True)
        sys.exit(1)
    click.echo("Environment verification successful!")

@cli.command()
def process_intersections():
    """Process intersections to create base files."""
    from scripts.file_handler import process_intersections
    try:
        process_intersections()
        click.echo("Successfully processed intersections")
    except Exception as e:
        logger.error(f"Failed to process intersections: {e}")
        click.echo("Failed to process intersections. Check logs for details.", err=True)
        sys.exit(1)

@cli.command()
def process_veg():
    """Process vegetation management data."""
    from scripts.file_handler import process_veg
    try:
        process_veg()
        click.echo("Successfully processed vegetation management data")
    except Exception as e:
        logger.error(f"Failed to process vegetation data: {e}")
        click.echo("Failed to process vegetation data. Check logs for details.", err=True)
        sys.exit(1)

@cli.command()
def process_maps():
    """Process maps and generate PDFs."""
    from scripts.process_mxd import process_maps
    try:
        process_maps()
        click.echo("Successfully processed maps and generated PDFs")
    except Exception as e:
        logger.error(f"Failed to process maps: {e}")
        click.echo("Failed to process maps. Check logs for details.", err=True)
        sys.exit(1)

@cli.command()
@click.argument('source_sub')
@click.option('--year', '-y', default='2024', help='Processing year')
@click.option('--resolution', '-r', default=300, help='PDF export resolution (DPI)')
def generate_maps(source_sub: str, year: str, resolution: int):
    """Generate maps for a source substation."""
    try:
        config = load_config()
        
        # Validate substation
        if not validate_substation(source_sub, config):
            valid_subs = ', '.join(sorted(config['substations']))
            click.echo(f"Error: Invalid substation. Valid options are: {valid_subs}", err=True)
            sys.exit(1)
        
        # Get workspace from config
        workspace = Path(config['paths']['workspace'])
        if not workspace.exists():
            click.echo(f"Error: Workspace directory does not exist: {workspace}", err=True)
            sys.exit(1)
            
        generator = MapGenerator(workspace)
        
        if generator.generate_maps(source_sub, year):
            click.echo(f"Successfully generated maps for {source_sub}")
        else:
            click.echo(f"Failed to generate maps for {source_sub}", err=True)
            sys.exit(1)
            
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to generate maps: {e}")
        click.echo(f"Error generating maps: {e}", err=True)
        sys.exit(1)

@cli.command()
def gui():
    """Launch the graphical user interface."""
    try:
        from scripts.tkinter_gui import main as gui_main
        gui_main()
    except Exception as e:
        logger.error(f"Failed to start GUI: {e}")
        click.echo(f"Error starting GUI: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
