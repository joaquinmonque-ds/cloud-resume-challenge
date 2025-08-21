import pytest

@pytest.fixture(autouse=True)
def _set_region_env(monkeypatch):
    # Ensure boto3 has a default region during tests/CI
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
