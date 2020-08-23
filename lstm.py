# https://www.datacamp.com/community/tutorials/lstm-python-stock-market

import sys

import numpy as np
import tensorflow as tf

from data_accessor import get_data


def main():
    print("Python version: ", sys.version)
    print("Version info: ", sys.version_info)
    print("Tensorflow version: ", tf.__version__)  # 2.2.0

    data_df = get_data(ticker='AAPL')
    print(data_df)


if __name__ == "__main__":
    main()
