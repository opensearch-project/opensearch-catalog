import json

import click
from beartype import beartype

from src.utils.mappings import load_mapping


@beartype
def check_asset(_asset: object) -> bool:
    return False


@click.command()
@click.option(
    "--assets",
    type=click.Path(exists=True, readable=True),
    help="A json file containing assets to scan",
)
@click.option(
    "--mapping",
    type=click.Path(exists=True, readable=True),
    help="The mapping for the format the data should have",
)
def scanviz(assets, mapping):
    """Type check your integration visualizations against your schemas."""
    with open(assets, "r") as asset_file:
        data_assets = json.load(asset_file)
    properties = load_mapping(mapping)
    if not isinstance(data_assets, list):
        data_assets = [data_assets]
    for asset in data_assets:
        check_asset(asset)


if __name__ == "__main__":
    scanviz()
