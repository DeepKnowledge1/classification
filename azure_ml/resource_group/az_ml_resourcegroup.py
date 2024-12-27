import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


def create_resource_group(subscription_id, resource_group_name, location):
    """
    Create an Azure Resource Group using the Azure SDK for Python.

    Parameters:
        subscription_id (str): Azure subscription ID.
        resource_group_name (str): Name of the resource group to create.
        location (str): Azure region for the resource group.
    """
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create ResourceManagementClient
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Resource Group parameters
    resource_group_params = {"location": location}

    print(f"Creating Resource Group '{resource_group_name}' in '{location}'...")
    resource_group = resource_client.resource_groups.create_or_update(
        resource_group_name, resource_group_params
    )

    print(f"Resource Group '{resource_group.name}' created successfully!")
    print(f"Location: {resource_group.location}")


def main():
    # Set up argument parsing for dynamic input
    parser = argparse.ArgumentParser(description="Create an Azure Resource Group.")
    parser.add_argument(
        "--subscription_id",
        type=str,
        default="5eab4ecc-5ecf-4754-802d-6da984293b70",
        help="Azure Subscription ID.",
    )
    parser.add_argument(
        "--resource_group_name",
        type=str,
        default="resource_group_py01",
        help="Resource Group Name.",
    )
    parser.add_argument(
        "--location",
        type=str,
        default="eastus",
        help="Azure Region (e.g., eastus, westus).",
    )

    args = parser.parse_args()

    # Call the function to create the resource group
    create_resource_group(args.subscription_id, args.resource_group_name, args.location)


if __name__ == "__main__":
    main()
