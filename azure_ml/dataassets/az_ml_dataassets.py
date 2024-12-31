import argparse
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data


def create_data_asset(
    subscription_id,
    resource_group,
    workspace_name,
    data_asset_name,
    version,
    data_type,
    datastore_path,
    description,
    tags,
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

    # Define the data asset
    data_asset = Data(
        name=data_asset_name,
        version=version,
        type=data_type,  # uri_file, uri_folder, or mltable
        path=datastore_path,
        description=description,
        tags=tags,
    )

    # Create or update the data asset
    try:
        ml_client.data.create_or_update(data_asset)
        print(
            f"Data asset '{data_asset.name}' (version: {data_asset.version}) created successfully."
        )
    except Exception as e:
        print(f"Failed to create data asset: {e}")

    # List all data assets in the workspace
    print("Listing all data assets in the workspace:")
    data_assets = ml_client.data.list()
    for asset in data_assets:
        print(f"- {asset.name} (version: {asset.version})")


def main():
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(description="Create a Data Asset in Azure ML.")
    parser.add_argument(
        "--subscription-id", required=True, help="Azure Subscription ID"
    )
    parser.add_argument("--resource-group", required=True, help="Resource Group Name")
    parser.add_argument(
        "--workspace-name", required=True, help="Azure ML Workspace Name"
    )
    parser.add_argument("--data-asset-name", required=True, help="Data Asset Name")
    parser.add_argument("--version", required=True, help="Data Asset Version")
    parser.add_argument(
        "--data-type", required=True, help="Data Type (uri_file, uri_folder, mltable)"
    )
    parser.add_argument(
        "--datastore-path", required=True, help="Datastore Path (e.g., azureml://...)"
    )
    parser.add_argument(
        "--description", required=True, help="Description of the Data Asset"
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        help="Tags for the Data Asset (key=value pairs)",
        default=[],
    )

    args = parser.parse_args()

    # Convert tags from list of key=value to dictionary
    tags_dict = dict(tag.split("=") for tag in args.tags) if args.tags else {}

    # Call the function to create a data asset
    create_data_asset(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        data_asset_name=args.data_asset_name,
        version=args.version,
        data_type=args.data_type,
        datastore_path=args.datastore_path,
        description=args.description,
        tags=tags_dict,
    )


if __name__ == "__main__":
    main()


# python azure_ml\dataassets\az_ml_dataassets.py `
#   --subscription-id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#   --resource-group "rg_demo03" `
#   --workspace-name "ws_demo_pipeline03" `
#   --data-asset-name "fruits_data_asset" `
#   --version "5" `
#   --data-type "uri_file" `
#   --datastore-path "azureml://datastores/datastorefruits/paths/data/Date_Fruit_Datasets.csv" `
#   --description "Fruits data asset for training" `
#   --tags "purpose=training" "project=fruit-classification"
