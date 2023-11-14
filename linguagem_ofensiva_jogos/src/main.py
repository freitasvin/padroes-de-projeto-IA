from sklearn.model_selection import train_test_split 
from PreprocessData import PreprocessData
from TrainModels import TrainModels

# Preprocessamento
data_processor = PreprocessData("/content/drive/MyDrive/TCC/dataset.csv")
data_processor.load_data()
data_processor.transform_categorical_data(['Span', 'Portugues', 'Racismo', 'Ofensivo', 'Não ofensivo', 'Homofobia', 'Xenofobia', 'Sexismo'])
X_data, y_data = data_processor.select_experiment_data('Texto', 'Ofensivo')

# Divisao Treino/Teste
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.20, random_state=123)

# Treinamento
model_trainer = TrainModels(X_train, X_test, y_train, y_test)
X_train_tfidf, X_test_tfidf = model_trainer.vectorize_data()

y_pred_svm = model_trainer.train_svm(X_train_tfidf, y_train, X_test_tfidf)
y_pred_nb = model_trainer.train_naive_bayes(X_train_tfidf, y_train, X_test_tfidf)
y_pred_lr = model_trainer.train_logistic_regression(X_train_tfidf, y_train, X_test_tfidf)
y_pred_lstm = model_trainer.train_lstm(X_train, y_train, X_test)

# Buscando resultados
svm_results = model_trainer.evaluate_svm(y_test, y_pred_svm)
nb_results = model_trainer.evaluate_naive_bayes(y_test, y_pred_nb)
lr_results = model_trainer.evaluate_logistic_regression(y_test, y_pred_lr)
lstm_results = model_trainer.evaluate_lstm(y_test, y_pred_lstm)

# Impressão dos resultados
print("SVM Results:", svm_results)
print("Naive Bayes Results:", nb_results)
print("Logistic Regression Results:", lr_results)
print("LSTM Results:", lstm_results)