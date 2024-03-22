import base64
import copy
import json
import sys
import typing
import uuid
from datetime import datetime
from glob import glob
from pathlib import Path

from beartype import beartype
import click
import ndjson

# Random UUID4, use as namespace for UUID5s for helpful collision identification
NAMESPACE_OS_CATALOG: uuid.UUID = uuid.UUID("f21aff9f-a6b3-43eb-85af-5ce18a880430")
CONFIG_FIELD_DIR_INFO: dict[str, tuple[str, str]] = {
    "statics": ("static", "bin"),
    "components": ("schemas", "mapping.json"),
    "assets": ("assets", "text"),
    "sampleData": ("data", "json"),
}
OS_OBJECT_SIZE_LIMIT = 1_048_576  # 1 MB

# Minified JSON serialization helper
# Due to hashing and object size limits we want to be consistent about whitespace and key ordering
min_json = lambda obj: json.dumps(obj, separators=(",", ":"), sort_keys=True)


def try_attach_assets(config: dict, path: Path, info: None | tuple[str, str]) -> bool:
    # Guard clauses: Skip anything that can't be read
    if not info:
        return False
    if not ("path" in config or ("name" in config and "version" in config)):
        return False
    subdir, encoding = info

    # Read data
    read_mode = "r" if encoding != "bin" else "rb"
    match (config.get("path"), encoding):
        case (
            None,
            "text",
        ):  # If no path and text encoding, rely on language for extension
            full_path = (
                path
                / subdir
                / f"{config['name']}-{config['version']}.{config['extension']}"
            )
        case (None, _):  # Otherwise, use encoding as extension with name
            full_path = (
                path / subdir / f"{config['name']}-{config['version']}.{encoding}"
            )
        case (_, _):  # If a path is present, use it regardless of specified encoding
            full_path = path / subdir / config["path"]
    with open(full_path, read_mode) as data_file:
        data = data_file.read()

    # Attach data to config
    match encoding:
        case "bin":
            config["data"] = str(base64.b64encode(data), encoding="ascii")
        case "mapping.json" | "json":
            config["data"] = min_json(json.loads(data))
        case "ndjson":
            config["data"] = min_json(ndjson.loads(data))
        case "text":
            config["data"] = data
    return True


def attach_assets_in_place(
    config: typing.Any, path: Path, info: None | tuple[str, str] = None
) -> None:
    if not isinstance(config, list) and not isinstance(config, dict):
        return
    if isinstance(config, list):
        for item in config:
            attach_assets_in_place(item, path, info)
        return
    if try_attach_assets(config, path, info):
        return
    for key, value in config.items():
        info = CONFIG_FIELD_DIR_INFO.get(key, info)
        attach_assets_in_place(value, path, info)


def attach_assets(config: dict, path: Path) -> dict:
    config = copy.deepcopy(config)
    attach_assets_in_place(config, path)
    return config


# Serialize integration as local dictionary
def scan_integration(path: Path) -> dict:
    integration_name = path.stem
    # TODO detect latest version instead of defaulting to 1.0.0
    with open(path / f"{integration_name}-1.0.0.json", "r") as config_file:
        config = json.load(config_file)
    config = attach_assets(config, path)
    return config


# Convert an integration json config to a full saved object
def bundle_integration(integration: dict):
    obj_id = uuid.uuid5(
        NAMESPACE_OS_CATALOG,
        min_json([integration["name"], integration["type"], integration["version"]]),
    )
    return {
        "type": "integration-template",
        "id": str(obj_id),
        "updated_at": datetime.utcnow().isoformat(),
        "attributes": integration,
    }


# If the object is too large, truncate sample data and inform user
# Necessary as some integrations have lots of sample data
def check_truncate_sample(integration: dict, dir: str):
    if not integration["attributes"].get("sampleData"):
        return
    if len(min_json(integration)) > OS_OBJECT_SIZE_LIMIT:
        print(f"{dir}: Integration too large! Truncating sample data to 100 records")
        data = integration["attributes"]["sampleData"]["data"]
        data = min_json(json.loads(data)[:100])
        integration["attributes"]["sampleData"]["data"] = data


def convert_integration(integration_dir: str) -> str | None:
    scanned = scan_integration(Path(integration_dir))
    saved_object = bundle_integration(scanned)
    check_truncate_sample(saved_object, integration_dir)
    return min_json(saved_object)


@click.command()
@click.option(
    "--integrations",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="The directory to scan for integrations",
)
@click.option(
    "--output",
    type=click.Path(writable=True),
    help="The destination file to put the bundle (.ndjson)",
)
@beartype
def bundle(integrations: str, output: str) -> int:
    """Convert local integration folders into an ndjson bundle."""
    input_files = glob(str(Path(integrations) / "*"))
    integ_map = map(convert_integration, input_files)

    summary = {"exportedCount": 0, "missingRefCount": 0, "missingReferences": []}
    with open(Path(output), "w") as bundle:
        for integration in integ_map:
            if not integration:
                continue
            bundle.write(f"{integration}\n")
            summary["exportedCount"] += 1
        bundle.write(f"{min_json(summary)}\n")
    print(f"Wrote {summary['exportedCount']} integrations to {output}")

    return int(len(input_files) > summary["exportedCount"]) # Status code 0 or 1

if __name__ == "__main__":
    # Inputs: The directory to scan for integrations, and where to put the bundle
    input_files = glob("repository/*")
    output_path = Path("integrations_bundle.ndjson")
    sys.exit(bundle(input_files, output_path))
