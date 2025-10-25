from typing import Any, Dict
import click
from cli.services.api_client import ApiClient

@click.group()
def auth():
    """Authentication commands for the CLI."""
    pass

@auth.command()
@click.option('--email', required=True, help='Email address of the user.')
@click.option('--password', required=True, help='Password for the user.')
def login(email: str, password: str) -> None:
    """Log in a user."""
    client = ApiClient()
    response = client.login(email, password)
    click.echo(response)

@auth.command()
@click.option('--email', required=True, help='Email address of the user.')
@click.option('--password', required=True, help='Password for the user.')
def register(email: str, password: str) -> None:
    """Register a new user."""
    client = ApiClient()
    response = client.register(email, password)
    click.echo(response)

@auth.command()
@click.option('--token', required=True, help='Authentication token for the user.')
def logout(token: str) -> None:
    """Log out a user."""
    client = ApiClient()
    response = client.logout(token)
    click.echo(response)