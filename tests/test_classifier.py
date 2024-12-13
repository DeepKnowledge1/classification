import pytest
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score
from classification.classifier import ClassificationDemo


@pytest.fixture
def classification_demo():
    """Fixture to initialize the ClassificationDemo class."""
    return ClassificationDemo()


def test_dataset_loading(classification_demo):
    """Test that the dataset is loaded correctly."""
    assert classification_demo.X.shape[0] > 0, "Dataset X should not be empty"
    assert classification_demo.y.shape[0] > 0, "Dataset y should not be empty"
    assert len(classification_demo.X) == len(classification_demo.y), "Features and labels should match in length"


def test_data_split(classification_demo):
    """Test that the data is split correctly."""
    assert classification_demo.X_train.shape[0] > 0, "Training set should not be empty"
    assert classification_demo.X_test.shape[0] > 0, "Testing set should not be empty"
    assert len(classification_demo.X_train) + len(classification_demo.X_test) == len(classification_demo.X), \
        "Training and testing sets should sum up to the total dataset size"


def test_feature_scaling(classification_demo):
    """Test that feature scaling is applied correctly."""
    assert np.allclose(classification_demo.X_train_scaled.mean(), 0, atol=1e-2), \
        "Scaled training features should have approximately zero mean"
    assert np.allclose(classification_demo.X_train_scaled.std(), 1, atol=1e-2), \
        "Scaled training features should have approximately unit variance"


def test_training_and_evaluation(classification_demo):
    """Test that the model trains and evaluates successfully."""
    model, results = classification_demo.train_and_evaluate()
    assert results['Accuracy'] > 0.5, "Model accuracy should be greater than 0.5"
    assert 'Confusion Matrix' in results, "Results should include a confusion matrix"
    assert 'Classification Report' in results, "Results should include a classification report"
    assert 'ROC AUC' in results, "Results should include ROC AUC score"
