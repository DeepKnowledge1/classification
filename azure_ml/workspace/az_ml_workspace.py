import argparse
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace


def create_workspace(subscription_id, resource_group, workspace_name, region):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Initialize MLClient
    ml_client = MLClient(credential, subscription_id, resource_group)

    print(
        f"Creating Azure ML Workspace '{workspace_name}' in resource group '{resource_group}'..."
    )

    # Define the workspace object
    workspace = Workspace(
        name=workspace_name,
        location=region,
        display_name="My Azure ML Workspace",
        description="Workspace created via Python SDK v2",
        tags={"environment": "demo", "project": "azure-ml"},
    )

    # Create the workspace
    ml_client.workspaces.begin_create(workspace)
    print(f"Workspace '{workspace_name}' created successfully!")


def main():
    # Define argument parser
    parser = argparse.ArgumentParser(
        description="Create an Azure ML Workspace via Python SDK v2."
    )
    parser.add_argument(
        "--subscription_id", type=str, required=True, help="Azure Subscription ID"
    )
    parser.add_argument(
        "--resource_group", type=str, required=True, help="Resource group name"
    )
    parser.add_argument(
        "--workspace_name", type=str, required=True, help="Workspace name"
    )
    parser.add_argument(
        "--region",
        type=str,
        required=True,
        help="Azure region for the workspace (e.g., eastus)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Call the create_workspace function
    create_workspace(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        region=args.region,
    )


if __name__ == "__main__":
    main()


## Usage

# python az_ml_workspace.py `
#   --subscription_id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#   --resource_group "rg_demo_01" `
#   --workspace_name "ws_demo_py01" `
#   --region "eastus"
