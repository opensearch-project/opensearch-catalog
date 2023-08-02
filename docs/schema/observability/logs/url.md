# Observability Category: URL Log Fields

The URL-based field set described here provide a comprehensive and structured representation of URLs.

## Field Names and Types

| Field Name             | Type    |
|------------------------|---------|
| url.original           | keyword |
| url.full               | keyword |
| url.scheme             | keyword |
| url.domain             | keyword |
| url.top_level_domain   | keyword |
| url.registered_domain  | keyword |
| url.subdomain          | keyword |
| url.port               | long    |
| url.path               | keyword |
| url.query              | keyword |
| url.fragment           | keyword |

## Field Explanations

- **url.original**: The original URL as it was observed.
- **url.full**: The full URL, may be reconstructed.
- **url.scheme**: The scheme of the request.
- **url.domain**: Domain of the URL.
- **url.top_level_domain**: The type of organization the website is registered to.
- **url.registered_domain**: The highest level registered url domain.
- **url.subdomain**: The type of resource.
- **url.port**: The type of service requested, the port number.
- **url.path**: The exact location of the web page.
- **url.query**: The parameters of the data being queried from a website.
- **url.fragment**: The fragment of the url.