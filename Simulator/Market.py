
import numpy as np
import pandas as pd
import glob
import datetime

class Market(object):


    def __init__(self, data_file, inital_balance, settings=None):

        self.data = Data(data_file) # parse data

        self.balance = inital_balance
        self.settings_file = settings

        if(self.settings_file == None):
            self.CC_balance = [0 for i in range(3)] # total of 4 CC
            self.trans_per_day = 0

        self.time_current = self.data.get_start_time() # we start at the beginning of dataset


    def get_USD(self):

        return self.balance

    def get_CC(self, idx):

        return self.CC_balance[idx]

    def deposit_USD(self, value):

        if(value > 0):
            self.balance = self.balance + value

        return 1

    def deposit_CC(self, idx, value):

        if(value > 0):
            self.CC_balance[idx] = self.CC_balance[idx] + value

        return 1

    def get_CC_value(self, idx):
        if idx == 0:
            return self.data.get_closest(self.time_current)['btc_val']
        elif idx == 1:
            return self.data.get_closest(self.time_current)['ltc_val']
        else:
            return self.data.get_closest(self.time_current)['eth_val']

    def get_sentiment(self, idx):

        if idx == 0:
            return self.data.get_closest(self.time_current)['btc_sent'].astype(float)
        elif idx == 1:
            return self.data.get_closest(self.time_current)['ltc_sent']
        else:
            return self.data.get_closest(self.time_current)['eth_sent']

    def get_time(self):

        return self.time_current

    def get_transactions(self):

        return self.trans_per_day

    # assumes dt is in seconds
    def inc_time(self, dt):

        if(dt > 0):
            self.time_current = self.time_current + datetime.timedelta(0, dt)

        return 1

    def sell_CC(self, idx, cc_amount):

        if cc_amount > self.CC_balance[idx]: # Not enough CC to sell
            return 0
        
        
        sale_value = self.get_CC_value(idx) * cc_amount # value in USD 
        
        self.CC_balance[idx] = self.CC_balance - cc_amount # remove sold CC from balance
        
        self.balance = self.balance + sale_value # add sale value to USD balance
        return 1

    def buy_CC(self, idx, usd_amount):
        
        if usd_amount > self.balance: # not enough USD to make purchase
            return 0
        
        value = self.get_CC_value(idx)
        purchase_amount = usd_amount / value
        
        self.balance = self.balance - usd_amount # remove money spent
        self.CC_balance[idx] = self.CC_balance[idx] + purchase_amount # add purchased CC
        
        return 1



class Data(object):

    def __init__(self, data_file):
        self.data_file = data_file # File containing the csv files with all the data

        # get all the data files
        self.files = glob.glob(data_file + "/*.csv")

        dfs = []

        labels = ["date", "time", "btc_sent_vol", "btc_sent", "btc_val", "ltc_sent_vol", "ltc_sent", "ltc_val",
                          "eth_sent_vol", "eth_sent", "eth_val"]

        for f in self.files:
            df = pd.read_csv(f, header=None, usecols=[0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 13])
            df.columns = labels

            df['datetime'] = df['date'] + ' ' + df['time']
            df.drop('time', axis=1, inplace=True)
            df.drop('date', axis=1, inplace=True)

            df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y  %H/%M/%S')

            df = df.set_index(df['datetime'])
            df.drop('datetime', axis=1, inplace=True)

            dfs.append(df)

        self.frame = pd.concat(dfs)
        self.frame = self.frame.sort_index()

    def get_closest(self, time):

        if time < self.get_start_time():
            return 0

        # assumes entries are at max 50 seconds apart and are ordered chronologically
        df1 = time - datetime.timedelta(0, 50)

        if df1 < self.get_start_time():
            df1 = self.get_start_time()

        df2 = time + datetime.timedelta(0, 50)

        result = self.frame[df1:df2]

        if len(result) == 1:
            return result.loc[result.index[0]]
        else:
            if abs(result.index[0] - time) < abs(result.index[1] - time):
                return result.loc[result.index[0]]
            else:
                return result.loc[result.index[1]]

    # returns the starting time index of tha dataset
    def get_start_time(self):
        return self.frame.index[0]
