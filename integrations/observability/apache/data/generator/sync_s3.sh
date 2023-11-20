#!/bin/bash

# Check for AWS CLI and exit if not installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI could not be found. Please install it to use this script."
    exit 1
fi

# Parse command line arguments for filename and bucket name
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--filename) filename="$2"; shift ;;
        -b|--bucket) bucket="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if the file and bucket name arguments were provided
if [ -z "$filename" ] || [ -z "$bucket" ]; then
    echo "Usage: $0 --filename FILENAME --bucket BUCKET_NAME"
    exit 1
fi

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "Error: File $filename does not exist."
    exit 1
fi

# Sync the file to the S3 bucket
echo "Syncing $filename to s3://$bucket/"
aws s3 cp "$filename" "s3://$bucket/"

# Check if AWS CLI command succeeded
if [ $? -ne 0 ]; then
    echo "Sync to S3 failed."
    exit 1
else
    echo "File successfully synced to S3."
fi
