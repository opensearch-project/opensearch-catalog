
# Service Map Widget

## Introduction
The Service Map Widget for OpenSearch Dashboards uses Vega for complex visualization of service interactions. It's designed to map out relationships and dependencies in microservices architectures.

## Info
This widget graphically presents service map interactions, ingested via [data-prepper service_map pipelines](https://opensearch.org/docs/2.4/data-prepper/pipelines/configuration/processors/service-map-stateful/), aiding in performance monitoring and troubleshooting.
See additional [instruction](../../vega-visualizations.md) on how to use and build [vega based visualization](https://opensearch.org/docs/latest/dashboards/visualize/viz-index/#vega) in the dashboards.

![Service Map Visualization](static/service-map.png)

## Vega Integration
Vega's integration allows for customized, interactive graph creation, enabling detailed visual analysis of service maps.

## Structure
The widget includes:
- **Data Folder**: Node based Scripts for synthetic data generation for visualization using the [faker](https://fakerjs.dev/api/) framework .
- **Queries**: The actual queries used to fetch the visualized data
- **PPL Query Based Widget**: Vega spec that uses OpenSearch's Piped Processing Language for data querying.
- **DQL Query Based Widget**: Vega spec that employs OpenSearch DSL for data querying.
- **Visualization**: The actual `ndjson` visualization predefined with dql based vega specs
- **Self-Contained Widget**: Predefined for use in [Vega Editor](https://vega.github.io/editor/), allowing customization.

## Data Model
Adheres to OTEL specs:
- [Service Map Schema](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/services-1.0.0.mapping) - Represents service interactions.
- [Traces Signals Schema](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/traces-1.0.0.mapping) - For traceability.

## Widget Queries

### Nodes Queries
Represent services in the system.
- **PPL Based**: Counts occurrences of each service.
  ```text
  source = otel-v1-apm-span-* | stats count(serviceName) by serviceName
  ```
- **DQL Based**:
Aggregates service names from spans.
  ```json5
  {
    "%context%": "true",
    "index": "otel-v1-apm-span-*",
    "body": {
      "size": 0,
      "aggs": {
        "services": {
          "terms": {
            "field": "serviceName",
            "size": 10000
          }
        }
      }
    }
  }
  ```

### Edges Queries
Represent interactions between services.
- **PPL Based**: Maps service connections.
  ```text
  source = otel-v1-apm-service-map* | stats count(serviceName) by serviceName, destination.domain
  ```
- **DQL Based**: 
Aggregates connections between services and their destinations.
  ```json5
  {
    "%context%": "true",
    "index": "otel-v1-apm-service-map*",
    "body": {
      "size": 0,
      "aggs": {
        "services": {
          "terms": {
            "size": 10000,
            "field": "serviceName"
          },
          "aggs": {
            "target": {
              "terms": {
                "size": 10000,
                "field": "destination.domain"
              }
            }
          }
        }
      }
    }
  }
  ```
## Navigation
The Service graph map offers a new navigation capability from the service graph into a dedicated dashboard including the 
selected serviceName as part of the target dashboard's filter.

This feature is using the `"href": {"signal": "datum.link"}` vega url navigation capability.

Here is how the `link` field is structured:

 - target URL: `http://localhost:5601/app/dashboards#/view/single-service-correlated-dashboard-1_0_0_ID`
 - target dashboard (navigating using dashboard ID) : `single-service-correlated-dashboard-1_0_0_ID`
 - filter in the target dashboard: `_a=(filters:!(....,query:(match_phrase:(serviceName:' + datum.name + ')))),...'`
   - here the `datum.name` is the parameterized user mouse click selection


## Prerequisites
Required indices: `otel-v1-apm-service-map`, `otel-v1-apm-span-*`.

## Try Me
[Open the widget in the Vega Editor](https://vega.github.io/editor/#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-AZR2n8+VsUAj2N9uh6x0cZUPL-ICuAp91rqugwKAAPtxoiGIJZS0vjCRjWG2jMZfLxF5lH3nUZ+TJgFvFgXi1o30Uagn44ywxDY74z6GVMrQiAAA4uyHAVzIOIiPAKLlhkRx2ClAKKwBVsgzAUPQ+gCGZBtq1ihtiqEOIHywxJ1j7GsVcfRvxu4nVqHTGcqwYoeoZoQaJa24BNrcyhbLqARQSFwJpQkOIIEBmMrtHkv57Sdzgt4culi4A11FDXVQIcOLcq9TqmuulQroHHKNYBNSTAYZmsIEoFo8qBNHrXQJkN0q3aPIQCkBNxMEQmF3mw7+ST258O1fqwoRrbEBQdYK0V5lEBGttCgiGvTr7ispAAGJ2CQGQAS1nyqQwFLdoTfKEDdmmMygUEwJAxePOCrtnIKqIeASqyGKG0MtDluVvaM9K3ZOQz7TjNAYOGqgxj5G1UMxQR2m1aYKA9rebgONYn-V2R6KjWODCWqUiOAKCOec6RaVsCgAAfQckUY9KgpWYWGGtMcagngM-QHOXI+HKTuETtutqHPueFBHKoamgvdiqFF98cXqQCgKFnJgT0x47BsDIDLuXXIExc55yr1AAv3oa58GLltEvgLm5MZbxXNvj1VBkA74XaB5glu1y7323LMBwScA9s370LcZCt0r3naAzbq4D8W+YWvQA67MI+A6sePfx698r49Kf-ejBvc7zFEu4JcrHl9fP8uE-e8vX7oX5ench6rx4IEYRujFF+45BvnvrfF5b6n9vmeQA64gDAV9H8Y+y4L+zkfSfc2t8d0sSvcNkB5Xd43ovq+r1l7HMHrPofsje6sAvuPy-E+26P23scVQzF+2QMemuBj0CiH7D7KEHIICv6+Sf6+xrTfYPYZB6jKqLyxbDZN6j7RA4R-6GTtrF6tBPC1yv4-YQF9BQHNgwGaotoIFhrYjoHAGYHgF+44GFRE4R7DYM5EHoD5CFBMgJTAEOQ9hFb1BrTv7XxUglDj57BrRazUHPqs5X4rCkHDLkEoCUG4E0FxbH4ZD-CbDZqc6KE6acxro5AU7HhU5IB6L-BShjzohuQbSEh05n5d5M4SAzASRwGr786pyzY8Eka5BzbaQ66einh77D537HqLBb7vx64G5G7NCm4+GF4r624BGd5LI17zgYoRG37N6oDzCBEgDmBJEK5RF87pGS45DS5D6RF+GqDpE2a96s4D4ZRFHJGj7Fo2J5HwBS6xBZH2G24LBOHuBWI8FtGYBqFt6c4TCAjuCc7BBFAlD5rOSc7IjvSc69GBCZCziKp3j06h5eGjg1HZElGpHpEz5z5X6tEH625pGxHLRQCX7WCHE5GlGnEgBMS16JGbHzH1G3GIBIC75PFHG5G3FM4xAWAeTHaD6L777XEvGWEpA5594bHAm+EpGn5T6h7Kr2whHE4m7X5L5bFwkNGE6v7TAgy1zf6SC-6ygAGgFAFSEPbYA+Q5RJx2AKB06gzOGUCuHLGtCE7KHoSMldEeQABCSxHkIAhcGBoBWBshIh+B8xDBZhEIkhsw0h2Bch029BGROEo2Eowp7gYBMhmEVB0BtBM23JmAfJbhJUypHJXJ3R6pwBJubAOQcUOUBQ4Qy4RKOhSAeheiOucINJfBDJapnRlp7JvpfScAAAcilv6R5GGT5kKWQTfOtJAeKfqaNlGbyqLA1MhAKFjtNsJN0SmQKGmbVBBuBKliyFoa6VwQZESFYNoYcG6dTvisAqNv1J1oCSVousGSkGWbWe6WZCSYAXtLXI9vkHwEcDIEwRMEwFXm0HPB2YTv4AybToKd6XSQyTmQKYGe0HcUdt1iVjGVISKRQSqeDM4XsAmRCeCLkINvgS2TufNgdmuZgNdIAtBA+c2ducVnsGqegF2ZTvWanH2WSQOcAUOVyhQKOSAOOTgJOZuQ+UuahHgJuYuTibSfSZuWqRuZyTeR+YKbKYzgedqeaaNqebqe-BeTkFefqVhSdu1qNk+SWbMDauWe2ZWdWlrK6T2f+f-v2RhLXDaXaTRr7I6fCMGW+eIF1thTINPh2cuahZyXCITouZyQ+WyQwdOcpXBVrGht2MetOThawcMnxfaYJXRAyM4aJeJSdhkDrrBTJQyfJSxEGZWSpUeZyURRpU4DEPlJuXpR-vufHDIHQO9FUWOLejIFDsBC7G4vAuFaeFjKwugH7PLoleVNpMlUshuLDDIDmsjvAqcljFXjlUspio+t8GlRLn+NSD5mFRGpFVkvAhAKyldGoPrMliahGi1Y2t6kciAIFeyNhcWoulCE-G8D4JQM-qVUJmGsEAoDSnPENXjrVVWs6VrJ2rNhIRNZpiAFoRkFoThD+boX+VvD-NLIVd+dWZuitAxj1fwXCBofon5VqUoThI4GcmKYzhjn1GmRmVjjavVNNq1jBh1G9B9HdJ6D9FINBioqgMhFaQ9aKS5b7LNWeQlR9ZNF9eBJmfqq1XAH9fgQDZ1MDQNp9N9HAI9JDeTNDcWTYoTiTRYaGuVSbutLXEIVYAvOzjvhxKALWaxeTtzTJSkJBVjKmpyaUGoCbIYPMEwGoBkKLSbHLVLTLWLVLQAJzS0yClBS0mxVBi0y1S1i0mw3IgClBIBqCVBIDLCzI6gk0ZBJAFBoCw4YYK4c2LXZIkxC2no9CnWsipolWcxfRg1ci21sD230bs3vGc1zxRUpBNLu1yiwJR1TIe0SGE7IDuA5B021xmDKBebAK7USxCWzzc1nXrrlk+xOZBWgZ2Soah2YRjwpazygosJQi2me2R11V6lxajbxZax9BfVEoZaXSsBuZZn4EPnd16h91awD3vRD3RbXSlDK3zDK2LDK3K2NbdDcmlgQB2Bhgk03TsFrS-TTZd2QUvQCjAAvgIomyi7dVHgFCKoBiXIu3wLH3Bnj2921Tpbsaz0j36lj0A2T1wDT3uCz1dQIoCCpESHElcWAU8XWnVlZ0ojd6soMA0BcrP14Xxw+wz5IAGU0gVn+wAAaIMyNc8AdN0oND06o02r9lZlAfQt9wZOsJDJFZDXoN0-tVDQOcWtD-slAUo3VD5xDs8pDe9t0JNR9Epo9TJDDWMD5zDIjrDYjnD4N3DsB0jhp-DU8uFCV+FCp1BxO4g8wFFPDGj3R-DAowiND+BXdUoUg1jSZb9MGVjUjf9Mj14Upp6DgTU+lcpejb16AJjw2XjcAKg3ytUGgHU02ITyKayKYAACj6AzNE9YN48mC1WGIsCbBslGHE4k47J46k3AFHL5X45qfDaQ5k9kzoXFiE-MKmGGIkwQPzock9TiEU8sDoyAeU4eZUw5CWCk2QA4IsA051e+ATAIMmATLveQ+IwHY9A43FmPQwx4wjSeAULIMQ10-KQE+GPEJWIM8M6MzWk2hM1MzM+w8TfM-Y640s0yQI6s+aes7uMw3dbXBJhDiyM87IHsAkADfzMZU6VzcTp2dWWgX7nXT5g3W-Cwl2v5KAFGuDP+kU1jCExg+gDU8E0U-MP1MrRoFjNlW3UtfIcE0Lps-leiyS5QN8686nBAvHe3egNdIAE2k10WM0M7sXtizw2XdADn9-d39igmNajlsZjHk79gDwDoDB2C9S9K9a9r470ViW9O9YjB97gkj+pvDhk1ABQEwZ9F9o119EQt9-KlLYzEA9UVqGgqA2TUD0EXKKDr2EAfoj2XItcNAyAZ6gLIMRdzwLp3NZdLO7Ildwm8OCR9dg4wbIMcEnL0prw2AeAhABAJijklAl0Uoqb4glADkCABAOA1gBAHAWw0AVID2hWE4BAhWnka02his2cDq6UuUZAcEVR-UWbBAWAuAVOcATrR4-UMwCAOAlJcAlABbNgJVkyoA-g2QdABVRL2S4DDMS7BsQTlAx+ljAo6aOwwuFMuTYcxS-QO7owm727j+jsPshL8V4YkNmo6NPYwrv1uN+p+NHUt7ooqAYjlDqj02Kz-a+LPs8717YY5Noo97dgj7RK6M-1CWgNoHn7szKjpN1D+BDz-7WM6YlLVwPskSlLGYCBgIwIlL-whHLg2DiIyIlLCISIygPsuIjQxH1IDHPsFIVI+DDLxLrHa61iOHoWs8M7UAc7IMiLo1jwj60E+ufVzKrr3rHrXrXI1hQLNBJO-rbFgbAVwbLmYGYbELDkULUbzcDd7gcbInGAib+ARAUACg4g7b58-U47lATO3k-cOQObYQBAAgCwBAiwhghgiw3nvnPnagiwY71g61U78Fs75klLS7RMK7-C02G7wiZ7uwe7-CB7-CR7j+p72w57iYBM8whgBLlLIHH1d7n9GNP1UHz7LWsHnU77CHlz37yHIrf7-OFLHH2Shg0zoH4HkHWs0HeNdXb7qNH7yjEjKH+pDzGHT9nX8C2HOgOKPB17+HKppHxHAInB5HNHI1Xt1HlHdHTHEd179HRJQQPK3HlLXH+Dk7PCNW-HZggn0Xs8In4D4n0EZeMn7rwBnrbr+dJlwLKky1vNILQbzmobJh4bkLrdGVhUoAsbwnm0ZnuAFnBAVn2bQETK5xfVo7ubnAfguQ-UMACgBATgjgRWEABAksIQbrIqvIPbCg-UZetnEgoXE7aOMLkXT3QHCdIAsXGolAAgGTiX2XyXuXqXLMysDMYYWXuwOX4gx7EAF7WVlL3XpXfQn1FXD7VXA3NXw2r7DXX7E3rXyv0kqvPXo3fXOvONev799Xo3jXDgHDxv0203PsmHc34UWMuHnv6Aq3JHnBvva3W3i6FHygQf+3tH0QR3jHeIWM13hWV3F3N3vH9307j3QnL3m0b34nxyDFRKew7zOGf4Nt-zA1PrhdILwPpdunkbEXAnmfCLm0we18q4QfX9g9igg3L7dXvGjmsHbAjgYYHfM9VFjkk3cWLwiY3yjqnUarf4h9E-w2p9irm9gEqrsz6rmrcWp9Oy59l9lAxrt9zdiq5rArnfCg3ftXPdPGfGANg-w-5-o-751FIrU-M-YcHU8-jN2-y-erOAiYVfsq3X4XMneh2H-kv11bMEDWB-QwDfTion84Aj9EUIj0QioAYic1e+nAAADyGfZ7k3zQEt95krda9s1QNgWsOqJzb1FjCYhiA4e8bCEmwHLrwRL2lLd9lbyxpPshUQ3G-iNw16ahHef8OZlw1-bdUeejLa+BrzRpa8IO1vK-vr2G7wdxu1zEVgI3C53db4NcJEPlFfSUtpst1XPqU3BiOJ6aW1ADFSD2CKdfWVfVTilR9h-NYOgeDTuDyZRV0HaUPQzsAB9gRt9OEXDlpS2uhHRAqbLQDiDFyh8Fo6xXWeOELpI0Q5G9LUADEP4L6CSC0fOPlnzQF3FYe7LGwh+jNYZD6QM6Fjsn0T4FCYoigBQA4CxjUgtgy3XnssiHa71GqA2MgdjSDQQBKBbVJtGNF9zqwZ0WgbqmW1fTxAK0DAsFPayghAA)

---

## Acknowledge

This graph widget was originated from [Deneb-Showcase work](https://github.com/PBI-David/Deneb-Showcase/blob/main/README.md)
