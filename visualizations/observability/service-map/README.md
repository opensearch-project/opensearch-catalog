
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
[Open the widget in the Vega Editor](https://vega.github.io/editor/#/url/vega/N4IgJAzgxgFgpgWwIYgFwhgF0wBwqgegIDc4BzJAOjIEtMYBXAI0poHsDp5kTykSArJQBWENgDsQAGhAB3GgBN6aAIwAWAAwaZ8GmSxoAHFpk4kChTXFk0oADZwAZpjTaQAJz0HUbzGxyuMkxs2GwIrgC+MkgMfhA0AF5waCBmCtIgTEhQANZk7mwM4unoAMSOao4A7I6OGfFk4kh2EGgA2qBNCMnoshnEzQw9AEwCUZ1I3Skw-YMjY1ITU+hIEDhwUC4yA3ZDaJjuQ+MgXT0gEAhsITPbc-uHcMenKc16kre7Zw7OIE+TZ1kIHA7FZkh89ug-AE-ssQAAPdxIaxgkAMHAKJCYM5tbQAAnkShgAF1fosTv8UgBPRHIjJojFYlJtXT6TBSXEaEkws5wuBwrao9GY7F4gn0Llk57oSl8gX04VMllYdmc0lLM7QZpwBQASQQZAA6nShYz0AAKWQEXFrJFmuEKMIASkdACoxTNuSlNQ5dfqABLGhlnJBMCBmmBWm3iM2Uh0IZ0upUuT3oB2yd4gHYQ8QMOx2GQSdqgOCkcSYVroS4MIFoqR+BiwODFQMK9A5vNqkAlpvllJVoFp8Ts+uwCCYJDuOUmnmUs2OzvdssV86UhDBOyofvatjp9kQVfr1AjmBjidToMpdt2X5ElPwqAMdyzT5oK8FySoDpd0u9yuFAc7kOuLHqek7DoUjbNjI8qmvCcY3nelIPk+4I9G+ICFp+xY-suW6DuBDYnuOYHARB8BQYKF7SvBES3pKFKpsC47PhCOJSJy75Ft+PYVl+YiPlAZzyMUO4ZJglLrH2-6IGwpAZFAEgQAwywHEMQRwJgshwE2XHiZJf7Vtu6advx7iCSkwlpmJElnFuaIIWSelnMelxyTICniEpKkPDIjg0HYWJPugi6YJQx5wBAlAONY9C4gAvAluIqDe0HTikg64gA-LibSDjiRIALRwnO7Kzo6BV5SoRJEriqA5doqq0XeSKwGwKGZncn4NUSnFYdxS4WfAwItrBbRWKQk5mgA5HC3pwFN7LFc67LjXAk1TZSc0LbiZWOhK2E8bYIBOSkIHEQKfkBWtKQhWFZERVFTZkPQCVxcMpKUa2IBtHacb5biADUuL2mEbRVY6uJWsM7Ixn9nKAztf3g5DuLDFydHqikCRXOEqGqL1X4hcushDXYACEGSOG15lHj5n2wTgO5miolBaCo7K3QoTFIAAmriLq4ozsjMwAbBzP6UFzAVIAAsmwXPOguOFHQ0TTXqmNBju9UQgFTZk9KpcCpVRICWGOKgo2bmDa2SRNcaZNOZjQcB9DIJ2pkwdhQCCuQpfTZzJU19GwlbyV4z4BMHQNqCgO7x1kaBF3+YFN0S+FkXRc9MCvTb-spDgViwAAIpr47iIJZohfOxx2zH5xvM06Wl7nMFnFb2sY+SIfNyxPRuJhhPK3XccubJKIeV5Bt05dKfBWn90Z09L0JS3aXoAX5cwCXp7l3Alc-tXndSnBYQjTysoZAPUe-qAquN4x0sfa3TJwsh-1A1GdrIRDAtS+O-1WndItN+VUEaf1fo+H+uI-5IAAfiRQ4olaHTrnfdWIBsanx1s-dAbQWowDau-XEv1QbwwKriPBBDORQIwQgdkFD3CEOIQgMGNUyH0PytQnG+1+q-j4oUfWKRiDO1dsdGy6VPbexoL7WixsvoIiRGQZIQdMbUVPrI2CMp+SXw-IPZBt8G5oJgU-Ne30kKPkIZ-Mx7goEwJYSjJMpUQE1Q-mYaMVibHczsVaJM3Da76MaPfdBONjEm1wZvAhoCgawxIaw8h4SGHIwFjQuh8S7FRNjKDUBbDUmJNxDQ3xQ8+ECTOEIl21l9KmwkT7HIftsEgGpAopRR8GL1ySGfFI3tJg4DNMMDQKNwFxkdOydmSUtAaGrsHM4UA4TtN6AgmAKN3qRx4cuNo+41xsA3HhQC7JLI7k3NJNENUAB88CRKyAOYZVyKI6m4mmQld0BBhiZWmQDDQrMNAqFQI8jud4oCUlmRgOAXhMCLM7MfcQ8s4AACVzA0GrAAaTgACmQXNoCeBwJgdgH4QAAEc4qF3cHAVYcBrSJCNuQuKXMoBEpJWStp4dDDLNrnIKwaZUA5GRTgIlEBWjqLOLdTllIEpTSQFNAAZOKyFXNYWWERci45KhMrSphXC+VlICpfMFcikVuKprKqhbK+FEAkWUgBl8lVRr1UORUScQ1aq+UdRfKgFQTKMI6OvhWfxatLz2rlSa5FISvqWodaam1XczgqoAMIwAnIo3uaACoAGYBAaDvCCcQORt5l3MuHUYaayRoppTQTF2KUgAGVxxYlxAMTwIYHC4j1uQzYNBSC4hVY2mgcJrRVurJQDIx8-IzPDo4ZoQJmVDxXBsrZ0lCiYDaGTW6TBYh+E8j1M57K7IBH5SkUdLQlG20nesw8W4x7tTqUO3EAAfK9wEHiU2plPI4h7kHfWPZsy5AFdwbv2Vuk5P6LlbmuRTHd6A4RlQfQI2mRxO5FoxVizCIAADiiIcALI7ZcMcuIiWCTLHYSkuIrCBWyFiBQ8D6D9pkBCqFCbUDoSvisr0B4P2nomoCy9r071DCytAzEylWDFD5LVdtNHlERt9VzP0Z7aOgEUK+XM+YQAeXEBsBDnl2h0XdVxFl76Z2GWk6BkAwApqKCmqgBk-G2V8nZFNZTqnsUQDM2sEEmAzQWYQJQB2EUAYLSmgDdzYU40aQgFIXzjoIhIOjlOk9s7YiAuM6ZujCmbN2ZbYpMzbRbzhrgyWtTKQABidgkBkFIthiK51cT5cfWShAuZMTYtxGiCQvHxx3NjciSKA6Wk8vOrRvd46tN9T8fXAJaCh1BtgpeyVna4SPRih6W8PVTaYhQH1ajXMKorYKoiERWYIpcSFbugoZYmzpFRWwKAAB9BSRQXAurdWtAo7gKxqFRY+eriHU0aAQI6oluKhhjmXEmtQNTjiHfQI2XIc6gTuCEbm02F3ruFDLKoaGXZ3BPYrOoN7iI8voF6T9jIf2Ae-hACoLQoOyTg9SAUBQDZMBQBW3YNgZAYdw5RA6K7N2UeoAexjtqFY3B09x2W9AKgvuE5kMT8rQPKegGp4zycbOpEc8R9zu7VQZCPYF2gYY7NTbvbxyAJNBPftwH+zLlIAg1Ag87NTxwxLMCPicEV1na12cZE50j27aAxbo8x6j17BuReIbUBLs3FvAdW60HbwN68kCrh4u7lXnu1fI7u377Xz20BJpxx9nFhgRbfYjyT5c+aNBy5AArx8RLy6bWT-Dr36u0ACC1-z7PEdg-55SKbon5vS8pCTZX6nOGwjdGKPn5Xje08+9QK3-3OvUBB+F939AAgACcxe++R9JyLW3YO4-nBgCWjebvYcp-O1z9PLe28B9QMMXPXejfr96VvqX-fLdi+B8Pw-iAkD+Sn1Vyv1n3nyzyxzzyNzDy0Elw8A-yj3QCH1jwBRWCgHVysDPw90v29x51APbwrE1yf1FxACqGgJL0-xAEMCqAED9j1mQDu1jjEXQFEELB1gOCRAgFoN0kYN1jalqyKwyD5G5XSj4w8yb2v2iGXDYMEijXT1aGODjloLqwELhCENTBEMoEOwkMvApHkO4MUP4K1xUKCmWydw800JAFWBSHyEKGhEcm4IUjzFU3qDanoN1mdjsBKAX2zwLHcC5mMKLVO3QN+F0IqX0JQEMNUJMP4zAIyEsMrCQDhEuxiLE2PgzRyE23HG2yQBEVWEpHLnuDUidQBwO0P0cGOyxAojENn1dTdiC1cOXVyGCxKOQKUzPEANT2AJ5yTQPxaO5Xlnp0Z3HGZwwIvwR06Lu26Kp0P2Qlr3+XaKwOb3vx6JeAUHmLGOwLuxUGWIh3gCh1iDWKqJ5y2KmJaNHwQHHwZAcwbyAI2NUCam2KU12JyGh2uI6NuJdTR2IkUVcMOMwCSPb0uzRHWHcEu2CCKBKDcC8ku2uDWku1+MCEyAbE5V4Xl2mLaNeIWOvyWJOK9GPxwFPwOJnx52GAeOyDQOsEJPGLuJxIhxrybDmIxPWMWOONRJaL-wAMZPhJdQeLKJiAsA0ns0Uk5KJM2IeLMETyXGFKpO5JpJp36M2EGOaBZ0pPeK2NvBkR4PcDoKOjjmYMkFYJpA4N4K4NCKK2wB0l8ncNWPaGOjqMoAaORNaCWziLaFtPcG+IACEkSNIQBO4FDeClCIj-D1D4StD0A9tOx-StTAyuwjDhDTCNDA0wzzh+FzIQizgwjlDIiAsviNIvTGjQpzC4i3TvjIzuDmc2Ach7JfIChwg2woUMikAsiRFqdnhLTgRrTPwUzikxI6jfSwzXSvMAA5GjWo90jSEcrmX09M3dZOa6IM+M-jYcqFXEMmRKK8XEabHMuoyc0lNcuKdtBTcNVIqwdIhkcI7sqDEANIxs5s8FFpLzAqVLNTR1LzFIG888u8t2Q0zgvqOOYrfIPgRkGQawtEJgZAwc1M5IJbfwXiIo-bJbPyDsuC3MlwZ0uC58hzacuw0IgMgwiwyQuox1QQ4wnAXYXINzdQzCxSGzVCqaQ+O8VCp8iQFTNLdTGQN89AD8rbHbMSH840v87ggColCgYCkAUCnAcCm01C-sjCPAG0vbJ09sjwuCt89Cm06i9TP0vQvCi84srzYiuM9ecinISihMzSkLXEKaLzei48lpFVRs5wns+sjbT83i789g38r8OOCsqs7dXWWsr0KC5i8QVil8jIanN85Szs1054JbRS6Soi2Sl0kspopbLmUdXMO7V07ChgipXy6sgK0+SEOokKsKrCmQanGS6KuCuK1CVSqCpSgim0gy2SjKmIAKG03K0RXCgRGQOgNaSfHPEwWAxOFWAxFIHrM8D6VBXdR9SDQSXiUAPWR2XDFOGQGZFBCaiHGZHWZA71QJf5YIskFaqZTZEEKcqXB1ca0bL0XFSaNQfmETGVB1J6kNf1CZEAAakPdTF1Dig4JeGYHwSgKoY4U6y8YIBQFFc4AG+bG6n1FyuAGNILY65a+ari08jINI5cbizI9y02UuFqHoA6tBNI7NImj6OTNsHQ7S3qvgvS5cRwYdWMyIodfKNcjc6bFVBKALKzbtTKVadaWaRnBwBaNmqhJLDsGc9ATM5MxwaGki2cuEFhDmhTTc8VZ6uAHm9QvmrKQW1zDaLaKQNm8GSW68JqJbOaJa8TdAMcAoTlA0eZctEWlEHy0ECcVPZAKwI6c8iTOARy6Km6PAj6GkeNT8dmcnTkP5TZNqcpM4NqSwH1c7L2j8UAX2xGgOtwjsqwgoeyHWUOnoV00oNQEWQwYYJgNQDIYukWGuiuqukuiu9fSumQUoCukWKoEuquiukukWJZEAUoJAG3UdJNbq4+YWrUDIJIAoNAfrI2BHFO+GwJEGcIfOxpRetBeRWkCIRCOaSetaNgGesdOeuMf-VOkbBG+pGiK62kLa266UAu4IpbZAdwHIa2uOMwZQKjFpbGymQKuudO6808xynWIjQaltOSVAWerXcuGjOubBW+A4Ss4m8+wJALLzATLmOEDmqFKTCaVgMjLc9Q1CjBvkbByTM9fBnjKaUoF-dfJNdfdfMzbocc8MCAOwM0OaaaBwtqbaNBqC6gXOnAZaXEYADcd5PfCIT6u2pBx2wkdexcjzdBvmshuAXBtaShwhhM4h5RuKFVNR9wSh7Kd5AQe-YIg0zygS7y8s08j+m4WA-7GgIleRmW+anWCAWNfK0EJy-WAADSOkVttpdumnHtFvZACz4eKUoDhCkagp5n8aMvOCCcNpdt4ZDPUPQcpE+tQr8brgCcSa1GCaNpa3423PHNCmiY+lQridyYSc4eSa1FSYTNKe+MoEydRp6ozN0qzOMJW3EGGDMpKaIbtIIzIXCfSf4cpCkDGYTPQe7VGbSa0btIqeTIUQcEDhws6ejPwryYGY81WbgBUGOTig0EygC32a+R6RdAAAUdQEYznrA1nnQnqzQk0i8UZLmbnFYVmHm4AbY8rNn6bumUgXmi8Mj+N9nhhXQzQbmCBXVxlYjlx9mR7pbNTAWFzzQFIwx7myAHAk0oX3rjUAYBBnQAYOGkmQn5opmFn+NiHon5wVn+dZA-GUXZaWbjCOGrBdnKAkX8W-VCXiXHRSW6nNoUmqWmmhmynWmvnmqVhGW4mxM45dMutYQJwChZBHUEg+b8Yiq6y06Vt3zTy5DoGFIpy4G15b4PHkGIzIQ60fmPp9nnGQAwW9mfnhgCpN8PpNqSaFHuXGXmWZB9qUHDF1DVWdx5W3YL5b6L6ppAAm0img+kunVm9bUPFZmf4Z0b0YocUHVuKdEIlZaYzZwazbI2ymodofocYc3DWkUVYfYbqe4fcEacGbTciYkuEdEeBokakfJUdYJerASiVQ0FQCLzMbvBVQgCfMce9ldu4KVZkE1cE02v1zKOKr1eYgzt9p1npNgdAHgbkuyDoEDeteOLcI7DrmteOkNLMFr2TH+vtuQdmsRv0fwdel5sXevVvT5rYEcDNEzbwYsrCfUNOEdGOU1SynrZjsbcA4TLbarZYZPDraSYbabY8zbaGREbEcoEMDUEkZmsQYdvmRVhdq9Hw7gFkfoGdonsDuCmDrcdI4AHkzAoBD2jprXjG3Ge2o3Alyc3q+XqxeOXr-UPpkIxAgpQAL3GZQGnwdYvWg2lb2bdG1auaoVX2db33MpxaiRUA6mKWUOonPrA3H23DlaqpVa8wc3ubtaEzdaNOu0WFtOkmRWGnoP+M2nt6dBpNh4rgAoS1HXgAsVMAHA6oAtTgbMABBCaYrUlMAszXNygMA3ERLiLbe9z21cduOpjadSerVv6nVn2-Vjd-VrdmB013d81-d5j8SVjzqE9xN3totvBxQVT6z99m9QjRd7939hr9RgDuL4D0Di2TKCD5nKDuL2D5hmthDslgp2zSDvTtD9kDt8RnDqR0j+r8hxrhQZryzVrz9jrn9v9nrliwUzyFzjzfrsDobpDubs7gRmwx0ODybth6bhwLhm7sbwR9tzD7D3Duj+98joG8TzqSYmG+9xjg9qr89mrjjtpLjtBR6gWPtiAAT1VITnWET2OqH51VINgKTz1x1zTszuwCzlTqznbzBrKTThzmb3T27ipvagnuz0zxT8z5TrmbbjzGzk2rT4VopgLNznWfBNjLzzZLFAIOHlIfzugILvr-4cLyLxRXEGL4L9QhL0LCLwaxXlfNTWL8Jw3BreXzX0laXQHbDYUXX9Qk38sJL0djZ06C+L+2EIrJgYER1Fd3Vkw1bO1NFD6BdzB3Xfqk7REcBnoKBrsIP2wYrk15BvduriX9AKaEmAa+NhnuuJCjwqkfHtPq0lIXaiNrRbP7OlN-jZ4HWV4Roar7Hta66HWKmMsctTjoH51cnHWQEYELxrHiEEABARQBQBwD6EEHv1wozzpBAbpCAe61zBHzWq1ZHxHvjiAcqTXCOsZT64EEEPATWSvrv3EUd28IAA/view)

---

## Acknowledge

This graph widget was originated from [Deneb-Showcase work](https://github.com/PBI-David/Deneb-Showcase/blob/main/README.md)
