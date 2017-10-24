#!/usr/bin/python3 -i
#wlkr's bot

from Market import Market
from random import randint
from scipy import signal
from scipy.signal import butter, lfilter, freqz

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

windowSize = 50;
def runningMeanFast(x, N):
	return np.convolve(x, np.ones((N,))/N)[(N-1):]

#file = "../Datasets/Oct"
file = "../Datasets/Contig" #Contingious dataset

BTC = 0 #Index value

sim = Market(file, 1000)

#We need an initial amount of data to calculate the lag
tau = 10*2*60 #10hrs * 2 * 60 to get to elements
tauD = 5*2*60

#Thresholding - this is used when finding buy/sell triggers
Thresh = 0.8 

M = np.arange(2*tau, dtype = np.float).reshape(tau, 2)

#Initial lag finder
for i in range(0, tau):
	M[i,0] = sim.get_CC_value(BTC)
	M[i,1] = sim.get_sentiment(BTC)
	sim.inc_time(30)

Value = M[1:len(M), 0]
Sen = M[1:len(M), 1]

#TODO
#1. Fitler both, sentiment is butter, cost should be moving average - done
b, a = butter(3, 0.1, btype='low')
Sen = lfilter(b, a, Sen)

Value = runningMeanFast(Value, windowSize)
Value = Value[0 : len(Value) - windowSize] #The last elements get all fucked up
Sen = Sen[0 : len(Sen) - windowSize]

#Everything above here is basically init code. Below should now loop.
#--------------------------------------------------------------------
#3. Take norms
nSen = Sen - min(Sen);
nSen = nSen*(1/max(nSen));
nValue = Value - min(Value);
nValue = nValue*(1/max(nValue));

#3. Diff
dSen = np.diff(nSen);
dValue = np.diff(nValue);

#4. Time Corr Vector
tValue = dValue;
tSen = dSen;

meanResult = np.zeros(tauD)

for i in range(0,tauD) :
	tValue = tValue[1:len(tValue)];
	tSen = tSen[0:len(tSen) - 1];
	meanResult[i] = np.mean(tValue - tSen);

#4. Find lag
#plt.plot(dSen)
tauL = meanResult.argmin()
SenOP = dSen[tau-tauL:tau]

#5. Find the buy and sell triggers
BuyTrigger = np.array(1)
SellTrigger = np.array(1)

for i in range(0,len(SenOP)):
	if SenOP[i] > max(SenOP) * Thresh:
		BuyTrigger = np.append(BuyTrigger, i)
	if SenOP[i] < min(SenOP) * Thresh:
		SellTrigger = np.append(SellTrigger,  i)

for i in range(0, tau):
	if i in BuyTrigger:
		print('Buying')
		sim.buy_CC(BTC, 10)
	if i in SellTrigger:
		print('Selling')
		sim.sell_CC(BTC, 10)
	
	#M[i,0] = sim.get_CC_value(BTC)
	#M[i,1] = sim.get_sentiment(BTC)
	sim.inc_time(30)

#Value = M[1:len(M), 0]
#Sen = M[1:len(M), 1]

#Alright we've gone through one full tauL
sim.sell_CC(BTC, sim.get_CC(BTC))
sim.plot_trading_stats(BTC)

#-----------------------Part Two (This is where the magic happens)------------------

#1. Calculate lag (Done above)
#2. Inc a fixed point in time (Lets start with 30 mins), filter the sentament, diff
#3. If the slope is considered to be high (above a threshold) just buy or sell
#4. Wait the time lag, sell or buy if money has been made


