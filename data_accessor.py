import datetime as dt
import json
import os

import pandas as pd
import urllib.request


# data_source = 'alphavantage' or 'kaggle'
# Known issues: Alphavantage does not account for stock splits.
def get_data(ticker, data_source='alphavantage'):
    ticker = ticker.lower()
    if data_source == 'alphavantage':
        # ====================== Loading Data from Alpha Vantage ==================================
        get_data.API_KEY = 'OJ3ER5ZTPSZ28ELU'

        # JSON file with all the stock market data.
        url_str = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}".format(
            ticker, get_data.API_KEY)

        # Save data to this file
        file_to_save = 'data/cached_data_{}_{}.csv'.format(ticker, dt.date.today().strftime('%m_%d_%Y'))

        # If you haven't already saved data, grab it from the url.
        # Store date, low, high, volume, close, open values to a Pandas DataFrame.
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_str) as url:
                data_json = json.loads(url.read().decode())
                # Extract stock market data.
                df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open'])
                for k, v in data_json['Time Series (Daily)'].items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(), float(v['3. low']), float(v['2. high']),
                                float(v['4. close']), float(v['1. open'])]
                    df.loc[-1, :] = data_row
                    df.index += 1
            print('Loaded data from the alphavantage')

            file_to_save_dir = os.path.dirname(file_to_save)
            if not os.path.exists(file_to_save_dir):
                os.makedirs(file_to_save_dir)
            df.to_csv(file_to_save)
            print('Data saved to : ', file_to_save)

        # If the data is already there, just load it from the CSV.
        else:
            print('File {} already exists. Loading data from file.'.format(file_to_save))
            df = pd.read_csv(file_to_save)

    elif data_source == 'kaggle':
        # ====================== Loading Data from Kaggle ==================================
        # You will be using HP's data. Feel free to experiment with other data.
        # But while doing so, be careful to have a large enough dataset and also pay attention to the data normalization.
        df = pd.read_csv('data/kaggle/Stocks/{}.us.txt'.format(ticker), delimiter=',',
                         usecols=['Date', 'Open', 'High', 'Low', 'Close'])
        print('Loaded data from the kaggle repository')
    else:
        raise NotImplementedError("Unknown data_source {}".format(data_source))

    return df.sort_values('Date')
