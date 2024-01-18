# Vega Visualizations

### Tutorial: Creating a Vega Visualization in OpenSearch

#### Introduction

Vega is a declarative language for custom visualizations in OpenSearch Dashboards. This tutorial guides you through
creating a Vega visualization.

#### Prerequisites

- Access to OpenSearch Dashboards.
- Basic understanding of JSON and Vega syntax.
- Familiarity with OpenSearch data.

#### Step 1: Access OpenSearch Dashboards

- Log into OpenSearch Dashboards.
- Navigate to "Dashboard" or "Visualize" section.

#### Step 2: Create a New Vega Visualization

- Click “Create Visualization” or “Add”.
- Select “Vega”.

#### Step 3: Vega Editor

- The left side for entering Vega JSON code.
- The right side displays the visualization.

#### Step 4: Basic Vega Syntax

- Vega visualizations are in JSON format - see [additional sources](https://github.com/vega/vega).
- Basic structure includes `$schema`, `data`, and `marks`.

#### Step 5: Define Data Source

- Use static data or retrieve from an OpenSearch index.
- OpenSearch data example:
```json
{
  "aggregations": {
    "time_buckets": {
      "buckets": [
        {
          "key_as_string": "2024-01-10T00:00:00.000Z",
          "key": 1344920800000,
          "doc_count": 10
        },
        {
          "key_as_string": "2024-10-10T00:00:00.000Z",
          "key": 1458924532000,
          "doc_count": 100
        }...
      ]
```

#### Step 6: Create a Simple Visualization

- Example: a simple bar chart.
- Define `marks` as `rect`.
- Set up `scales` and `axes`.

#### Step 7: Write an OpenSearch Query

- Replace static data with an OpenSearch query.
- Use PPL or DSL.
- Example PPL Query:
  ```text
  source=<index-pattern> | where <condition> | stats count() by <field>
  ```

#### Step 8: Add Interactivity (Optional)

- Vega supports interactive visualizations.
- Add signals, event handlers, etc.

#### Step 9: Finalize and Save

- Save and give it a meaningful title.

#### Example Aggregation Query

- Incorporate `%context%` and `%timefield%` in your data URL:
  ```json
  {
    "data": {
      "%context%": true,
      "url": {
        "index": "<index-pattern>",
        "body": {
          "aggs": {
            "my_agg": {
              "terms": {
                "field": "<field-to-aggregate>"
              }
            }
          }
        },
        "%timefield%": "<your-time-field>"
      }
    }
  }
  ```

#### Additional Resources

- Vega Docs: https://vega.github.io/vega/docs/
- OpenSearch Docs: https://opensearch.org/docs/

