# S3 Based Ingestion Flow

This is a brief overview of a sample ingestion flow for the AWS ELB integration which is S3 based.

## List of Prerequisites

- An OpenSearch domain running through Docker
- A Spark agent running cluster with [Flint Opensearch Extension](https://github.com/opensearch-project/opensearch-spark)
- An ELB instance generating logs into S3 [setup info](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-access-logs.html)

