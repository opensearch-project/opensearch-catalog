# Amazon ELB Integration

>  Amazon ELB Logs schema, see protocol details [protocol](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html#access-log-file-format)

## What is AWS ELB?

ELB Access Logs is a data signal that allows you to capture information about requests sent to your load balancer.

Access logs can help with a number of tasks, such as:

- Optimizing performance by showing response and processing times

- Security analysis by monitoring unusual request patterns or user agents

- Understanding traffic patterns and peak loads

While disabled by default, you can [enable storing access logs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html) for your load balancer in an AWS S3 bucket.

See additional details [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html).

## What is AWS ELB Access Logs Integration ?

An integration is a bundle of pre-canned assets which are bundled together in a meaningful manner.

AWS ELB access logs integration includes dashboards, visualizations, queries and index mapping

### Dashboard

![](https://github.com/opensearch-project/opensearch-catalog/blob/main/integrations/observability/amazon_elb/static/dashboard1.png?raw=true)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `amazon_elb-1.0.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/amazon_elb-1.0.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon_elb-1.0.0.ndjson` suffix)

4) Open the [elb integration](https://localhost:5601/app/integrations#/available/amazon_elb) and install
