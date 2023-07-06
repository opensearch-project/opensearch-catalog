# Observability Category: Metrics Fields

The metrics protocol hold all the information used to build the summary / aggregation of the time-series data points in a form that will allow several types of summation information to be accessible.
For additional info [see](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#model-details) 

## Field Names and Types


| Field Name       | Type      | Description |
| ---------------- | --------- | ----------- |
| name | text/keyword | The name of the metric. |
| attributes.data_stream.dataset | keyword | Identifies the data set. |
| attributes.data_stream.namespace | keyword | Specifies the namespace of the data stream. |
| attributes.data_stream.type | keyword | Specifies the type of data in the stream. |
| description | text/keyword | Description of the metric. |
| unit | keyword | The unit of the metric, e.g., bytes, seconds, etc. |
| kind | keyword | The kind of metric (e.g., gauge, counter, histogram, etc.). |
| aggregationTemporality | keyword | Specifies the temporality of the aggregation (e.g., cumulative, delta). |
| monotonic | boolean | Indicates if the value can only increase. |
| startTime | date | The start time of the metric collection. |
| @timestamp | date | The timestamp when the metric was collected or received. |
| observedTimestamp | date_nanos | The precise timestamp of when the metric was observed. |
| value.int | integer | Integer value of the metric. |
| value.double | double | Double/float value of the metric. |
| buckets.count | long | Count of the observed values in the bucket (used in histogram metrics). |
| buckets.sum | double | Sum of the observed values in the bucket (used in histogram metrics). |
| buckets.max | float | Maximum observed value in the bucket (used in histogram metrics). |
| buckets.min | float | Minimum observed value in the bucket (used in histogram metrics). |
| bucketCount | long | The total number of buckets. |
| bucketCountsList | long | A list of counts for multiple buckets. |
| explicitBoundsList | float | A list of explicit bounds for histogram metrics. |
| explicitBoundsCount | float | Count of explicit bounds. |
| quantiles.quantile | double | The quantile value (e.g., 0.95 for 95th percentile). |
| quantiles.value | double | The value at the specified quantile. |
| quantileValuesCount | long | Count of quantile values. |
| positiveBuckets.count | long | Count of positive observed values in the bucket (used in histogram metrics). |
| positiveBuckets.max | float | Maximum of positive observed values in the bucket (used in histogram metrics). |
| positiveBuckets.min | float | Minimum of positive observed values in the bucket (used in histogram metrics). |
| negativeBuckets.count | long | Count of negative observed values in the bucket (used in histogram metrics). |
| negativeBuckets.max | float | Maximum of negative observed values in the bucket (used in histogram metrics). |
| negativeBuckets.min | float | Minimum of negative observed values in the bucket (used in histogram metrics). |
| negativeOffset | integer | Offset for the negative buckets in a histogram. |
| positiveOffset | integer | Offset for the positive buckets in a histogram. |
| zeroCount | long | Count of observed values that are zero. |
| scale | long | The scale factor for the observed values. |
| max | float | Maximum value of the observed metric. |
| min | float | Minimum value of the observed metric. |
| sum | float | Sum of the observed metric values. |
| count | long | Total count of the observed values. |
| exemplar.time | date | The timestamp of the exemplar (an example point that represents the distribution). |
| exemplar.traceId | keyword | Trace ID linked with the exemplar (useful for correlation between metrics and traces). |
| exemplar.spanId | keyword | Span ID linked with the exemplar (useful for correlation between metrics and traces). |
| instrumentationScope.name | text/keyword | Name of the instrumentation scope. |
| instrumentationScope.version | text/keyword | Version of the instrumentation scope. |
| instrumentationScope.droppedAttributesCount | integer | Count of attributes that were dropped due to exceeding the limit. |
| instrumentationScope.schemaUrl | text/keyword | URL of the schema used for the instrumentation scope. |
| schemaUrl | text/keyword | URL of the schema used for this metric. |

---

## Semantic Conventions for HTTP Metrics

The conventions described in this section are HTTP specific. When HTTP operations occur, metric events about those operations will be generated and reported to provide insight into the operations. By adding HTTP attributes to metric events it allows for finely tuned filtering.
* HTTP Server
    * Metric: [http.server.duration](samples/http/http_server_duration_histogram.json) [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpserverduration)
    * Metric: [http.server.active_requests](samples/http/http_server_active_requests.json) [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpserveractive_requests)
    * Metric: [http.server.request.size](samples/http/http_server_request_size_histogram.json) [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpserverrequestsize) 
    * Metric: [http.server.response.size](samples/http/http_server_response_size_histogram.json)  [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpserverresponsesize)
* HTTP Client
    * Metric: [http.client.duration](samples/http/http_client_duration_histogram.json)  [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpclientduration)
    * Metric: [http.client.request.size](samples/http/http_client_request_size_histogram.json) [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpclientrequestsize)
    * Metric: [http.client.response.size](samples/http/http_client_response_size_histogram.json) [see](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-metrics.md#metric-httpclientresponsesize)
