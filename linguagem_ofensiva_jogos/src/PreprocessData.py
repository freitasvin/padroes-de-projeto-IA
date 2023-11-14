import pandas as pd
from google.colab import drive

class PreprocessData:
    def __init__(self, data_path):
        self.data_path = data_path
        self.dataset = None

    def load_data(self):
        drive.mount('/content/drive')
        self.dataset = pd.read_csv(self.data_path)

    def filter_data(self, condition, sample_size=None):
        filtered_data = self.dataset.query(condition)
        if sample_size:
            filtered_data = filtered_data.sample(n=sample_size)
        return filtered_data

    def transform_categorical_data(self, columns):
        for column in columns:
            self.dataset[column].replace({False: 0, True: 1}, inplace=True)

    def select_experiment_data(self, features_column, target_column):
        X = self.dataset[features_column].values
        y = self.dataset[target_column].values
        return X, y
