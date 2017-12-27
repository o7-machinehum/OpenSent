#!/usr/bin/python3 -i

import numpy as np
import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt
import pdb

windowSize = 500;
def runningMeanFast(x, N):
	return np.convolve(x, np.ones((N,))/N)[(N-1):]

files = glob.glob('Oct' + "/*.csv") + glob.glob('Nov' + "/*.csv") 
 
dfs = []
labels = ["date", "time", "btc_sent_vol", "btc_sent", "btc_val", "ltc_sent_vol", "ltc_sent", "ltc_val", 
	"eth_sent_vol", "eth_sent", "eth_val"]

for f in files:
	print('Loading File:', f)
	df = pd.read_csv(f, header=None, usecols=[0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 13])
	df.columns = labels
	

	df['datetime'] = df['date'] + ' ' + df['time']
	df.drop('time', axis=1, inplace=True)
	df.drop('date', axis=1, inplace=True)

	
	df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y  %H/%M/%S')
	df = df.set_index(df['datetime'])
	df.drop('datetime', axis=1, inplace=True)

	dfs.append(df)

frame = pd.concat(dfs)
frame = frame.sort_index()

frame[['btc_val', 'btc_sent', 'ltc_val', 'ltc_sent', 'eth_val', 'eth_sent']] = frame[['btc_val','btc_sent', 'ltc_val', 'ltc_sent', 'eth_val', 'eth_sent']].apply(pd.to_numeric, errors='coerce')

# resample so that everything is 30s apart

frame = frame.dropna(how='any')
frame = frame.ix[(frame['btc_val'] > 3000) & (frame['btc_val'] < 10000)] 
frame = frame.resample('30S').mean().interpolate(method='nearest') #wlkr- this was breakin

#Fitler 
#--------------------------------------------------------------------
frame['btc_sent_vol'] = runningMeanFast(frame['btc_sent_vol'], windowSize)
frame['btc_sent'] = runningMeanFast(frame['btc_sent'], windowSize)


frame.plot(y='btc_sent')
frame.plot(y='btc_val')

#plt.title('Tweets/second relating to Bitcoin Oct1st - Dec15th')
#plt.xlabel('Date')
#plt.ylabel('1% of tweets')
plt.show()
