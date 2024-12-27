# Creating a Blob Storage Account via Azure CLI

This guide explains how to create a Blob Storage Account in Azure using Azure CLI commands. Follow the steps below to set up your storage account.

## Prerequisites

- Azure CLI installed on your system.
- Logged into your Azure account using `az login`.
- A valid resource group exists, or you can create one.

## Commands

### Step 1: Define Variables
Set environment variables for reuse in commands:

```bash
RESOURCE_GROUP="<your-resource-group-name>"
STORAGE_ACCOUNT_NAME="<your-storage-account-name>"
LOCATION="<your-azure-region>"  # Example: eastus
```

Replace `<your-resource-group-name>`, `<your-storage-account-name>`, and `<your-azure-region>` with appropriate values.

### Step 2: Create a Resource Group (If Needed)
If you don't already have a resource group, create one using the following command:

```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### Step 3: Create the Blob Storage Account
Use the `az storage account create` command to create a Blob Storage Account:

```bash
az storage account create `
  --name $STORAGE_ACCOUNT_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS `
  --kind BlobStorage `
  --access-tier Hot
```

### Step 4: Verify the Storage Account
Confirm the storage account creation:

```bash
az storage account show --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP
```

### Step 5: List Storage Accounts (Optional)
List all storage accounts in your subscription:

```bash
az storage account list --output table
```

## Notes
- The `--access-tier` can be set to `Hot` for frequently accessed data or `Cool` for infrequently accessed data.
- Replace `Standard_LRS` with another SKU like `Standard_GRS` if required.

## Cleanup (Optional)
If you want to delete the storage account or resource group:

### Delete the Storage Account
```bash
az storage account delete --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP
```

### Delete the Resource Group
```bash
az group delete --name $RESOURCE_GROUP --no-wait --yes
```

## Conclusion
You've successfully created a Blob Storage Account using Azure CLI. Use this account to store and manage your blobs efficiently in Azure.

