# Amazon S3 Access Logs Integration

>  Amazon S3 Access Logs schema, see protocol details [protocol](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html)

## What is AWS S3 Access Logs?

Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance. It is designed to make web-scale computing easier for developers.

Server access logging provides detailed records for the requests that are made to a bucket. Server access logs are useful for many applications. For example, access log information can be useful in security and access audits. This information can also help you learn about your customer base and understand your Amazon S3 bill.

See additional details [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-s3-access-logs-to-identify-requests.html).

## What is AWS S3 Integration?

An integration is a bundle of pre-canned assets which are brought together in a meaningful manner.

AWS S3 integration includes dashboards, visualizations, queries, and an index mapping.

### Dashboards

The Dashboard uses the index alias `logs-aws-s3` for shortening the index name - be advised.

![AWS S3 Dashboard](https://github.com/opensearch-project/opensearch-catalog/raw/main/integrations/observability/amazon_s3/static/dashboard.png)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `amazon-s3-logs-1.1.0` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/amazon_s3_access-logs-1.1.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon-s3-logs-1.1.0` suffix)

4) Open the [S3 access logs integration](https://localhost:5601/app/integrations#/available/amazon_s3) and install

