# -*- coding: utf-8 -*-
"""Tubes PADS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pgXmPxL_tfZAZMGAyxsbTHfRCLMcJDR0
"""

import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import accuracy_score
plt.style.use('fivethirtyeight')

df = pd.read_excel('Data Historis USD_IDR clean.xlsx')
df2 = df.iloc[::-1]
df3 = df2[(df2['Tanggal'] >= "2018-01-01") & (df2['Tanggal'] <= "2023-05-25")]
data = df3.set_index('Tanggal')
data

data.shape

plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(data['Terakhir'])
plt.xlabel('Tanggal', fontsize=18)
plt.ylabel('Close Price IDR', fontsize=18)
plt.show()

data = data.filter(['Terakhir'])
dataset = data.values
training_data_len = math.ceil(len(dataset)* .8)
training_data_len

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

train_data = scaled_data[0:training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<= 61:
    print(x_train)
    print(y_train)
    print()

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, batch_size=1, epochs=1)

test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

rmse = np.sqrt(np.mean(predictions - y_test)**2)
rmse

train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close', fontsize=18)
plt.plot(train['Terakhir'])
plt.plot(valid[['Terakhir', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

valid
#valid['Predictions']

#data2 = pd.read_excel('Data Historis USD_IDR clean.xlsx', index_col='Tanggal')
df = pd.read_excel('Data Historis USD_IDR clean.xlsx')
df2 = df.iloc[::-1]
df3 = df2[(df2['Tanggal'] >= "2018-01-01") & (df2['Tanggal'] <= "2023-05-25")]
data2 = df3.set_index('Tanggal')

new_df = data2.filter(['Terakhir'])
last_60_days = new_df[-60:].values
last_60_days_scaled = scaler.transform(last_60_days)
X_test = []
X_test.append(last_60_days_scaled)
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
pred_price = model.predict(X_test)
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

#data3 = pd.read_excel('Data Historis USD_IDR clean.xlsx', index_col='Tanggal')
df = pd.read_excel('Data Historis USD_IDR clean.xlsx')
df2 = df.iloc[::-1]
df3 = df2[(df2['Tanggal'] == "2023-05-26")]
data3 = df3.set_index('Tanggal')

print(data3['Terakhir'])