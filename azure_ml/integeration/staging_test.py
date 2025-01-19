# staging_test.py
import os
import json
import requests

"""
Run the staging test using:

pytest ./integeration/staging_test.py `
    --doctest-modules `
    --junitxml=junit/staging-test-results.xml `
    --cov-report=xml `
    --cov-report=html `
    --score_uri $(az ml online-endpoint show -g rg_demo03 -w ws_demo_pipeline03 -n fruit-endpoint --query scoring_uri -o tsv) `
    --score_key $(az ml online-endpoint get-credentials -g rg_demo03 -w ws_demo_pipeline03 -n fruit-endpoint --query primaryKey -o tsv)

"""

# score_uri = "https://fruit-endpoint.eastus.inference.ml.azure.com/score"

# score_key = "L0fP0vLrDEPiU9aLPKlY6H2LcUNT2dl6"


def load_test_data(filename="test.json"):
    """Load test data from JSON file"""
    test_data_path = os.path.join(os.path.dirname(__file__), filename)
    with open(test_data_path) as f:
        return json.load(f)


def test_staging_service(score_uri, score_key):
    """Test the ML service in staging environment"""
    assert score_uri is not None, "Score URL cannot be None"

    # Load test data
    test_data = load_test_data()

    # Set up headers with authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {score_key}" if score_key else None,
    }
    headers = {k: v for k, v in headers.items() if v is not None}

    # Make prediction request
    response = requests.post(score_uri, data=json.dumps(test_data), headers=headers)

    # Basic API response tests
    assert (
        response.status_code == 200
    ), f"Request failed with status {response.status_code}"
    assert response.headers.get("content-type", "").startswith("application/json")
    assert int(response.headers.get("Content-Length", 0)) > 0

    # Parse response - handle both string and dictionary responses
    try:
        prediction_result = response.json()
        # If the response is a string, parse it again
        if isinstance(prediction_result, str):
            prediction_result = json.loads(prediction_result)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Failed to parse response as JSON: {str(e)}")

    # Validate response structure and content
    assert isinstance(prediction_result, dict), "Response must be a JSON object"
    assert "predictions" in prediction_result, "Response must contain predictions"
    assert "probabilities" in prediction_result, "Response must contain probabilities"

    # Get predictions and probabilities
    predictions = prediction_result["predictions"]
    probabilities = prediction_result["probabilities"]

    # Validate predictions
    assert isinstance(predictions, list), "Predictions should be a list"
    assert len(predictions) > 0, "Predictions should not be empty"
    assert all(
        isinstance(p, str) for p in predictions
    ), "Each prediction should be a string"

    # Validate probabilities
    assert isinstance(probabilities, dict), "Probabilities should be a dictionary"
    assert len(probabilities) > 0, "Probabilities should not be empty"

    # Check that all classes have probability values
    for class_name, class_probs in probabilities.items():
        assert isinstance(
            class_probs, list
        ), f"Probabilities for class {class_name} should be a list"
        assert len(class_probs) == len(
            predictions
        ), f"Number of probabilities for class {class_name} should match number of predictions"
        assert all(
            isinstance(p, (int, float)) and 0 <= p <= 1 for p in class_probs
        ), f"Probabilities for class {class_name} should be numbers between 0 and 1"

    # Test response time
    assert (
        response.elapsed.total_seconds() < 5
    ), "Response time should be under 5 seconds"
