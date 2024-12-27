# Azure Machine Learning Workspace CLI v2 Commands Guide

## Prerequisites

Before creating an Azure ML workspace, ensure you have the necessary tools and authentication:

```bash
# Install Azure CLI ML extension
az extension add -n ml

# Login to Azure
az login

# Set subscription
az account set -s "<subscription-id>"
```

## Resource Group Creation

Create a resource group if you don't have one:

```bash
az group create `
    --name "my-resource-group" `
    --location "eastus"
```

## Workspace Creation Commands

### Basic Workspace Creation
The simplest way to create a workspace with default settings:

```bash
az ml workspace create `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --location "eastus"
```

### Advanced Workspace Creation
Create a workspace with all available parameters:

```bash
az ml workspace create `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --location "eastus" `
    --display-name "My ML Workspace" `
    --description "Workspace for ML projects" `
    --storage-account "mystorageaccount" `
    --key-vault "mykeyvault" `
    --application-insights "myappinsights" `
    --container-registry "myacr" `
    --tags "environment=development" "project=mlops" `
    --image-build-compute-name "image-build-cluster" `
    --public-network-access "Enabled" `
    --v1-legacy-mode false
```

### Custom Storage SKU Workspace
Create a workspace with a specific storage account SKU:

```bash
az ml workspace create `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --location "eastus" `
    --storage-account-sku "Standard_LRS"
```

### ARM Template-based Creation
Create a workspace using an ARM template:

```bash
az ml workspace create `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --template-file "workspace-template.json"
```

## Workspace Management Commands

### View Workspace Details
Get information about an existing workspace:

```bash
az ml workspace show `
    --name "my-workspace" `
    --resource-group "my-resource-group"
```

### List Workspaces
List all workspaces in a resource group:

```bash
az ml workspace list `
    --resource-group "my-resource-group"
```

### Update Workspace
Modify an existing workspace:

```bash
az ml workspace update `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --description "Updated workspace description"
```

### Delete Workspace
Remove a workspace and its resources:

```bash
az ml workspace delete `
    --name "my-workspace" `
    --resource-group "my-resource-group" `
    --yes
```

## Parameter Reference

### Required Parameters
- `--name`: Workspace name (must be globally unique within subscription)
- `--resource-group`: Resource group name
- `--location`: Azure region (e.g., eastus, westeurope)

### Optional Parameters
- `--display-name`: Friendly name for the workspace
- `--description`: Workspace description
- `--storage-account`: Existing storage account name
- `--key-vault`: Existing key vault name
- `--application-insights`: Existing Application Insights instance
- `--container-registry`: Existing container registry
- `--storage-account-sku`: SKU for new storage account (default: Standard_LRS)
- `--tags`: Resource tags in key=value format
- `--public-network-access`: Enable/disable public network access
- `--v1-legacy-mode`: Enable/disable v1 legacy mode
- `--image-build-compute-name`: Compute name for image building

## Important Notes

1. **Resource Dependencies**
   - If not specified, dependent resources (storage, key vault, etc.) are created automatically
   - Use existing resource parameters to connect to pre-existing resources

2. **Location Considerations**
   - Workspace location should match resource group location
   - Choose a region that supports all required services

3. **Security**
   - Ensure proper RBAC permissions in your subscription
   - Consider network access requirements when setting public-network-access

4. **Best Practices**
   - Use meaningful tags for resource organization
   - Include descriptive names and descriptions
   - Consider using ARM templates for repeatable deployments

5. **Naming Rules**
   - Workspace names must be globally unique
   - Use lowercase letters, numbers, and hyphens
   - Length between 2-32 characters