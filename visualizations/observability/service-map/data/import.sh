#!/bin/bash

# Variables
OPENSEARCH_HOST="http://localhost:9200"  # Replace with your OpenSearch host
BULK_FILE="bulk_data.json"  # Path to the bulk JSON file
CONTENT_TYPE="application/x-ndjson"

# Importing the data
echo "Importing data from $BULK_FILE to OpenSearch at $OPENSEARCH_HOST"
curl -H "Content-Type: $CONTENT_TYPE" -XPOST "$OPENSEARCH_HOST/_bulk" --data-binary "@$BULK_FILE"

echo "Import completed"
