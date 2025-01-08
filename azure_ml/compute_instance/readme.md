# Creating a Compute Instance in Azure ML Using CLI v2

This guide walks you through the process of creating a compute instance in Azure Machine Learning (Azure ML) using the Azure CLI v2.

---

## **Prerequisites**

Ensure the following before proceeding:

1. **Azure CLI Installed**: Download and install the Azure CLI from [Azure CLI Installation Guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. **Azure ML Extension Installed**: Add the Azure ML extension by running:

   ```bash
   az extension add -n ml
   ```

3. **Log in to Azure**: Authenticate your Azure CLI session:

   ```bash
   az login
   ```

4. **Access to Azure ML Workspace**: You need an existing Azure ML workspace to create a compute instance.

---

## **Step 1: Verify Your Azure ML Workspace**

List all available Azure ML workspaces in your resource group:

```bash
az ml workspace list -g <your-resource-group>
```

Replace `<your-resource-group>` with your actual resource group name. Note the `workspaceName` for the next steps.

---

## **Step 2: Create a Compute Instance**

Use the following command to create a compute instance:

```bash
az ml compute create --name compute-cli01 `
                     --type ComputeInstance `
                     --size Standard_DS3_v2 `
                     --workspace-name ws_demo_pipeline03 `
                     --resource-group rg_demo03
```


### **Parameters Explained**
- `--name`: The name of the compute instance (e.g., `ml-compute-demo`).
- `--type`: Always set to `ComputeInstance`.
- `--size`: Specify the virtual machine size. Common options include `Standard_DS11_v2` or `Standard_DS3_v2`.
- `--workspace-name`: The name of your Azure ML workspace.
- `--resource-group`: The resource group containing your Azure ML workspace.

### **Example**

```bash
az ml compute create --name my-compute-instance `
                     --type ComputeInstance `
                     --size Standard_DS11_v2 `
                     --workspace-name my-ml-workspace `
                     --resource-group my-resource-group
```

The compute instance will now be provisioned. This may take a few minutes.

---

## **Step 3: Check the Status of the Compute Instance**

After creating the compute instance, verify its status using:

```bash
az ml compute show --name <compute-instance-name> `
                   --workspace-name <workspace-name> `
                   --resource-group <resource-group-name>
```

This command will display details about the compute instance, including its current status (e.g., `Creating`, `Running`, `Stopped`).

---

## **Step 4: List All Compute Instances**

To view all compute resources in your Azure ML workspace:

```bash
az ml compute list --workspace-name <workspace-name> `
                   --resource-group <resource-group-name>
```

---

## **Step 5: Stop the Compute Instance**

Stopping a compute instance when not in use can help save costs. Use the following command:

```bash
az ml compute stop --name <compute-instance-name> `
                   --workspace-name <workspace-name> `
                   --resource-group <resource-group-name>
```

---

## **Step 6: Delete the Compute Instance**

If you no longer need the compute instance, delete it to free up resources:

```bash
az ml compute delete --name <compute-instance-name> `
                     --workspace-name <workspace-name> `
                     --resource-group <resource-group-name> --yes
```

The `--yes` flag confirms the deletion without further prompts.

---

## **Additional Tips**

- Always stop compute instances when they are not in use to save costs.
- Use parameterized scripts to automate the creation and management of compute instances.
- Regularly monitor your compute resources to optimize resource usage.

---

By following this guide, you have successfully learned how to create and manage compute instances in Azure ML using the CLI v2. If you have any questions, feel free to explore the [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/ml) for more details!
