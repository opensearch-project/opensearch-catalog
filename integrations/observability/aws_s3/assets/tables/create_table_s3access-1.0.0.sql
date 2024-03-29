CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                                bucket_owner STRING,
                                bucket_name STRING,
                                request_datetime TIMESTAMP,
                                remote_ip STRING,
                                request_arn STRING,
                                request_id STRING,
                                operation STRING,
                                request_key STRING,
                                request_uri STRING,
                                http_status INT,
                                error_code STRING,
                                bytes_sent INT,
                                object_size INT,
                                total_time INT,
                                turn_around_time INT,
                                referrer STRING,
                                user_agent STRING,
                                version_id STRING,
                                host_id STRING,
                                signature_version STRING,
                                cipher_suite STRING,
                                auth_type STRING,
                                host_header STRING,
                                tls_version STRING
)
USING csv
LOCATION '{s3_bucket_location}'
OPTIONS (
  sep=' '
);