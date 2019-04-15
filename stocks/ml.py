from keras.models import load_model
from keras.callbacks import ModelCheckpoint
import time
import datetime
from iexfinance.stocks import Stock
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
import datetime
from sklearn.preprocessing import MinMaxScaler
import math
from iex import Stock
import pandas as pd
import os
import numpy as np




class Preprocessing:
    strFormat = "%Y-%m-%d"
    dateparse = lambda word : datetime.datetime.fromtimestamp(        
        time.mktime(time.strptime(
            str(word),Preprocessing.strFormat))).strftime("%d-%b-%Y")

    cols_to_delete = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    path = os.getcwd()

    def __init__(self, stock):
        self.stock_name = stock.stock_name
        # self.stock_name = stock.symbols[0]
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def pre_process(self):

        self.file = os.path.join(
            Preprocessing.path, "stocks_data", self.stock_name) + ".csv"
        self.df = pd.read_csv(self.file, parse_dates=[
                              'Date'], date_parser=Preprocessing.dateparse)

        for col in Preprocessing.cols_to_delete:
            del self.df[col]

        self.data = self.df.sort_index(ascending=True, axis=0)
        self.new_data = pd.DataFrame(index=range(
            0, len(self.df)), columns=['Date', 'Close'])

        for i in range(0, len(self.data)):
            self.new_data['Date'][i] = self.data['Date'][i]
            self.new_data['Close'][i] = self.data['Close'][i]

        self.new_data.index = self.new_data.Date
        self.new_data.drop('Date', axis=1, inplace=True)

        self.dataset = self.new_data.values
        self.scaled_data = self.scaler.fit_transform(self.dataset)

        return self.scaled_data




class Prediction:

    path = os.getcwd()

    def __init__(self, stock):
        self.stock_name  = stock.stock_name
        self.preprocessing = Preprocessing(stock)
        self.scaled_data = self.preprocessing.pre_process()

        self.model_exists()

    def model_exists(self):
        self.file_path = os.path.join(
            Prediction.path, "ml_models", self.stock_name) + ".h5"

        print("\n\n\n",self.file_path)

        if os.path.isfile(self.file_path):
            self.model = load_model(self.file_path)
        else:
            self.create_model()

    def transform(self):
        self.x_train, self.y_train = [], []

        for i in range(60, len(self.scaled_data)):
            self.x_train.append(self.scaled_data[i-60:i, 0])
            self.y_train.append(self.scaled_data[i, 0])
        self.x_train, self.y_train = np.array(
            self.x_train), np.array(self.y_train)
        self.x_train = np.reshape(
            self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))

    def train_model(self):
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.checkpointer = ModelCheckpoint(
            filepath=self.file_path, verbose=1, save_best_only=True)
        self.model.fit(self.x_train, self.y_train, batch_size=100, epochs=5,
                       verbose=2, validation_split=0.25, callbacks=[self.checkpointer])
        #self.model.fit(self.x_train, self.y_train,validation_split = 0.25,epochs=5, batch_size=100, verbose=2)

    def create_model(self):
        self.transform()

        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True,
                            input_shape=(self.x_train.shape[1], 1)))
        self.model.add(LSTM(units=50))
        self.model.add(Dense(1))

        self.train_model()

        self.model.save(self.file_path)

    def update_model(self, number_of_days):
        self.new_data = self.scaled_data
        self.x_new, self.y_new = [], []

        for i in range(len(self.new_data) - number_of_days, len(self.new_data)):
            self.x_new.append(self.new_data[i-60:i, 0])
            self.y_new.append(self.new_data[i, 0])

        self.x_new, self.y_new = np.array(self.x_new), np.array(self.y_new)
        self.x_new = np.reshape(
            self.x_new, (self.x_new.shape[0], self.x_new.shape[1], 1))

        self.model.fit(self.x_new, self.y_new, epochs=1,
                       batch_size=1, verbose=2)
        self.model.save(self.file_path)

    def predict_stock_price(self):
        self.x_latest, self.y_latest = [], []

        self.x_latest.append(self.scaled_data[len(self.scaled_data) - 60:])
        self.y_latest.append(self.scaled_data[[-1, 0]])

        self.x_latest, self.y_latest = np.array(
            self.x_latest), np.array(self.y_latest)
        self.x_latest = np.reshape(
            self.x_latest, (self.x_latest.shape[0], self.x_latest.shape[1], 1))

        self.predicted_price = self.model.predict(self.x_latest)
        self.predicted_price = self.preprocessing.scaler.inverse_transform(
            self.predicted_price)

        return self.predicted_price[0][0]
