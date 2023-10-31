CREATE MATERIALIZED VIEW {table_name}_mview AS
    SELECT
        version as `aws.vpc.version`,
        account_id as `aws.vpc.account-id`,
        interface_id as `aws.vpc.interface-id`,
        srcaddr as `aws.vpc.srcaddr`,
        dstaddr as `aws.vpc.dstaddr`,
        CAST(srcport AS LONG) as `aws.vpc.srcport`,
        CAST(dstport AS LONG) as `aws.vpc.dstport`,
        protocol as `aws.vpc.protocol`,
        CAST(packets AS LONG) as `aws.vpc.packets`,
        CAST(bytes AS LONG) as `aws.vpc.bytes`,
        FROM_UNIXTIME(start) as `@timestamp`,
        FROM_UNIXTIME(end) as `aws.vpc.end`,
        action as `aws.vpc.action`,
        log_status as `aws.vpc.log-status`,
        vpc_id as `aws.vpc.vpc-id`,
        subnet_id as `aws.vpc.subnet-id`,
        instance_id as `aws.vpc.instance-id`,
        region as `aws.vpc.region`,
        az_id as `aws.vpc.az-id`,
        sublocation_type as `aws.vpc.sublocation-type`,
        sublocation_id as `aws.vpc.sublocation-id`,
        tcp_flags as `aws.vpc.tcp-flags`,
        pkt_srcaddr as `aws.vpc.pkt-srcaddr`,
        pkt_dstaddr as `aws.vpc.pkt-dstaddr`,
        pkt_src_aws_service as `aws.vpc.pkt-src-aws-service`,
        pkt_dst_aws_service as `aws.vpc.pkt-dst-aws-service`,
        traffic_path as `aws.vpc.traffic-path`,
        CASE
            WHEN regexp(dstaddr, '(10\\..*)|(192\\.168\\..*)|(172\\.1[6-9]\\..*)|(172\\.2[0-9]\\..*)|(172\\.3[0-1]\\.*)')
            THEN 'ingress'
            ELSE 'egress'
        END AS `aws.vpc.flow-direction`
FROM
    {table_name};