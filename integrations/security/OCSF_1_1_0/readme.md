# OCSF 1.1.0 integration with OpenSearch
This set of files will 

## Install instructions
Right now, the install instructions are script-based, based on the existing [blog post](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/).

### 1. Initialise aliases
Set up the aliases and the state management policies necessary for Security Analytics to work. Run the `alias_init.sh` file (in the proxy if necessary) with this command 
```
./alias_init.sh -e <OpenSearch Cluster Endpoint> -u <myusername> -p <mypassword>
#!/bin/bash
```

### 2. Install Templates
Install the component and then the index templates with these commands

```
ls component_templates | awk -F'_body' '{print $1}' | xargs -I{} curl  -u adminuser:password -X PUT -H 'Content-Type: application/json' -d @component_templates/{}_body.json https://my-opensearch-domain.es.amazonaws.com/_component_template/{}
```

```
ls index_templates | awk -F'_body' '{print $1}' | xargs -I{} curl  -uadminuser:password -X PUT -H 'Content-Type: application/json' -d @index_templates/{}_body.json https://my-opensearch-domain.es.amazonaws.com/_index_template/{}
```

### 3. Create the OSI pipeline
Set up your OpenSerach Ingestion pipeline to the OpenSearch cluster with the pipeline configuration specified in the `OSI-pipeline.yaml` file. Update the `queue_url`, `sts_role_arn`, `region`, and `host` fields. 

## To do: Convert these instructions into an integration