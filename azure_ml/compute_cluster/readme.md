# Creating a Compute Cluster in Azure ML using CLI v2

This document provides step-by-step instructions for creating a compute cluster in Azure Machine Learning (Azure ML) using CLI v2, along with related commands for managing compute resources.

---

## Prerequisites
1. Azure CLI installed and updated to version 2.0 or later.
2. Azure Machine Learning CLI v2 extension installed.
   ```bash
   az extension add -n ml -y
   ```
3. An Azure ML workspace created.
4. Sufficient permissions to create and manage compute resources.
5. A configured Azure ML workspace using the `az ml workspace` command.
   ```bash
   $RESOURCE_GROUP="rg_demo03"
   $WORKSPACE="ws_demo_pipeline03"

   az ml workspace update -w $WORKSPACE -g $RESOURCE_GROUP
   ```

---

## Step-by-Step Guide

### 1. Create a Compute Cluster

Run the following command to create a compute cluster:
```bash
az ml compute create --name my-compute-cluster `
                     --type AmlCompute `
                     --size <vm-size> `
                     --min-instances <min-nodes> `
                     --max-instances <max-nodes> `
                     --idle-time-before-scale-down <idle-time> `
                     -w $WORKSPACE `
                     -g $RESOURCE_GROUP
```
**Parameters:**
- `my-compute-cluster`: Unique name for your compute cluster.
- `<vm-size>`: Virtual machine size (e.g., `Standard_DS3_v2`).
- `<min-nodes>`: Minimum number of nodes (default: 0).
- `<max-nodes>`: Maximum number of nodes.
- `<idle-time>`: Time (in seconds) before idle nodes are deallocated.

### Example:
```bash
az ml compute create --name my-compute-cluster `
                     --type AmlCompute `
                     --size Standard_DS3_v2 `
                     --min-instances 0 `
                     --max-instances 4 `
                     --idle-time-before-scale-down 120 `
                     -w $WORKSPACE `
                     -g $RESOURCE_GROUP
```

---

## Related Commands

### 1. List Available Compute Resources
To list all compute resources in your workspace:
```bash
az ml compute list -w $WORKSPACE -g $RESOURCE_GROUP
```

### 2. Show Compute Cluster Details
To view details about a specific compute cluster:
```bash
az ml compute show --name my-compute-cluster -w $WORKSPACE -g $RESOURCE_GROUP
```

### 3. Update Compute Cluster Settings
To update the settings of an existing compute cluster:
```bash
az ml compute update --name my-compute-cluster `
                     --min-instances <new-min-nodes> `
                     --max-instances <new-max-nodes> `
                     -w $WORKSPACE `
                     -g $RESOURCE_GROUP
```

### 4. Delete a Compute Cluster
To delete a compute cluster:
```bash
az ml compute delete --name my-compute-cluster -w $WORKSPACE -g $RESOURCE_GROUP --yes
```

### 5. Monitor Cluster Usage
To monitor cluster metrics (e.g., CPU, memory usage):
```bash
az ml compute monitor --name my-compute-cluster -w $WORKSPACE -g $RESOURCE_GROUP
```

---

## Notes
- Use appropriate VM sizes based on your workload requirements and budget.
- Configure autoscaling carefully to minimize idle costs.
- Always monitor usage and optimize the cluster for cost efficiency.

---

## Conclusion
This README provides the necessary commands to create and manage a compute cluster in Azure ML using CLI v2. With these commands, you can streamline the process of scaling and managing your machine learning workloads effectively. For additional details, refer to the [Azure ML documentation](https://learn.microsoft.com/en-us/azure/machine-learning/).

