import click
from pathlib import Path
from scripts.file_handler import FileHandler
from scripts.helpers.config_utils import load_config
from scripts.helpers.logging_utils import get_logger
import sys
from scripts.helpers.verify_setup import run_verification
from scripts.process_mxd import MXDProcessor
from scripts.process_aprx import APRXProcessor

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

if __name__ == '__main__':
    cli()
