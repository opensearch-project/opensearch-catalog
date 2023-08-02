# OsInts: the OpenSearch Integrations CLI

The OsInts CLI is a utility CLI for developing integrations with OpenSearch Integrations.
It provides a few convenience methods:

- `diff`: Type check your integration given a sample data record and the appropriate SS4O schema.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the CLI.

```bash
$ cd cli
$ pip install .
...
Successfully installed osints-0.1.0
$ osints
```

If you want the installation to be editable (for development), you can either specify the editable flag:

```bash
$ pip install --editable .
$ osints
```

Or you can skip the install entirely and run it as a module:

```bash
$ python3 -m src.main
```

## Usage

See `osints --help` for a summary of all commands.

### Usage: `diff`

Here's an example usage of `diff` on the [current (buggy) version of the Nginx integration](https://github.com/opensearch-project/dashboards-observability/tree/6d5bd478704dc7342b1471767ced7036bb23f335/server/adaptors/integrations/__data__/repository/nginx):
```bash
$ osints diff --mapping schemas/logs-1.0.0.mapping.json --data data/sample.json
- event.category: ["web"]
+ event.category: "keyword"
- event.type: ["access"]
+ event.type: "keyword"
- http.response.status_code: "200"
+ http.response.status_code: "integer"
- span_id: "abcdef1010"
- trace_id: "102981ABCD2901"
```

From this, we can gather:
- `event.category`, `event.type`, and `http.response.status_code` are all the wrong type. The first two should be a `keyword` instead of a list of strings, while the latter should be an integer `200` instead of a string `"200"`.
- `span_id` and `trace_id` are present in the data but not accounted for in the schema. This indicates that they are either redundant or incorrectly named. In this case, it turns out to be the latter, there are appropriate `spanId` and `traceId` fields.
