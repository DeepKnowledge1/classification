# Azure ML Model Deployment Guide

This repository contains code and configuration files for training and deploying a LightGBM classification model using Azure ML.

## Project Structure

```
.
├── classification/
│   └── classifier.py        # Contains DataSplitter and ModelTrainer classes
├── deploy/
│   ├── deployment.yml      # Model deployment configuration
│   └── endpoint.yml        # Endpoint configuration
│   └── score.py                # Model scoring script for inference
├── main.py                # Training pipeline script
└── README.md
```

## Prerequisites

- Azure CLI with ML extension
- Azure ML workspace
- Required Python packages (see environment configuration)

## Training the Model

The model is trained using the `main.py` script which:
1. Loads and preprocesses the data
2. Splits data into training and validation sets
3. Trains a LightGBM model
4. Saves the model using MLflow

To train the model:
```bash
az ml job create `
    --file "./yml_files/job.yaml" `
    --resource-group "rg_demo03" `
    --workspace-name "ws_demo_pipeline03"
```

## Deployment Process

### 1. Create an Endpoint

```bash
az ml online-endpoint create `
    --file ./azure_ml/deploy_model/endpoint.yml `
    --resource-group rg_demo03 `
    --workspace-name ws_demo_pipeline03
```

### 2. Deploy the Model

```bash
az ml online-deployment create `
    --file ./azure_ml/deploy_model//deployment.yml `
    --resource-group rg_demo03 `
    --workspace-name ws_demo_pipeline03
```

### 3. Check Deployment Logs

```bash
az ml online-deployment get-logs `
    --name blue `
    --endpoint-name fruit-endpoint `
    --resource-group rg_demo03 `
    --workspace-name ws_demo_pipeline03
```

### 4. Delete a Deployment (if needed)

```bash
az ml online-deployment delete `
    --name blue `
    --endpoint-name fruit-endpoint `
    --resource-group rg_demo03 `
    --workspace-name ws_demo_pipeline03 `
    --yes
```

## Important Notes

- Always wait 2-3 minutes between deleting and creating new deployments
- Monitor deployment logs while deploying to track progress
- The scoring script (`score.py`) must match the training process:
  - Model is loaded from the "outputs" directory
  - Uses `model.predict()` for predictions
  - Handles both binary and multi-class cases
  - Properly maps numeric predictions to class labels

## Model Input/Output Format

### Input Format
```json
{
    "data": [
        {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    ]
}
```

### Output Format
```json
{
    "predictions": ["Class1", "Class2", ...],
    "probabilities": {
        "Class1": [0.8, 0.1, ...],
        "Class2": [0.1, 0.7, ...],
        ...
    }
}
```

## Troubleshooting

1. **Container Crashes**: Check if model path in `score.py` points to "outputs" directory
2. **Model Loading Errors**: Verify unique_labels.json exists in model artifacts
3. **Deployment Failures**: Ensure previous deployments are fully deleted before creating new ones

## Contributing

Please follow these steps for contributing:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

# Data

```
{
    "data": [{
        "AREA": 21909,
        "PERIMETER": 542.17,
        "MAJOR_AXIS": 172.44,
        "MINOR_AXIS": 162.37,
        "ECCENTRICITY": 0.32,
        "EQDIASQ": 166.92,
        "SOLIDITY": 0.9859,
        "CONVEX_AREA": 22223,
        "EXTENT": 0.7354,
        "ASPECT_RATIO": 1.0619,
        "ROUNDNESS": 0.9368,
        "COMPACTNESS": 0.9408,
        "SHAPEFACTOR_1": 0.0134,
        "SHAPEFACTOR_2": 0.0066,
        "SHAPEFACTOR_3": 0.9866,
        "SHAPEFACTOR_4": 0.9934,
        "MeanRR": 0.3255,
        "MeanRG": 0.3438,
        "MeanRB": 0.3307,
        "StdDevRR": 0.0458,
        "StdDevRG": 0.0431,
        "StdDevRB": 0.0445,
        "SkewRR": -0.0055,
        "SkewRG": -0.0371,
        "SkewRB": -0.0092,
        "KurtosisRR": 0.0928,
        "KurtosisRG": 0.1421,
        "KurtosisRB": 0.1213,
        "EntropyRR": 0.9856,
        "EntropyRG": 0.9897,
        "EntropyRB": 0.9885,
        "ALLdaub4RR": 99.4614,
        "ALLdaub4RG": 99.4331,
        "ALLdaub4RB": 99.4521
    }]
}
```
