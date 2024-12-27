CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    version int,
    account_id string,
    interface_id string,
    srcaddr string,
    dstaddr string,
    srcport int,
    dstport int,
    protocol int,
    packets bigint,
    bytes bigint,
    start bigint,
    `end` bigint,
    action string,
    log_status string,
    vpc_id string,
    subnet_id string,
    instance_id string,
    tcp_flags int,
    type string,
    pkt_srcaddr string,
    pkt_dstaddr string,
    region string,
    az_id string,
    sublocation_type string,
    sublocation_id string,
    pkt_src_aws_service string,
    pkt_dst_aws_service string,
    flow_direction string,
    traffic_path int
) USING parquet
OPTIONS (
  recursiveFileLookup='true'
)
LOCATION '{s3_bucket_location}'
