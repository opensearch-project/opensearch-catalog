# Amazon VPC Flow Logs Integration (VPC file format)

>  VPC flow based on 1.1 specification for vpc parquet based format
>   See protocol details [protocol](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html)

## What is Amazon VPC Flow Logs ?

VPC Flow Logs is a feature that enables you to capture information about the IP traffic going to and from network interfaces in your VPC.

Flow logs can help you with a number of tasks, such as:

- Diagnosing overly restrictive security group rules

- Monitoring the traffic that is reaching your instance

- Determining the direction of the traffic to and from the network interfaces

Flow log data is collected outside of the path of your network traffic, and therefore does not affect network throughput or latency. You can create or delete flow logs without any risk of impact to network performance.

- See additional Amazon Logs Info details [Here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html).
- Flint S3 VPC integration [Readme](https://github.com/opensearch-project/dashboards-observability/blob/main/server/adaptors/integrations/__data__/repository/amazon_vpc_flow/info/Flint-Integration.md)

## What is Amazon VPC FLow Logs Integration ?

An integration is a bundle of pre-canned assets which are bundled togather in a meaningful manner.

Amazon VPC flow logs integration includes dashboards, visualisations, queries and an index mapping.

### Dashboards

The Dashboard uses the index alias `logs-vpc` for shortening the index name - be advised.

![](https://github.com/opensearch-project/dashboards-observability/blob/main/server/adaptors/integrations/__data__/repository/amazon_vpc_flow/static/dashboard1.png?raw=true)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `amazon_vpc_flow-1.1.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/amazon_vpc_flow_1.1.0)


2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon_vpc_flow-1.1.0.ndjson` suffix)

4) Open the [VPC integration](https://localhost:5601/_dashboards/app/integrations#/available/amazon_vpc_flow) and install
