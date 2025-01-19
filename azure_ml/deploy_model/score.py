import os
import logging
import json
import numpy as np
import pandas as pd
import mlflow.sklearn


def init():
    """
    Initialize model. This function is called when the container is initialized/started.
    """
    global model
    global unique_labels

    try:
        # Get model path
        model_path = os.getenv("AZUREML_MODEL_DIR")
        model_path = os.path.join(model_path, "outputs")
        logging.info(f"Loading model from: {model_path}")

        # Load the model
        model = mlflow.sklearn.load_model(model_path)
        logging.info("Model loaded successfully")

        # Load unique labels
        labels_path = os.path.join(model_path, "unique_labels.json")
        with open(labels_path) as f:
            unique_labels = json.load(f)["unique_labels"]
        logging.info(f"Loaded {len(unique_labels)} unique labels")

    except Exception as e:
        logging.error(f"Error in init: {str(e)}")
        raise


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    """
    try:
        # Parse input data
        data = json.loads(raw_data)
        input_df = pd.DataFrame(data["data"])

        # Get predictions (LightGBM returns probabilities by default for multi-class)
        probabilities = model.predict(input_df)

        # Convert to class predictions
        if probabilities.ndim > 1:
            # Multi-class case
            predicted_classes = np.argmax(probabilities, axis=1)
            class_probabilities = {
                unique_labels[i]: probabilities[:, i].tolist()
                for i in range(len(unique_labels))
            }
        else:
            # Binary case
            predicted_classes = (probabilities >= 0.5).astype(int)
            class_probabilities = {
                unique_labels[0]: (1 - probabilities).tolist(),
                unique_labels[1]: probabilities.tolist(),
            }

        # Map numeric predictions to class labels
        predicted_labels = [unique_labels[idx] for idx in predicted_classes]

        return json.dumps(
            {"predictions": predicted_labels, "probabilities": class_probabilities}
        )

    except Exception as e:
        return json.dumps({"error": str(e)})
