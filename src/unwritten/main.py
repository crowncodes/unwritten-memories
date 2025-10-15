"""
Main entry point for the Unwritten application.
"""

import click
from typing import Optional


@click.command()
@click.option('--config', '-c', type=click.Path(exists=True), 
              help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, 
              help='Enable verbose output')
def main(config: Optional[str] = None, verbose: bool = False):
    """
    Unwritten - Main application entry point.
    """
    if verbose:
        click.echo("Verbose mode enabled")
    
    click.echo("Welcome to Unwritten!")
    
    if config:
        click.echo(f"Loading configuration from: {config}")
    
    # Your application logic here
    click.echo("Application running...")


if __name__ == "__main__":
    main()

