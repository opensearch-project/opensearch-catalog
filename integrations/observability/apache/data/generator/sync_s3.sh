#!/bin/bash

# Check for AWS CLI and exit if not installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI could not be found. Please install it to use this script."
    exit 1
fi

# Parse command line arguments for filename pattern and bucket name
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--filename) filename_pattern="$2"; shift ;;
        -b|--bucket) bucket="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if the filename pattern and bucket name arguments were provided
if [ -z "$filename_pattern" ] || [ -z "$bucket" ]; then
    echo "Usage: $0 --filename FILENAME_PATTERN --bucket BUCKET_NAME"
    exit 1
fi

# Find files that match the pattern
matching_files=($(find . -type f -name "$filename_pattern"))

# Check if any matching files were found
if [ ${#matching_files[@]} -eq 0 ]; then
    echo "No files found matching the pattern: $filename_pattern"
    exit 1
fi

# Sync each matching file to the S3 bucket
for filename in "${matching_files[@]}"; do
    echo "Syncing $filename to s3://$bucket/"
    aws s3 cp "$filename" "s3://$bucket/"

    # Check if AWS CLI command succeeded
    if [ $? -ne 0 ]; then
        echo "Sync to S3 failed for $filename."
    else
        echo "File $filename successfully synced to S3."
    fi
done
