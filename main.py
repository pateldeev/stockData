import sys

import matplotlib.pyplot as plt
import numpy as np

from data_accessor import get_data


def main():
    print("Python version: ", sys.version)
    print("Version info: ", sys.version_info)

    data_df = get_data(ticker='AAPL')
    print(data_df)

    # plt.figure(figsize=(18, 9))
    # plt.plot(range(data_df.shape[0]), (data_df['Low'] + data_df['High']) / 2.0)
    # plt.xticks(range(0, data_df.shape[0], 500), data_df['Date'].loc[::500], rotation=45)
    # plt.xlabel('Date', fontsize=18)
    # plt.ylabel('Mid Price', fontsize=18)

    data = data_df.loc[:, ['Open', 'Date']].to_numpy()
    print(data)

    start_date = '2014-06-09'
    ret_full = [(float((o2 - o1) / o1), (o1, d1), (o2, d2))
                for (o1, d1), (o2, d2) in zip(data, data[1:]) if np.datetime64(d1) > np.datetime64(start_date)]
    ret = [r for r, _, _ in ret_full]
    # print(ret)
    print('|||||||||||||||||||||||||||||')
    print('Since {}'.format(start_date))

    print('|||MIN|||')
    print(min(ret))
    print(ret_full[np.argmin(ret)])
    print(len([r for r in ret if r < 0.0]))

    print('|||MAX|||')
    print(max(ret))
    print(ret_full[np.argmax(ret)])
    print(len([r for r in ret if r > 0.0]))

    print('|||Aggregate|||')
    print('Avg: {}'.format(np.average(ret)))
    print('Std: {}'.format(np.std(ret)))

    data_filtered = [d for d in data if np.datetime64(d[1]) > np.datetime64(start_date)]
    print(data_filtered[0], data_filtered[-1], len(data_filtered))

    plt.hist(ret, bins=100)

    plt.show()


if __name__ == "__main__":
    main()
