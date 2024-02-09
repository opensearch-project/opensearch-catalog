# Observability Category: S3 Log Fields

S3 log fields set describes a standardized structured representation of Amazon S3 bucket logs, enabling efficient monitoring, analysis, and management of operations performed on S3 buckets.

## Field Names and Types

| Field Name                | Type    |
|---------------------------|---------|
| aws.s3.bucket             | keyword |
| aws.s3.key                | keyword |
| aws.s3.copy_source        | keyword |
| aws.s3.upload_id          | keyword |
| aws.s3.delete             | keyword |
| aws.s3.part_number        | keyword |

## Field Explanations

- **aws.s3.bucket**: The name of the S3 bucket.
- **aws.s3.key**: The object key in the S3 bucket.
- **aws.s3.copy_source**: The source from where the object was copied, if applicable.
- **aws.s3.upload_id**: The upload identifier, if the operation is multipart upload.
- **aws.s3.delete**: The deletion marker, if the operation was a deletion.
- **aws.s3.part_number**: The part number, if the operation is a part of a multipart upload.

## Fields for KPI Monitoring and Alerts

The following fields are suitable for creating KPIs to monitor and alert when exhibiting abnormal behavior:

- **aws.s3.bucket**: Monitoring operations on various buckets can help identify unauthorized access attempts or abnormal activity.
- **aws.s3.key**: Tracking object keys can help identify frequently accessed or modified objects.
- **aws.s3.delete**: Observing the deletion field can help identify accidental or malicious data deletions.

By using these fields, users can efficiently monitor, analyze, and manage data in S3 buckets, aiding in performance optimization and security management.
