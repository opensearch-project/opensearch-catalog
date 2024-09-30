# OCSF 1.1.0 integration with OpenSearch
These instructions are based on this existing [blog post](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/).

They are script-based and you will need to run the scripts from a host that can connect to the OpenSearch cluster. You will need to use a proxy if your OpenSearch cluster is in a private subnet. 

## Prerequisites
* You will need to have set up Amazon Security Lake and an S3-based Subscriber.
* you will need to have created an OpenSearch cluster. You can follow the guidance from this [blog post](https://aws.amazon.com/blogs/security/how-to-deploy-an-amazon-opensearch-cluster-to-ingest-logs-from-amazon-security-lake/) to size and deploy your OpenSearch cluster. This cluster cannot be serverless.
* The `Max clause count` in your cluster's **Advanced cluster settings** must be set to `4096.

## Install instructions
### 1. Download the files
Download the `alias_init.sh` and the `schemas` folder from this repository to your local machine or proxy.

### 2. Initialise aliases
After the cluster has been deployed, set up the aliases and the state management policies necessary for Security Analytics to work. Run the `alias_init.sh` file with this command, replacing the information with your own.
```
./alias_init.sh -e <OpenSearch Cluster Endpoint> -u <AdminUsername> -p <AdminPassword>
#!/bin/bash
```

### 3. Install Templates
Install the component and then the index templates with these commands

```
ls component_templates | awk -F'_body' '{print $1}' | xargs -I{} curl  -u adminuser:password -X PUT -H 'Content-Type: application/json' -d @component_templates/{}_body.json https://my-opensearch-domain.es.amazonaws.com/_component_template/{}
```

```
ls index_templates | awk -F'_body' '{print $1}' | xargs -I{} curl  -uadminuser:password -X PUT -H 'Content-Type: application/json' -d @index_templates/{}_body.json https://my-opensearch-domain.es.amazonaws.com/_index_template/{}
```

### 5. Create the OSI pipeline
Follow the instructions from the `Configure OpenSearch Ingestion` section in the existing [blog post](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/). However, use the configuration specified in the `OSI-pipeline.yaml` file instead of the blog post. Update the `queue_url`, `sts_role_arn`, `region`, and `host` fields. 

## To do: Convert these instructions into an integration