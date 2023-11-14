# Importando bibliotecas necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

# Constantes para caminhos de arquivos
FEATURES_FILE_PATH = "../epidemy/dengue_features_train.csv"
LABELS_FILE_PATH = "../epidemy/dengue_labels_train.csv"
CLEANED_DATA_FILE_PATH = 'Dengue_Hotspot_Data.csv'

# Observer Pattern: Classe notificadora para salvar dados
class DataSaver:
    _observers = set()

    def add_observer(self, observer):
        self._observers.add(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)

# Strategy Pattern: Classe ModelSelection para escolha do modelo
class ModelSelection:
    def __init__(self, model):
        self.model = model

    def choose_model(self, X_train, y_train):
        # Grid Search para ajuste de parâmetros
        param_grid = {'max_depth': [5, 10, 25, 100],
                      'max_features': ['sqrt', 'log2', None],
                      'max_samples': [100, 500, None]}

        grid = GridSearchCV(estimator=self.model,
                            param_grid=param_grid,
                            cv=4,
                            n_jobs=-1)
        grid.fit(X_train, y_train)

        # Criando o modelo final com melhores parâmetros
        params = grid.best_params_
        final_model = type(self.model)(**params)
        final_model.fit(X_train, y_train)

        return final_model

# DataSaver Observer: Classe Observer para salvar dados
class DataSaverObserver:
    def update(self, data):
        df = pd.DataFrame(data, columns=data.columns)
        df.to_csv(CLEANED_DATA_FILE_PATH, index=False)

# Função para preencher valores ausentes usando SimpleImputer
def fill_missing_values(df):
    imputer = SimpleImputer(strategy='mean')
    df[df.columns] = imputer.fit_transform(df)
    return df

# Função para converter nomes de cidades em valores numéricos
def encode_city(df):
    encoder = ce.OrdinalEncoder(cols=['city'],
                                return_df=True,
                                mapping=[{'col': 'city', 'mapping': {"sj": 0, "iq": 1}}])
    df = encoder.fit_transform(df)
    df[["start_year", "start_month", "start_date"]] = df["week_start_date"].str.split("-", n=3, expand=True)
    df.drop(["week_start_date"], axis=1, inplace=True)
    return df

# Função para pré-processamento de dados
def preprocess_data(features_path, labels_path):
    # Reading in data
    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path)

    # Preenchendo valores faltantes
    X = fill_missing_values(X.copy())

    # Convertendo San Juan e Iquitos para 0 e 1
    X = encode_city(X)

    # Adicionando total_cases ao DataFrame
    X["total_cases"] = y["total_cases"]

    # Salvando os dados limpos usando o padrão Observer
    notifier = DataSaver()
    observer = DataSaverObserver()
    notifier.add_observer(observer)
    notifier.notify_observers(X)

    return X

# Função para treinamento de modelo
def train_model(X):
    # Extraindo features X e y
    X_train, X_test, y_train, y_test = train_test_split(X.drop('total_cases', axis=1), X['total_cases'],
                                                        test_size=0.15, random_state=42)

    # Dimensionando os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Escolhendo um modelo usando o padrão Strategy
    rf = ModelSelection(RandomForestRegressor())

    # Treinando o modelo
    final_model = rf.choose_model(X_train, y_train)

    return final_model, X_test, y_test

# Função para avaliação de modelo
def evaluate_model(model, X_test, y_test):
    # Obtendo mse para os dados de teste
    preds = model.predict(X_test)
    mse = model.score(X_test, y_test)

    # Traçando as melhores previsões
    plt.figure(figsize=(4, 4), dpi=100)
    plt.scatter(list(preds), list(y_test), alpha=0.25, color='b')
    plt.title('Total Cases')
    plt.xlim(0, 120)
    plt.ylim(0, 120)
    plt.xlabel('Prediction')
    plt.ylabel('True Value')
    plt.show()

    return mse

# Main execution
if __name__ == "__main__":
    # Pré-processar dados
    data = preprocess_data(FEATURES_FILE_PATH, LABELS_FILE_PATH)

    # Treinar o modelo
    trained_model, X_test, y_test = train_model(data)

    # Avaliar o modelo
    mse = evaluate_model(trained_model, X_test, y_test)
