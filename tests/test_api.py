from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app, get_db_manager
from app.database import OracleDBManager

client = TestClient(app)

mock_db = MagicMock(spec=OracleDBManager)
mock_db.save_prediction.return_value = 777

app.dependency_overrides[get_db_manager] = lambda: mock_db

def test_predict_endpoint_success():
    mock_db.save_prediction.reset_mock()

    response = client.post(
        "/predict",
        json={
            "full_text": "Amazing beauty product, highly recommend!"
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_rating" in data
    assert isinstance(data["predicted_rating"], int)
    assert 1 <= data["predicted_rating"] <= 5

    mock_db.save_prediction.assert_called_once()


def test_predict_endpoint_validation_error():
    mock_db.save_prediction.reset_mock()

    response = client.post(
        "/predict",
        json={
            "text": "Excellent!"
        }
    )
    
    # 422 Unprocessable Entity
    assert response.status_code == 422

    mock_db.save_prediction.assert_not_called()