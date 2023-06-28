import click
from .diff import diff

@click.group()
def cli():
    """Various tools for working with OpenSearch Integrations."""
    pass


cli.add_command(diff)


if __name__ == "__main__":
    cli()
