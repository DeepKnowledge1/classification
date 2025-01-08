import argparse
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ComputeInstance
from azure.identity import DefaultAzureCredential


def create_compute_instance(
    subscription_id, resource_group, workspace_name, compute_name, vm_size
):
    """
    Create a Compute Instance in Azure ML workspace.

    Args:
        subscription_id (str): Azure Subscription ID.
        resource_group (str): Azure Resource Group Name.
        workspace_name (str): Azure ML Workspace Name.
        compute_name (str): Name of the Compute Instance.
        vm_size (str): VM size for the Compute Instance (e.g., Standard_DS11_v2).
    """
    try:
        # Initialize MLClient
        ml_client = MLClient(
            DefaultAzureCredential(), subscription_id, resource_group, workspace_name
        )

        # Create Compute Instance configuration
        compute_instance = ComputeInstance(name=compute_name, size=vm_size)

        # Create Compute Instance
        ml_client.compute.begin_create_or_update(compute_instance).result()
        print(f"Compute instance '{compute_name}' created successfully.")

    except Exception as e:
        print(f"Failed to create compute instance: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a Compute Instance in Azure ML using SDK v2."
    )
    parser.add_argument(
        "--subscription_id", required=True, help="Azure Subscription ID"
    )
    parser.add_argument(
        "--resource_group", required=True, help="Azure Resource Group Name"
    )
    parser.add_argument(
        "--workspace_name", required=True, help="Azure ML Workspace Name"
    )
    parser.add_argument(
        "--compute_name",
        default="compute-instance-demo",
        help="Name of the Compute Instance",
    )
    parser.add_argument(
        "--vm_size", default="Standard_DS11_v2", help="VM size for the Compute Instance"
    )

    args = parser.parse_args()

    # Create Compute Instance
    create_compute_instance(
        args.subscription_id,
        args.resource_group,
        args.workspace_name,
        args.compute_name,
        args.vm_size,
    )


if __name__ == "__main__":
    main()


# python azure_ml\compute_instance\az_ml_compute_instance.py `
#         --subscription_id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#         --resource_group "rg_demo03" `
#         --workspace_name "ws_demo_pipeline03" `
#         --compute_name "compute-py01" `
#         --vm_size "Standard_DS3_v2"
