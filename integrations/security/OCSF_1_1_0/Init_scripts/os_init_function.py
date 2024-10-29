from urllib.parse import urlparse
import boto3
from botocore.exceptions import ClientError
import zipfile
import os
import json
from boto3 import Session
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection
from datetime import datetime

## Set up connection to OpenSearch cluster
OSEndpoint = os.environ.get('ES_ENDPOINT')
print (OSEndpoint)
region = os.environ.get('AWS_REGION')
print (region)

url = urlparse(OSEndpoint)

credentials = Session().get_credentials()

auth = AWSV4SignerAuth(credentials, region)

client = OpenSearch(
hosts=[{
    'host': url.netloc,
    'port': url.port or 443
}],
http_auth=auth,
use_ssl=True,
verify_certs=True,
connection_class=RequestsHttpConnection
)
info = client.info()
print(f"{info['version']['distribution']}: {info['version']['number']}")

def ISM_INIT():
    ## This function creates the ISM policy
    ism_policy = {
        "policy": {
            "policy_id": "rollover-expiration-policy",
            "description": "This policy rollsover the index daily or if it reaches 40gb. It also expires logs older than 15 days",
            "default_state": "rollover",
            "states": [
                {
                    "name": "rollover",
                    "actions": [
                        {
                            "retry": {
                                "count": 3,
                                "backoff": "exponential",
                                "delay": "1h"
                            },
                            "rollover": {
                                "min_size": "40gb",
                                "min_index_age": "1d",
                                "copy_alias": False
                            }
                        }
                    ],
                    "transitions": [
                    {
                        "state_name": "delete",
                        "conditions": {
                            "min_index_age": "15d"
                        }
                    }
                ]
                },
                {
                    "name": "hot",
                    "actions": [],
                    "transitions": [
                        {
                            "state_name": "delete",
                            "conditions": {
                                "min_index_age": "15d"
                            }
                        }
                    ]
                },
                {
                    "name": "delete",
                    "actions": [
                        {
                            "timeout": "5h",
                            "retry": {
                                "count": 3,
                                "backoff": "exponential",
                                "delay": "1h"
                            },
                            "delete": {}
                        }
                    ],
                    "transitions": []
                }
            ],
            "ism_template": [
                {
                    "index_patterns": [
                        "ocsf-*"
                    ],
                    "priority": 9
                }
            ]
        }
    }
    try:
        client.plugins.index_management.put_policy(policy = "rollover-expiration-policy", body=ism_policy)
        print ("ISM Policy created")
    except Exception as e:
        print(f"Error creating ISM Policy: {e}")
        pass

def alias_init():
    index_date = datetime.now().strftime("%Y.%m.%d")
    index_list = ["ocsf-1.1.0-2002-vulnerability_finding", "ocsf-1.1.0-2003-compliance_finding", "ocsf-1.1.0-2004-detection_finding", "ocsf-1.1.0-3001-account_change","ocsf-1.1.0-3002-authentication", "ocsf-1.1.0-4001-network_activity","ocsf-1.1.0-4002-http_activity","ocsf-1.1.0-4003-dns_activity","ocsf-1.1.0-6003-api_activity",]
    for index in index_list:
    # Create the index 
        try: 
            index_name = f"<{index}-{{now/d}}-000000>"
            client.indices.create(index=index_name, body = {})
            print (f"created index {index}")
        except Exception as e:
            print(f"Error creating {index} index: {e}")
            pass

        # Create the alias
        try:
            alias_name = index
            alias_index = f"{index}-*"
            client.indices.put_alias(index=alias_index, name=alias_name)
            print (f"created alias {alias_name}")
        except Exception as e:
            print(f"Error creating {alias_name} alias: {e}")
            pass

        ## Set the index settings
        settings = {
            "settings": {
                "index": {
                    "plugins": {
                    "index_state_management": {
                        "rollover_alias": f"{index}"
                                            }
                                        }
                                    }
                                }
                            }

        client.indices.put_settings(index=index_name, body=settings)
        print (f"Applied settings to {index_name}")

    ## Increase docvalue setting
    index_name = "ocsf-1.1.0*"
    settings = {
        "index.max_docvalue_fields_search": "300"
    }

    client.indices.put_settings(
        index=index_name,
        body=settings
    )
    print (f"Increased docvalue_fields to 300")

def install_component_templates():
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Specify the bucket and file to download
    bucket_name = 'ws-assets-prod-iad-r-sin-694a125e41645312'
    file_key = '4192e8ce-704a-4400-8d18-81cac3e20e09/assets/component_templates.zip'

    try:
        # Use the get_object API to download the file
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Get the file content from the response
        file_content = response['Body'].read()

        # Save the file content to a local file
        local_file_path = '/tmp/component_templates.zip'
        with open(local_file_path, 'wb') as f:
            f.write(file_content)

        # Unzip the file
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp')

        print(f'File downloaded and unzipped successfully: {file_key}')

        for root, dirs, files in os.walk('/tmp/component_templates'):
            for file in files:
                if file.endswith('_body.json'):
                    file_path = os.path.join(root, file)
                    template_name = os.path.splitext(file)[0][:-5]  # Remove the "_body" suffix

                    with open(file_path, 'r') as f:
                        template_content = json.load(f)

                        try:
                            response = client.cluster.put_component_template(name=template_name, body=template_content)
                            if response['acknowledged']:
                                print(f'Created component template: {template_name}')
                            else:
                                print(f'Error creating component template: {template_name} - {response}')
                        except Exception as e:
                            print(f'Error creating component template: {template_name} - {e}')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f'Error: The file {file_key} does not exist in the bucket {bucket_name}')
        else:
            print(f'Error downloading file: {e}')

    return {
        'statusCode': 200,
        'body': 'File download complete'
    }

def install_index_templates():
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Specify the bucket and file to download
    bucket_name = 'ws-assets-prod-iad-r-sin-694a125e41645312'
    file_key = '4192e8ce-704a-4400-8d18-81cac3e20e09/assets/index_templates.zip'

    try:
        # Use the get_object API to download the file
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Get the file content from the response
        file_content = response['Body'].read()

        # Save the file content to a local file
        local_file_path = '/tmp/index_templates.zip'
        with open(local_file_path, 'wb') as f:
            f.write(file_content)

        # Unzip the file
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp')

        print(f'File downloaded and unzipped successfully: {file_key}')

        for root, dirs, files in os.walk('/tmp/index_templates'):
            for file in files:
                if file.endswith('_body.json'):
                    file_path = os.path.join(root, file)
                    template_name = os.path.splitext(file)[0][:-5]  # Remove the "_body" suffix

                    with open(file_path, 'r') as f:
                        template_content = json.load(f)

                        try:
                            response = client.indices.put_index_template(name=template_name, body=template_content)
                            if response['acknowledged']:
                                print(f'Created index template: {template_name}')
                            else:
                                print(f'Error creating index template: {template_name} - {response}')
                        except Exception as e:
                            print(f'Error creating index template: {template_name} - {e}')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f'Error: The file {file_key} does not exist in the bucket {bucket_name}')
        else:
            print(f'Error downloading file: {e}')

    return {
        'statusCode': 200,
        'body': 'OS Initialisation complete'
    }


def lambda_handler(event, context):
    install_component_templates()
    install_index_templates()
    ISM_INIT()
    alias_init()

