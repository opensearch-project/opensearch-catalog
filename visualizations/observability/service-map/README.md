
# Service Map Widget

## Introduction
The Service Map Widget for OpenSearch Dashboards uses Vega for complex visualization of service interactions. It's designed to map out relationships and dependencies in microservices architectures.

## Info
This widget graphically presents service map interactions, ingested via [data-prepper service_map pipelines](https://opensearch.org/docs/2.4/data-prepper/pipelines/configuration/processors/service-map-stateful/), aiding in performance monitoring and troubleshooting.

![Service Map Visualization](service-map.png)

## Vega Integration
Vega's integration allows for customized, interactive graph creation, enabling detailed visual analysis of service maps.

## Structure
The widget includes:
- **Data Folder**: Node based Scripts for synthetic data generation for visualization using the [faker](https://fakerjs.dev/api/) framework .
- **Queries**: The actual queries used to fetch the visualized data
- **PPL Query Based Widget**: Uses OpenSearch's Piped Processing Language for data querying and visualization.
- **DQL Query Based Widget**: Employs OpenSearch DSL for advanced querying.
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

## Prerequisites
Required indices: `otel-v1-apm-service-map`, `otel-v1-apm-span-*`.

## Try Me
[Open the widget in the Vega Editor](https://vega.github.io/editor/#/url/vega/N4IgJAzgxgFgpgWwIYgFwhgF0wBwqgegIDc4BzJAOjIEtMYBXAI0poHsDp5kTykSArJQBWENgDsQAGhAB3GgBN6aAIwAWAAwaZ8GmSxoAHFpk4kChTXFk0oADZwAZpjTaQAJz0HUbzGxyuMkxs2GwIrgC+MkgMfhA0AF5waCBmCtIgTEhQANZk7mwM4unoAMSOao4A7I6OGfFk4kh2EGgA2qBNCMnoAB7uSNbJMgw4CkiYPSBt2gAE8kowALogUZ1I3SkAngNDGaPjkyltuvqYUrMaK2sgXVO9cL0uI2MTUzMXC-TXUuub6FtHs8QAc3sdTlgLldVr9bhspgo2LJJDJiM0GD1xAw7HYZBJ2qA4KRxJhWugEIUIHBRlI-AxYHBivtXkd0FicTDCcTSSkKQwqYjkRc6bAIJgkO5gaDWSBelsABQASk5ICJjJ56AgWwQwTsqD5AqR4guWp1bD1IpgYolUpZU3ZdlWSxudxSvSgDHcGTRdgxaAdeMkqA6qu5ZJABrgguNs0t1slwsKDKZL0O90R4QizthroBHq9qPRmOxuJA+ODXPV4cj0cT9Kt4oTsaT8BTILt2wzTpd8JSCjgdnF3qL7W0V0DBNDVcnYk9UCm8mKSIymC2OCmkYppAyUAkEAY-0w7gxQTgmFkcEZk9X695lKjRpVs-c85Si8FK7XG-vo27sJvUyWluwwgLu4j7oex5wDIjg0IOcBeugaokpQlpwBAlAONY9CzAAvPhswqE6qZgug0azAA-LMbTRjMSwALS9EqFwKoq9G0SoSxLLMqDUWO1zZn8UyDLAbAFiAPp+sG-EThWU4kuGsjwAOzJpscVikJK8oAOS9NAzRwNpFxMYqioXBpCGYDpWz6Q4RmzKxio-JWCm2CAAEpHGjbArB8GIfJmCoS26GYYyZD0PhuEAEwwu2anoG08q9BmdGzAA1LMyVhG0nGKrMBCzFFFzylsKVXOlDkpbl+WFQJPb-CACRsGEw6+j0KiySGyEanIyl2AAhBkjhia+qBHiecWkakSLyiolBaB1szdZQ-aDkgACaswAFSzDgM0qAAbBcy2reKACybD9qZKrdWSoANE0jpkTQYoxVEIDDS+PTjdBk0ypYYoqDVAOYG9sK3TOhRfSkxA0HAsifreZFMHYUB2DQuTEX9UxEVm9UIi9mBEYWbWBGWQZdWGbkeegXk2kNcGTP5y1oRhWHhTAkVg9jKQ4FYsAACKEyJcDyt1yo3BDqD3Xoj19oT3PSgTr1-kJ8sqyTUluOWlPTtL7lfp5LbATue4Ht9UEwYzCEpCzwVs2FEX4YrHboHz4iC8LHui+Lqtwg1WXhCRMoPE8GQ6y5Goy40zR9gOQ7vUrxzup6qUZRAZjiEl+Z5Ttp1IKlBVfDAxn5jl3Hp5n2eernsz54X8yKN8N1U-rD2x+gTUtYnrvTCJMBiWnsxJWV3H0bM-eD1ctddwgFyT+4Q8j9lnGzOPC90TPzUIM5AVkiGz6jRJcMIzINMgAoKNoxjORY0nfS7GQyR4zmvYAl2wdTICYedZHd0gO3J6F944oB7vFaYWwy7lUroMEqOdtp1xAeXGqEJzgOTLqvGBWdIE1wQfXVeBVUG7yltHOWndt6xXvn3D2A9F6YOHqVbK5V140MHtVHas956sLoRXBhVUx4T24eXLeYRiGtwPlDI+sN4aIwRFfdGmMsyf22I-Z+gl-ZTHiEkVSU00YbBwPKKKGgaoZ1gYHMyhELgqC0BoCWr8GpQF6DomUxcaoxV-nvY4ppdT6nvLWRuS5ZC+P5NSHA3EAB8ATBTBKpCbZR6BZiOPwsXAgUUKKOLShoeaGgVCoBSW9dRuZQJbGcVMVBbiVRFPEJdOAAAlcwNB+QAGk4AlJkP2aAngcCYHYEGEAABHXC-N3BwCQFSWYWjoIT1wv2KAIyxlwAmYkECkkeiGA8VLOQVhok5FaTgEZEBWjxICpQXZWx8LaSQNpAAZNc6p-Z6mWGaa08JKgKL3LqQ055Wx6K5OWmci5-TtLvJqY8xpEAWlbDSrkj5YLvl+yqaCr5RyJIjlQOszI2y3JWBwLEFIqiMgICsKoGQyAnGoAEG4MUcAAioBUO9COni26yw7rcJFTyIWtMob3WFyLIUIrfmy-sABhGAEon6tSkvRAAzG4JgWL9Y4rxegAlpLiWoF+SYCMSByXWJkNS2l9L8YpHRuIHIQtrTe0lT0WVQQFWgCVS4FVgwJVqqDAIUlOq0CyqpZMQ1EQbgdLmTQbpvSUgAGVxSTFmGiTwSAUaLM+hPKAPTSCzA+bMWCvQJlRv5JQDIRSs3WrQI4ZoVINmtwAdqHxkZCiYDaP1ZaTBYh+HAksT42ykQxNCaUlIpaWjP3BpW7x5pu1sE0r29AWbZgAB8Z2xigkNEaFsMSS0rW0EdeoaxGg7YE7towIlRK7ZucdcBBrHLlEqJd0MxpQRfqAINXSenlhAAAcQGDgGA6aamzApGKWYIz5wkjsFsWYVgmbZEmAoRu9B80yERf2YtqAAzk0nJszdY6J3HOnZFBdGJKJ1wmAeVgxRHg8W-Yh+9GiUgfIABKnvEqs7FJQUNgXEHAFNvT97ZlQ3JdD1bR21qwzzdAwBtKKG0qgQ4xHtmPAuNpNjHHn3gUkxndGVlpMIEoIfdCaUjLaTSpp1C4qzwQCkPpxUEQW56yrWaLd9462TpAGJiTyGSzycU5xvckm2jOj9o+kNymUgADE7BIDIM2AD6FvKzGC8upZCBsQTF6bMUYEhCPikSWKoYGEC2CoOd5JD-by28d1q5ZlMcgFFrAVNadtzM00F6KFbCMBuztovhMFAckENwHYp1+iAxT6oravvUAZy+0FBJIydI7S2BQAAPq7iKE6lQhgbjjfQAyXIdaqTuFhq+WbC2lsklUFFdbXK3YFAUPSTAUBOt2DYGQXb+2QKIiO4UE76LzslM2zaZ7GNXtzcWx9p1VRvt9tGZgT0TgwtPYQi9jIb3gfLbQAdcHbskDairPDgHiOgfHadWj2EG3QKehGR7GyOODsX3xyDtAAh0ceA42EboxRkt7ip4D97KOKWM4gDAEN7s4d7dx4d5Hn2GfE4u6qZAcF-vU6RwT+njPsgE6sMLhHYule8-a59ZATrQDn1EPid6R5BgQD19eQ2U6xKJbCxkR4+y+xEa04run0Rwxm-nMKkHrQbjnz10lh3vQndkRd6crlHuaO9n99bj6tug8yEd-5Iz42o-oHyIUAIVGimmpyH18UA2kBDbGVsD2aAfqa3QpOEnjhJuTDbG7nnq2z4mYN5kekuyNQhhJ3dyU8uufi6ddKxn+zLo3bu+KB7GvRc0+559kfUufuk-cOTqAlORcK9pzzs7S+UjmAH3j+fK3GdbZyDtznR+h+qEZ4Bln032fgUv1rundK8an-gNt2Ih+X-N6Ku5NvNyJvEkebBCAodwebUYdcCA4IIoEoKlA8ebEIeACA4Ap1OVTvUzGvaXPvUkZ-Ofa-VAXfMbaXfnQXdXH-Ag7XYgkAEnVXEHCg-AtAm-PfTbMnRkdfSg5gt-VgmXJAOXJg7fT7elXguvGICwM8JTLjQQ4-Fgkg5fMwLHBSGQwgkQ+Q3mK7Cfe7R7LgoQk-Z0JRePdwfXamOPY3SQU3XYC3W3K3JGD6MLbAK8K2AcBQfeAA9wJ+QKZtXILA9rMZdodwzwgAIUwJcHUQDwT3tyTxDxT3D2YPT2Gz9FjzsMDyiNVBiOdyhy0zTxAH8M1EkUHUNzj1SJQGiNDw6yyOMw8LPBCJ8MChyLyMCLPBVHPgezYByF-BggKHCDZBqQLyQCLyGxJ1dGcLsFcICJ0xXEAL8LcJ0wADkakpjqjMAFjENwjijrZxJk9MjiN5if1+oCIHRZh6sjNGxPDVjFkDjcJ00SwBUGo89+j6gCiTUrB89DgBjBtKlBUdN6JPNlMUVJj0AHj3jBiVwrDLc5Jz5wt8g+AjgZBM9RgmAfs2gAFnj2t-A3DVlWhdc4Yxi3CzjmiZiAi-iuMQB1iUjIjSjcjPc28UVti3ZfRch5QjMSS9x5MCTMBtIJZClBUOTfiJB2MvNwIni5wphgT+tPiz5wSbDIS49oSRkKA4SQAEScAkSAiOSyS8Q8AAisTNSPpcTxjgxUTRS9S8iUTWThTySpgSiMhGidM6SMiGTO9mTw8LSzNZhtIdMuS7j7Q+j3iRSb0hVesQTJT3JpTjDbCxTmoOiAguiWp8jRT+TxBBT-iMgSdJjRjDSUTXR2tdSjSOTsT08USCy9T+xS1sQnUUSyTkioz2jOiPpujPI28kyUzSSZAScNTMy3Ccyq9ZiCjCzqSJj+zSynAYhBwAjqz-xijl0Mg6AEJH8yQfUZACt6YKsyEmd4wXB3pAE+0ZyYJl1RsjCj4gMmYMhyVSFWVHFYofsLygF19VgbhPpjzzR0ZENlzkU3IdzNR+ktI1AEFeUOV-z2VwU7EQA5yBhUy6V9UjxHZWsfBKAwdYQnz7RggFA2kAEYKWtPyWUgEPlRUTMHykKZygTXiMg89wxxTC9QyQYRZsLKsXizULVxQrV3pFBo9NgqMIjjDE9Byp0nEyj-Is06IDijj6sPl8IjNZNs0KILItJdJbJDIpAhLp43MOQazdzuK0jGjHB0L6T9Tehy4RKSxjjrkKM4AJLw8pLKJZKrJtIbI7s7IlLGthFVLHQ8Z2sFLDyildwHtxJz4xJLA5ZZtZcgwH1OsaM-TwrMyUgVTYoCUjTSg1ADpDAoomA1AMhEqDosq0qMqkq0qABOdKmQUoNKg6KoJKjKtKpKg6dxEAUoJANQSoJAaVSctWPoBSjIJIAoEtMtX6DMfg0KgBHCt0Lsd6eK28t0AlANexL+DqmQLqtgHqgdYKgaui9cxhTMd8vYNc1lHYF1Z+Qw5AdwHIQ88+MwZQeDQVcioaRs-Wf0kis1R41iqbAYTjbcVAYrX6DgxY-We+e6I8donoCasPSonTEjfsXoESmpejTSVgaDE48PDk8Gx4KG-sGGhCOGgjbSUofKqKfK6VfK-KyTboao+UK0OweUBSnSHysSeyIzMGlU0yC4YAPULJA6NQCIUCsUAoXZAAdSbjguBoqN2IKORshtwjowY0xoRsqKRqktRrgHRvcExqoiyQECIIfMsPNwhJDFaNePOta2XLgH6QYBoBGTWtZWQtin5yQDsNNRAh0wAA03I9Kqb5KHLFKMtiN6bRbeguaCj1oXbHSAEPbrIFK6a4jw8wathQKOTnb9ZXbQ73aDII7KjTi29KA-bYoOTA6E7g63b7KU6LgjN07ljKAY7CKiiKTNKqS9LOtxAooXS07EaM7QNx4S6o7RatgpAO7Qbfa14vbXcW6y6s6EiXUHBcYpzq67da7g6m7iNx64AVBwlcINAKIjNF7clDEtoAAFAASQqg3usAntMgQXlGlQOmMQKm3v3uujHuPrgDBirutMpOD3KPPsvoLwXofqikVC2nlH3oIFW1sVtPDEXpavUptxrrfv8nlF3AgHnq03Ab-vlAAvBTSgEFMjSkpqTr0g9qMl7uIyRr9uVDHtXyRGdsgaMJnpgZSEpqsEQcoGQf-rQf5AwawZwYMjDvwZ7sjtltbrvt4tyPIdkEDs4rj03TywaglAKFkBRQSCkpJQbPjLCqHAepOtim+sQ1+tdnujFSRlACY1pjjQftikXotqAS-qQZ-vonyo0FinPKGvopBoXpEcoZkBvKcfXI3pEbEbPiBAsZSG0kACbSbSWKXyJ6IWwhrTMG+WiW6GqWxQEywelaYezwsWhWpWlWj0nGvGgmom-UBCJ+MmiACmt2mm9wVO72zu0U6gAoUYJm2YFm+C9mzm625ZQJ3oh5ZFfCN5DQVAS+zW41Lp6vM+CRgTR0eaxRqC5Rno1RrrIMp6pPD2H60AP6ssMwKAOgTxoxkQ-UjkHa3ChJ2GxQSKSS0jbNOdMDC5tgRwVB45jGt04u8PO4RUcJX5Sicp80Wm55yoxmwp0m8mzhhwam75yp354jRmixZptmjmrmgG3ZTpoMrJ05iyyoqyq5qS25+5tGqWp5lJ1595oGCiL53yqprTf5km4poF0ln5lJqF5m1mygQwOF62hFuAfmxYNyIxxfDCnmuAAAeU2e2e5bRT2cmSRb-J2lYYgCAu6Y5VinzDEEQkMbRWmnAxtnekca-P0uEoluMrEpqTOcsoucomUqWFQDdrwaLpSazvek8Z1aEs4iMpxGSfErRZk1NYoidYtYLvDoha0wrumowAY2pmakHBDSRaM1dADWmufs8gCcuvuPjQHBRTrxUYqIWY+T9ymYubQH-w1detTR6E+uWdPOlnei0aBpE1AAiaRe0iUjnLCftbclghcO2AcdbYNLdGzoCf1jbbGJ2K0xjeiHRkaFFdJk23VE1f3JJHDQ6f1l2Y0HeiyCpHtonakgjEUAUAcFinRiJXbx1b0QQAMQgB-KsilbMrhVleleAv5DYiqCkA6msS0FAoHHRjwBeg3amFmCGedCAA)

---

## Acknowledge

This graph widget was originated from [Deneb-Showcase work](https://github.com/PBI-David/Deneb-Showcase/blob/main/README.md)
