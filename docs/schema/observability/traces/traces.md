# Observability Category: Trace Fields


## Field Names and Types


| Field Name                | Type         | Description                        |
|---------------------------|--------------|------------------------------------|
| traceId                   | keyword      | The trace ID.                      |
| spanId                    | keyword      | The span ID.                       |
| traceState                | text         | The trace state.                   |
| parentSpanId              | keyword      | The parent span ID.                |
| name                      | keyword      | The name of the trace.             |
| kind                      | keyword      | The kind of the trace.             |
| startTime                 | date_nanos   | The start time of the trace.       |
| endTime                   | date_nanos   | The end time of the trace.         |
| droppedAttributesCount    | long         | The count of dropped attributes.   |
| droppedEventsCount        | long         | The count of dropped events.       |
| droppedLinksCount         | long         | The count of dropped links.        |
| status.code               | long         | The status code of the trace.      |
| status.message            | keyword      | The status message of the trace.   |
| attributes.serviceName    | keyword      | The name of the service.           |
| attributes.data_stream    | object       | Data stream attributes.            |
| events.name               | keyword      | The name of the event.             |
| events.@timestamp         | date_nanos   | The timestamp of the event.        |
| events.observedTimestamp  | date_nanos   | The observed timestamp of the event.|
| links.traceId             | keyword      | The trace ID of the link.          |
| links.spanId              | keyword      | The span ID of the link.           |
| links.traceState          | text         | The trace state of the link.       |
| instrumentationScope.name | keyword      | The name of the instrumentation scope.  |
| instrumentationScope.version | keyword   | The version of the instrumentation scope.  |
| instrumentationScope.droppedAttributesCount | integer | The count of dropped attributes in the instrumentation scope. |
| instrumentationScope.schemaUrl | keyword  | The URL of the schema for the instrumentation scope.   |
| schemaUrl                 | keyword      | The URL of the schema.             |
