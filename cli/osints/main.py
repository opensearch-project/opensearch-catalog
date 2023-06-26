import click
from diff import diff

@click.group()
def cli():
    pass

cli.add_command(diff)
