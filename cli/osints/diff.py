from beartype import beartype
import click
import json
import os.path
import glob


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
            click.echo(f"ERROR: mapping file {mapping} references component {item}, which does not exist.", err=True, color='red')
            raise click.Abort()
        if properties.get(item) is not None:
            click.echo(f"ERROR: mapping file {mapping} references component {item} and defines conflicting key '{item}'", err=True, color='red')
            raise click.Abort()
        # Greedily take any mapping that matches the name for now.
        # Later, configuration will need to be implemented.
        if len(item_glob) > 1:
            click.echo(f"WARNING: found more than one mapping for component {item}. Assuming {item_glob[0]}.", err=True, color='yellow')
        properties.update(load_mapping(item_glob[0]))
    return properties


@beartype
def flat_type_check(expect: str, actual: object) -> dict[str, dict]:
    match expect:
        case "text" | "keyword":
            if not isinstance(actual, str):
                return { "expected": expect, "actual": actual }
        case "long":
            if not isinstance(actual, int):
                return { "expected": expect, "actual": actual }
        case "alias":
            # We assume aliases were already unwrapped by the caller and ignore them.            
            return {}
        case "date":
            if not isinstance(actual, str) and not isinstance(actual, int):
                return { "expected": expect, "actual": actual }
        case _:
            click.echo(f"WARNING: unknown type '{expect}'", err=True, color='yellow')
    return {}


@beartype
def do_check(mapping: dict[str, dict], data: dict[str, object]) -> dict[str, dict]:
    result = {}
    for key, value in mapping.items():
        if key not in data:
            continue
        elif "properties" in value and isinstance(data[key], dict):
            check = do_check(value, data[key])
            if check != {}:
                result[key] = check
        elif value.get("type") == "alias":
            # Unwrap aliases split by '.'
            value_path = value["path"].split('.')
            curr_data = data
            for step in value_path[:-1]:
                if step not in curr_data:
                    curr_data[step] = {}
                curr_data = curr_data[step]
            curr_data[value_path[-1]] = data[key]
        elif "type" in value:
            check = flat_type_check(value["type"], data[key])
            if check != {}:
                result[key] = check
    for key, value in data.items():
        if key not in mapping:
            result[key] = { "expected": None, "actual": value }
    return result


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
@click.option(
    "--json",
    'output_json',
    is_flag=True,
    help="Output machine-readable JSON instead of the default diff format."
)
def diff(mapping, data, output_json):
    """Diff between a mapping and some data. Experimental."""
    properties = load_mapping(mapping)
    with open(data, "r") as data_file:
        data_json = json.load(data_file)
    check = do_check(properties, data_json)
    if output_json:
        click.echo(json.dumps(check, indent=4, sort_keys=True))