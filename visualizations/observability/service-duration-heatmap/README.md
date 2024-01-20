
# Service Duration Widget

## Introduction
The Service Duration Widget for OpenSearch Dashboards uses Vega for complex visualization of service interactions.

## Info
This widget graphically presents service duration heat-map, ingested via [data-prepper traces pipelines](https://github.com/opensearch-project/data-prepper/blob/main/docs/trace_analytics.md), aiding in service performance monitoring and troubleshooting.
See additional [instruction](../../vega-visualizations.md) on how to use and build [vega based visualization](https://opensearch.org/docs/latest/dashboards/visualize/viz-index/#vega) in the dashboards.

![Service Duration Visualization](service-duration.png)

## Vega Integration
Vega's integration allows for customized, interactive graph creation, enabling detailed visual analysis of service maps.

## Structure
The widget includes:
- **Data Folder**: Node based Scripts for synthetic data generation for visualization using the [faker](https://fakerjs.dev/api/) framework .
- **Queries**: The actual queries used to fetch the visualized data (whether using PPL or DQL)
- **PPL Query Based Widget**: Vega spec that uses OpenSearch's Piped Processing Language for data querying.
- **DQL Query Based Widget**: Vega spec that employs OpenSearch DSL for data querying.
- **Index Transformation**: Optional index transformation to allow pre-aggregation transformation index to accelerate query performance 
- **Visualization**: The actual `ndjson` visualization predefined with dql based vega specs
- **Self-Contained Widget**: Predefined for use in [Vega Editor](https://vega.github.io/editor/), allowing customization.

## Data Model
Adheres to OTEL specs:
- [Traces Signals Schema](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/traces-1.0.0.mapping) - For traceability.

## Widget Queries

Represent services duration average over a given timely bucket.
 
- **PPL Based**:
Avg duration per service per time bucket
```text
   source = otel-v1-apm-span-* | stats avg(durationInNanos) by span(startTime, 1h) , serviceName | sort - `avg(durationInNanos)`
```
- **DQL Based**:
Avg duration per service per time bucket using the `date_histogram` aggregation and binding the interval to the external dashboard timeframe context
```json5
  {
  "%context%": "true",
  "%timefield%": "startTime",
  "index": "otel-v1-apm-span-*",
  "body": {
    "size": 0,
    "aggs": {
      "time_buckets": {
        "date_histogram": {
          "field": "startTime",
          "interval": {
            "%autointerval%": true
          },
          "extended_bounds": {
            "min": {
              "%timefilter%": "min"
            },
            "max": {
              "%timefilter%": "max"
            }
          },
          "min_doc_count": 0
        },
        "aggs": {
          "time_buckets": {
            "date_histogram": {
              "field": "startTime",
              "interval": {
                "%autointerval%": true
              }
            },
            "aggs": {
              "service_names": {
                "terms": {
                  "field": "serviceName",
                  "order": {
                    "_count": "desc"
                  }
                },
                "aggs":{
                  "status_code":{
                    "terms": {
                      "field": "status.code"
                    }
                  },
                  "status_code_ranges": {
                    "terms": {
                      "field": "span.attributes.http@status_code"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Prerequisites
Required indices:  `otel-v1-apm-span-*`.

## Try Me
[Open the widget in the Vega Editor](todo)
