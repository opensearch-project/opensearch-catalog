import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--schema', type=click.Path(exists=True), help='The mapping for the format the data should have')
@click.option('--data', type=click.Path(exists=True), help='The location of data to validate')
def diff(schema, data):
    """Diff between a mapping and some data. Experimental."""
    print(schema, data)

cli.add_command(diff)
