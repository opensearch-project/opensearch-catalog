# S3 Based Ingestion Flow

This is a brief overview of a sample ingestion flow for the AWS ELB integration which is S3 based.

## List of Prerequisites

- An OpenSearch domain running through Docker
- A Spark agent running cluster with [Flint Opensearch Extension](https://github.com/opensearch-project/opensearch-spark)
- An ELB instance generating logs into S3 [setup info](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-access-logs.html)

## S3 Table Definition
Using S3 datasource as the raw data for this integration requires the following assets to be present:

 - S3-ELB [Table definition](../assets/tables/create_table_elb-1.0.0.sql) this table definition is used by the Spark/EMR catalog
 - S3-ELB [Acceleration table refresh command](../assets/tables/aws_elb_s3_refresh_covering_index-1.0.0.sql) this command will initiate the flint job processing that
   will populate the secondary index according to the specified fields in the mapping metadata section.
 - S3 [opensearch acceleration index template definition ](../assets/indices/aws_elb_covering_index-1.0.0.mapping)
   - Covering Index for accelerating general SQL/PPL queries targeted for S3 and cached in OpenSearch secondery index - see  [covering index acceleration process](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#covering-index).


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

### Integration Flow
The next section describes the integration responsibilities for creating the required assets to project ELB s3 based tables into OpenSearch ELB dashboards.

Assuming all the prerequisites mentioned above are resolved, the first step would be to create the ELB logical table on the catalog ([Glue](https://aws.amazon.com/glue/)/[Hive](https://hive.apache.org/)) 

- [The ELB table definition](../assets/tables/create_table_elb-1.0.0.sql) this table definition is used by the Spark/EMR catalog)
Once the table is created the next phase will be to generate the index template for the ELB log based on the simple schema for Observability index standard.

This index template will be augmented with the [covering index component template](../assets/indices/aws_elb_covering_index-1.0.0.mapping) (In addition to the other component templates)
So that the flint data loading process will have a valid index to load into.

- Once this is done, the next phase will be to initiate the s3 based data loading into the ELB index by calling the [`refresh` command](../assets/tables/aws_elb_s3_refresh_covering_index-1.0.0.sql)

The last part would be loading the visual assets including the dashboard that will show the ELB status according to the covering index data. 
- [Dashboards & visualization loading](../assets/aws_elb-1.0.0.ndjson) 

### User Custom Parameters
The user has the next custom parameter which can be used to dictate the names of the indices and tables:

- {table_name} - the table (FQN) name used to create the catalog table, example:`glue.default.elb-logs`
- {s3_bucket_location} - S3 bucket location, example -`'s3://your-alb-logs-directory/AWSLogs/<ACCOUNT-ID>/elasticloadbalancing/<REGION>/'`
- {object_name} - the actual object name used to refer to by the index name , example -`elb_logs`