from beartype import beartype
import click
import json
import glob
import os.path
from datetime import datetime

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
                f"ERROR: mapping file {mapping} references component {item}, which does not exist.",
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
                f"WARNING: found more than one mapping for component {item}. Assuming {item_glob[0]}.",
                err=True,
                fg="yellow",
            )
        properties.update(load_mapping(item_glob[0]))
    return properties

# Populates a field in the index pattern list object
@beartype
def populate(
    json_fields: list[dict], name: str, type: str, esTypes: str, count: int, scripted: bool, searchable: bool, aggregatable: bool, readFromDocValues: bool, parent: str = ""
) -> None:
    json_dict = dict()
    json_dict["name"] = name
    json_dict["type"] = type
    json_dict["esTypes"] = [esTypes]
    json_dict["count"] = count
    json_dict["scripted"] = scripted
    json_dict["searchable"] = searchable
    json_dict["aggregatable"] = aggregatable
    json_dict["readFromDocValues"] = readFromDocValues
    if parent != "":
        json_dict["subType"] = {"multi": {"parent": parent}}
    json_fields.append(json_dict)

# Parses a key in a dictionary and all its subfields
@beartype
def get_fields(
    mapping: dict[str, str], suffix: str
) -> list[dict]:
    
    json_fields = list()

    for key in mapping.keys():     
        entry = (key) if suffix == "" else (suffix + "." + key)    
        # Check for subclasses
        if "properties" in mapping[key].keys():
            json_fields += get_fields(mapping[key]["properties"], entry)
        else:
            type = mapping[key]["type"]
            type_dict = {
                "ip":"ip",
                "keyword":"string",
                "text":"string",
                "integer":"number",
                "half_float":"number",
                "short":"number",
                "long":"number",
                "date":"date",
                "geo_point":"geo_point",
                "alias": "string"
            }
            # if "fields" in data[key].keys() and "keyword" in data[key]["fields"]:
            #     populate(entry_name, type_dict.get(type), "text", 0, False, True, False, False)
            #     populate(entry_name + ".keyword", type_dict.get(type), "keyword", 0, False, True, True, True, entry)
            if type == "@message":
                populate(json_fields, entry, type_dict.get(type), "text", 0, False, True, False, False)
            else:
                populate(json_fields, entry, type_dict.get(type), type, 0, False, True, True, True)
                
    return json_fields
                
# Adds fields that are in all index pattern, i.e. _index and _source
@beartype
def pre_populate(json_fields: list[dict]) -> list[dict]:
    populate(json_fields, "_index", "string", "_index", 0, False, True, True, False)
    populate(json_fields, "_score", "number", "", 0, False, True, True, False)
    populate(json_fields, "_source", "_source", "_source", 0, False, False, False, False)
    populate(json_fields, "_type", "string", "_type", 0, False, True, True, False)
    return json_fields

# Creates index pattern as an ndjson file
@beartype
def create_index_pattern(json_fields: str) -> None:
    output_file = open("index_pattern.json", "w")
    current_datetime = datetime.now()
    json_dict = {
        "attributes": {
            "fields": json_fields,
            "timeFieldName": "@timestamp",
            "title": "ss4o_logs-*-*"
        },
        "id": "9d96cb30-f01b-11ea-99e6-53b5a9b5c41b",
        "migrationVersion": {
            "index-pattern": "7.6.0"
        },
        "references": [],
        "type": "index-pattern",
        "updated_at": current_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "version": "WzE0LDFd"
    }
    json.dump(json_dict, output_file)

@click.command()
@click.option(
    "--mappings",
    multiple=True,
    type=click.Path(exists=True, readable=True),
    help="The mapping schemas the index pattern should include"
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output machine-readable JSON instead of the default ndjson format"
)
def index_pattern(mappings, output_json):
    data = dict()
    for mapping in mappings:
        data.update(load_mapping(mapping))
    json_fields = get_fields(data, "")
    # print(json.dumps(json_fields))
    create_index_pattern(json.dumps(json_fields))
    
if __name__ == "__main__":
    index_pattern()