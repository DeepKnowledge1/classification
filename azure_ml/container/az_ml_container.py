import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient


def get_storage_account_key(subscription_id, resource_group, storage_account_name):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)

    keys = storage_client.storage_accounts.list_keys(
        resource_group, storage_account_name
    )
    return keys.keys[0].value


def create_container(blob_service_client, container_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
        print(f"Container '{container_name}' created successfully.")
    except Exception as e:
        print(f"Container creation failed or already exists: {e}")


def upload_blob(blob_service_client, container_name, blob_name, file_path):
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(
            f"File '{file_path}' uploaded to blob '{blob_name}' in container '{container_name}'."
        )
    except Exception as e:
        print(f"Blob upload failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a container and upload a file using Azure SDK v2."
    )
    parser.add_argument(
        "--subscription_id",
        default="5eab4ecc-5ecf-4754-802d-6da984293b70",
        help="Azure Subscription ID",
    )
    parser.add_argument(
        "--resource_group", default="rg_demo01", help="Azure Resource Group Name"
    )
    parser.add_argument(
        "--storage_account",
        default="storageaccountcli01",
        help="Azure Storage Account Name",
    )
    parser.add_argument(
        "--container_name", default="containerpy01", help="Container Name"
    )
    parser.add_argument(
        "--file_path", default="./data/Date_Fruit_Datasets.csv", help="Local File Path"
    )
    parser.add_argument(
        "--blob_name", default="Date_Fruit_Datasets.csv", help="Blob Name"
    )

    args = parser.parse_args()

    # Get storage account key
    storage_account_key = get_storage_account_key(
        args.subscription_id, args.resource_group, args.storage_account
    )

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient(
        account_url=f"https://{args.storage_account}.blob.core.windows.net",
        credential=storage_account_key,
    )

    # Create container
    create_container(blob_service_client, args.container_name)

    # Upload file to container
    upload_blob(
        blob_service_client, args.container_name, args.blob_name, args.file_path
    )


if __name__ == "__main__":
    main()
