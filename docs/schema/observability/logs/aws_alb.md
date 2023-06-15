# Observability Category: Alb Log Fields

AWS Application Load Balancer (ALB) logs contain information that provides insights into the traffic patterns, application behavior, and operational performance of the load balancer.

## Field Names and Types

| Field Name              | Type    | Description                             |
|-------------------------|---------|-----------------------------------------|
| `aws.alb.name`           | keyword | The name of the ALB.                    |
| `aws.alb.type`           | keyword | The type of the ALB.                    |
| `aws.alb.target_group.arn`| keyword | The ARN of the target group.             |
| `aws.alb.listener`       | keyword | The listener of the ALB.                |
| `aws.alb.protocol`       | keyword | The protocol of the ALB.                |
| `aws.alb.request_processing_time.sec` | float | The request processing time in seconds.   |
| `aws.alb.backend_processing_time.sec` | float | The backend processing time in seconds.   |
| `aws.alb.response_processing_time.sec` | float | The response processing time in seconds. |
| `aws.alb.connection_time.ms` | long  | The connection time in milliseconds.     |
| `aws.alb.tls_handshake_time.ms` | long | The TLS handshake time in milliseconds. |
| `aws.alb.backend.ip`     | keyword | The IP address of the backend.          |
| `aws.alb.backend.port`    | keyword | The port of the backend.                |
| `aws.alb.backend.http.response.status_code` | long | The HTTP response status code of the backend. |
| `aws.alb.ssl_cipher`      | keyword | The SSL cipher used.                    |
| `aws.alb.ssl_protocol`    | keyword | The SSL protocol used.                  |
| `aws.alb.chosen_cert.arn` | keyword | The ARN of the chosen certificate.       |
| `aws.alb.chosen_cert.serial` | keyword | The serial number of the chosen certificate. |
| `aws.alb.incoming_tls_alert` | keyword | The incoming TLS alert.                 |
| `aws.alb.tls_named_group` | keyword | The named TLS group.                    |
| `aws.alb.trace_id`        | keyword | The trace ID.                           |
| `aws.alb.matched_rule_priority` | keyword | The priority of the matched rule. |
| `aws.alb.action_executed` | keyword | The executed action.                    |
| `aws.alb.redirect_url`    | keyword | The redirect URL.                       |
| `aws.alb.error.reason `   | keyword | The reason for the error.               |
| `aws.alb.target_port `    | keyword | The target port.                        |
| `aws.alb.target_status_code `| keyword | The target status code.                 |
| `aws.alb.classification`  | keyword | The classification.                     |
| `aws.alb.classification_reason` | keyword | The reason for the classification. |
