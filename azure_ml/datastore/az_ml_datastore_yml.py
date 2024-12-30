import argparse
import yaml
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AzureBlobDatastore, AccountKeyConfiguration


def create_blob_datastore(subscription_id, resource_group, workspace_name, config):
    # Extract parameters from the configuration
    datastore_name = config.get("name")
    storage_account_name = config.get("account_name")
    container_name = config.get("container_name")
    storage_account_key = config["credentials"]["account_key"]

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
        description="Create an Azure Blob Datastore in Azure ML using a YAML configuration file."
    )
    parser.add_argument(
        "--config-file", required=True, help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--subscription-id", required=True, help="Azure Subscription ID"
    )
    parser.add_argument("--resource-group", required=True, help="Resource Group Name")
    parser.add_argument(
        "--workspace-name", required=True, help="Azure ML Workspace Name"
    )

    args = parser.parse_args()

    # Load YAML configuration file
    try:
        with open(args.config_file) as yaml_file:
            config = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config_file}' not found.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return

    # Call the function to create a datastore
    create_blob_datastore(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        config=config,
    )


if __name__ == "__main__":
    main()


# python azure_ml/datastore/az_ml_datastore_yml.py `
#     --config-file "yml_files\datastore.yml" `
#     --subscription-id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#     --resource-group "rg_demo03" `
#     --workspace-name "ws_demo_pipeline03"
