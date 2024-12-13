import pytest
import numpy as np
import lightgbm
from sklearn.metrics import accuracy_score, roc_auc_score

def test_class_initialization():
    """
    Test that the ClassificationDemo class initializes correctly
    """
    demo = ClassificationDemo()
    
    # Check data loading
    assert demo.X is not None, "Data not loaded correctly"
    assert demo.y is not None, "Target not loaded correctly"
    
    # Check data splitting
    assert demo.X_train.shape[0] > 0, "Training data not split correctly"
    assert demo.X_test.shape[0] > 0, "Test data not split correctly"
    
    # Check scaling
    assert demo.X_train_scaled.shape == demo.X_train.shape, "Scaling failed"

def test_train_and_evaluate():
    """
    Test the train_and_evaluate method
    """
    demo = ClassificationDemo()
    model, results = demo.train_and_evaluate()
    
    # Check model is trained
    assert model is not None, "Model not trained successfully"
    
    # Check results dictionary
    assert 'Accuracy' in results, "Accuracy not calculated"
    assert 'Confusion Matrix' in results, "Confusion matrix not calculated"
    assert 'Classification Report' in results, "Classification report not generated"
    assert 'ROC AUC' in results, "ROC AUC not calculated"
    
    # Check performance metrics
    accuracy = results['Accuracy']
    roc_auc = results['ROC AUC']
    
    # Performance sanity checks
    assert 0.5 <= accuracy <= 1.0, f"Unreasonable accuracy: {accuracy}"
    assert 0.5 <= roc_auc <= 1.0, f"Unreasonable ROC AUC: {roc_auc}"

def test_prediction_probabilities():
    """
    Test prediction probabilities
    """
    demo = ClassificationDemo()
    model, results = demo.train_and_evaluate()
    
    # Predict probabilities
    y_pred_proba = model.predict(demo.X_test_scaled)
    
    # Check probabilities
    assert y_pred_proba.shape[0] == demo.X_test.shape[0], "Prediction shape mismatch"
    assert np.all((y_pred_proba >= 0) & (y_pred_proba <= 1)), "Probabilities out of range"

def test_feature_importance():
    """
    Test feature importance plotting method
    """
    demo = ClassificationDemo()
    model, _ = demo.train_and_evaluate()
    
    # Get feature importance
    feature_importance = model.feature_importance()
    
    # Checks
    assert feature_importance is not None, "Feature importance not calculated"
    assert len(feature_importance) == demo.X.shape[1], "Feature importance length mismatch"
    assert np.all(feature_importance >= 0), "Negative feature importance values found"

def test_model_hyperparameters():
    """
    Test model hyperparameters
    """
    demo = ClassificationDemo()
    
    # Check key hyperparameters
    assert demo.params['objective'] == 'binary', "Incorrect objective"
    assert demo.params['metric'] == 'binary_logloss', "Incorrect metric"
    assert 'num_leaves' in demo.params, "Missing num_leaves parameter"
    assert 'learning_rate' in demo.params, "Missing learning_rate parameter"

def test_data_preprocessing():
    """
    Test data preprocessing steps
    """
    demo = ClassificationDemo()
    
    # Check scaling
    assert np.allclose(demo.X_train_scaled.mean(axis=0), 0, atol=1e-5), "Scaled data not zero-centered"
    assert np.allclose(demo.X_train_scaled.std(axis=0), 1, atol=1e-5), "Scaled data not unit variance"

def test_reproducibility():
    """
    Test reproducibility of train-test split
    """
    demo1 = ClassificationDemo()
    demo2 = ClassificationDemo()
    
    # Check that train-test split is consistent with the same random state
    assert np.array_equal(demo1.X_train, demo2.X_train), "Train split not reproducible"
    assert np.array_equal(demo1.X_test, demo2.X_test), "Test split not reproducible"