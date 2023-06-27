import click
import json
import os.path
import glob


def load_mapping(mapping: str):
    with open(mapping, "r") as mapping_file:
        data = json.load(mapping_file)
    properties = data.get("template", {}).get("mappings", {}).get("properties")
    if properties is None:
        return {}
    composed_of = data.get("composed_of", [])
    curr_dir = os.path.dirname(mapping)
    for item in composed_of:
        item_glob = glob.glob(os.path.join(curr_dir, f"{item}*"))
        if len(item_glob) == 0:
            click.echo(f"ERROR: mapping file {mapping} references component {item}, which does not exist.", err=True, fg='red')
            raise click.Abort()
        if properties.get(item) is not None:
            click.echo(f"mapping file {mapping} references component {item} and defines conflicting key '{item}'", err=True, fg='red')
            raise click.Abort()
        # Greedily take any mapping that matches the name for now.
        # Later, configuration will need to be implemented.
        if len(item_glob) > 1:
            click.echo(f"WARNING: Found more than one mapping for component {item}. Assuming {item_glob[0]}.", err=True, fg='yellow')
        properties[item] = load_mapping(item_glob[0])
    return properties


@click.command()
@click.option(
    "--mapping",
    type=click.Path(exists=True, readable=True),
    help="The mapping for the format the data should have",
)
@click.option(
    "--data",
    type=click.Path(exists=True, readable=True),
    help="The location of data to validate",
)
def diff(mapping, data):
    """Diff between a mapping and some data. Experimental."""
    properties = load_mapping(mapping)
    click.echo(json.dumps(properties, indent=4))
