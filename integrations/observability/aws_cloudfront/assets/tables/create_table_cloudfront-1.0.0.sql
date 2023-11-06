CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    log_date DATE,
    log_time TIME,
    x_edge_location STRING,
    sc_bytes BIGINT,
    c_ip STRING,
    cs_method STRING,
    cs_host STRING,
    cs_uri_stem STRING,
    sc_status INT,
    cs_referer STRING,
    cs_user_agent STRING,
    cs_uri_query STRING,
    cs_cookie STRING,
    x_edge_result_type STRING,
    x_edge_request_id STRING,
    x_host_header STRING,
    cs_protocol STRING,
    cs_bytes BIGINT,
    time_taken FLOAT,
    x_forwarded_for STRING,
    ssl_protocol STRING,
    ssl_cipher STRING,
    x_edge_response_result_type STRING,
    cs_protocol_version STRING,
    fle_status STRING,
    fle_encrypted_fields STRING,
    c_port INT,
    time_to_first_byte FLOAT,
    x_edge_detailed_result_type STRING,
    sc_content_type STRING,
    sc_content_len STRING,
    sc_range_start STRING,
    sc_range_end STRING
)
USING csv
LOCATION '{s3_bucket_location}'
OPTIONS (
  sep='\t'
);