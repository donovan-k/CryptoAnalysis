from pandas_datareader import data as pdr
import pandas as pd
import datetime


class CoinInfo:
    """
        Class: Creates dictionary of dataframes of information of daily information of cryptocurrency
                such as opening price, closing price, high price, and low price

        Parameters:
            :param coins (array of strings) - name of coin ex: 'DOGE-USD' for doge coin
            :param from_date (string) - date to find data from, in format 'yyyy-mm-dd'
            :param end_date (string) - date to find data up to, in format 'yyyy-mm-dd' Default = today's date

        Attributes:
            :var self.from_date - same as parameter
            :var self.end_date - same as parameter
            :var self.all_coin_data - (1) when len(coins) > 1: dictionary of dataframes holding coin data
                                    - (2) when len(coins) == 1: dataframe of coins[0]'s coin data

    """
    def __init__(self, coins, from_date, end_date=datetime.date.today()):
        self.from_date = from_date
        self.end_date = end_date

        if len(coins) == 1:
            self.all_coin_data = self.get_coin_data(coins[0])
        if len(coins) > 1:
            self.all_coin_data = {c: self.get_coin_data(c) for c in coins}

    """
        To get the coin's data from the pandas data reader
        
        Parameters:
            :param coin (string) - name of coin to get, ex: 'DOGE-USD' for doge coin
    """
    def get_coin_data(self, coin):
        data = pdr.get_data_yahoo(coin, start=self.from_date, end=self.end_date)
        return pd.DataFrame(data)

    """
        To get the coin's data from accessing it through the mega data (faster than above)
        
        Parameters:
            :param coin (string) - name of coin to get, ex: 'DOGE-USD' for doge coin
    """
    def fetch_coin_data(self, coin):
        if isinstance(self.all_coin_data, dict):
            return self.all_coin_data[coin]

        # return all_coin_data if there is only one coin total
        return self.all_coin_data
