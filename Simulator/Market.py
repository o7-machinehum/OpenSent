
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
            self.CC_balance = [0 for i in range(4)] # total of 4 CC
            self.trans_per_day = 0
            self.time_current = 0 # this will be set to the time idx of the first entry in the data

        self.date = self.data.get_start_time() # we start at the beginning of dataset

    def get_CAD(self):

        return self.balance

    def get_CC(self, idx):

        return self.CC_balance[idx]

    def deposit_CAD(self, value):


        if(value > 0):
            self.balance += value

        return 1

    def deposit_CC(self, idx, value):

        if(value > 0):
            self.CC_balance[idx] += value

        return 1

    def get_CC_value(self, idx):


        return 1

    def get_sentiment(self, idx):

        return 1

    def get_time(self):

        return self.time_current

    def get_transactions(self):

        return self.trans_per_day

    def inc_time(self, dt):

        if(dt > 0):
            self.time_current += dt

        return 1

    def sell_CC(self, amount):


        return 1

    def buy_CC(self, amount):

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
            df.set_index(['date', 'time'], drop=True)

            df['datetime'] = df['date'] + ' ' + df['time']
            df.drop('time', axis=1, inplace=True)
            df.drop('date', axis=1, inplace=True)
            df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y  %H/%M/%S')

            df = df.set_index(df['datetime'])
            df.drop('datetime', axis=1, inplace=True)

            dfs.append(df)

        self.frame = pd.concat(dfs, ignore_index=True)

        self.frame = self.frame.sort_index()



    # Gets the value of CAD at a given time (using closest point in data file)
    def get_CAD(self, time):


        return 1

    # Gets the value of a given CC at a given time (using closest point in data file)
    def get_CC(self, idx, time):

        return 1

    # Gets the value of the sentiment for a given CC (using closest point in data file)
    def get_sentiment(self, idx, time):

        return 1

    def get_closest(df, time):

        # assumes entries are 30 seconds apart and are ordered chronologically
        df1 = time - datetime.timedelta(0, 30)
        df2 = time + datetime.timedelta(0, 30)
        result = df[df1:df2]

        if abs(result.index[0] - time) < abs(result.index[1] - time):
            return result.loc[result.index[0]]
        else:
            return result.loc[result.index[1]]

    # returns the starting time index of tha dataset
    def get_start_time(self):
        return self.frame.index[0]
