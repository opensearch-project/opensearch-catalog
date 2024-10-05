# Sample command: ./alias_init.sh -e <OpenSearch Cluster Endpoint> -u <myusername> -p <mypassword>
#!/bin/bash

# Parse the command-line arguments
while getopts ":e:u:p:" opt; do
  case ${opt} in
    e )
      ES_ENDPOINT=$OPTARG
      ;;
    u )
      ES_USERNAME=$OPTARG
      ;;
    p )
      ES_PASSWORD=$OPTARG
      ;;
   \? )
     echo "Usage: $0 -e <ES_ENDPOINT> -u <ES_USERNAME> -p <ES_PASSWORD>"
     exit 1
     ;;
  esac
done

# Create the ISM policy
curl -X PUT "$ES_ENDPOINT/_plugins/_ism/policies/rollover-expiration-policy" \
-H "Content-Type: application/json" -u "$ES_USERNAME:$ES_PASSWORD" -d '{
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
                            "delay": "1m"
                        },
                        "rollover": {
                            "min_size": "40gb",
                            "min_index_age": "1d",
                            "copy_alias": false
                        }
                    }
                ],
                "transitions": []
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
        ],
        "error_notification": {
            "channel": {
                "id": "gmJ6kpEBF-og_hBde60R"
            },
            "message_template": {
                "source": "",
                "lang": "mustache"
            }
        }
    }
}'


# Create the vulnerability_finding index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2002-vulnerability_finding-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-2002-vulnerability_finding-*",
        "alias": "ocsf-1.1.0-2002-vulnerability_finding"
      }
    }
  ]
}'

# Set the vulnerability_finding index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2002-vulnerability_finding-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-2002-vulnerability_finding"
      }
    }
  }
}'

# Create the compliance_finding index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2003-compliance_finding-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-2003-compliance_finding-*",
        "alias": "ocsf-1.1.0-2003-compliance_finding"
      }
    }
  ]
}'

# Set the compliance_finding index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2003-compliance_finding-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-2003-compliance_finding"
      }
    }
  }
}'

# Create the detection_finding index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2004-detection_finding-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-2004-detection_finding-*",
        "alias": "ocsf-1.1.0-2004-detection_finding"
      }
    }
  ]
}'

# Set the detection_finding-2004 index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-2004-detection_finding-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-2004-detection_finding"
      }
    }
  }
}'

# Create the authentication index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-3002-authentication-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-3002-authentication-*",
        "alias": "ocsf-1.1.0-3002-authentication"
      }
    }
  ]
}'

# Set the authentication index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-3002-authentication-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-3002-authentication"
      }
    }
  }
}'

# Create the network_activity index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-4001-network_activity-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-4001-network_activity-*",
        "alias": "ocsf-1.1.0-4001-network_activity"
      }
    }
  ]
}'

# Set the network_activity index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-4001-network_activity-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-4001-network_activity"
      }
    }
  }
}'

# Create the dns_activity index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-4003-dns_activity-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-4003-dns_activity-*",
        "alias": "ocsf-1.1.0-4003-dns_activity"
      }
    }
  ]
}'

# Set the dns_activity index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-4003-dns_activity-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-4003-dns_activity"
      }
    }
  }
}'

# Create the api_activity index and alias
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-6003-api_activity-%7Bnow%2Fd%7D-000000%3E -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{}'
curl -X POST $ES_ENDPOINT/_aliases -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "actions": [
    {
      "add": {
        "index": "ocsf-1.1.0-6003-api_activity-*",
        "alias": "ocsf-1.1.0-6003-api_activity"
      }
    }
  ]
}'

# Set the api_activity index settings
curl -X PUT $ES_ENDPOINT/%3Cocsf-1.1.0-6003-api_activity-%7Bnow%2Fd%7D-000000%3E/_settings -H 'Content-Type: application/json' -u "$ES_USERNAME:$ES_PASSWORD" -d '{
  "index": {
    "plugins": {
      "index_state_management": {
        "rollover_alias": "ocsf-1.1.0-6003-api_activity"
      }
    }
  }
}'

# Download the component_templates.zip file
component_templates_url="https://raw.githubusercontent.com/Kevlw-AWS/opensearch-catalog-security/security-lake/integrations/security/OCSF_1_1_0/schemas/component_templates.zip"
component_templates_local="component_templates.zip"
curl -o "$component_templates_local" "$component_templates_url"

# Extract the component templates from the zip file
unzip "$component_templates_local"

# Create the component templates in the Opensearch domain
for file in component_templates/*_body.json; do
    template_name=$(basename "$file" "_body.json")
    curl -u "$ES_USERNAME:$ES_PASSWORD" -X PUT -H 'Content-Type: application/json' -d "@$file" "$ES_ENDPOINT/_component_template/$template_name"
    echo "Created component template: $template_name"
done

# Download the index_templates.zip file
index_templates_url="https://raw.githubusercontent.com/Kevlw-AWS/opensearch-catalog-security/security-lake/integrations/security/OCSF_1_1_0/schemas/index_templates.zip"
index_templates_local="index_templates.zip"
curl -o "$index_templates_local" "$index_templates_url"

# Extract the index templates from the zip file
unzip "$index_templates_local"

# Create the index templates in the Opensearch domain
    for template_file in index_templates/*_body.json; do
        template_name=$(basename "$template_file" "_body.json")
        curl -u "$ES_USERNAME:$ES_PASSWORD" -X PUT -H 'Content-Type: application/json' -d "@$template_file" "$ES_ENDPOINT/_index_template/$template_name"
        echo "Created index template: $template_name"
    done
