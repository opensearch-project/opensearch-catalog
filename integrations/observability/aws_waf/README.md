# AWS WAF Integration

>  AWS WAF Logs schema, see protocol details [protocol](https://docs.aws.amazon.com/waf/latest/developerguide/logging-fields.html)

## What is AWS WAF?

AWS WAF (Web Application Firewall) is a web application firewall service that helps protect your web applications from common web exploits that could affect application availability, compromise security, or consume excessive resources. AWS WAF provides firewall rules to filter and monitor HTTP/HTTPS requests based on specific conditions.

AWS WAF can be used for various purposes, such as:

- Mitigating web application layer DDoS attacks
- Blocking common web attack patterns like SQL injection and cross-site scripting (XSS)
- Filtering traffic based on IP addresses or geographic locations
- Controlling access to specific parts of your application

AWS WAF allows you to define rules to match specific conditions and then take actions, such as allowing, blocking, or rate-limiting requests, based on those rules.

See additional details [here](https://aws.amazon.com/waf/).

## What is AWS WAF Log Integration?

An integration is a set of pre-configured assets bundled together to facilitate monitoring and analysis.

AWS WAF log integration includes dashboards, visualizations, queries, and an index mapping.

### Dashboard

![](https://raw.githubusercontent.com/opensearch-project/opensearch-catalog/main/integrations/observability/amazon_waf/static/dashboard.png)

---
## Loading Integrations via DashboardManagement

To update an integration template navigate to the DashboardManagement and select [savedObjects](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects) and import the new artifact:

1) Download the `amazon_waf-1.0.0.ndjson` artifact from the [catalog release page](https://github.com/opensearch-project/opensearch-catalog/releases/edit/aws_waf-1.0.0)

2) Go to the [DashboardManagement -> savedObjects ](https://localhost:5601/_dashboards/app/management/opensearch-dashboards/objects)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/d96e9a78-e3de-4cce-ba66-23f7c084778d)

![](https://github.com/opensearch-project/opensearch-catalog/assets/48943349/a63ae102-706a-4980-b758-fff7f6b24a94)

3) Once there select import to load the recently downloaded integration artifact (`amazon_waf-1.0.0.ndjson` suffix)

4) Open the [waf integration](https://localhost:5601/app/integrations#/available/amazon_elb) and install
