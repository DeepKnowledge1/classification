# conftest.py
import pytest


def pytest_addoption(parser):
    """Add command line options for test configuration"""
    parser.addoption(
        "--score_uri", action="store", help="the score url of the ml web service"
    )
    parser.addoption(
        "--score_key", action="store", help="the score key of the ml web service"
    )


@pytest.fixture
def score_uri(request):
    """Fixture to provide the scoring URL"""
    return request.config.getoption("--score_uri")


@pytest.fixture
def score_key(request):
    """Fixture to provide the scoring key"""
    return request.config.getoption("--score_key")
