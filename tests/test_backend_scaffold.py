from fastapi.testclient import TestClient

from backend.main import app


def test_health_does_not_expose_secrets():
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["app_name"] == "OfficeFlow"
    assert "GEMINI_API_KEY" not in str(data)


def test_unknown_file_has_friendly_error():
    response = TestClient(app).get("/api/files/missing.zip")

    assert response.status_code == 404
    assert "error" in response.json()
