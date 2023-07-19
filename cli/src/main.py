import click
from .diff import diff
from .index_pattern import index_pattern

@click.group()
def cli():
    """Various tools for working with OpenSearch Integrations."""
    pass


cli.add_command(diff)
cli.add_command(index_pattern)


if __name__ == "__main__":
    cli()
