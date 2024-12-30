import argparse
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AzureBlobDatastore, AccountKeyConfiguration


def create_blob_datastore(
    subscription_id,
    resource_group,
    workspace_name,
    datastore_name,
    storage_account_name,
    container_name,
    storage_account_key,
):
    # Define credentials (interactive authentication)
    credential = DefaultAzureCredential()

    # Initialize the MLClient
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name,
    )

    # Define the Azure Blob datastore configuration
    datastore = AzureBlobDatastore(
        name=datastore_name,
        account_name=storage_account_name,
        container_name=container_name,
        credentials=AccountKeyConfiguration(account_key=storage_account_key),
    )

    # Create or update the datastore
    try:
        ml_client.datastores.create_or_update(datastore)
        print(f"Datastore '{datastore.name}' created successfully.")
    except Exception as e:
        print(f"Failed to create datastore: {e}")

    # List all datastores in the workspace
    print("Listing all datastores:")
    datastores = ml_client.datastores.list()
    for ds in datastores:
        print(f"- {ds.name}")


def main():
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(
        description="Create an Azure Blob Datastore in Azure ML."
    )
    parser.add_argument(
        "--subscription-id", required=True, help="Azure Subscription ID"
    )
    parser.add_argument("--resource-group", required=True, help="Resource Group Name")
    parser.add_argument(
        "--workspace-name", required=True, help="Azure ML Workspace Name"
    )
    parser.add_argument("--datastore-name", required=True, help="Datastore Name")
    parser.add_argument(
        "--storage-account-name", required=True, help="Azure Storage Account Name"
    )
    parser.add_argument("--container-name", required=True, help="Blob Container Name")
    parser.add_argument(
        "--storage-account-key", required=True, help="Storage Account Key"
    )

    args = parser.parse_args()

    # Call the function to create a datastore
    create_blob_datastore(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        datastore_name=args.datastore_name,
        storage_account_name=args.storage_account_name,
        container_name=args.container_name,
        storage_account_key=args.storage_account_key,
    )


if __name__ == "__main__":
    main()


# python azure_ml\datastore\az_ml_datastore.py `
#   --subscription-id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#   --resource-group "rg_demo03" `
#   --workspace-name "ws_demo_pipeline03" `
#   --datastore-name "datastorepy01" `
#   --storage-account-name "azstorageblobci03" `
#   --container-name "containerpipline03" `
#   --storage-account-key "I5mdmIQyMmMviahbQ7Qv0DQZ8kRfouMh/os1m5ChkoNJ07tv+JK08AkSzwmbn8V9ARPwKiZ7JE6p+AStXD5hRA=="
