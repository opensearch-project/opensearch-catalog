
# Service Errors Widget

## Introduction
The Service Errors Widget for OpenSearch Dashboards uses Vega for complex visualization of service interactions.

## Info
This widget graphically presents service errors heat-map, ingested via [data-prepper traces pipelines](https://github.com/opensearch-project/data-prepper/blob/main/docs/trace_analytics.md), aiding in service performance monitoring and troubleshooting.
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

Represent services errors average over a given timely bucket including the histogram of the different http responses ranges.
 
- **PPL Based**:
Errors average over a given time
```text
   source = otel-v1-apm-span-* | stats avg(durationInNanos) by span(startTime, 1h) , serviceName | sort - `avg(durationInNanos)`
```
- **DQL Based**:
Services errors average over a given timely bucket including the histogram of the different http responses ranges -  using the `date_histogram`, including binding the interval to the external dashboard timeframe context
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
                "aggs": {
                  "avg_duration": {
                    "avg": {
                      "field": "durationInNanos"
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
[Open the widget in the Vega Editor](https://vega.github.io/editor/#/url/vega-lite/N4IgJAzgxgFgpgWwIYgFwhgF0wBwqgegIDc4BzJAOjIEtMYBXAI0poHsDp5kTykBaADZ04JAKyUAVhDYA7EABoQxKHKhJMaANqhMdQXDS64AD03oAygBkA8gAILcAE7EaUOBDsARBk43tZCEUQCGY9TAM0EAAVGgQ4QQBPB2dXd29ffzkHWzt4DWQcYNVBNicopkEkKABrEABfJQB3GgATejQAZgAGbqV4GjIsIxDMOCLUACYATkaQVo0UVFBZJHiohcwBPybg4iRBBg8RpDIyJz49OSDlkD14gH0mBlq4TBvQZ9f37VAauESDyQEAeEEwThosjIUUm3UmABZ+N0AIz8ZGdaLdADsqDEnVQPUovW6AC1gv9EmhkVjumJ0QjkcS+vM2FAHqoGLJzPDOsilPc4E8Xv8frcviKbjoQBSgSCwRCoTC4YiUWiMdjUL1Nd0ib0yUoKVSaXSZrCmUpWqz2WxOdzeUoIKk3ILVvEPiy2RyuQ9nE4yg8GDgcM4njbZK00MzQggHmx6CHLZ6w+ZOp0lOK3pK-gCogAzP1cuDh4KJ622ql0pRIYhkB6tTJXeS3faHQy4rFY5EANmRyMoYnh0y7XYAHCOsWJ6o1s5T0LA4LUbe8ne4S1aveYu5MqzW6w2AiMW0c0HTB6Ou5RU+PukOsSOpwoZ1FSkhWmQi84NGU10ny6h4cy1a1vWfiNoeBzHqgvbdJ0dLIrM07Sjm6A4H69ZQJg6hbKUZCOi4zo-mWXJdCOO7Afucjga2aCdvBI6dJQ8LwlinSjvCkzIg+T5zkgTjLvhq4WuuyZdF2ZF7qBB7NhBbaMjMxJcUhs4gIgSA0IIeFpIYQm-sRUyAbuIFZE2oBHrJN7wl2WLTJQI6TohhroAAjgwcYeCu2kekR5jImI4lGWB0nUf+PTTJM94OchIQwDQQaQrhHmERuFb+RRJnKDJVLwuOzGTJQ6KpoVhWKY5IBQL4FyyFAiSaQROneVSfIgEBEnGVRkGdCOvQMfCA59b1A3wiVUWvrVgleclUEGeRkmUUFkEsam3RTgAuqtw2AsCoLgvFSoIkiqLopiOIDtquqkuSyHUrS9JMeaE0iagW7TPycSChmoqfMKma-EpsrbQq0LoLC+2qkdGpar0536kpRo3aaTLMqWk3PQ6HkPK6xy3MjyY+k4fpOAGQYhkwYYRpqDoMDGcbwITON-pMWLpt9opSqV+ZyGMxb1ZNkxiH5zWGWl7VtmICJdiiOqTIzvU3iOnGRcpqFsOhmGLDhY2efTenTPCqWzelZlUp01mTF2NmsddHGM12G3Pmwr7vrIn6YN+POPeb+ttfN5kTubNKUCx0zot0PK24rUTzouDD8VpSWPdlXuBaZmW4gisHTFidvoLmcAaL4cC5lUCUCVrwl-uxSdSSnwV3gBUNjjeYudQrj6wzxfGa-Hf49FXc015BjIotMYgXsO48T+HbelRcqgIPE4bGV37sM3rgszd7A9tvLd6dEOlCT+PWcR+go2JSvendn3hup75PaDjqyJ89nZUVUW1XLw9f5P9fItdNLXYerdkPsOCK08oqqXUp-bWPltzr1asnDKwVezoislifKICrLrXqGtRW-15S7WBsqA6apjq4nhASHUxIYaOWunSToCIaTEgvuYTsa8BRCm+O6D6WY-pbQIYqIhoNDrqhxJDKhepLqzjoU-MKiMWE0WRGvTWGM1hY1ADAvGBMibBkJqTTk5MoxU1jPGOm5c9KdWZlw367MCxcwjAoqYdlf4+xPAOei3QLwjkAb5O8usX7K1VlhA4bAS5x0cUOFxW8qRbgApZfKmdg4T2PuA5SL43wflAm7L+ekupRKQYPbEvUwoSFpC-KONQlzQPMZuMS8CArVwKaLdidJpgMW8axTpgDym8VjnVHJ3ImotQaf3JpVJQ7YhHvlDiI8n7wXsqkvMedMAFyLqcapukUykXqcLVxqAuq635gfMQfjmKsQQos9AkCNLnwGWgWE+SjZTWmGFHsgcX6zzYPPIsmwAgbIavpR5qcd7ZTaZQC53EQAuTcv8yavkgXBTEN0EcYURyUEmC-CAMU4pQlhY9eFOyDZ-ygl2ACSLlo4Owak-BO1BEgBBiqERZD+ZnWoVIuG9C+byLuU9Syr1Hg8JGIK1AbMAQ0sBntRlpCIbdFZZIg0V1jSyLNMwnlpK6kqMxu6TRvp-SBl0aGAxkZKbU1MXWGpokrEShsVFDmhZuY8rNnA4Zuzom4l7HeeWB9sp2TPBik+IBAkvDVthUJeK-xjgRYPXsHj2nInlgm+NrdIXpKdi7bJMC0Ce0JZvMZU1LKTFggxEeXYxbUk6uU+A0c+njUzbiOpLqiV7IHHzEc8I+zPwDeoTuty62WJzYgp5jJzbTG8bZdijIxY+JfrnfOFw1lhP6X251Qsm1uoTR2eEjFPGdsuSAT53zF6NnDXpBEUbt6FsZNlRiYh6JFU6C-a5J6fINtXbmodjJOjtovE-BZkKz6l27pfNMA7GlPKxOxNp5S35VRqr2i1UEV0b0HanWCSit33sw+HXBuDqX8NpUDelxCwaiNxGISh0N2VQSVQwvE9061D22Rw4VX1rEipnOKwhRHhHSrEbKqGbKFXSKVQjejCHGNo1Lqot0IwdX4z1cTPRZNjUhGMTTBMCGTlWp+ux9uIA7X2KA9yGC560A+t7J1A+EtQ5DnCpWhclSY7PsamvRt77U70JHmC0tpyWIpJTQ7DJzssnlEcRZ0zqAR5Tszsc7KVk+ZT0hUGjCwSNbwc2eMl6oHRlPIHD2L9-YxBDiWozP9enu01rLhl-ZQy30oeQdiXoI48qdgloOTqjNH3ICgelgFDCIvodHoyWyE4Z3LNWcXZzUxX3IbA8C6kpaJCdUsr5ZbiXyswY-r13mAs3P1Y6tlXdkLoVjCm2e7LN9grZXgsHQOSTJ7+b01i2KOB4pndc3VubyD+aeo7fZHDG1ON0oZSQ8GJ0uxyoukJjl9JR5ieq-RJmdw3qcOtWKFmvCZT4YlUIqVYPtSQ5oYq+Gcj4cAsR5JrS0n1EDK0Qpg1+jiwU1U6a2m5rqu9W06zSFBmflGa6CbCLYs8S2cYr1T9dkwFJbQsG1LYbtv4pvAN2JYU8pWTHC85FZsX6psyV+ULPLpjTQQV9wp-NwpFbF0xa3TF7PVqm1iGbJucsea3CbXytlfEorOT0ntgHHGjwGzBUde90V2TYRbx77NxvzsmwriuSHneXcgh4mC7TMOpiGgGg9C9fnXHj6ej7s2XfBWa7e9EpS733pfgB8JjrjcjOT22Cc8EGLrdKk+gv5gHkXeJagtr6Dk0bfxu-OD-ueXxoi7BSyNl-tUo49jrjIOSPMoh4SQT7cZG0aN6qutWIZj8vehjoVx-dNY7lARyVoPSPiMo9D6jJOVW9EcfvrLmq1HapqXTwm+qSbKeZ9GCYmznWkxFzpjranYnzo4uFFlntqbs0ryKeHdresxC3gEjLilurPLuPnWiPANqmH5j+mxBxLSNrgGrrsFvrvzqgB2ANuiOxDyLPhHuHnbo5pVtQaOELr6rCOgo7sxLSGOP6nuhVlNu2kHmwvBP2HMrMtLGNnOoXHHjgQhqxBFvRHiHSLZGOFoVoRCnpjnj8kvF3vckXknsStZM1jyGrkdnprXkughj3nASXgtCOlulnnup3kodVg4Z9k4bJLRt2Gir5C-Cdu5J4QCgSo4U3m4rrBxIxJgsfADpSg+PpmUMgOYLoIkMGFENIJREoMrLopgMpKcOcJcH8pQMxhjpQIKskeCEgIELmKkb9OoIIOVFUGMFEAKAAGKpEaAAAUMcUAAACrxI6L0ZsFTJQOfgDPFAoAAOQACkAAmvwPMQgCsa0NEPMQABKoDzEACyuxFglA8xVgJIsxAAlAoHYAsQAEJ2DzGtBXFLH3E7H7EXHBDAgdFvQNBtzNGtEaBtjzD5wIDlEo48JVHH5Vg3AhAeQQBeCLA-GgBrLYBFjaAwmlxwkIkrRQlonIlcwgBrRtx4mokir6ZtFcyUDv5ugQnWLYnNSSjolaQACSsgDRBJiEfxDAbRgJ4xIJmsLJDRkxOYOJ6AXcHJBw-x7R6AvJlJHkApbAlAkRlARsIpZUIkOCeRvEawvCmMUQMUQwwgQwmgaMBgGEIwhRWRKEbAkIxpIAc0IACANojobApA5Qq0SgyATgdQtwFpgJs8mgcw78KshCoAJgIwuYNACQ5MyO6w-ImRgJZQrQkIBwPxIAs4SJkZgg0Zn8vpUQsgXyyZggqZEZggRZtwEZUZkcIkcZlpUKDAdR4Q-gpAwQ0ABwbYoAfgUIbYWgIAAAxJ0QAMKdFYgACiyIwQ-ZA5I5nRXgYgE5nRAAggOQOeOPOQuSOLOZ0BOV4J0fCDcZMAueyUoAYE7OTBoh4FABCDgIFCAAAGp8D8BWAiB2CWgeCyCzGYB2BYpsBNB2Dxh2ARlOBgh2BmR2BsC5h-nwB2Ank-KzGeDnCviRlchflsB2BMl2AMCOitB2AABezgqFmALQ6QkIkFcAIFMkngvEfglISgZkkofQfQQ8fQ5KjF5oXKz+LFdJ4QkQpJPgBsOQ9gLJrQpgdgvRXgFgTJ5xwQsqdgAAcqhXxcZHYAANx2AsUyUjkmDuDXkBAHAZBEq4ajB+j-AADqbQHQtwqg4YdAUkUoOAWpCAepgwMAhpwwSgiA15s4uYBwjotFt8Gpeay0-IbAbAggegEwUoFZWZUQYpRJmZ0ZAowQ3FgJ8J7RiEUV0ZyUSRbcmwSwW8WYlKx5SAiQzgv0np3pGRtZYwZgSVpg5gIAAASiOV4KgHYFsTaE4EkCkBifpUpVscsnYHsUgDgHYHYMEA0XpCADYDHBGbaa0GGQSBLBaNIhFGtHSVZRGUDJ8NUDUOcP-n2bmPCLmFiLmLmMEPZa0EmYIroGwBMIyOmHGK7I5VNMeYXCmMyBCEaV0EFcoJGbsLcPKGwP8GgLIFyYIHMBNfVdEB4J+QANK8SkzyBVgmA0DujnBtBoDeU3JFVMAJADmhXfjoCVA7XBBVC42CDdFcgWA0B4VGivQRBtig2llzBIAo0QAAAaIwZQSF9VpM2AXya43Wsg+NpQ5QRNVQtQwQ4FuYjo5gAsegtQ+N38zICtNQNgp1stJ4r0tQ1NtN+y2tNQIthNIAxNktONCQwxl1hCAsZNCQnRhwWKmNPlcALNbNixsmXyakTYWNvlyOtQNwPtcA5tggC5hpTYIABguYtpttggltV1QMSiP1-pIwLQ7QMAWU-Y-QcAzl3eUY4IQNgJptdQcw1V6RKRVNNNfhcwMFTOoA3NRY9V+ZzsJYNA-pUkGA3NOFnMKZSgCFSZDdVgRYZAFlPQzIfdPN0QMUtQzsEANw91IA49A9SA5N6tMtbwWtEdy9dtnMUQ01mAs1pNW9FNnMutfh9NBgcd1t59cAlN9Ve9B919t9p9WUj9nMJl2dX16A+ZTgyARZ19T5zs-VOd9yKt+gcAT5CAdA31zINdrQnNNBJmEd5APy7tqAaIAEJdYDJwVUMAxtYIvSUtGt69-4zIkNz9BIAsoQTAyVl9gi89VDyVT9ld9yk4SgVlWEIwEA9lUAhCFK9QQAA)
