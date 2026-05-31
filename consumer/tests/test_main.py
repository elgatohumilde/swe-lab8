from fastapi.testclient import TestClient

from app.main import app


class TestMain:
    def test_health(self):
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
