#!/usr/bin/python3 -i
#wlkr's bot

#pdb.set_trace() <- for breaks

from Market import Market
from random import randint
from scipy import signal
from scipy.signal import butter, lfilter, freqz

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pdb

windowSize = 50;
def runningMeanFast(x, N):
	return np.convolve(x, np.ones((N,))/N)[(N-1):]

#Trading methods
#--------------------------------------------------------------------
#Method = 'SimpleSam'
Method = 'TycoonJoe'

file = "../Datasets/Oct"
#file = "../Datasets/Contig" 

DebugBreaks = True
Debug = False
Plot = False 

BTC = 0 #Index value

sim = Market(file, 1000)
hrToSamples = 2*60
SamplesTohr = 1 / (2*60)

#We need an initial amount of data to calculate the lag
tau = 10*hrToSamples #10hrs * 2 * 60 to get to elements
tauD = 5*hrToSamples #How much shift are we allowing for time lag

#Thresholding - this is used when finding buy/sell triggers
Thresh = 0.9 

M = np.arange(2*tau, dtype = np.float).reshape(tau, 2)
time = [None] * tau

sim.inc_time(30)

#Initial lag finder
#--------------------------------------------------------------------
for i in range(0, tau):
	M[i,0] = sim.get_CC_value(BTC)
	M[i,1] = sim.get_sentiment(BTC)
	time[i] = sim.get_time()
	sim.inc_time(30)

#Everything above here is basically init code. Below should now loop.

for k in range(0,75):
#1. Fitler both, sentiment is butter, cost should be moving average - done
#--------------------------------------------------------------------
	Value = M[1:len(M), 0]
	Sen = M[1:len(M), 1]

	b, a = butter(3, 0.01, btype='low')
	Sen = lfilter(b, a, Sen)

	Value = runningMeanFast(Value, windowSize)
	Value = Value[0 : len(Value) - windowSize] #The last elements get all fucked up
	Sen = Sen[0 : len(Sen) - windowSize]

#2. Take norms
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
#--------------------------------------------------------------------
	tauL = meanResult.argmin()
	SenOP = dSen[tau-tauL:tau]
	timeOP = time[tau-tauL:tau]

#	if Plot:
		#plt.plot(timeOP, SenOP)
		#plt.show()

	if Debug:
		#print('Operational Sentiment', SenOP)
		print('LagTime',tauL*SamplesTohr)

#4.5 Plotting for Debug
	if Plot:
		plt.plot(nValue);
		plt.plot(nSen);
		plt.show()

#5. Find the buy and sell triggers
#--------------------------------------------------------------------
	BuyTrigger = np.array(1)
	SellTrigger = np.array(1)
	
	#Clear dat shit out
	BuyTrigger = []
	SellTrigger = []

	BuySen = 0.006
	SellSen = -1*BuySen

	if Debug:
		print('Previous Buy Triggers > ', BuyTrigger)
		print('Previous Sell Triggers > ', SellTrigger)

	LastSenOPbuy = 0
	LastSenOPsell = 0

	for i in range(0,len(SenOP)):
		if SenOP[i] > max(SenOP) * Thresh:
			if i > LastSenOPbuy + 1*hrToSamples:
				BuyTrigger = np.append(BuyTrigger, i)
				LastSenOPbuy = i #To avoid continious buying

		if SenOP[i] < min(SenOP) * Thresh:
			if i > LastSenOPsell + 1*hrToSamples:
				SellTrigger = np.append(SellTrigger,  i)
				LastSenOPsell = i
	
	if Debug:
		print('Buy Triggers > ', BuyTrigger)
		print('Sell Triggers > ', SellTrigger)
		#plt.plot(BuyTrigger, 'ro')
		#plt.plot(SellTrigger, 'g^')
		#plt.show();

#6. Lets start to trade
#--------------------------------------------------------------------

#Method one - Simple Sam. Buy on buy triggers and sell on sell triggers
#--------------------------------------------------------------------
	if Method == 'SimpleSam':
		NextBuy = True
		
		for i in range(0, tau):
			if i in BuyTrigger:
				if NextBuy == True:
					sim.buy_CC(BTC, 10);
					NextBuy = False
			if i in SellTrigger:	
				if NextBuy == False:
					sim.sell_CC(BTC, (10 / sim.get_CC_value(BTC)))	
					NextBuy = True

			M[i,0] = sim.get_CC_value(BTC)
			M[i,1] = sim.get_sentiment(BTC)
			sim.inc_time(30)

#Method Two - Buy on buy triggers and sell when gains higher %10
#						- If high density of sell triggers sell
#--------------------------------------------------------------------
	if Method == 'TycoonJoe':
		buyPoint = 1000000.123412 #blaaa
		Lastsell = 0
		for i in range(0, tau):
			if i in BuyTrigger:
				sim.buy_CC(BTC, 0.5*sim.get_USD())
				buyPoint = sim.get_CC_value(BTC)
			
			if sim.get_CC_value(BTC) > (buyPoint + buyPoint*0.01):
				if i > Lastsell + 1*hrToSamples:
					sim.sell_CC(BTC, (0.5*sim.get_USD() / sim.get_CC_value(BTC)))
					Lastsell = i

			M[i,0] = sim.get_CC_value(BTC)
			M[i,1] = sim.get_sentiment(BTC)
			sim.inc_time(30)

	#pdb.set_trace()

#Alright we've gone through one full tauL
sim.sell_CC(BTC, sim.get_CC(BTC))
print(sim.get_USD())
sim.plot_trading_stats(BTC)
