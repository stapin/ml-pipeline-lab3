import pytest
from app.model import Predictor

def test_predictor_initialization_and_prediction():
    try:
        predictor = Predictor(model_path="models/model.cbm")
    except Exception as e:
        pytest.fail(f"Failed to load the model. Error: {e}")

    dummy_input = {
        "full_text": "This is a great product! I love it."
    }

    prediction = predictor.predict(dummy_input)

    assert isinstance(prediction, int), "Prediction must be integer"
    assert 1 <= prediction <= 5, "Predicted raiting must be between 0 and 5"