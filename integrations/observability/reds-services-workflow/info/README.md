# REDS Services Workflow

**What is the integration resource ?**

This is a workflows based integration in which the RED's needed indices are being build as workflow steps

### What is The RED Method?

The RED Method defines the three key metrics you should measure for every microservice in your architecture. Those metrics are:

(Request) Rate - the number of requests, per second, you services are serving.
(Request) Errors - the number of failed requests per second.
(Request) Duration - distributions of the amount of time each request takes.


---
The workflow includes the following steps

 - create a new `otel-v1-apm-spam-*` index to append the `@timestamp` mapping 
 - `reindex` the `otel-v1-apm-spam-*` to the new index
 - setup rollup job to prepare the RED services metrics dimensions and metrics

---

This specific RED services rollup index is generated to answer the following questions:
- average duration by service in hourly time bucket
- max duration by service in hourly time bucket
- success count by service by http status code in hourly time bucket
- errors count by service by http status code in hourly time bucket
- total requests count by service by http status code in hourly time bucket





**What is the integration source protocol ?**

The specific RED services workflow is based on [`otel-v1-apm-spam-*` ](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/traces-1.0.0.mapping). index mapping and data-prepper's traces ingestion pipeline

**What is the integration target protocol ?**

OTEL Traces protocol which simple schema is aligned with

**Which agents would you use to ship this data ?**

[Data Prepper OTEL based pipeline](https://opensearch.org/docs/latest/data-prepper/)

**Would you be using an ingestion pipeline ?**

[Using Data-Prepper's traces ingestion pipeline](https://github.com/opensearch-project/data-prepper/blob/main/docs/trace_analytics.md)

**Which Dashboards would you be using ?**

This is a workflow integration which only prepares the backend assets (indices, queries, transformations, rollups) for the possible usage by API or Dashboards
