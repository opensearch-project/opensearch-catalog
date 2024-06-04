# AWS CloudTrails Logs Integration

> Minor fix for the Amazon Log Integration for Flint Version 1.1.0
>   Fix skipping index related [issue](https://github.com/opensearch-project/opensearch-spark/issues/353)
>   Update table creation statement according to [Athena DDL Statement](https://docs.aws.amazon.com/athena/latest/ug/cloudtrail-logs.html#create-cloudtrail-table-understanding)
> See related [Athena S3 setup tutorial](https://aws.amazon.com/blogs/big-data/aws-cloudtrail-and-amazon-athena-dive-deep-to-analyze-security-compliance-and-operational-activity/)

# AWS CloudTrail Log Integration

## What is AWS CloudTrail?

AWS CloudTrail is a service that enables governance, compliance, operational auditing, and risk auditing of your AWS account. With CloudTrail, you can log, continuously monitor, and retain account activity related to actions across your AWS infrastructure.

CloudTrail provides event history of your AWS account activity, including actions taken through the AWS Management Console, AWS SDKs, command-line tools, and other AWS services.

CloudTrail can be used for a number of tasks, such as:

- Simplifying compliance auditing
- Tracking changes to AWS resources
- Troubleshooting operational issues
- Identifying unwanted actions or unexpected patterns in behavior

CloudTrail's event log data is delivered to an S3 bucket, and does not affect network throughput or latency. You can create or delete CloudTrail logs without any risk of impact to system performance.

See additional details [here](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/what_is_cloud_trail_top_level.html).

## What is AWS CloudTrail Log Integration?

An integration is a set of pre-configured assets which are bundled together in a meaningful manner.

AWS CloudTrail log integration includes dashboards, visualizations, queries, and an index mapping.

### Dashboards

The Dashboard uses the index alias `logs-cloudtrail` for shortening the index name - be advised.

![Dashboard](https://github.com/opensearch-project/opensearch-catalog/blob/main/integrations/observability/aws_cloudtrail/static/dashboard.png?raw=true)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://github.com/opensearch-project/opensearch-catalog/releases/edit/aws_cloudtrail-1.1.0) and import the new artifact:

1) Download the `amazon_cloudtrail-1.1.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/amazon_elb-1.0.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon_cloudtrail-1.1.0.ndjson` suffix)

4) Open the [CloudTrail integration](https://localhost:5601/_dashboards/app/integrations#/available/aws_cloudtrail) and install

