# Observability Category: Elb Log Fields

AWS Elastic Load Balancer (ELB) logs contain information that provides insights into the traffic patterns, application behavior, and operational performance of the load balancer. The aws.elb fields capture a range of data points from these logs.

## Field Names and Types

| Field Name                         | Type         | Description |
|------------------------------------|--------------|-------------|
| `aws.elb.backend.ip`               | ip           | Backend IP address of the request |
| `aws.elb.backend.port`             | integer      | Backend port of the request |
| `aws.elb.backend.processing_time`  | half_float   | Processing time on the backend |
| `aws.elb.backend.status_code`      | short        | Status code returned from the backend |
| `aws.elb.client.ip`                | ip           | Client's IP address |
| `aws.elb.client.port`              | integer      | Client's port |
| `aws.elb.connection_time`          | integer      | Connection time |
| `aws.elb.destination.ip`           | ip           | Destination IP address of the request |
| `aws.elb.destination.port`         | integer      | Destination port of the request |
| `aws.elb.elb_status_code`          | short        | Status code returned by the ELB |
| `aws.elb.http.port`                | integer      | Port for the HTTP request |
| `aws.elb.http.version`             | keyword      | HTTP version used |
| `aws.elb.matched_rule_priority`    | integer      | Priority of the rule matched |
| `aws.elb.received_bytes`           | integer      | Bytes received |
| `aws.elb.request_creation_time`    | date         | Request creation time |
| `aws.elb.request_processing_time`  | half_float   | Time spent processing the request |
| `aws.elb.response_processing_time` | half_float   | Time spent processing the response |
| `aws.elb.sent_bytes`               | integer      | Bytes sent |
| `aws.elb.target_ip`                | ip           | Target IP address for the request |
| `aws.elb.target_port`              | integer      | Target port for the request |
| `aws.elb.target_processing_time`   | half_float   | Processing time at the target |
| `aws.elb.target_status_code`       | short        | Status code returned by the target |
| `aws.elb.timestamp`                | date         | Timestamp of the event |
