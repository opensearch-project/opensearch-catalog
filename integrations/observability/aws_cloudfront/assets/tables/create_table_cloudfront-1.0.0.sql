CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    log_date DATE,
    log_time TIME,
    x_edge_location VARCHAR(50),
    sc_bytes BIGINT,
    c_ip VARCHAR(50),
    cs_method VARCHAR(10),
    cs_host VARCHAR(255),
    cs_uri_stem TEXT,
    sc_status INT,
    cs_referer TEXT,
    cs_user_agent TEXT,
    cs_uri_query TEXT,
    cs_cookie TEXT,
    x_edge_result_type VARCHAR(50),
    x_edge_request_id VARCHAR(255),
    x_host_header VARCHAR(255),
    cs_protocol VARCHAR(10),
    cs_bytes BIGINT,
    time_taken DECIMAL(10, 3),
    x_forwarded_for VARCHAR(50),
    ssl_protocol VARCHAR(50),
    ssl_cipher VARCHAR(50),
    x_edge_response_result_type VARCHAR(50),
    cs_protocol_version VARCHAR(20),
    fle_status VARCHAR(50),
    fle_encrypted_fields VARCHAR(50),
    c_port INT,
    time_to_first_byte DECIMAL(10, 3),
    x_edge_detailed_result_type VARCHAR(50),
    sc_content_type VARCHAR(100),
    sc_content_len BIGINT,
    sc_range_start BIGINT,
    sc_range_end BIGINT
)
USING csv
LOCATION '{s3_bucket_location}'
OPTIONS (
  sep=' '
);