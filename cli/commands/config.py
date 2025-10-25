from typing import Any, Dict
import click
import json
import os

@click.group()
def config():
    """Manage CLI configuration settings."""
    pass

@config.command()
@click.option('--key', required=True, help='Configuration key to set.')
@click.option('--value', required=True, help='Value for the configuration key.')
def set(key: str, value: str) -> None:
    """Set a configuration key-value pair."""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    else:
        config_data = {}

    config_data[key] = value

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

    click.echo(f'Set {key} = {value} in configuration.')

@config.command()
@click.option('--key', required=True, help='Configuration key to get.')
def get(key: str) -> None:
    """Get the value of a configuration key."""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            value = config_data.get(key)
            if value is not None:
                click.echo(f'{key} = {value}')
            else:
                click.echo(f'Key {key} not found in configuration.')
    else:
        click.echo('Configuration file does not exist.')

@config.command()
def list() -> None:
    """List all configuration settings."""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            for key, value in config_data.items():
                click.echo(f'{key} = {value}')
    else:
        click.echo('Configuration file does not exist.')