# Observability Category: VPC Flow Log Fields

VPC flow logs field set describes a standardized structured representation of VPC network traffic flow information, enabling efficient monitoring, analysis, and management of network interactions across different cloud instances and services.

## Field Names and Types

| Field Name                     | Type    |
|--------------------------------|---------|
| aws.vpc.version                | keyword |
| aws.vpc.account-id             | keyword |
| aws.vpc.interface-id           | keyword |
| cloud.region                   | keyword |
| aws.vpc.vpc-id                 | keyword |
| aws.vpc.subnet-id              | keyword |
| aws.vpc.az-id                  | keyword |
| aws.vpc.instance-id            | keyword |
| aws.vpc.srcaddr                | ip      |
| aws.vpc.dstaddr                | ip      |
| aws.vpc.srcport                | integer |
| aws.vpc.dstport                | integer |
| aws.vpc.protocol               | keyword |
| aws.vpc.packets                | integer |
| aws.vpc.bytes                  | integer |
| aws.vpc.pkt-src-aws-service    | keyword |
| aws.vpc.pkt-dst-aws-service    | keyword |
| aws.vpc.flow-direction         | keyword |
| aws.vpc.start                  | keyword |
| aws.vpc.end                    | keyword |
| aws.vpc.action                 | keyword |
| aws.vpc.log-status             | keyword |

## Field Explanations

- **aws.vpc.version**: The version of the VPC flow logs.
- **aws.vpc.account-id**: The unique identifier of the AWS account.
- **aws.vpc.interface-id**: The ID of the network interface for which the flow log was recorded.
- **cloud.region**: The region of the AWS resource within the provider's infrastructure.
- **aws.vpc.vpc-id**: The ID of the VPC for the flow log.
- **aws.vpc.subnet-id**: The ID of the subnet for the flow log.
- **aws.vpc.az-id**: The ID of the availability zone for the flow log.
- **aws.vpc.instance-id**: The ID of the instance for the flow log.
- **aws.vpc.srcaddr**: The source IP address of the traffic.
- **aws.vpc.dstaddr**: The destination IP address of the traffic.
- **aws.vpc.srcport**: The source port of the traffic.
- **aws.vpc.dstport**: The destination port of the traffic.
- **aws.vpc.protocol**: The protocol of the network traffic.
- **aws.vpc.packets**: The number of packets transferred in the flow.
- **aws.vpc.bytes**: The number of bytes transferred in the flow.
- **aws.vpc.pkt-src-aws-service**: The AWS service that the flow originates from.
- **aws.vpc.pkt-dst-aws-service**: The AWS service that the flow is sent to.
- **aws.vpc.flow-direction**: The direction of the network flow, either ingress or egress.
- **aws.vpc.start**: The start time of the flow.
- **aws.vpc.end**: The end time of the flow.
- **aws.vpc.action**: The action taken for the network flow, either ACCEPT or REJECT.
- **aws.vpc.log-status**: The status of the logging, usually "OK".

## Fields for KPI Monitoring and Alerts

The following fields are suitable for creating KPIs to monitor and alert when exhibiting abnormal behavior:

- **aws.vpc.packets**: Monitoring the number of packets can help identify unusual data transfer patterns, which could indicate a security concern.
- **aws.vpc.bytes**: Monitoring the number of bytes can identify potential bandwidth issues.
- **aws.vpc.action**: Keeping track of rejected actions can help identify potential security concerns or misconfigured security rules.
- **aws.vpc.flow-direction**: Observing the flow direction can help identify potential security concerns or network configuration issues.

By using these fields, users can efficiently monitor, analyze, and manage network traffic within their VPC, aiding in performance optimization and security management.
