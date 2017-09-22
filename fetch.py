#!/usr/bin/python3
#pip3 install coinmarketcap 

from coinmarketcap import Market
import time
import datetime
import pandas as pd

def fetchPrice(ticker):
	data = pd.read_csv("data/tickers.csv", names = ["Date", "Time", "Name", "Ticker", "Volume", "Price"])

	for x in range(0, len(data)):
		if data.Ticker[x] == ticker:
			return("%s" % (data.Price[x]))
			#return("%s,%s,%s" % (data.Date[x], data.Time[x], data.Price[x]))
