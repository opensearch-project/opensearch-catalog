# Getting Started
Integrating Kubernetes (K8s) logs into an OpenSearch system enables efficient storage, transformation, and analysis of cluster logs. This document will guide you through setting up Fluent Bit in a Kubernetes environment to collect, transform, and ship logs to OpenSearch.

## Steps
- **Collection Method** - how data can be collected from the emitting components
- **Transformation Method** -  How data can be transformed into a unified schema to better analyze and process
- **Shipment Method** - How data can be shipped into an opensearch index including the index naming conventions
- **Schema preparation** - How OpenSearch prepares the index template to standardize the logs format
- **Analytics** - How OpenSearch-Dashboard can analyze the logs using discover or pre-defined dashboards

### Prerequisites
A running Kubernetes cluster.
An OpenSearch instance accessible from the Kubernetes cluster.
kubectl configured to interact with your Kubernetes cluster.

### K8s + Flunet-Bit main concepts
K8s manages a cluster of nodes, the agent tool will need to run on every node to collect logs from every POD, i.e Fluent Bit is deployed as a DaemonSet (a POD that runs on every node of the cluster).
When Fluent Bit runs, it will read, parse and filter the logs of every POD and will enrich each entry with the following information (metadata):

- Pod Name
- Pod ID
- Container Name
- Container ID
- Labels
- Annotations

To obtain this information, a built-in filter plugin called kubernetes talks to the Kubernetes API Server to retrieve relevant information such as the pod_id, labels and annotations, other fields such as pod_name, container_id and container_name are retrieved locally from the log file names.
The recommended way to deploy Fluent Bit is with the official Helm Chart: https://github.com/fluent/helm-charts

To add the Fluent Helm Charts repo use the following command
```yaml
helm repo add fluent https://fluent.github.io/helm-charts
```

### Helm Default Values
The default chart values include configuration to read container logs, with Docker parsing, systemd logs apply Kubernetes metadata enrichment and finally output to an Elasticsearch cluster.
You can modify the values file included https://github.com/fluent/helm-charts/blob/master/charts/fluent-bit/values.yaml to specify additional outputs, health checks, monitoring endpoints, or other configuration options.


## Collection Method
To collect logs from Kubernetes pods, set up Fluent Bit as a DaemonSet to monitor and forward logs to OpenSearch.

#### Details
The default configuration of Fluent Bit makes sure of the following:
- Consume all containers logs from the running Node and parse them with either the docker or cri multiline parser.
- Persist how far it got into each file it is tailing so if a pod is restarted it picks up from where it left off.
- The Kubernetes filter will enrich the logs with Kubernetes metadata, specifically labels and annotations. The filter only goes to the API Server when it cannot find the cached info, otherwise it uses the cache.
- The default backend in the configuration is OpenSearch set by the OpenSearch Output Plugin. It uses the Logstash format to ingest the logs. If you need a different Index and Type, please refer to the plugin option and do your own adjustments.
- There is an option called Retry_Limit set to False, that means if Fluent Bit cannot flush the records to OpenSearch it will re-try indefinitely until it succeed.
