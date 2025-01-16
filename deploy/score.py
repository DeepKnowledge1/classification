import json
import logging
import os
import pandas as pd
import mlflow


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model

    logging.info("Started model initialization.")
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"))
    logging.info(f"Loading model from {model_path}")

    # Print contents of model directory
    logging.info(f"Contents of {model_path}:")
    for item in os.listdir(model_path):
        logging.info(f"- {item}")

    try:
        model = mlflow.sklearn.load_model(model_path)
        logging.info("Model loaded successfully")

        # Log model type
        logging.info(f"Model type: {type(model)}")

    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        raise


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    """
    logging.info("Running model inference.")
    try:
        data = json.loads(raw_data)
        input_df = pd.DataFrame(data["data"])
        logging.info(f"Input data shape: {input_df.shape}")

        # Make predictions
        predictions = model.predict(input_df)
        logging.info("Predictions generated successfully")

        return json.dumps({"predictions": predictions.tolist()})

    except Exception as e:
        logging.error(f"Error during inference: {str(e)}")
        return json.dumps({"error": str(e)})
