"""
Tests for the main module.
"""

import pytest
from click.testing import CliRunner
from unwritten.main import main


def test_main_basic():
    """Test basic main function execution."""
    runner = CliRunner()
    result = runner.invoke(main)
    
    assert result.exit_code == 0
    assert "Welcome to Unwritten!" in result.output


def test_main_verbose():
    """Test main function with verbose flag."""
    runner = CliRunner()
    result = runner.invoke(main, ['--verbose'])
    
    assert result.exit_code == 0
    assert "Verbose mode enabled" in result.output
    assert "Welcome to Unwritten!" in result.output


def test_main_with_config():
    """Test main function with config file."""
    runner = CliRunner()
    
    # Create a temporary config file
    with runner.isolated_filesystem():
        with open('test_config.yaml', 'w') as f:
            f.write('test: value\n')
        
        result = runner.invoke(main, ['--config', 'test_config.yaml'])
        
        assert result.exit_code == 0
        assert "Loading configuration from:" in result.output

