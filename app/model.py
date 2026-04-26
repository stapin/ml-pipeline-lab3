import pandas as pd
from catboost import CatBoostClassifier

class Predictor:
    def __init__(self, model_path: str = "models/model.cbm"):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)

    def predict(self, input_data: dict) -> int:
        df = pd.DataFrame([input_data])
        
        raw_pred = self.model.predict(df)
        
        if len(raw_pred.shape) > 1:
            final_pred = int(raw_pred[0][0])
        else:
            final_pred = int(raw_pred[0])
            
        return final_pred