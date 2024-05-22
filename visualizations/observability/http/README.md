
# Http Network Graph Widget

## Introduction
The Http Network Graph Widget for OpenSearch Dashboards uses Vega for complex visualization of service interactions. It's designed to map out http relationships .

## Info
This widget graphically presents http network sankey graph, ingested via [data-prepper logs pipelines](https://opensearch.org/docs/2.4/data-prepper/pipelines/configuration/sources/otel-logs-source/) or using standard OTEL collector ingestion alternative.
See additional [instruction](../../vega-visualizations.md) on how to use and build [vega based visualization](https://opensearch.org/docs/latest/dashboards/visualize/viz-index/#vega) in the dashboards.

## Vega Integration
Vega's integration allows for customized, interactive graph creation, enabling detailed visual analysis of http network graph.

## Structure
The widget includes:
- **Queries**: The actual queries used to fetch the visualized data (whether using PPL or DQL)
- **PPL Query Based Widget**: Vega spec that uses OpenSearch's Piped Processing Language for data querying.
- **DQL Query Based Widget**: Vega spec that employs OpenSearch DSL for data querying.
- **Visualization**: The actual `ndjson` visualization predefined with dql based vega specs
- **Self-Contained Widget**: Predefined for use in [Vega Editor](https://vega.github.io/editor/), allowing customization.

## Data Model
Adheres to OTEL specs:
- [Http-communication sematic convention](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/logs/communication-1.0.0.mapping)
- [Http with aws-vpc flow logs](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/logs/aws/aws_vpc_flow-1.0.0.mapping)

## Widget Queries

Represent http source / target based aggregation.
 
- **DQL Based**:
Avg duration per service per time bucket using the `date_histogram` aggregation and binding the interval to the external dashboard timeframe context

- **AWS VPC based Query**
```json5
  {
  "%context%": "true",
  "%timefield%": "@timestamp",
  "index": "ss4o_logs_vpc-*-*",
  "body": {
    "size": 0,
    "aggs": {
      "table": {
        "composite": {
          "size": 10000,
          "sources": [
            {
              "stk1": {
                "terms": {
                  "field": "aws.vpc.srcaddr"
                }
              }
            },
            {
              "stk2": {
                "terms": {
                  "field": "aws.vpc.dstaddr"
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

- **HTTP sematic convention based Query**
```json5
  {
  "%context%": "true",
  "%timefield%": "@timestamp",
  "index": "ss4o_logs-*-*",
  "body": {
    "size": 0,
    "aggs": {
      "table": {
        "composite": {
          "size": 10000,
          "sources": [
            {
              "stk1": {
                "terms": {
                  "field": "communication.source.address"
                }
              }
            },
            {
              "stk2": {
                "terms": {
                  "field": "communication.destination.address"
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

## Screenshot 
![](https://raw.githubusercontent.com/opensearch-project/opensearch-catalog/main/visualizations/observability/http/static/http-network-graph.png)

## Prerequisites
Required indices:  `ss4o_logs-*-*` Or `ss4o_logs_vpc-*-*`.

## Try Me
[Open the widget in the Vega Editor]([Open the Chart in the Vega Editor](https://vega.github.io/editor/#/url/vega/N4IgJAzgxgFgpgWwIYgFwhgF0wBwqgegIDc4BzJAOjIEtMYBXAI0poHsDp5kTykSArJQBWENgDsQAGhAATJJhSoA2qHFIEcNCABOSAO4ARBShkAzNjuSY0oHDrY44OzAE9tSMmR19M7cRCUikwANnCUTAxQANZwmBAgAL4ymHoBFlZoqiBuTtoZCAwhpiBwAB722vKYDAiUsa6UEJjRAIzSIEgJ6M1tSVKguVroBUUl5ZXo1bX1cI29AEwdXdqL-YOueSOWhcUdEzpVCjOybFAA+lBsDOI2Mis9NABeWokAujLESCEMcN2DbDY0TQrRSNE0snO1xsqDM3wgcBk5wgMCQOlk-xybEUIRBMggUSgfwgZiKeJAEGiNBwTlkaAADOYkDQwnTUPTkhg6JjMNjvmgFgsZMgysirj40OIiiEZDBuVk3pzPN5fP4eUhQsNQEgzJhnOcGrYKS12uhWgA2BaUVoAFitrQWQlaAHZnR01mb6ZQvV6FvT6f0QJEYnFutlDahQL1TSBWj7vZQ-QH8S0lmbLda7dbHdbXYHThcrjcYa1Qca+p6E77-e7U9oLfasw6nXn8c9hqXkqAI1GTfWM7b7TmXW6U9E07H49WA5yC5drrcQWXo-3G0OW6PyxO41XEzW2y8l+9EieuyB1JptOI2LI-u7rjoido9EYTB1Ukh0jsshstiAzCyeqHDIBzaAAhN41w4AAynAYRQLyOgAAQAD4oUhkEMDBcFwAhlhNCaSEALxEUh0x1NGqHoZh2HwYhBHjsRpHkQxSxnkM+Q7GM+wVIcUzHBRJoANQsWs9zdCAhrsZswz-mwIR0uYNBwRiWTlu0Y5LB8nRhsaSAxB03g4AAknSioDDkMmcVY3EgbxRw1IJ+nRExSEAOTRm5SEAPxkQJDGtCJ-mLEhqB+Y5rFBRFK7iasliYAAYspCnrJZf7NM5hkOFhTDuCoekGdpYguEaAEqXFLhJeVMiWLefFyH8RLiLINDiGQgZlSljyHtJf6jHsdmTCAAAULGuPSUUzK4rQAJQEEssXoK4UBJOZagaLJNEJPiD5Pug163ttORpCS34qL+snKj4FB6llUG5WpGUGTIRmmSA2mdap+UQO2701Xgj21H9OlqbyOLvb1slPcCL3ZTgD3fYohU7SVkb-slbIgK9ikgLVzhVI1cDNa17Wcp92hg-ykPWbs4z2T0UDfHAw1ua4blSOFU30jNywSdATOyAAmjOFkcdsNkDaU9MUozYQs2zHNjbNvOrLLcBC+01Pi7TPFDaJSMuSR7meSr6A6DQZBYAAMhqcGpWLckS3Tev+ZTIQEKcyCtfLbkzcorRvKbIBOI+ROKGQrxreeG0E80rUKP4AByN53jtDCh1eKdHR+X6ZOdaWyQBIRAbr9X685rkeambmrWeF6yerEdHWI6d7eeWfvidBQ-gX+SAfjg1l8FBuVybWsgCEgLRFhHRmA4CCx346h+BIyeHR0EaSXMs8Y7phraQ8yg5GiEc2FHDshK10Q4AoMAdJYymLugMAP08Ejg-iqJ-i1ngSPyaeh0FkaUCDMmY+0Vv5ZaPNOQt1DgADWAdLfmcs3JlHZsbE0vskJCSQkwT8sh9A0FkPQFmaDoEpBPnEIBaMQEyzAazdBLFFA6FPpQKBgZmGnwQTQpBatSHoKruOX2SRx79WdvVNIEcfZ+3pG8AAtMg5mDCIHRXbDzRaxoHCxAAOpEPoPbKy2tbJSxdqol4Hs2Be3ENI-2gcNEhyauHSO7x8RqzDOtS86AyjvkMUGfBHRJGyUIcQu+MhPbMkkIjPomlgY31kC1NqAB5BgJd2TegEDIOJCSyDGXEOIfGaSACcAg64xyWj4v8l98logCZ+CO2h4AWywB0cJrUjTVCUO3deSlypLU1qUzxIAriT2Ar3dAtV464hkIE7QjM9RkEsO4MJliIntLfGbAwxhFA716epERFl66rANonDa2dfETPUFM3QdThhH2grtLQMhDB-CXgnCQwNWmRKPjFLcEMD5lDvPnB+YdtBMGxLyBerimbaG8SBcQVxbxGmKEwOCmIsLVC1DkcoMIoxqyOc5E5mgjrk3QF8H4rxTxnmBU-CecBdTujxeUlxIBkA6GiO4sZwdb4dEOegRucAACyaIYb-nnms7ZfLZBN0DFAS+OA0CpF+HChFmL0UKExc0LRtzBgvO0DRWCdFLBIQAGTGownDA1uF6LQxIoI1oNcoVhFmfJSwOyuq-LPIo51Iy3WYxXMyzVQI4C6JCaVDGRytUhv0ZyG++i0Ykq5dGlMWrEk3ygHQPKUYLaXPAvqnCeFkKmqQsNGiAAJNgpAdABVcvrNoVFzVQXLZW1iNbh7jhmj5JCXpCmhS7ZQAAzIGJ4rVbzeLRj9MgOb0AQQtfmxCJqzUlrhk25w1aja1taPWstFbV0hXXW2hYHbfKbrCiLLE8k-DyvHdm-k-FoqERwV5QASYTuWwZzQSjFH0AB1MBeRwQUBQo1grtg5uzb0ZgsGPqQtBlmb6AOYCAxFBxYdPCInctaAApJB9yM0a4nllDuvivYU1pozUaMlvwQSUtFr4nwCEeVlKxnDIVbLZ5irRh0vVcMEiciJiq4BtwCmgCLricdjKhkutGQm7GgZglxtxdCrxHQ8HNSo5yNVt00ZjoU06pTPT3XQ0DJm9GuzFFCzPa4NMwnw2gNZILTWSkQghFTfpMjaMKPDC9OaTkvIL3UiNBOqdch-LYzfV5aDf6kLwcQzMN2oGpDgew+F4tkXossWQ7cVDoHMNJdw-sjAhGw1OZc+mtw5HviUdQK0ajF0KbYrY5Y8VnStqBlakBfSfhSBoDhCEBEyqU5Gg05i7TFIb2iboSgtBKiZjQw7TgmLdRzaW0wDbFFIRO0qYIXomA-C5tIQABy9rkft8hIBloBbG9oBbTQ1bmbfaJW79m5psXuJfSdF3J23uCxFJb1tbbrd8m5MIuovJhTcr939gY8EIiqZijz2gEBENkE6sm79tFwCaTikA8P0BgpSj5+r17PvjY1BAa7ZnhZyIewLJ7SEAB8SFWj9s7SxULYO8Onho3+GiLT1nZF5d9pACVLDQRfvoAAgk5joHn3HMpzqdPO2QHZFxLoPLjUFLUFtrtpPjA2aGCaIyAMoK0idBbkzAeaRnyvkrQP2jkMhzfW8q-t+3GAMfLad8MO3nOWXCo5Q7HnMgBc0QAEp-DiA1heHH1mC+FzoUXbAJdS94-CvXoAw5CYkzofJOgQ9IBagwTEOPvOOdE6AHHIAADECUBAJWdAlcXgZA2xE99oSvUBWgd47031IQao133cxV4YCxOSNI9-GmzoAefP3d80-DIBHcT96VPuG2hHc+6G0aRwrmyuD5t1V+fL9K1b9I7v8vQ+GSUGdD71l7Ke4Oz1GUO4IA2vOA6zQLrsJ4SIlKKnxF+vUlQBjcw1l8mMoI19ttAxdgYQvQSkZBzsl8uoV9wCZ9McoCigYDKAMlcYzAzAEQYQR9Xts1W90BHF8ZORoc4JWo4cL90BEd4kUdzA0dZ8scK88c6QCcn8SCQAE99AkJJdcRKVFRhC2xicOVg9l1CtPhaDgBOR3l844BSBbgJIAABGiFjaIVABAa4BEKQkATfdAYAaMVAcuGIW1TyBdd9agHQEyWQDmRYEw4eZycw6uSw1nGw0yRIVKRQsOCSbQwvOAaEDoAwkAWQ2uA5RjPNQ1UZHHHrPrXGL5dPJQ+IbQNQ5jYVVAWVGgGIMCYInADFbQIwg2Rw+9Zyewk0EombA2FwtoLyItdw2w8o8cSopyMwoiQRBYOos1Bozw7w5I-3XxLI56X3NlCQqCMPfAgxb+UIIY4EZlEIuI5xbSK4cQACdqNGGZNGOZcgRZNSSvAQG0AAIX7UKUKQ6Er3NHpEKQWAAGFkwq9DB+1Lj9tzRzjCkXR6RDj9tzibjxd9sABRcXf484wwc0Q4mvTcSvQ4wpP4-bb4mQSvQwP4w4m0AQc48XcXc0AQAQV4hE-450c0c0G0G4iGe4R8IrcbfYo4k4s4pUHwJQazKXdAKk4404wMWHALXvFvZkg41k2kzJblcdLk2SFkmkwMOjLHETNvXksUzkHQIoDVYU6U6ktkmBL+RUrVZUvkpvVwBAPHCkrU2UlIQnRkyk2QMwOAAQOlDhPQFkA0nklU-knIOgXTUAYZV1Zk80uAftOAb4mBNwV0rGBgIhOAORZFO2CfJkqvfbWQQpfbJAQdTkMgYM28ORPwTAQMqUz0i0n0v02GKCNMl0zFLMqvL03MwMGiBRZgdMzMlkM0nM30-LJAMoGgHkbI6IG4yTNvBYQpftfbG0TcT5Tsn1ZknsvsgcrKIhYcj0qvMc-st0Cg5yTCVTdAeXG+HwRcTkRfZsRkN3NA1AF3XcpAFJNgH6Q8NGZXOgDoFYxQVqCSLJEmERIAA))
