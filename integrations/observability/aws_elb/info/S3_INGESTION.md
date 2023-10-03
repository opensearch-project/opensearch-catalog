# S3 Based Ingestion Flow

This is a brief overview of a sample ingestion flow for the AWS ELB integration which is S3 based.

## List of Prerequisites

- An OpenSearch domain running through Docker
- A Spark agent running cluster with [Flint Opensearch Extension](https://github.com/opensearch-project/opensearch-spark)
- An ELB instance generating logs into S3 [setup info](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-access-logs.html)

## S3 Table Definition
Using S3 datasource as the raw data for this integration requires the following assets to be present:

 - S3-ELB [Table definition](../assets/aws_elb_s3_table-1.0.0.sql) this table definition is used by the Spark/EMR catalog
 - S3-ELB [Acceleration table definition](../assets/aws_elb_s3_skipping_index-1.0.0.sql) this table is used by opensearch flint-spark 
 - S3 opensearch acceleration index template definition 
   - Covering Index for accelerating general SQL/PPL queries targeted for S3
   - Materialized view Index for accelerating the ELB dashboards based on OpenSearch indices


#### ELB table mapping
The next columns mapping between the S3-ELB table definition and the ELB schema index mapping:

| Field Source Name           | Field Target Name               | Type     |
|-----------------------------|---------------------------------|----------|
| type                        | aws.elb.elb_type                | string   |
| time                        | @timestamp                      | string   |
| elb                         | aws.elb.elb_name                | string   |
| client_ip                   | aws.elb.client.ip               | string   |
| client_port                 | aws.elb.client.port             | int      |
| target_ip                   | aws.elb.target_ip               | string   |
| target_port                 | aws.elb.target_port             | int      |
| request_processing_time     | aws.elb.request_processing_time | double   |
| target_processing_time      | aws.elb.target_processing_time  | double   |
| response_processing_time    | aws.elb.response_processing_time| double   |
| elb_status_code             | aws.elb.elb_status_code         | int      |
| target_status_code          | aws.elb.target_status_code      | string   |
| received_bytes              | aws.elb.received_bytes          | bigint   |
| sent_bytes                  | aws.elb.sent_bytes              | bigint   |
| request_verb                | http.request.method             | string   |
| request_url                 | url.full                        | string   |
| request_proto               | url.schema                      | string   |
| user_agent                  | http.user_agent.name            | string   |
| ssl_cipher                  | aws.elb.ssl_cipher              | string   |
| ssl_protocol                | aws.elb.ssl_protocol            | string   |
| target_group_arn            | aws.elb.target_group_arn        | string   |
| trace_id                    | traceId                         | string   |
| domain_name                 | url.domain                      | string   |
| chosen_cert_arn             | aws.elb.chosen_cert_arn         | string   |
| matched_rule_priority       | aws.elb.matched_rule_priority   | string   |
| request_creation_time       | aws.elb.request_creation_time   | string   |
| actions_executed            | aws.elb.actions_executed        | string   |
| redirect_url                | aws.elb.redirect_url            | string   |
| lambda_error_reason         | aws.elb.lambda_error_reason     | string   |
| target_port_list            | aws.elb.target_port_list        | string   |
| target_status_code_list     | aws.elb.target_status_code_list | string   |
| classification              | aws.elb.classification         | string   |
| classification_reason       | aws.elb.classification_reason  | string   |

