# Running OpenSearch Joining Existing Cluster
### Create the External Network
Before running any docker-compose files, create the opensearch-net network:
`docker network create opensearch-net`

### Run the Main OpenSearch Cluster
Run the initial opensearch cluster :
`docker-compose -f os-cluster.yml up -d`

Check cluster status and health:
```
curl -X GET "https://admin:my_%25New%25_passW0rd%21%40%23@localhost:9200/_cluster/health?pretty" --insecure
curl -X GET "https://admin:my_%25New%25_passW0rd%21%40%23@localhost:9200/_cat/nodes?v" --insecure
```

Connect to the dashboard:
`http://localhost:5601`
    -   User:`admin`
    -   Password:`my_%New%_passW0rd!@#`


Next run the joining node:
`docker-compose -f nginx-node.yml up -d`

Check cluster status and health:
```
curl -X GET "https://admin:my_%25New%25_passW0rd%21%40%23@localhost:9200/_cluster/health?pretty" --insecure
curl -X GET "https://admin:my_%25New%25_passW0rd%21%40%23@localhost:9200/_cat/nodes?v" --insecure
```
