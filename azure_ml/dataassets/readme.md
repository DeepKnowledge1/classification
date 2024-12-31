### README.md

---

# Create a Data Asset in Azure Machine Learning Using CLI v3

This guide explains how to create a **data asset** in Azure Machine Learning using **Azure CLI v3**. A data asset is a key component of Azure ML, enabling you to manage datasets for training, testing, and validation efficiently.

---

## Prerequisites

Before starting, ensure the following:

1. **Azure CLI Installed**:
   Download and install the Azure CLI from [Microsoft's official page](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

2. **Azure ML Extension**:
   Add the Azure Machine Learning extension using:
   ```bash
   az extension add --name ml
   ```

3. **Login to Azure**:
   Authenticate your Azure CLI session:
   ```bash
   az login
   ```

4. **Resource Group and Workspace**:
   You must have an existing Azure resource group and ML workspace.

5. **Prepare a YAML File**:
   Create a YAML file (`data-asset.yml`) with metadata about the data asset.

---

## YAML File Structure

Below is an example of a YAML file (`data-asset.yml`) used to define the data asset:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
name: fruits_data_asset
version: 1
type: uri_file
path: azureml://datastores/datastorefruits/paths/data/Date_Fruit_Datasets.csv
description: "fruits_data_asset data for training"
tags:
  purpose: training
```

- **`name`**: Name of the data asset.
- **`version`**: Version number for version control.
- **`type`**: The type of data (`uri_file` or `uri_folder`).
- **`path`**: Path to the data, e.g., a file in an Azure Blob Storage.
- **`description`**: Description of the data asset.
- **`tags`**: Optional metadata for categorization.

---

## Create the Data Asset

Use the following command to create the data asset in Azure Machine Learning:

```bash
az ml data create `
    --file "./yml_files/data-asset.yml" `
    --resource-group "rg_demo03" `
    --workspace-name "ws_demo_pipeline03"
```

### Command Breakdown:
- `--file`: Path to the YAML file.
- `--resource-group`: Your Azure resource group name.
- `--workspace-name`: Your Azure ML workspace name.

---

## Verify the Data Asset

### In Azure CLI:
If the command is successful, you’ll see a confirmation output similar to:

```bash
{
  "name": "fruits_data_asset",
  "version": "1",
  "type": "uri_file",
  "description": "fruits_data_asset data for training",
  "tags": {
    "purpose": "training"
  }
}
```

### In Azure ML Studio:
1. Navigate to your Azure ML Studio at [Azure ML Studio](https://ml.azure.com/).
2. Click on **Data** in the sidebar.
3. Search for `fruits_data_asset` and verify its details.

---

## Tips and Best Practices

- **Version Control**: Always increment the version for updates to your data assets.
- **Tags**: Add meaningful tags for better organization and easier searchability.
- **Datastore Configuration**: Ensure that the datastore path (`datastorefruits`) is correctly set up in your workspace.

---

## Troubleshooting

If the command fails, check the following:
- **YAML File**: Verify the file structure and ensure there are no typos.
- **Resource Group and Workspace**: Ensure the provided names exist in your Azure account.
- **Datastore Path**: Confirm that the path specified in the YAML file is correct and accessible.

---

## Resources

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/ml)
- [Azure Machine Learning Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Azure ML YAML Schemas](https://azuremlschemas.azureedge.net/latest/)

---

Feel free to adapt this README for your project!