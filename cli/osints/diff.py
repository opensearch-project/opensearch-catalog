import click

@click.command()
@click.option('--mapping', type=click.Path(exists=True), help='The mapping for the format the data should have')
@click.option('--data', type=click.Path(exists=True), help='The location of data to validate')
def diff(mapping, data):
    """Diff between a mapping and some data. Experimental."""
    print(mapping, data)
