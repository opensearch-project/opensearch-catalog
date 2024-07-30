# OpenSearch Docker Compose Setup

This repository contains a Docker Compose configuration to set up an OpenSearch cluster with OpenSearch Dashboards. The setup includes one OpenSearch node and an instance of OpenSearch Dashboards, designed for easy deployment and management of an OpenSearch environment.

## Purpose

The purpose of this setup is to provide a simple and efficient way to deploy and run OpenSearch and OpenSearch Dashboards using Docker. This setup is ideal for development, testing, and small-scale deployments.

## Prerequisites

Before you start, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Services

### OpenSearch Node 1

- **Image:** `opensearchproject/opensearch:${OPENSEARCH_VERSION}`
- **Container Name:** `opensearch-node1`
- **Ports:** `9200` (OpenSearch API), `9600` (Metrics)
- **Environment Variables:**
    - `cluster.name=opensearch-cluster`
    - `node.name=opensearch-node1`
    - `discovery.type=single-node`
    - `bootstrap.memory_lock=true`
    - `plugins.query.datasources.encryption.masterkey`
    - `OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m`
    - `OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_ADMIN_PASSWORD}`
- **Volumes:**
    - `opensearch-data1:/usr/share/opensearch/data`
- **Network Mode:** `host`
- **Ulimits:** Memory lock set to unlimited

### OpenSearch Dashboards

- **Image:** `opensearchproject/opensearch-dashboards:${OPENSEARCH_VERSION}`
- **Container Name:** `opensearch-dashboards`
- **Ports:** `5601` (Dashboards UI)
- **Environment Variables:**
    - `OPENSEARCH_HOSTS=["http://localhost:9200"]`
- **Volumes:**
    - `./opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml`
- **Network Mode:** `host`

## Usage

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/opensearch-docker-compose.git
   cd opensearch-docker-compose
2. **Set Environment Variables:**
 Review the `.env` file in the root directory and with the following variables:
   ```sh
    # OpenSearch version
    OPENSEARCH_VERSION=2.15.0
    OPENSEARCH_ADMIN_PASSWORD=Open$earch123
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=Open$earch123
    
    # OpenSearch Node1
    OPENSEARCH_PORT=9200
    OPENSEARCH_HOST=localhost
    OPENSEARCH_ADDR=${OPENSEARCH_HOST}:${OPENSEARCH_PORT}
    
    # OpenSearch Dashboard
    OPENSEARCH_DASHBOARD_PORT=5601
    OPENSEARCH_DASHBOARD_HOST=localhost
    OPENSEARCH_DASHBOARD_ADDR=${OPENSEARCH_DASHBOARD_HOST}:${OPENSEARCH_DASHBOARD_PORT}
3. **Start the Services:**
   ```sh
    docker-compose up -d
4. **Access OpenSearch Dashboards:**
Open your web browser and navigate to http://localhost:5601 to access OpenSearch Dashboards.

5. **Server Configuration**
The OpenSearch node is configured to run as a single-node cluster with memory locking enabled to improve performance. Java options are set to allocate 512MB of heap memory.

6. **Dashboards Configuration**
OpenSearch Dashboards is configured to connect to the OpenSearch node running on http://localhost:9200.
You can modify the opensearch_dashboards.yml file to customize the Dashboards settings.
7. **Troubleshooting**
If you encounter any issues, please check the container logs for more details:
   ```sh
   docker-compose logs

