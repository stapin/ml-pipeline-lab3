import pandas as pd
import yaml
import os
from sklearn.model_selection import train_test_split


class DataPreparer:
    def __init__(self, params_path="params.yaml", input_data="data/All_Beauty.jsonl", output_dir="data/prepared"):
        self.params_path = params_path
        self.input_data = input_data
        self.output_dir = output_dir
        self.params = self._load_params()

    def _load_params(self):
        with open(self.params_path, "r") as f:
            return yaml.safe_load(f)["prepare"]

    def load_data(self):
        return pd.read_json(self.input_data, lines=True)

    def process_data(self, df):
        df = df.dropna(subset=['rating'])
        df['rating'] = df['rating'].astype(int)

        df['title'] = df['title'].fillna('')
        df['text'] = df['text'].fillna('')
        df['full_text'] = df['title'] + " " + df['text']

        return df[['full_text']], df['rating']

    def split_and_save(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.params['test_size'],
            random_state=self.params['random_state'],
            stratify=y
        )

        os.makedirs(self.output_dir, exist_ok=True)

        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)

        train_df.to_csv(os.path.join(self.output_dir, "train.csv"), index=False)
        test_df.to_csv(os.path.join(self.output_dir, "test.csv"), index=False)

    def run(self):
        df = self.load_data()
        X, y = self.process_data(df)
        self.split_and_save(X, y)


if __name__ == "__main__":
    preparer = DataPreparer()
    preparer.run()
