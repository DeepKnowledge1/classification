import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient


def create_storage_account(
    subscription_id, resource_group, storage_account_name, region
):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Initialize StorageManagementClient
    storage_client = StorageManagementClient(credential, subscription_id)

    print(
        f"Creating Azure Storage Account '{storage_account_name}' in resource group '{resource_group}'..."
    )

    # Define the storage account parameters
    storage_account_params = {
        "sku": {"name": "Standard_LRS"},
        "kind": "BlobStorage",
        "location": region,
        "tags": {"environment": "demo", "project": "azure-ml"},
        "properties": {"accessTier": "Hot"},  # Options: "Hot" or "Cool"
    }

    # Create the storage account
    storage_client.storage_accounts.begin_create(
        resource_group_name=resource_group,
        account_name=storage_account_name,
        parameters=storage_account_params,
    ).result()

    print(f"Storage Account '{storage_account_name}' created successfully!")


def connect_to_blob_service(storage_account_name):
    # Authenticate and connect to Blob Service
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net/",
        credential=credential,
    )

    print(f"Connected to Blob Service for Storage Account '{storage_account_name}'.")

    # List containers
    print("Available containers:")
    for container in blob_service_client.list_containers():
        print(f" - {container['name']}")


def main():
    # Define argument parser
    parser = argparse.ArgumentParser(
        description="Create an Azure Storage Account via Python SDK v2."
    )
    parser.add_argument(
        "--subscription_id", type=str, required=True, help="Azure Subscription ID"
    )
    parser.add_argument(
        "--resource_group", type=str, required=True, help="Resource group name"
    )
    parser.add_argument(
        "--storage_account_name", type=str, required=True, help="Storage account name"
    )
    parser.add_argument(
        "--region",
        type=str,
        required=True,
        help="Azure region for the storage account (e.g., eastus)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Call the create_storage_account function
    create_storage_account(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        storage_account_name=args.storage_account_name,
        region=args.region,
    )

    # Connect to the blob service
    connect_to_blob_service(storage_account_name=args.storage_account_name)


if __name__ == "__main__":
    main()


# python az_storage_account.py `
#   --subscription_id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#   --resource_group "rg_demo_01" `
#   --storage_account_name "storageacctdemo01" `
#   --region "eastus"
