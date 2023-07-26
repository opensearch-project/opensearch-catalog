import json

import click
from beartype import beartype

from src.utils.mappings import load_mapping


@beartype
def check_type(field_type: str | None, mapping_type: str | None) -> bool:
    match field_type:
        case "string":
            return mapping_type in ["keyword", "text"]
        case "number":
            return mapping_type in ["integer", "long"]
        case _:
            return field_type == mapping_type or mapping_type == "alias"


@beartype
def check_index_pattern(asset: dict, mapping: dict) -> None:
    fields = json.loads(asset["attributes"]["fields"])
    for field in fields:
        if field["name"].startswith("_"):
            continue
        split = field["name"].split(".")
        curr_mapping = mapping
        for step in split:
            if step == "keyword":
                curr_mapping = curr_mapping.get("fields", {}).get("keyword", {})
                continue
            curr_mapping = curr_mapping.get(step, {})
            if "properties" in curr_mapping:
                curr_mapping = curr_mapping["properties"]
        if not check_type(field["type"], curr_mapping.get("type", None)):
            if field["name"].endswith("keyword"):
                # Ignore all weird keyword stuff for now because it's complicated
                continue
            print(field["name"], field["type"], curr_mapping.get("type", None))


@beartype
def check_asset(asset: dict, mapping: dict) -> None:
    if "type" not in asset:
        # Some metadata assets have no type, they should be safe to skip.
        return
    match asset["type"]:
        case "index-pattern":
            check_index_pattern(asset, mapping)
        case other:
            click.secho(f"WARNING: unknown type '{other}'", err=True, fg="yellow")


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
        if assets.endswith(".json"):
            data_assets = json.load(asset_file)
        elif assets.endswith(".ndjson"):
            data_assets = list(
                json.loads(line) for line in asset_file.read().splitlines()
            )
        else:
            click.secho(f"WARNING: assets must be Json or NDJson", err=True, fg="red")
            raise click.Abort()
        if not isinstance(data_assets, list):
            data_assets = [data_assets]
    properties = load_mapping(mapping)
    for asset in data_assets:
        check_asset(asset, properties)


if __name__ == "__main__":
    scanviz()
