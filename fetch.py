#!/usr/bin/python3
#pip3 install coinmarketcap 

from coinmarketcap import Market
import time
import datetime
import pandas as pd
import pdb

numberTickers = 10

def fetchPrice(ticker):
	coinmarketcap = Market()
	coin = coinmarketcap.ticker(limit=numberTickers, convert='USD')
	
	#pdb.set_trace();

	t = datetime.datetime.now()
	ct = t.strftime('%m/%d/%Y,%H/%M/%S')
	
	for x in range(0, len(coin)):
		if coin[x]['symbol'] == ticker:
			return("%s" % (coin[x]['price_usd']))
