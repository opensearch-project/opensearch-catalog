import json

import click
from beartype import beartype

from src.utils.mappings import load_mapping


@beartype
def flat_type_check(expect: str, actual: object) -> dict[str, dict]:
    match expect:
        case "text" | "keyword":
            if not isinstance(actual, str):
                return {"expected": expect, "actual": actual}
        case "long" | "integer":
            if not isinstance(actual, int):
                return {"expected": expect, "actual": actual}
        case "alias":
            # We assume aliases were already unwrapped by the caller and ignore them.
            return {}
        case "date":
            if not isinstance(actual, str) and not isinstance(actual, int):
                return {"expected": expect, "actual": actual}
        case _:
            click.secho(f"WARNING: unknown type '{expect}'", err=True, fg="yellow")
    return {}


@beartype
def get_type(mapping: dict) -> str | dict:
    if mapping.get("properties"):
        return {
            key: get_type(value) for key, value in mapping.get("properties").items()
        }
    return mapping.get("type", "unknown")


@beartype
def do_check(
    mapping: dict[str, dict], data: dict[str, object], show_missing: bool = False
) -> dict[str, dict]:
    result = {}
    for key, value in mapping.items():
        if key not in data:
            if show_missing and value.get("type") != "alias":
                result[key] = {"expected": get_type(value), "actual": None}
            continue
        elif "properties" in value and isinstance(data[key], dict):
            check = do_check(value["properties"], data[key], show_missing)
            if check != {}:
                result[key] = check
        elif value.get("type") == "alias":
            # Unwrap aliases split by '.'
            value_path = value["path"].split(".")
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
            result[key] = {"expected": None, "actual": value}
    return result


@beartype
def output_diff(difference: dict[str, object], prefix: str = "") -> None:
    for key, value in sorted(difference.items()):
        out_key = prefix + key
        if "expected" not in value and "actual" not in value:
            output_diff(value, f"{prefix}{key}.")
        if value.get("actual") is not None:
            click.echo(f"- {out_key}: {json.dumps(value.get('actual'))}")
        if value.get("expected") is not None:
            click.echo(f"+ {out_key}: {json.dumps(value.get('expected'))}")


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
    "output_json",
    is_flag=True,
    help="Output machine-readable JSON instead of the default diff format",
)
@click.option(
    "--show-missing",
    "show_missing",
    is_flag=True,
    help="Output fields that are expected in the mappings but missing in the data",
)
def diff(mapping, data, output_json, show_missing):
    """Type check your integration given a sample data record and the appropriate SS4O schema."""
    properties = load_mapping(mapping)
    with open(data, "r") as data_file:
        data_json = json.load(data_file)
    if isinstance(data_json, list):
        # Unwrap list of data, assume first record is representative
        data_json = data_json[0]
    check = do_check(properties, data_json, show_missing)
    if output_json:
        click.echo(json.dumps(check, sort_keys=True))
    else:
        output_diff(check)


if __name__ == "__main__":
    diff()
