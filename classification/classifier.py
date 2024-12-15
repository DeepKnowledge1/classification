import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
import lightgbm
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)

from lightgbm.callback import early_stopping


class ClassificationDemo:
    def __init__(self):
        # Load dataset
        self.data = load_breast_cancer()
        self.X = self.data.data
        self.y = self.data.target

        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        # Prepare LightGBM datasets
        self.train_data = lightgbm.Dataset(self.X_train_scaled, label=self.y_train)
        self.valid_data = lightgbm.Dataset(
            self.X_test_scaled, label=self.y_test, free_raw_data=False
        )

        # Define LightGBM parameters
        self.params = {
            "objective": "binary",
            "metric": "binary_logloss",
            "boosting_type": "gbdt",
            "num_leaves": 31,
            "learning_rate": 0.05,
            "feature_fraction": 0.9,
        }

    def train_and_evaluate(self):
        """
        Train and evaluate LightGBM classifier
        """
        # Train the model
        model = lightgbm.train(
            self.params,
            self.train_data,
            valid_sets=[self.valid_data],
            num_boost_round=500,
            callbacks=[early_stopping(stopping_rounds=20)],
        )

        # Predict probabilities and classes
        y_pred_proba = model.predict(self.X_test_scaled)
        y_pred = (y_pred_proba > 0.5).astype(int)

        # Evaluate
        results = {
            "Accuracy": accuracy_score(self.y_test, y_pred),
            "Confusion Matrix": confusion_matrix(self.y_test, y_pred),
            "Classification Report": classification_report(self.y_test, y_pred),
            "ROC AUC": roc_auc_score(self.y_test, y_pred_proba),
        }

        return model, results

    def visualize_results(self, results):
        """
        Visualize classification results
        """
        # Accuracy and ROC AUC Comparison
        plt.figure(figsize=(10, 6))
        metrics = ["Accuracy", "ROC AUC"]
        values = [results["Accuracy"], results["ROC AUC"]]
        plt.bar(metrics, values)
        plt.title("Model Performance Metrics")
        plt.ylabel("Score")
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()

    def plot_feature_importance(self, model):
        """
        Plot feature importances for LightGBM model
        """
        feature_importance = model.feature_importance()
        feature_names = self.data.feature_names

        plt.figure(figsize=(10, 6))
        indices = np.argsort(feature_importance)[::-1]
        top_n = 10
        plt.title(f"Top {top_n} Feature Importances")
        plt.bar(range(top_n), feature_importance[indices][:top_n])
        plt.xticks(
            range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=45
        )
        plt.tight_layout()
        plt.show()
