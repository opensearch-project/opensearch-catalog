# Amazon CloudFront Integration

>  Amazon CloudFront Logs schema, see protocol details [protocol](https://docs.aws.amazon.com/athena/latest/ug/cloudfront-logs.html)

# AWS CloudFront Integration

## What is AWS CloudFront?

Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds. CloudFront is integrated with other Amazon Web Services products to give developers and businesses an easy way to distribute content to end-users with low latency and high data transfer speeds.

See additional details [here](https://aws.amazon.com/cloudfront/).

## What is AWS CloudFront Integration?

An integration is a bundle of pre-canned assets which are brought together in a meaningful manner.

AWS CloudFront integration includes dashboards, visualizations, queries, and an index mapping.

### Dashboards

The Dashboard uses the index alias `logs-aws-cloudfront` for shortening the index name - be advised.

![AWS CloudFront Dashboard](https://github.com/opensearch-project/opensearch-catalog/blob/main/integrations/observability/amazon_cloudfront/static/dashboard.png?raw=true)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `amazon_cloudfront-1.0.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/amazon_cloudfront-1.0.0)


2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon_cloudfront-1.0.0.ndjson` suffix)

4) Open the [cloud front integration](https://localhost:5601/app/integrations#/available/amazon_cloudfront) and install
