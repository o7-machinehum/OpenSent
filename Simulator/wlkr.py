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

Debug = False

BTC = 0 #Index value

sim = Market(file, 1000)
hrToSamples = 2*60
SamplesTohr = 1 / (2*60)

#We need an initial amount of data to calculate the lag
tau = 10*hrToSamples #10hrs * 2 * 60 to get to elements
tauD = 5*hrToSamples #How much shift are we allowing for time lag

#Thresholding - this is used when finding buy/sell triggers
Thresh = 0.6 

M = np.arange(2*tau, dtype = np.float).reshape(tau, 2)

#Initial lag finder
#--------------------------------------------------------------------
for i in range(0, tau):
	M[i,0] = sim.get_CC_value(BTC)
	M[i,1] = sim.get_sentiment(BTC)
	sim.inc_time(30)

#Everything above here is basically init code. Below should now loop.

for k in range(0,25):
#1. Fitler both, sentiment is butter, cost should be moving average - done
#--------------------------------------------------------------------
	Value = M[1:len(M), 0]
	Sen = M[1:len(M), 1]

	b, a = butter(3, 0.01, btype='low')
	Sen = lfilter(b, a, Sen)

	Value = runningMeanFast(Value, windowSize)
	Value = Value[0 : len(Value) - windowSize] #The last elements get all fucked up
	Sen = Sen[0 : len(Sen) - windowSize]

#3. Take norms
#--------------------------------------------------------------------
	nSen = Sen - min(Sen);
	nSen = nSen*(1/max(nSen));
	nValue = Value - min(Value);
	nValue = nValue*(1/max(nValue));

#3. Diff
#--------------------------------------------------------------------
	dSen = np.diff(nSen);
	dValue = np.diff(nValue);

#4. Time Corr Vector
#--------------------------------------------------------------------
	tValue = dValue;
	tSen = dSen;

	meanResult = np.zeros(tauD)

	for i in range(0,tauD) :
		tValue = tValue[1:len(tValue)];
		tSen = tSen[0:len(tSen) - 1];
		meanResult[i] = np.mean(tValue - tSen);

#4. Find lag
#**TODO: Start actually plotting the lag, Making sure no red hairing**
#--------------------------------------------------------------------
	tauL = meanResult.argmin()
	SenOP = dSen[tau-tauL:tau]
	
	if Debug:
		print('Operational Sentiment', SenOP)
		print('LagTime',tauL*SamplesTohr)

#4.5 Plotting for Debug
	if Debug:
		plt.plot(nValue);
		plt.plot(nSen);
		plt.show()

#5. Find the buy and sell triggers
#TODO: We want to minamize our buy and sell triggers
#TODO: I don't know if this alternating sitch makes sense
	NextBuy = True
#--------------------------------------------------------------------
	BuyTrigger = np.array(1)
	SellTrigger = np.array(1)

	for i in range(0,len(SenOP)):
		if SenOP[i] > max(SenOP) * Thresh:
			if NextBuy == True:
				BuyTrigger = np.append(BuyTrigger, i)
				NextBuy = False
		if SenOP[i] < min(SenOP) * Thresh:
			if NextBuy == False:
				SellTrigger = np.append(SellTrigger,  i)
				NextBuy = True
	
	if Debug:
		print('Buy Triggers > ', BuyTrigger)
		print('Sell Triggers > ', SellTrigger)
		#plt.plot(BuyTrigger, 'ro')
		#plt.plot(SellTrigger, 'g^')
		#plt.show();

#6. Lets start to trade
#TODO: If the value you're selling is lower, don't sell (Maybe)
#TODO: Make sure the plotting is working properly - Print the times of selling and buying
#--------------------------------------------------------------------
	for i in range(0, tau):
		if i in BuyTrigger:
			if Debug:
				print('Buying')
				print(sim.buy_CC(BTC, 10))
			else:
				sim.buy_CC(BTC, 10);
		if i in SellTrigger:
			if Debug:
				print('Selling')
				print(sim.sell_CC(BTC, (10 / sim.get_CC_value(BTC))))
			else:
				sim.sell_CC(BTC, (10 / sim.get_CC_value(BTC)))
			
		M[i,0] = sim.get_CC_value(BTC)
		M[i,1] = sim.get_sentiment(BTC)
		sim.inc_time(30)

#Alright we've gone through one full tauL
sim.sell_CC(BTC, sim.get_CC(BTC))
print(sim.get_USD())
sim.plot_trading_stats(BTC)

