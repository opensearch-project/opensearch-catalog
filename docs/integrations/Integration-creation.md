## What makes an integration?

An integration has four parts:

* A configuration that ties together the following three parts with some metadata.
* A schema that defines the data format, currently based on SS4O. [Docs](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema)
* Assets that are loaded into Dashboards via the Saved Object API.
    * In the future, more asset types will be supported, but for the moment we only support saved objects.
* Statics: logos, screenshots, the works.

For some examples of integrations, see the current list in the [Observability Integrations ](../../integrations).

The [Nginx integration](../../integrations/observability/nginx) in particular is a prototypical example that we’ll reference throughout the guide.

## How to create one?

Getting a working pair of schemas and assets is challenging. Here’s 7 general steps to get it done. We assume you are trying to create an integration using an existing dashboards on the web (e.g. Beats) instead of making one from scratch.

### Set up example infrastructure based on what’s already available

Follow the docs from some target project to set up a sample infrastructure.

### Collect sample data records from that infrastructure

In particular, you want records as they’re submitted to OpenSearch, in JSON. The tooling in the next step generally depends on the data being in a JSON format.

### Make a converter to convert records to SS4O

In the future this can be automated with a code generation framework, but the general idea is to use some agent to make OTEL-compliant or ECS-compliant data. Some options:

* **Jaeger**
* **Fluentbit**
* **Data Prepper**
* **OTEL Collector**
* **Logstash**

For determining what actually needs to be done for conversion, there is an [open PR](https://github.com/opensearch-project/opensearch-catalog/pull/32) for a tool that lets you quickly check how your data differs from a selected SS4O schema. This can be a valuable debugging tool for making an SS4O converter.

### Make an alternative infrastructure that uses this converter

Docker is ideal here, if possible. Strictly speaking, you only need this for testing, making a “correct” alternative infrastructure with other users is out of scope. The goal is to just get schema-compliant data stored in an OpenSearch data stream.

### Convert or remake assets from the original system using SS4O

In the future this can be automated. For now, I think the main idea is to go through the panels in the existing dashboard(s) and update their queries for the new schema. If a field is needed in the panel that isn’t present anywhere in the schema, either remove it or ask @YANG-DB about adding it to the schema.

New visualizations should be put in the Visualization Catalog in opensearch-catalog.

### Compile the integration

In the future this can be automated, but generally, model it on some of the existing integrations. Put all the relevant info in the directory and write a config.

### Test the integration

Try using the integration in OpenSearch Dashboards with the Integrations Plugin. Make sure all the visualizations work, the logo and screenshots render correctly, no weird display bugs, and similar things. This is also a good opportunity to test the integrations plugin for bugs.

A simple sanity check is to use the UI’s “try it” button. There should be no visible errors when the button is pressed and the integration’s dashboard is opened.
