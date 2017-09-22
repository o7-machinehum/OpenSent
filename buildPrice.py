#!/usr/bin/python3
#pip3 install coinmarketcap 

from coinmarketcap import Market
import time
import datetime

numberTickers = 10
delay = 10

while(1):

	coinmarketcap = Market()
	coin = coinmarketcap.ticker(limit=numberTickers, convert='USD')
	file = open("data/tickers.csv", "w")


	for x in range(0,numberTickers):
		t = datetime.datetime.now()
		ct = t.strftime('%m/%d/%Y,%H/%M/%S')
		output = "%s,%s,%s,%s,%s \n" % (ct, coin[x]["name"],coin[x]["symbol"],coin[x]["24h_volume_usd"], coin[x]["price_usd"])
		file.write(output)

	file.close()
	time.sleep(delay)
