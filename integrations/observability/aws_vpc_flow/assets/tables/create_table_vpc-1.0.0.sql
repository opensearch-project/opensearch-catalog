CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    version INT,
    srcaddr STRING,
    dstaddr STRING,
    srcport INT,
    dstport INT,
    protocol INT,
    start BIGINT,
    end BIGINT,
    type STRING,
    packets INT,
    bytes BIGINT,
    account_id STRING,
    vpc_id STRING,
    subnet_id STRING,
    instance_id STRING,
    interface_id STRING,
    region STRING,
    az_id STRING,
    sublocation_type STRING,
    sublocation_id STRING,
    action STRING,
    tcp_flags STRING,
    pkt_srcaddr STRING,
    pkt_dstaddr STRING,
    pkt_src_aws_service STRING,
    pkt_dst_aws_service STRING,
    traffic_path STRING,
    flow_direction STRING,
    log_status STRING

)USING csv
LOCATION '{s3_bucket_location}'
OPTIONS (
  sep=' '
);