import requests
import subprocess
import os
import zipfile

# Sample command: ./alias_init.sh -e <OpenSearch Cluster Endpoint> -u <myusername> -p <mypassword>
es_endpoint = "https://search-os-test-domain-2-oct-standby-e5pueph5voy3mirwv2h5pquhkq.aos.ap-southeast-1.on.aws"
es_username = "kevlw"
es_password = "123Legoland!"

# GitHub raw URL
url = "https://raw.githubusercontent.com/Kevlw-AWS/opensearch-catalog-security/security-lake/integrations/security/OCSF_1_1_0/Init_scripts/alias_init.sh"

# Save the file to a local path
local_file = "alias_init.sh"

# Use the requests library to download the file
response = requests.get(url)

with open(local_file, "w") as f:
    f.write(response.text)

print(f"File saved to: {local_file}")

# Make the script executable
import os
os.chmod(local_file, 0o755)

# Run the script with the provided arguments
subprocess.run(["/bin/bash", local_file, "-e", es_endpoint, "-u", es_username, "-p", es_password], check=True)

print("Script executed successfully")

# Download the component_templates.zip file
component_templates_url = "https://raw.githubusercontent.com/Kevlw-AWS/opensearch-catalog-security/security-lake/integrations/security/OCSF_1_1_0/schemas/component_templates.zip"
component_templates_local = "component_templates.zip"

response = requests.get(component_templates_url)
with open(component_templates_local, "wb") as f:
    f.write(response.content)

print(f"Downloaded {component_templates_local}")

# Extract the component templates from the zip file
with zipfile.ZipFile(component_templates_local, 'r') as zip_ref:
    zip_ref.extractall('.')

print("Extracted component templates")

# Change to the component_templates directory
os.chdir("component_templates")

# Run the bash command
for file in os.listdir():
    if file.endswith(".json"):
        template_name = os.path.splitext(file)[0].replace("_body", "")
        command = f"curl -u {es_username}:{es_password} -X PUT -H 'Content-Type: application/json' -d @{file} {es_endpoint}/_component_template/{template_name}"
        subprocess.run(command, shell=True, check=True)
        print(f"Created component template: {template_name}")


# Download the index_templates.zip file
index_templates_url = "https://raw.githubusercontent.com/Kevlw-AWS/opensearch-catalog-security/blob/security-lake/integrations/security/OCSF_1_1_0/schemas/index_templates.zip"
component_templates_local = "index_templates.zip"

response = requests.get(component_templates_url)
with open(component_templates_local, "wb") as f:
    f.write(response.content)

print(f"Downloaded {component_templates_local}")

# Extract the component templates from the zip file
with zipfile.ZipFile(component_templates_local, 'r') as zip_ref:
    zip_ref.extractall('.')

print("Extracted component templates")

# Change to the component_templates directory
os.chdir("component_templates")

# Run the bash command
for file in os.listdir():
    if file.endswith(".json"):
        template_name = os.path.splitext(file)[0].replace("_body", "")
        command = f"curl -u {es_username}:{es_password} -X PUT -H 'Content-Type: application/json' -d @{file} {es_endpoint}/_component_template/{template_name}"
        subprocess.run(command, shell=True, check=True)
        print(f"Created component template: {template_name}")