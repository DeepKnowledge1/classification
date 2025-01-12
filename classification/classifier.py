import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import lightgbm
import logging
from lightgbm.callback import early_stopping
from typing import Tuple, Dict

from sklearn.preprocessing import label_binarize

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataSplitter:
    """
    A class to handle splitting data into training and validation sets.
    """

    @staticmethod
    def split(data_df: pd.DataFrame) -> Tuple[lightgbm.Dataset, lightgbm.Dataset]:
        """
        Split a dataframe into training and validation datasets.

        Args:
            data_df (pd.DataFrame): The input dataframe containing features and class.

        Returns:
            Tuple[lightgbm.Dataset, lightgbm.Dataset]: Training and validation datasets for LightGBM.
        """
        try:
            features = data_df.drop(["Class"], axis=1)
            labels = np.array(data_df["Class"])
            labels, unique_labels = pd.factorize(labels)
            (
                features_train,
                features_valid,
                labels_train,
                labels_valid,
            ) = train_test_split(features, labels, test_size=0.2, random_state=0)
            train_data = lightgbm.Dataset(features_train, label=labels_train)
            valid_data = lightgbm.Dataset(
                features_valid, label=labels_valid, free_raw_data=False
            )
            logging.info("Data split successfully into training and validation sets.")
            return train_data, valid_data
        except Exception as e:
            logging.error(f"Error in data splitting: {e}")
            raise


class ModelTrainer:
    """
    A class to handle model training and evaluation.
    """

    def __init__(self, parameters: Dict):
        self.parameters = parameters

    def train(
        self, data: Tuple[lightgbm.Dataset, lightgbm.Dataset]
    ) -> lightgbm.Booster:
        """
        Train a LightGBM model with the given datasets and parameters.

        Args:
            data (Tuple[lightgbm.Dataset, lightgbm.Dataset]): Training and validation datasets.

        Returns:
            lightgbm.Booster: The trained LightGBM model.
        """
        try:
            train_data, valid_data = data
            model = lightgbm.train(
                self.parameters,
                train_data,
                valid_sets=[valid_data],
                num_boost_round=500,
                callbacks=[early_stopping(stopping_rounds=20)],
            )
            logging.info("Model training completed.")
            return model
        except Exception as e:
            logging.error(f"Error during model training: {e}")
            raise

    @staticmethod
    def evaluate(
        model: lightgbm.Booster, data: Tuple[lightgbm.Dataset, lightgbm.Dataset]
    ) -> Dict[str, float]:
        """
        Evaluate metrics for the trained model, supporting both binary and multi-class classification.

        Args:
            model (lightgbm.Booster): The trained LightGBM model.
            data (Tuple[lightgbm.Dataset, lightgbm.Dataset]): Training and validation datasets.

        Returns:
            Dict[str, float]: A dictionary containing AUC metrics for each class (for multi-class)
                            or a single AUC score (for binary classification).
        """
        try:
            # Get predictions and true labels
            predictions = model.predict(data[1].data)
            true_labels = pd.factorize(data[1].label)[0]

            # Get number of unique classes
            num_classes = len(np.unique(true_labels))

            model_metrics = {}

            if num_classes == 2:
                # Binary classification case
                fpr, tpr, thresholds = metrics.roc_curve(true_labels, predictions)
                auc_score = metrics.auc(fpr, tpr)
                model_metrics["auc"] = auc_score
            else:
                # Multi-class case
                # Convert labels to binary format
                binary_labels = label_binarize(true_labels, classes=range(num_classes))

                # Calculate AUC for each class
                for i in range(num_classes):
                    if predictions.ndim == 1:
                        # Handle case where model outputs single column of predictions
                        class_predictions = (predictions == i).astype(float)
                    else:
                        # Handle case where model outputs probability for each class
                        class_predictions = predictions[:, i]

                    fpr, tpr, _ = metrics.roc_curve(
                        binary_labels[:, i], class_predictions
                    )
                    auc_score = metrics.auc(fpr, tpr)
                    model_metrics[f"auc_class_{i}"] = auc_score

                # Calculate macro-average AUC
                model_metrics["auc_macro"] = np.mean(list(model_metrics.values()))

            logging.info(f"Model metrics: {model_metrics}")
            return model_metrics

        except Exception as e:
            logging.error(f"Error calculating model metrics: {e}")
            raise
