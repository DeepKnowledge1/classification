import os
import argparse
import json
import yaml
import logging
import pandas as pd
import joblib
from classification.classifier import DataSplitter, ModelTrainer
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TrainingPipeline:
    """
    A class to handle the entire training pipeline.
    """

    def __init__(
        self,
        input_data: str,
        model_name: str,
        output_dir: str,
        parameters_file: str = "yml_files/algo_parms.yaml",
    ):
        self.input_data = input_data
        self.model_name = model_name
        self.output_dir = output_dir
        self.parameters_file = parameters_file
        self.parameters = self._load_parameters()

    def _load_parameters(self) -> Dict:
        """
        Load training parameters from a JSON file.

        Returns:
            Dict: Training parameters dictionary.
        """
        try:
            # Single-line safe yaml loading
            with open(self.parameters_file, errors="ignore") as f:
                return yaml.safe_load(f)["training"]

        except Exception as e:
            logging.warning(f"Error loading parameters: {e}")
            return {}

    def run(self):
        """
        Execute the training pipeline: load data, train model, evaluate, and save outputs.
        """
        # Read input data
        try:
            df = pd.read_csv(self.input_data)
            logging.info("Input data loaded successfully.")
        except Exception as e:
            logging.error(f"Error reading input data: {e}")
            return

        # Split data
        splitter = DataSplitter()
        data = splitter.split(df)

        # Train model
        trainer = ModelTrainer(parameters=self.parameters)
        model = trainer.train(data)

        # Evaluate metrics
        metrics = trainer.evaluate(model, data)

        # Save outputs
        self._save_outputs(model, metrics)

    def _save_outputs(self, model, metrics):
        """
        Save the trained model and evaluation metrics.

        Args:
            model: The trained model.
            metrics: Evaluation metrics.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            model_path = os.path.join(self.output_dir, self.model_name)
            joblib.dump(model, model_path)
            logging.info(f"Model saved to {model_path}")

            metrics_path = os.path.join(self.output_dir, "metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(metrics, f)
            logging.info(f"Metrics saved to {metrics_path}")
        except Exception as e:
            logging.error(f"Error saving outputs: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("train")
    parser.add_argument(
        "--input_data",
        type=str,
        default="data/Date_Fruit_Datasets.csv",
        help="Input data path provided by Azure ML",
    )
    parser.add_argument(
        "--model_name", type=str, default="Fruit_model.pkl", help="Name of the Model"
    )
    parser.add_argument(
        "--output_dir", type=str, default="outputs", help="Directory to save outputs"
    )
    args, _ = parser.parse_known_args()

    pipeline = TrainingPipeline(
        input_data=args.input_data,
        model_name=args.model_name,
        output_dir=args.output_dir,
    )
    pipeline.run()
