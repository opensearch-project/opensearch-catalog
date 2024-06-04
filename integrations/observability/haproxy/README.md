# HAProxy Integration

## What is HAProxy?

HAProxy is open-source software that provides a high availability load balancer and proxy server for TCP and HTTP-based applications.

See additional details [here](http://www.haproxy.org/).

## What is HAProxy Integration?

An integration is a bundle of pre-canned assets that are packaged together in a meaningful manner.
HAProxy integration includes dashboards, visualisations, queries and an index mapping.

### Dashboards

![](https://github.com/opensearch-project/dashboards-observability/raw/main/server/adaptors/integrations/__data__/repository/haproxy/static/dashboard1.png)
![](https://github.com/opensearch-project/dashboards-observability/raw/main/server/adaptors/integrations/__data__/repository/haproxy/static/dashboard2.png)
---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `haproxy-1.0.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/haproxy-1.0.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`haproxy-1.0.0.ndjson` suffix)

4) Open the [haproxy integration](https://localhost:5601/app/integrations#/available/haproxy) and install
 