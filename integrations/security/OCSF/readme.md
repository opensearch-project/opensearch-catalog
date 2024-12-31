# README
# OCSF 1.1.0 integration with OpenSearch

## Overview
This section provides resources that will help you ingest [Open Cybersecurity Schema Framework](https://schema.ocsf.io/1.1.0/) (OCSF) logs into OpenSearch and use the logs for [Security Analytics](https://opensearch.org/docs/latest/security-analytics/).

 It consists of index and component templates, OpenSearch Ingestion template, [Index State Management](https://opensearch.org/docs/latest/im-plugin/ism/policies/) policy initialization scripts, and saved objects (visualizations and index templates).

## Overview of components
### Index and component templates
Index templates (`schemas/index_templates`) automatically apply predefined settings and mappings to indices. 

Component templates (`schemas/component_templates`) are reusable building blocks that contain mapping definitions. Component templates are used as part of index templates. 

The current set of index and component templates are mapped to the OSCF 1.1.0 standard. The repository contains index templates for the following OCSF 1.1.0 categories and classes:

  - System Activity
    - OCSF 1001 - File System Activity
    - OCSF 1002 - Kernel Extension Activity
    - OCSF 1003 - Kernel Activity
    - OCSF 1004 - Memory Activity
    - OCSF 1005 - Module Activity
    - OCSF 1006 - Scheduled Job Activity
    - OCSF 1007 - Process Activity
  - Findings
    - OCSF 2002 - Vulnerability Finding
    - OCSF 2003 - Compliance Finding
    - OCSF 2004 - Detection Finding
    - OCSF 2005 - Incident Finding
  - Identity and Access Management
    - OCSF 3001 - Account Change
    - OCSF 3002 - Authentication
    - OCSF 3003 - Authorize Session
    - OCSF 3004 - Entity Management
    - OCSF 3005 - User Access Management
    - OCSF 3006 - Group Management
  - Network Activity
    - OCSF 4001 - Network Activity
    - OCSF 4002 - HTTP Activity
    - OCSF 4003 - DNS Activity
    - OCSF 4004 - DHCP Activity
    - OCSF 4005 - RDP Activity
    - OCSF 4006 - SMB Activity
    - OCSF 4007 - SSH Activity
    - OCSF 4008 - FTP Activity
    - OCSF 4009 - Email Activity
    - OCSF 4010 - Network File Activity
    - OCSF 4011 - Email File Activity
    - OCSF 4012 - Email URL Activity
    - OCSF 4013 - NTP Activity
  - Discovery 
    - OCSF 5001 - Device Inventory Info
    - OCSF 5002 - Device Config State 
    - OCSF 5003 - User Inventory Info
    - OCSF 5004 - Operating System Patch State
    - OCSF 5019 - Device Config State Change 
  - Application Activity
    - OCSF 6001 - Web Resources Activity
    - OCSF 6002 - Application Lifecycle
    - OCSF 6003 - API Activity
    - OCSF 6004 - Web Resources Access Activity
    - OCSF 6005 - Datastore Activity
    - OCSF 6006 - File Hosting Activity
    - OCSF 6007 - Scan Activity

### OpenSearch Ingestion template
The OpenSearch Ingestion template (`assets/OSI-pipeline.yaml`) provides a template you can use with an OpenSearch Ingestion pipeline to ingest OCSF data. 

### Index State Management (ISM) policy
The ISM policy (`assets/ISM.json`) rollsover the indexes daily or when they have reached 40GB. The ISM policy also deletes indexes that are more than 15 days old.

### Initialization scripts
The initialization scripts helps set up the component templates, index templates, ISM policy, and aliases in the OpenSearch cluster. 

There are two scripts - one that uses basic auth (`assets/os_init_basic_auth.py`) - and one that uses IAM auth (`assets/os_init_IAM_auth.py`). 

### OpenSearch objects
The OpenSearch objects (`assets/OCSF_objects.ndjson`) contains visualizations, dashboards, and index patterns to help you get started with exploring OCSF data. Visualizations include: 

* OCSF High level overview (All OCSF categories) page
![OpenSearch Dashboard](static/all_ocsf_overview.png)

* OCSF Findings (2000 series) overview page
![OpenSearch Dashboard](static/ocsf_findings_overview_2000_series.png)

* Network Activity (4001) Org level overview
![OpenSearch Dashboard](static/ocsf_4001_overview.png)

* Network Activity (4001) Account Level Drill Down
![OpenSearch Dashboard](static/ocsf_4001_drilldown.png)

* DNS Activity (4003) Org level overview
![OpenSearch Dashboard](static/ocsf_4003_overview.png)

## Installing the index and component templates (IAM Auth)
* This script will install the mappings, aliases, index templates, and ISM policy for your cluster. 

* This method will use AWS IAM SigV4 request signing to authenticate to your cluster. The machine that runs the script will need `ec2:Describe*` and `es:ESHttp*` permissions.

* This is the recommended method if you are using Amazon OpenSearch service. 

1. Download the index (`schemas/index_templates.zip`) and component template (`schemas/component_templates.zip`) zip files. Upload them to an S3 bucket.
2. Download the `os_init_IAM_auth.py` file and open it in a code editor. 
3. Modify the `OSEndpoint`, `region`, `bucket_name`, `component_templates`, and `index_templates` variables to match your set up.
4. Run the `os_init_IAM_auth.py` file in your code editor. It will connect to your cluster and install the mappings, aliases, index templates, and the ISM policy to your cluster. 

## Installing the index and component templates (Basic Auth)
* This script will install the mappings, aliases, index templates, and ISM policy for your cluster. 
* This method will use the OpenSearch username and password to authenticate to your cluster.

1. Download the index (`schemas/index_templates.zip`) and component template (`schemas/component_templates.zip`) zip files. Upload them to an S3 bucket.
2. Download the `os_init_basic_auth.py` file and open it in a code editor. 
3. Modify the `OSEndpoint`, `region`, `bucket_name`, `OS_USERNAME`, `OS_PASSWORD`, `component_templates`, and `index_templates` variables to match your set up.
4. Run the `os_init_basic_auth.py` file in your code editor. It will connect to your cluster and install the mappings, aliases, index templates, and the ISM policy to your cluster. 

2. Download the right initialization script based on how you would like to authenticate to OpenSearch (basic auth or AWS IAM). 
3. Modify the variables in the initialization script. You will need to add your OpenSearch cluster endpoint, authentication information, and the location of the index and component templates.
4. Open and run the initialization script with a code editor. 

## Installing the Visualizations and Index templates
1. Log in to the OpenSearch cluster 
2. Expand the hamburger menu on the top left and select **Dashboards Management** 
![Dashboards Management](static/DashboardsManagementScreenshot.png)
3. Select **Saved Objects**, then select **Import**. 
![Saved Objects](static/DashboardsManagementSavedObjects.png)
4. Select **Import**, then select the `OCSF_objects.ndjson` file. Select **Open** and then **Import**. 
