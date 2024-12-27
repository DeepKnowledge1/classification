I'll provide you with a comprehensive guide to working with resource groups using Azure CLI v2 (Azure CLI). Here are all the key commands related to resource groups:

1. **Login to Azure**
```bash
az login
```

2. **Create a Resource Group**
```bash
# Basic syntax
az group create --name <resource-group-name> --location <location>

# Example
az group create --name MyResourceGroup --location eastus
```

3. **List Resource Groups**
```bash
# List all resource groups in the subscription
az group list

# List resource groups in a more readable table format
az group list --output table
```

4. **Show Details of a Specific Resource Group**
```bash
az group show --name <resource-group-name>
```

5. **Delete a Resource Group**
```bash
# Standard delete
az group delete --name <resource-group-name>

# Delete with confirmation prompt
az group delete --name <resource-group-name> --yes
```

6. **Update Resource Group Tags**
```bash
# Add or modify tags
az group update --name <resource-group-name> --tags key1=value1 key2=value2

# Remove all tags
az group update --name <resource-group-name> --tags ''
```

7. **List Resources within a Resource Group**
```bash
# List all resources in a resource group
az resource list --resource-group <resource-group-name>

# List in table format
az resource list --resource-group <resource-group-name> --output table
```

8. **Move Resources between Resource Groups**
```bash
# Move one or more resources to another resource group
az resource move --destination-group <destination-resource-group> --ids <resource-id1> <resource-id2>
```

9. **Check Existing Resource Group Names**
```bash
# Check if a resource group name is available
az group exists --name <resource-group-name>
```

10. **Export Resource Group Template**
```bash
# Export the template of an existing resource group
az group export --name <resource-group-name> > resourcegroup.json
```

**Pro Tips**:
- Always ensure you're in the correct subscription before creating or managing resource groups
- Use `az account show` to verify your current subscription
- Switch subscriptions if needed with `az account set --subscription <subscription-id>`

**Common Flags and Options**:
- `--output` or `-o`: Control output format (table, json, tsv)
- `--verbose`: Get more detailed output
- `--debug`: Get full debug information

Remember to replace `<resource-group-name>`, `<location>`, and `<resource-id>` with your actual resource group name, Azure region, and resource identifiers respectively.

Would you like me to elaborate on any of these commands or explain how to use them in more specific scenarios?