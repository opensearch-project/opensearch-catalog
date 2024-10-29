# OCSF 1.1.0 integration with OpenSearch

## Prerequisites
* You will need to have set up Amazon Security Lake and an S3-based Subscriber.
* you will need to have created an OpenSearch cluster. You can follow the guidance from this [blog post](https://aws.amazon.com/blogs/security/how-to-deploy-an-amazon-opensearch-cluster-to-ingest-logs-from-amazon-security-lake/) to size and deploy your OpenSearch cluster. This cluster cannot be serverless.
* The `Max clause count` in your cluster's **Advanced cluster settings** must be set to `4096.

## Install instructions
### Automated Install
The automated install method uses a Lambda function to load the OpenSearch cluster with the relevant mappings, ISM policy, and indexes. This is the recommended method.

#### Set up Lambda function
1. Create a python Lambda function in your AWS account. If you deployed your OpenSearch cluster in a VPC, you will need to deploy this function in the same VPC. 

2. Copy and paste the function code from the `os_init_function.py` file from the `Init_scripts` folder into the Lambda function. 

3. Add the `opensearch-py` package to the function. You can get the package from [klayers](https://github.com/keithrozario/Klayers). 

4. Under the Lambda function's `configuration` panel, go to `General Configuration`. Change the function's `Timeout` to 3 minutes.

5. Under `Permissions`, open the role that is attached to the function. Add the `AmazonS3ReadOnlyAccess` AWS-managed policy. Add an inline policy that contains the permissions below
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "ec2:Describe*",
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "es:ESHttp*"
            ],
            "Resource": "arn:aws:es:ap-southeast-1:<your AWS account ID>:domain/<your OpenSearch domain name>/*",
            "Effect": "Allow"
        }
    ]
}
```

6. Under the environment variables section, add an environment variable. The key should be `ES_ENDPOINT` and the value should be your OpenSearch endpoint. 

7. Invoke the function through the AWS console.

#### Create the OSI Pipeline
Follow the instructions from the `Configure OpenSearch Ingestion` section in the existing [blog post](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/). However, use the configuration specified in the `OSI-pipeline.yaml` file instead of the blog post. Update the `queue_url`, `sts_role_arn`, `region`, and `host` fields. 


### Script-based Install
The method uses scripts to set up the cluster. These instructions are based on this existing [blog post](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/).

You will need to run the scripts from a host that can connect to the OpenSearch cluster. You will need to use a proxy if your OpenSearch cluster is in a private subnet. 

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