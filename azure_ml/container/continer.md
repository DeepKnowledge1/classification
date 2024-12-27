# How to Create a Container in Azure Storage

This guide will help you create a container in Azure Storage, upload a file to it, and set the required configurations. Follow the steps below:

## Prerequisites
1. Azure CLI installed on your machine.
2. Access to an Azure subscription.
3. A storage account and resource group already set up in your Azure environment.

---

## Steps

### 1. Get the Storage Account Key
The storage account key is necessary for authentication to perform operations on the storage account.

```powershell
$STORAGE_ACCOUNT_KEY = az storage account keys list `
    --resource-group $RESOURCE_GROUP `
    --account-name $STORAGE_NAME `
    --query "[0].value" `
    -o tsv
```
Replace the following placeholders:
- `$RESOURCE_GROUP` with the name of your resource group.
- `$STORAGE_NAME` with the name of your storage account.

### 2. Create a Container
Create a container if it doesn't already exist. Containers are used to store blobs in Azure.

```powershell
az storage container create `
    --account-name $STORAGE_NAME `
    --name $CONTAINER_NAME `
    --account-key $STORAGE_ACCOUNT_KEY `
    --public-access off
```
Replace the following placeholders:
- `$STORAGE_NAME` with the name of your storage account.
- `$CONTAINER_NAME` with the desired name for your container.

### 3. Upload a File to the Container
Upload a file from your local machine to the Azure container.

```powershell
$localFilePath = "./data/Date_Fruit_Datasets.csv"  # Replace with the local file path
$blobName = "data/Date_Fruit_Datasets.csv"  # The name you want for the file in the container

az storage blob upload `
    --account-name $STORAGE_NAME `
    --container-name $CONTAINER_NAME `
    --file $localFilePath `
    --name $blobName `
    --account-key $STORAGE_ACCOUNT_KEY
```
Replace the following placeholders:
- `$localFilePath` with the path to the file on your local system.
- `$blobName` with the name you want the file to have in the container.

---

## Additional Notes
- Use the `--public-access` flag in the container creation command to configure access levels (`off`, `blob`, or `container`).
- Ensure your file paths and storage account details are correct to avoid errors.

For more details, refer to the [Azure CLI documentation](https://learn.microsoft.com/en-us/cli/azure/storage).

