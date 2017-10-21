
import numpy as np
import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt

class Market(object):


    def __init__(self, data_file, inital_balance, settings=None):

        self.data = Data(data_file) # parse data

        self.balance = inital_balance
        self.settings_file = settings

        if(self.settings_file == None):
            self.CC_balance = [0 for i in range(3)] # total of 4 CC
            self.trans_per_day = 0

        self.time_current = self.data.get_start_time() # we start at the beginning of dataset
        self.logger = Statistics()


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

        if dt > 0:
            multiple = round(dt / 30)
            dt = multiple * 30
            time_current = self.time_current + datetime.timedelta(0, dt)

            if time_current >= self.data.get_start_time():
                self.time_current = time_current
                return 1
            else:
                return 0
        else:
            return 0


    def sell_CC(self, idx, cc_amount):

        if cc_amount > self.CC_balance[idx]: # Not enough CC to sell
            return 0

        cc_value = self.get_CC_value(idx)
        sale_value = cc_value * cc_amount # value in USD
        
        self.CC_balance[idx] = self.CC_balance[idx] - cc_amount # remove sold CC from balance
        
        self.balance = self.balance + sale_value # add sale value to USD balance

        #log transaction
        self.logger.add_trade(0, cc_amount, self.time_current, idx, cc_value)

        return 1

    def buy_CC(self, idx, usd_amount):
        
        if usd_amount > self.balance: # not enough USD to make purchase
            return 0
        
        cc_value = self.get_CC_value(idx)
        purchase_amount = usd_amount / cc_value
        
        self.balance = self.balance - usd_amount # remove money spent
        self.CC_balance[idx] = self.CC_balance[idx] + purchase_amount # add purchased CC

        # log transaction
        self.logger.add_trade(1, usd_amount, self.time_current, idx, cc_value)
        return 1

    def plot_trading_stats(self, idx):
        if idx == 0:
            cc_value = self.data.frame['btc_val'].values
            time = self.data.frame.index

            sales = self.logger.get_sales(idx)
            buys = self.logger.get_buys(idx)

            plt.plot(time, cc_value)

            if(sales.size != 0):
                plt.plot(sales[:,0], sales[:,1], "*", markersize=15)

            if(buys.size != 0):
                plt.plot(buys[:,0], buys[:,1], "o", markersize=15)

            plt.show()




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

        self.frame[['btc_val', 'ltc_val', 'eth_val']] = self.frame[['btc_val', 'ltc_val', 'eth_val']].apply(pd.to_numeric, errors='coerce')
        # resample so that everything is 30s apart
        self.frame = self.frame.resample('30S').mean().interpolate(method='nearest')

    def get_closest(self, time):
         return self.frame.loc[time]

    # returns the starting time index of tha dataset
    def get_start_time(self):
        return self.frame.index[0]

class Statistics(object):
    def __init__(self):
        self.trades = []


    # logs a trade
    def add_trade(self, buy, amount, time, cc_idx, cc_value):
        self.trades.append([buy, amount, time, cc_idx, cc_value])

    # returns the dates of all sales in np array
    def get_sales(self, idx):
        sales = []

        for i in range(0, len(self.trades)):
            trade = self.trades[i]

            if trade[3] == idx: # correct CC
                if trade[0] == 0: # is an actual sale
                    sales.append([trade[2], trade[4]])

        return np.asarray(sales)

    # returns the dates of all sales in np array
    def get_buys(self, idx):
        buys = []

        for i in range(0, len(self.trades)):
            trade = self.trades[i]

            if trade[3] == idx: # correct CC
                if trade[0] == 1: # is an actual buy
                    buys.append([trade[2], trade[4]])

        return np.asarray(buys)
