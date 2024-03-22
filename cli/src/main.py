import click

from .diff import diff
from .scanviz import scanviz
from .bundle import bundle


@click.group()
def cli():
    """Various tools for working with OpenSearch Integrations"""
    pass


cli.add_command(diff)
cli.add_command(scanviz)
cli.add_command(bundle)


if __name__ == "__main__":
    cli()
