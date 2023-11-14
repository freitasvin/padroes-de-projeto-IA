from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class TrainModels:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def vectorize_data(self):
        vectorizer = TfidfVectorizer()
        X_train_tfidf = vectorizer.fit_transform(self.X_train)
        X_test_tfidf = vectorizer.transform(self.X_test)
        return X_train_tfidf, X_test_tfidf

    def train_svm(self, X_train, y_train, X_test):
        svm = SVC()
        svm.fit(X_train, y_train)
        return svm.predict(X_test)

    def train_naive_bayes(self, X_train, y_train, X_test):
        nb = MultinomialNB()
        nb.fit(X_train, y_train)
        return nb.predict(X_test)

    def train_logistic_regression(self, X_train, y_train, X_test):
        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        return lr.predict(X_test)

    def train_lstm(self, X_train, y_train, X_test):
        tokenizer = Tokenizer(num_words=10000)
        tokenizer.fit_on_texts(X_train)
        X_train_lstm = tokenizer.texts_to_sequences(X_train)
        X_test_lstm = tokenizer.texts_to_sequences(X_test)
        X_train_lstm = pad_sequences(X_train_lstm, maxlen=100)
        X_test_lstm = pad_sequences(X_test_lstm, maxlen=100)

        lstm = Sequential()
        lstm.add(Embedding(input_dim=10000, output_dim=64, input_length=100))
        lstm.add(LSTM(64))
        lstm.add(Dense(1, activation='sigmoid'))
        lstm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        lstm.fit(X_train_lstm, y_train, epochs=50, batch_size=32, validation_data=(X_test_lstm, y_test))
        y_pred_lstm = lstm.predict(X_test_lstm)
        y_pred_lstm = [1 if pred > 0.5 else 0 for pred in y_pred_lstm]
        return y_pred_lstm


    def evaluate_svm(self, y_test, y_pred):
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        return precision, recall, f1

    def evaluate_naive_bayes(self, y_test, y_pred):
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        return precision, recall, f1

    def evaluate_logistic_regression(self, y_test, y_pred):
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        return precision, recall, f1

    def evaluate_lstm(self, y_test, y_pred):
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        return precision, recall, f1
