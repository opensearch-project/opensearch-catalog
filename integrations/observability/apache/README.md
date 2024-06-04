# Apache Http Logs Integration

> Apache Http Logs schema, see protocol details [protocol](https://httpd.apache.org/docs/2.4/logs.html)

## What is Apache ?

Apache is an open source web server software for modern operating systems including UNIX and Windows.

See additional details [here](https://httpd.apache.org/).

## What is Apache Integration ?

An integration is a bundle of pre-canned assets which are bundled togather in a meaningful manner.

Apache integration includes dashboards, visualisations, queries and an index mapping.

### Dashboards

![](https://github.com/opensearch-project/opensearch-catalog/raw/main/integrations/observability/apache/static/dashboard1.png)
---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `apache-1.0.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/apache-1.0.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`apache-1.0.0.ndjson` suffix)

4) Open the [apache http logs integration](https://localhost:5601/app/integrations#/available/amazon_apache) and install
