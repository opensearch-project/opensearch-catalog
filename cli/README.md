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
```

## Usage

```bash
$ osints --help
Usage: osints [OPTIONS] COMMAND [ARGS]...

  Various tools for working with OpenSearch Integrations.

Options:
  --help  Show this message and exit.

Commands:
  diff  Diff between a mapping and some data.
```
