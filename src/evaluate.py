import pandas as pd
import json
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import root_mean_squared_error


class ModelEvaluator:
    def __init__(self, test_data_path="data/prepared/test.csv", model_path="models/model.cbm", metrics_path="metrics.json"):
        self.test_data_path = test_data_path
        self.model_path = model_path
        self.metrics_path = metrics_path

    def load_data(self):
        df = pd.read_csv(self.test_data_path)
        df['full_text'] = df['full_text'].fillna('')
        return df.drop('rating', axis=1), df['rating']

    def evaluate(self, X_test, y_test):
        model = CatBoostClassifier()
        model.load_model(self.model_path)

        raw_predictions = model.predict(X_test)
        final_predictions = np.clip(np.round(raw_predictions), 1, 5).astype(int)

        return root_mean_squared_error(y_test, final_predictions)

    def save_metrics(self, rmse):
        with open(self.metrics_path, "w") as f:
            json.dump({"rmse": rmse}, f)

    def run(self):
        X_test, y_test = self.load_data()
        rmse = self.evaluate(X_test, y_test)
        self.save_metrics(rmse)


if __name__ == "__main__":
    evaluator = ModelEvaluator()
    evaluator.run()
