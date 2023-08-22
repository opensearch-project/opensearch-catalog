# Correcting the file path and re-reading the contents of the JSON file
from beartype import beartype
@beartype
def generate_catalog_summery(file_path: str) -> bool:
    file_path = file_path + "/catalog.json"
    
    with open(file_path, 'r') as file:
        catalog_data = json.load(file)
    
    # Extracting the required fields
    catalog_name = catalog_data.get("catalog", "")
    version = catalog_data.get("version", "")
    url = catalog_data.get("url", "")
    description = catalog_data.get("description", "")
    display_name = catalog_data.get("displayName", "")
    license = catalog_data.get("license", "")
    labels = ", ".join(catalog_data.get("labels", []))
    author = catalog_data.get("author", "")
    logo_path = catalog_data.get("statics", {}).get("logo", {}).get("path", "")
    components = catalog_data.get("components", [])
    
    # Creating the HTML content with updated component structure (including logo and gallery)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{escape(display_name)}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 800px; margin: auto; }}
            .integrations {{ padding: 10px; border: 1px solid #ddd; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{escape(display_name)}</h1>
            <img src="{escape(logo_path)}" alt="Logo" />
            <p><strong>Version:</strong> {escape(version)}</p>
            <p><strong>URL:</strong> <a href="{escape(url)}">{escape(url)}</a></p>
            <p><strong>Description:</strong> {escape(description)}</p>
            <p><strong>License:</strong> {escape(license)}</p>
            <p><strong>Labels:</strong> {escape(labels)}</p>
            <p><strong>Author:</strong> {escape(author)}</p>
            <h2>Integrations</h2>
    """
    
    for component in components:
        component_name = component.get("component", "")
        component_description = component.get("description", "")
        component_version = component.get("version", "")
        component_logo = component.get("logo", "")
        component_url = component.get("url", "")
        component_tags = ", ".join(component.get("tags", []))
        gallery = component.get("gallery", [])
    
        html_content += f"""
            <div class="integrations">
                <h3>{escape(component_name)}</h3>
                <img src="{escape(component_logo)}" alt="{escape(component_name)} Logo" style="width: 75px; height: 75px;"/>
                <p><strong>Description:</strong> {escape(component_description)}</p>
                <p><strong>Version:</strong> {escape(component_version)}</p>
                <p><strong>URL:</strong> <a href="{escape(component_url)}">{escape(component_url)}</a></p>
                <p><strong>Tags:</strong> {escape(component_tags)}</p>
                <div class="gallery">
        """
    
        for asset in gallery:
            asset_name = asset.get("asset", "")
            asset_image = asset.get("image", "")
            html_content += f"""
                    <div class="asset">
                        <img src="{escape(asset_image)}" alt="{escape(asset_name)}" style="width: 350px; height: 250px;"/>
                    </div>
            """
    
        html_content += """
                </div>
            </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Saving the updated HTML file
    html_file_path = file_path + "/catalog.html"
    with open(html_file_path, 'w') as file:
        file.write(html_content)
    return true

if __name__ == "__main__":
    generate_catalog_summery("../../integrations/observability")
