import json

# Read JSON data
with open('../integrations/observability/catalog.json', 'r') as file:
    data = json.load(file)

# Define a list of background colors with fade effect
background_colors = ["#f8f9fa", "#e9ecef", "#dee2e6", "#ced4da", "#adb5bd"]  # Example light shades for fade effect

# Start HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenSearch Observability Integrations Catalog</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <style>
        font-family: Arial, sans-serif;
        background-color: #f4f7ff; 
        .container {{ max-width: 800px; margin: auto; }}
        .integrations {{ padding: 10px; border: 1px solid #ddd; margin-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <img src="{data.get('statics', {}).get('logo', {}).get('path', '')}" style="width: 750px; height: 250px; alt="Logo" />
        <h1>{data.get('displayName', '')}</h1>
        <p><strong>Version:</strong> {data.get('version', '')}</p>
        <p><strong>URL:</strong> <a href="{data.get('url', '')}">{data.get('url', '')}</a></p>
        <p><strong>Description:</strong> {data.get('description', '')}</p>
        <p><strong>License:</strong> {data.get('license', '')}</p>
        <p><strong>Labels:</strong> {", ".join(data.get('labels', []))}</p>
        <p><strong>Author:</strong> {data.get('author', '')}</p>
        <h2>Integrations</h2>
"""

# Start the grid layout with custom styles
html_content += """
    <style>
        .grid-item {
            border: 4px solid #f4f7ff;
            padding: 10px;
            margin-bottom: 15px; /* Space between rows */
        }
        .grid-item:hover {
            background-color: #f8f8f8; /* Slight highlight on hover */
        }
    </style>
    <div class="container">
        <div class="row">
"""

# Iterate over components to create grid cells with borders and padding
for i, component in enumerate(data.get('components', [])):
    if i % 6 == 0 and i != 0:
        html_content += '</div><div class="row">'  # Start a new row after every 5 integrations

    html_content += f"""
        <div class="col-md-2 grid-item text-center">
            <img src="{component.get('logo', '')}" style="width: 75px; height: 75px; cursor: pointer;" alt="{component.get('component', '')} Logo" data-toggle="modal" data-target="#modal{i}">
            <p>{component.get('component', '')}</p>
        </div>
    """

    # Modal with integration details
    html_content += f"""
        <div class="modal fade" id="modal{i}" tabindex="-1" role="dialog" aria-labelledby="modalLabel{i}" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalLabel{i}">{component.get('component', '')}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <img src="{component.get('logo', '')}" style="width: 100px; height: 100px;" alt="{component.get('component', '')} Logo">
                        <p><strong>Description:</strong> {component.get('description', '')}</p>
                        <p><strong>Version:</strong> {component.get('version', '')}</p>
                        <p><strong>URL:</strong> <a href="{component.get('url', '')}">{component.get('url', '')}</a></p>
                        <p><strong>Tags:</strong> {", ".join(component.get('tags', []))}</p>
                        <div>
                            {"".join([f'<img src="{asset.get("image", "")}" style="width: 100%; height: auto; margin-top: 10px;" alt="dashboard" />' for asset in component.get('gallery', [])])}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """
html_content += """
        </div> <!-- Closing row -->
    </div> <!-- Closing container -->
"""

# ... write HTML content to file ...


# Write HTML content to file
with open('../integrations/observability/catalog.html', 'w') as file:
    file.write(html_content)

print("HTML file created successfully.")
