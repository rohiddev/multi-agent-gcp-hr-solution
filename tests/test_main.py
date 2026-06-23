from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Patch startup dependencies so the app can be imported without GCP.
    with patch("security.iam.google_auth_default") as mock_adc, \
         patch("security.iam.aiplatform.init") as mock_init, \
         patch("observability.telemetry.CloudTraceSpanExporter") as mock_exporter:
        mock_adc.return_value = (MagicMock(service_account_email="test@example.com"), "test-project")
        mock_exporter.return_value = MagicMock()
        from main import app
        with TestClient(app) as test_client:
            yield test_client


class TestHealth:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAsk:
    def test_ask_missing_query(self, client):
        response = client.post("/ask", json={})
        assert response.status_code == 422

    def test_ask_empty_query(self, client):
        response = client.post("/ask", json={"query": "   "})
        assert response.status_code == 400
        assert "query is required" in response.text
