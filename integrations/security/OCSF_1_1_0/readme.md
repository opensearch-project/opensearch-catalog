# README
# OCSF 1.1.0 integration with OpenSearch

## Overview
This section provides resources that will help you ingest [Open Cybersecurity Schema Framework](https://schema.ocsf.io/1.1.0/) (OCSF) logs into OpenSearch and use the logs for [Security Analytics](https://opensearch.org/docs/latest/security-analytics/)

 It consists of index and component templates, OpenSearch Ingestion template, [Index State Management](https://opensearch.org/docs/latest/im-plugin/ism/policies/) policy initialization scripts, and saved objects (visualizations and index templates).

## Overview of components
### Index and component templates
Index templates (`schemas/index_templates`) automatically apply predefined settings and mappings to indices. 

Component templates (`schemas/component_templates`) are reusable building blocks that contain mapping definitions. Component templates are used as part of index templates. 

The current set of index and component templates are mapped to the OSCF 1.1.0 standard.

### OpenSearch Ingestion template
The OpenSearch Ingestion template (`scripts/OSI-pipeline.yaml`) provides a template you can use with an OpenSearch Ingestion pipeline to ingest OCSF data. 

### Index State Management (ISM) policy
The ISM policy (`scripts/ISM.json`) rollsover the indexes daily or when they have reached 40GB. The ISM policy also deletes indexes that are more than 15 days old.

### Initialization scripts
The initialization scripts helps set up the component templates, index templates, ISM policy, and aliases in the OpenSearch cluster. 

There are two scripts - one that uses basic auth (`scripts/os_init_basic_auth.py`) - and one that uses IAM auth (`scripts/os_init_IAM_auth.py`). 

### OpenSearch objects
The OpenSearch objects (`assets/OCSF_objects.ndjson`) contains visualizations, dashboards, and index patterns to help you get started with exploring OCSF data. Visualizations include: 

* OCSF High level overview (All OCSF categories) page
[[image:all_ocsf_overview.png||height="150" width="900"]]

* OCSF Findings (2000 series) overview page
![OpenSearch Dashboard](./images/all_ocsf_overview.png)

* Network Activity (4001) Org level overview
![OpenSearch Dashboard](images/ocsf_4001_overview.png)

* Network Activity (4001) Account Level Drill Down
![OpenSearch Dashboard](images/ocsf_4001_drilldown.png)

* DNS Activity (4003) Org level overview
![OpenSearch Dashboard](images/ocsf_4003_overview.png)

## Installation instructions
1. Download the index and component template zip files. Upload it to an S3 bucket or save it to your local machine.
2. Download the right initialization script based on how you would like to authenticate to OpenSearch (basic auth or AWS IAM). 
3. Modify the variables in the initialization script. You will need to add your OpenSearch cluster endpoint, authentication information, and the location of the index and component templates.
4. Run the initialization script. 
5. Log in to the OpenSearch cluster and upload the OpenSearch objects in the **Saved Objects** screen under **Dashboards Management**.  