import pandas as pd
import yaml
import os
from catboost import CatBoostClassifier, Pool


class ModelTrainer:
    def __init__(self, params_path="params.yaml", data_dir="data/prepared", model_dir="models"):
        self.params_path = params_path
        self.train_path = os.path.join(data_dir, "train.csv")
        self.test_path = os.path.join(data_dir, "test.csv")
        self.model_path = os.path.join(model_dir, "model.cbm")
        self.text_cols = ['full_text']
        self.params = self._load_params()

    def _load_params(self):
        with open(self.params_path, "r") as f:
            return yaml.safe_load(f)["train"]

    def _create_pool(self, filepath):
        df = pd.read_csv(filepath)
        df['full_text'] = df['full_text'].fillna('')
        X, y = df.drop('rating', axis=1), df['rating']
        return Pool(data=X, label=y, text_features=self.text_cols)

    def train_model(self, train_pool, test_pool):
        model = CatBoostClassifier(
            iterations=self.params['iterations'],
            learning_rate=self.params['learning_rate'],
            eval_metric='Accuracy',
            auto_class_weights='Balanced',
            task_type='GPU',
            early_stopping_rounds=self.params['early_stopping_rounds'],
            verbose=100
        )
        model.fit(train_pool, eval_set=test_pool)
        return model

    def save_model(self, model):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        model.save_model(self.model_path)

    def run(self):
        train_pool = self._create_pool(self.train_path)
        test_pool = self._create_pool(self.test_path)

        model = self.train_model(train_pool, test_pool)
        self.save_model(model)


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run()
