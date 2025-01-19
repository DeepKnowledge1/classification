# prod_test.py
import os
import json
import requests

"""
Run the production test using:

pytest ./integeration/prod_test.py  `
    --doctest-modules `
    --junitxml=junit/prod-test-results.xml `
    --cov-report=xml `
    --cov-report=html `
    --score_uri $(az ml online-endpoint show -g rg_demo03 -w ws_demo_pipeline03 -n fruit-endpoint --query scoring_uri -o tsv) `
    --score_key $(az ml online-endpoint get-credentials -g rg_demo03 -w ws_demo_pipeline03 -n fruit-endpoint --query primaryKey -o tsv)


"""

# --resource-group rg_demo03 --workspace-name ws_demo_pipeline03


def load_test_data(filename="test.json"):
    """Load test data from JSON file"""
    test_data_path = os.path.join(os.path.dirname(__file__), filename)
    with open(test_data_path) as f:
        return json.load(f)


def test_ml_service(score_uri, score_key):
    """Test the ML service endpoint"""
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

    # Test assertions
    assert (
        response.status_code == 200
    ), f"Request failed with status {response.status_code}"
    assert response.headers.get("content-type") == "application/json"
    assert int(response.headers.get("Content-Length", 0)) > 0

    # Validate response structure
    prediction_result = response.json()
    assert "predictions" in prediction_result
    assert "probabilities" in prediction_result


# test_ml_service("https://fruit-endpoint.eastus.inference.ml.azure.com/score","L0fP0vLrDEPiU9aLPKlY6H2LcUNT2dl6")
