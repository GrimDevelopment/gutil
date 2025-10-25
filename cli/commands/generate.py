from typing import Any, Dict
import click
from cli.services.api_client import ApiClient

@click.command()
@click.option('--prompt', required=True, help='The prompt to generate content for.')
@click.option('--max-tokens', default=100, help='The maximum number of tokens to generate.')
def generate(prompt: str, max_tokens: int) -> None:
    """Generate content using Codex."""
    api_client = ApiClient()
    try:
        response = api_client.generate_content(prompt, max_tokens)
        click.echo(response)
    except Exception as e:
        click.echo(f"Error generating content: {str(e)}")