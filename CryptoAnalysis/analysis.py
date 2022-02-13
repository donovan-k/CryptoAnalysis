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
        Calculate the daily adx value of a certain coin and returns an array of tuples of (+ or -), value 
    """
    def calculate_daily_adx(self, period=14):
        # calculate dm_plus and dm_minus for every row
        dm_pluses = []
        dm_minuses = []
        tr_values = []
        cur_high = []
        cur_low = []
        cur_open = []
        cur_close = []
        for i, row in enumerate(self.data):
            if i == 0:
                cur_high = row['High']
                cur_low = row['Low']
                cur_open = row['Open']
                cur_close = row['Close']
                continue

            # calculate previous values
            prev_high = cur_high
            prev_low = cur_low
            prev_open = cur_open
            prev_close = cur_close

            # calculate new values
            cur_high = row['High']
            cur_low = row['Low']
            cur_open = row['Open']
            cur_close = row['Close']

            # calculate dm plus and dm minus
            dm_plus = cur_high - prev_high
            dm_minus = prev_low - cur_low
            dm_pluses.append(dm_plus)
            dm_minuses.append(dm_minus)

            # calculate tr values
            tr = max(cur_high - cur_low, cur_high - prev_close, cur_low - prev_close)
            tr_values.append(tr)

        # find smoothed values
        tr_smooth = []
        dmm_smooth = []
        dmp_smooth = []
        first_values = [0, 0, 0]
        prior_values = [0, 0, 0]
        adx_values = []
        prior_adx = 0
        counter = 0
        for i in range(0, len(tr_values), period):
            access_end = i + period
            if access_end > len(tr_values):
                access_end = len(tr_values)

            if i == 0:
                first_values = [sum(tr_values[i:access_end]), sum(dm_minuses[i:access_end]),
                                sum(dm_pluses[i:access_end])]
                prior_values = first_values.copy()
                continue

            # find the smooth values
            tr_smooth.append(first_values[0] - prior_values[0]/period + sum(tr_values[i:access_end]))
            dmm_smooth.append(first_values[1] - prior_values[1]/period + sum(dm_minuses[i:access_end]))
            dmp_smooth.append(first_values[2] - prior_values[2]/period + sum(dm_pluses[i:access_end]))

            # reset the prior values
            prior_values = [tr_smooth[i-1], dmm_smooth[i-1], dmp_smooth[i-1]].copy()
            counter += 1

            # get the di values for plus and minus
            di_plus = np.array(dmp_smooth) / np.array(tr_smooth) * 100
            di_minus = np.array(dmm_smooth) / np.array(tr_smooth) * 100

            # get the dmi value
            dx = np.abs(di_plus - di_minus) / np.abs(di_plus + di_minus) * 100

            # calculate adx value
            if i != 0 and (i+1) % period == 0:
                # calculate first adx value
                if i+1 == period:
                    prior_adx = sum(dx) / period
                    adx_values.append(prior_adx)
                    continue

                # calculate later adx values
                prior_adx = ((prior_adx * 13) + dx) / 14
                adx_values.append(prior_adx)

        return adx_values
