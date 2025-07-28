from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
import pickle
import pandas as pd
import numpy as np

def create_sequences(dataset, window_size):
    X = []
    for i in range(window_size, len(dataset)):
        X.append(dataset[i-window_size:i, 0])
    return np.array(X)


class CreateDataFrame:
    def __init__(self, features):
        self.features = features

    def transform(self, X):
        X.reset_index(inplace=True)
        X.columns =['Date', 'Close','High','Low','Open'	,'Volume']
        X = X[self.features]
        return X

class Normalize:
    def __init__(self, scaler):
        self.scaler = scaler
        
    def transform(self, X):
        X = self.scaler.transform(X[['Close']])
        return X

class FeatureEngineering:
    def __init__(self, window_size):
        self.window_size = window_size

    def transform(self, X):
        X= create_sequences(X, self.window_size)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X

class Model:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler

    def fit(self):
        pass
        
    def predict(self, X):
        y_pred_test = self.model.predict(X)
        y_pred_inv_test = self.scaler.inverse_transform(y_pred_test)
        
        return {
            'valor_predito':float(y_pred_inv_test[-1][0])
        }

