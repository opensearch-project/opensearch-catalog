import glob
import json
import os.path

import click
from beartype import beartype


@beartype
def nested_update(base: dict, updates: dict) -> dict:
    for k, v in updates.items():
        if isinstance(v, dict):
            base[k] = nested_update(base.get(k, {}), v)
        else:
            base[k] = v
    return base


@beartype
def load_mapping(mapping: str) -> dict[str, dict]:
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
            click.secho(
                f"ERROR: mapping file {mapping} references component {item}, which does not exist",
                err=True,
                fg="red",
            )
            raise click.Abort()
        if properties.get(item) is not None:
            click.secho(
                f"ERROR: mapping file {mapping} references component {item} and defines conflicting key '{item}'",
                err=True,
                fg="red",
            )
            raise click.Abort()
        # Greedily take any mapping that matches the name for now.
        # Later, configuration will need to be implemented.
        if len(item_glob) > 1:
            click.secho(
                f"WARNING: found more than one mapping for component {item}. Assuming {item_glob[0]}",
                err=True,
                fg="yellow",
            )
        nested_update(properties, load_mapping(item_glob[0]))
    return properties
