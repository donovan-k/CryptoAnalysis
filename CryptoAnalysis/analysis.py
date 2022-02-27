import pandas as pd
import numpy as np


class Analysis:
    """
        Class: Performs analysis on coin's data such as the average direction index and others

        Parameters:
            :param coin_data (dataframe) - holds information such as daily high, low, closing, and opening price
    """
    def __init__(self, coin_data):
        self.data = coin_data

    """
        Calculate the daily average directional movement value of a coin 
        Returns empty array if the number of rows in data is not greater than the period
    """
    def calculate_daily_adx(self, period=14):
        # don't run anything if invalid period
        if len(self.data.index) <= period:
            return []

        # list of all average direction movement values
        adx_values = []

        # calculate dm_plus and dm_minus for every row
        dm_pluses = []
        dm_minuses = []
        tr_values = []

        # smoothed values
        sm_dplus = []
        sm_dminus = []
        sm_tr = []

        # lists for directional movement index
        di_pluses = []
        di_minuses = []
        dx_values = []

        # current daily statistics
        cur_high = 0
        cur_low = 0
        cur_close = 0
        for i, row in enumerate(self.data):
            if i == 0:
                cur_high = row['High']
                cur_low = row['Low']
                cur_close = row['Close']
                continue

            # calculate previous values
            prev_high = cur_high
            prev_low = cur_low
            prev_close = cur_close

            # calculate new values
            cur_high = row['High']
            cur_low = row['Low']
            cur_close = row['Close']

            # calculate dm plus and dm minus
            dm_plus = cur_high - prev_high
            dm_minus = prev_low - cur_low
            dm_pluses.append(dm_plus)
            dm_minuses.append(dm_minus)

            # calculate tr values
            tr = max(cur_high - cur_low, cur_high - prev_close, cur_low - prev_close)
            tr_values.append(tr)

            # continue loop if period is not met
            if i < period:
                continue

            # set the first value of the smoothed dm and tr values
            if i == period:
                sm_dplus = [sum(dm_pluses)]
                sm_dminus = [sum(dm_minuses)]
                sm_tr = [sum(tr_values)]
                continue

            # append following smoothed values
            sm_dplus.append(sm_dplus[0] - sm_dplus[-1]/period + dm_plus)
            sm_dminus.append(sm_dminus[0] - sm_dminus[-1]/period + dm_minus)
            sm_tr.append(sm_tr[0] - sm_tr[-1]/period + tr)

            # calculate the di values
            di_pluses.append(sm_dplus[-1] / sm_tr[-1] * 100)
            di_minuses.append(sm_dminus[-1] / sm_tr[-1] * 100)

            # calculate the directional movement index
            dx_values.append(abs(di_pluses[-1] - di_minuses[-1]) / abs(di_pluses[-1] + di_minuses[-1]))

            # finally, calculate the average directional index
            # first adx value
            if len(dx_values) == period:
                adx_values.append(sum(dx_values) / period)

            # following adx values
            if len(dx_values) > period:
                adx_values.append((adx_values[-1] * 13 + dx_values[-1]) / 14)

        return adx_values
