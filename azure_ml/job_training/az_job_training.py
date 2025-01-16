import argparse
from azure.ai.ml import MLClient, load_job
from azure.identity import DefaultAzureCredential


def train_model(
    subscription_id: str,
    resource_group: str,
    workspace_name: str,
    compute_name: str,
    job_yaml: str,
) -> None:
    """
    Train a Machine Learning Model in Azure ML using SDK v2.

    Args:
        subscription_id (str): Azure Subscription ID.
        resource_group (str): Azure Resource Group Name.
        workspace_name (str): Azure ML Workspace Name.
        compute_name (str): Name of the Compute Cluster.
        job_yaml (str): Path to the YAML file for the training job.
    """
    try:
        # Initialize MLClient
        ml_client = MLClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name,
        )

        # Load the job configuration
        job = load_job(source=job_yaml)

        # Override compute if specified (optional)
        # if compute_name:
        #     job.compute = compute_name

        # Submit the job
        returned_job = ml_client.jobs.create_or_update(job=job)
        print(f"Training job '{returned_job.name}' submitted successfully.")

        # Stream job logs
        ml_client.jobs.stream(returned_job.name)
        print(f"Training job '{returned_job.name}' completed.")

    except Exception as e:
        print(f"Error training model: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Train a Machine Learning Model in Azure ML using SDK v2."
    )
    parser.add_argument(
        "--subscription_id",
        # required=True,
        help="Azure Subscription ID",
    )
    parser.add_argument(
        "--resource_group",
        # required=True,
        help="Azure Resource Group Name",
    )
    parser.add_argument(
        "--workspace_name",
        # required=True,
        help="Azure ML Workspace Name",
    )
    parser.add_argument(
        "--compute_name",
        help="Name of the Compute Cluster (optional, overrides YAML if specified)",
    )
    parser.add_argument(
        "--job_yaml",
        # required=True,
        help="Path to the YAML file for the training job",
    )

    args = parser.parse_args()

    # Train the model
    train_model(
        args.subscription_id,
        args.resource_group,
        args.workspace_name,
        args.compute_name,
        args.job_yaml,
    )


if __name__ == "__main__":
    main()

# Example usage:

# python azure_ml\job_training\az_job_training.py `
#     --subscription_id "5eab4ecc-5ecf-4754-802d-6da984293b70" `
#     --resource_group "rg_demo03" `
#     --workspace_name "ws_demo_pipeline03" `
#     --compute_name "oo" `
#     --job_yaml "./yml_files/job.yaml"
