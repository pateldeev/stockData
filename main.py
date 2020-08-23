# https://www.datacamp.com/community/tutorials/lstm-python-stock-market

import datetime as dt
import json
import os
import sys


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data
from sklearn.preprocessing import MinMaxScaler
# import tensorflow as tf  # (TensorFlow 1.6?)
import urllib.request


print("Python version: ", sys.version)
print("Version info: ", sys.version_info)
# print("Tensorflow version: ", tf.__version__)


# data_source = alphavantage or kaggle
def get_data(ticker, data_source='alphavantage'):
    ticker = ticker.lower()
    if data_source == 'alphavantage':
        # ====================== Loading Data from Alpha Vantage ==================================
        api_key = 'OJ3ER5ZTPSZ28ELU'

        # JSON file with all the stock market data.
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}".format(ticker,api_key)

        # Save data to this file
        file_to_save = 'data/stock_market_data-{}.csv'.format(ticker)

        # If you haven't already saved data, grab it from the url.
        # Store date, low, high, volume, close, open values to a Pandas DataFrame.
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data_json = json.loads(url.read().decode())
                # Extract stock market data.
                df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
                for k, v in data_json['Time Series (Daily)'].items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(), float(v['3. low']), float(v['2. high']),
                                float(v['4. close']), float(v['1. open'])]
                    df.loc[-1,:] = data_row
                    df.index += 1
            print('Loaded data from the alphavantage')
            print('Data saved to : ', file_to_save)
            df.to_csv(file_to_save)

        # If the data is already there, just load it from the CSV.
        else:
            print('File already exists. Loading data from CSV')
            df = pd.read_csv(file_to_save)

    elif data_source == 'kaggle':

        # ====================== Loading Data from Kaggle ==================================
        # You will be using HP's data. Feel free to experiment with other data.
        # But while doing so, be careful to have a large enough dataset and also pay attention to the data normalization.
        df = pd.read_csv('data/kaggle/Stocks/{}.us.txt'.format(ticker), delimiter=',', usecols=['Date', 'Open', 'High', 'Low', 'Close'])
        print('Loaded data from the kaggle repository')
    else:
        raise NotImplementedError("Unknown data_source {}".format(data_source))

    return df.sort_values('Date')


data_df = get_data(ticker='GOOG')
print(data_df)

plt.figure(figsize=(18, 9))
plt.plot(range(data_df.shape[0]), (data_df['Low'] + data_df['High']) / 2.0)
plt.xticks(range(0, data_df.shape[0], 500), data_df['Date'].loc[::500], rotation=45)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Mid Price', fontsize=18)
# plt.show()

data = data_df.loc[:, ['Low', 'High', 'Open', 'Close']].to_numpy()
print(data)

SPLIT = 0.8
train_size = int(0.8 * len(data))
train_data = data[:train_size]
test_data = data[train_size:]
print('Train:', train_data)
print('Test:', test_data)
