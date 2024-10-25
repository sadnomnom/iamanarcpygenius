import click
from pathlib import Path
from scripts.file_handler import FileHandler
from scripts.helpers.config_utils import load_config
from scripts.helpers.logging_utils import get_logger
import sys
from scripts.helpers.verify_setup import run_verification

logger = get_logger(__name__)

@click.group()
def cli():
    """Command line interface for map processing pipeline."""
    pass

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--resolution', '-r', default=300, help='PDF export resolution (DPI)')
def process(input_path: str, output_path: str, resolution: int):
    """Process a single map file (MXD or APRX) to PDF."""
    file_handler = FileHandler()
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if file_handler.process_file(input_path, output_path, resolution):
        click.echo(f"Successfully processed {input_path} to {output_path}")
    else:
        click.echo(f"Failed to process {input_path}", err=True)

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--resolution', '-r', default=300, help='PDF export resolution (DPI)')
def batch_process(input_dir: str, output_dir: str, resolution: int):
    """Process all map files in a directory."""
    file_handler = FileHandler()
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for input_path in input_dir.glob('*.*'):
        if file_handler.validate_file(input_path):
            output_path = output_dir / f"{input_path.stem}.pdf"
            if file_handler.process_file(input_path, output_path, resolution):
                click.echo(f"Successfully processed {input_path}")
            else:
                click.echo(f"Failed to process {input_path}", err=True)

@cli.command()
def verify():
    """Verify the environment setup."""
    success = run_verification()
    if not success:
        click.echo("Environment verification failed. Check the logs for details.", err=True)
        sys.exit(1)
    click.echo("Environment verification successful!")

if __name__ == '__main__':
    cli()
