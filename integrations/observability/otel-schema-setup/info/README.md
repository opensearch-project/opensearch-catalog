# OTEL Schema Setup

**What is the integration resource ?**

This is a schema setup based integration in which the OpenTelemetry signals are defined using the SimpleSchema index template

![](../static/logo.png)

### What is The RED Method?

The RED Method defines the three key metrics you should measure for every microservice in your architecture. Those metrics are:

(Request) Rate - the number of requests, per second, you services are serving.
(Request) Errors - the number of failed requests per second.
(Request) Duration - distributions of the amount of time each request takes.


---
The workflow includes the following steps

 - create a new `ss4o-traces` index template  
 - create a new `ss4o-metrics` index template  
 - create a new `ss4o-logs` index template  
 - create a new `ss4o-services` index template  

---

**What is the integration source protocol ?**

The OTEL protocol is defined by the open-telemetry specifications and is converted into json schema using the OTEL collector

**What is the integration target protocol ?**

OTEL spec is translated by the simple schema for observability into OpenSearch mapping spec

**Which agents would you use to ship this data ?**

- [Data Prepper OTEL based pipeline](https://opensearch.org/docs/latest/data-prepper/)
 - [OpenSearch Exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/23611)

