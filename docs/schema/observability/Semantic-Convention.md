## What Do We Understand By Semantic Conventions?
Semantic conventions refer to the commonly accepted significance of words and phrases within a specific language or culture. They facilitate effective communication by establishing a mutual comprehension of our symbolic representations.

## What Is The Role Of Semantic Conventions In OTEL?
In OpenTelemetry (OTEL), semantic conventions are crucial as they prescribe how data should be structured and exchanged among different system components. 
Semantic conventions ensure consistent data interpretation and processing by various services and tools.

They can be used to outline data structure and the connections between different data components. A convention, for example, may stipulate that all data related to a specific resource be clustered together. This allows an analysis tool to readily identify all data items related to a particular resource without individually scrutinizing each data item.

Semantic conventions can also define data significance: a convention might determine that a certain data element represents a resource's temperature. 
This enables an analysis tool to automatically comprehend the data item's meaning, eliminating the need for human expertise.

## What Are The Metric Semantic Conventions?
Semantic conventions standardize metric meanings across diverse software implementations. Having commonly defined metrics simplifies comparing results from various tools. OpenTelemetry has created a set of metric semantic conventions applicable to any software that collects or presents metric data.

These conventions provide a standard set of core dimensions to be employed when recording metric data, including name, description, unit, and type, also suggesting labels to add more detail to the data. Adherence to these norms results in easily understood metrics that can be efficiently compared.

The metric semantic conventions are a part of the OpenTelemetry project, which aims to standardize the collection and storage of telemetry data. The objective is to simplify developers' work with telemetry data from diverse sources.

Along with metric semantic conventions, the OpenTelemetry team has also established standards for logging and tracing data. 


## What Are The Resource Semantic Conventions?
Resource semantic conventions consist of agreed-upon rules for representing monitored resources in telemetry data. These rules allow vendors to ensure their monitoring data is compatible with different systems and tools.

The Resource Semantic Conventions focus on four major areas:

- **Metrics**: Data about a resource's performance. Examples include response time, throughput, and error rate.
- **Spans**: Data about a trace's internal interactions inside a logical unit of work (AKA transaction) . 
- **Attributes**: Information about a resource's physical or logical traits. Examples include CPU usage, memory consumption, and network bandwidth.
- **Logs**: A chronological record of events associated with a resource. Logs are useful for auditing or debugging.
- **Events**: A record of a resource's activities. Events aid in troubleshooting or provide context to other telemetry data. Examples include starting or stopping a service, a disk error, or a user logging in.

### Attributes:
Attributes describe the data's dimensions. For example, network data might include source and destination IP addresses, port numbers, and so forth. 
Metadata about the data itself, such as timestamp or logging level, can also be attributed. Attributes are stored in AttributeMaps, which map attribute keys to values. 
The keys can be strings or other data types, while the values can be any data type that can be represented as a JSON value.

### Events: 
Events serve as significant timestamps or system states in OpenTelemetry. They can be either manually or automatically generated and contain metadata and any relevant data collected at the time of the event.
Events can track system progress through its lifecycle or flag state changes indicative of potential issues.

## Why Are These Constants Significant?
In OpenTelemetry, constants are crucial as they establish a set of definitions and resource types universally accepted, thereby ensuring compatibility between different software implementations.
Metric and resource semantic conventions define a uniform way to label metrics and resources, which is essential for aggregating data from various sources.
These constants give developers confidence that their data will be compatible with other systems using the same conventions.

OpenTelemetry's goal is to provide a vendor-neutral way to instrument cloud-native software. This goal is reliant on shared building blocks across all implementations.
Constants are one of these building blocks and are crucial in ensuring that data from different sources can be aggregated and analyzed consistently.


---


### Semantic Conventions are defined for the following areas:

* [Traces - HTTP](../../../schema/observability/traces/http.mapping): Semantic Conventions for Traces HTTP client and server operations.
* [Metrics HTTP](../../../schema/observability/metrics/http.mapping): Semantic Conventions for Metrics HTTP client and server operations.

Semantic Conventions by signals: (OpenTelemetry)

* [Resource](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/resource): Semantic Conventions for resources.
* [Trace](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/trace-general.md): Semantic Conventions for traces and spans.
* [Metrics](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/metrics-general.md): Semantic Conventions for metrics.
* [Events](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/events-general.md): Semantic Conventions for event data.

---

## Trace Conventions

In OpenTelemetry spans can be created freely and it’s up to the implementor to annotate them with attributes specific to the represented operation.
Spans represent specific operations in and between systems. Some of these operations represent calls that use well-known protocols like HTTP or database calls.
Depending on the protocol and the type of operation, additional information is needed to represent and analyze a span correctly in monitoring systems.

The following semantic conventions for spans are defined:

* [Traces - HTTP](../../../schema/observability/traces/http.mapping): For HTTP client and server spans.
* [Samples](../observability/traces/samples/http)


---

## Metrics Conventions

The following semantic conventions surrounding metrics are defined:

* [Metrics HTTP](../../../schema/observability/metrics/http.mapping): For HTTP client and server metrics.
* [Samples](../observability/metrics/samples/http)
---

> For additional details check the [openTelemetry semantic convention repository](https://github.com/open-telemetry/semantic-conventions/tree/main/semantic_conventions) 