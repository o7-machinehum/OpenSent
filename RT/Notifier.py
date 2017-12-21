#!/usr/bin/python3 -i
#Taken from Simulator, basically turning this into a realtime application.

#pdb.set_trace() <- for breaks

from random import randint
from scipy import signal
from scipy.signal import butter, lfilter, freqz

import push
import RT
import numpy as np
import scipy as sp
import pdb
import time
import Log

windowSize = 50;

def runningMeanFast(x, N):
	return np.convolve(x, np.ones((N,))/N)[(N-1):]

def waitForGoodData():
	Timeout = 0;
	while(True):
		if RT.CheckDataFrame() == True: #If we have bad data
			time.sleep(30)
			Timeout += 1
			if Timeout > 5:
				Log.Write('Bad data timeout, Servercrash or eq.')
				break
		else:
			Timeout = 0
			break;

Debug = True

dataSize = 25

hrToSamples = 2*60
SamplesTohr = 1 / (2*60)

#We need an initial amount of data to calculate the lag
tau = 10*hrToSamples #10hrs * 2 * 60 to get to elements
tauD = 5*hrToSamples #How much shift are we allowing for time lag

M = np.arange(2*tau, dtype = np.float).reshape(tau, 2)
Time = [None] * tau

#Initial lag finder
#--------------------------------------------------------------------
while(True):
	waitForGoodData()
	M[0,0] = RT.get_CC()
	M[0,1] = RT.get_sentiment()
	Time[0] = RT.get_time()
	time.sleep(30)

	for i in range(1, tau):
		waitForGoodData()
		Time[i] = RT.get_time()
		
		if Time[i] == Time[i-1]:
			time.sleep(45)
			waitForGoodData()
			Time[i] = RT.get_time()
			if Time[i] == Time[i-1]:
				Log.Write('Bad data timeout, Servercrash or eq.')
				#push.dump('Sentiment script not running' ,'ERROR:')

		waitForGoodData()
		M[i,0] = RT.get_CC()
		M[i,1] = RT.get_sentiment()
		time.sleep(30)

#1. Fitler both, sentiment is butter, cost should be moving average - done
#--------------------------------------------------------------------
	Value = M[0:len(M), 0]
	Sen = M[0:len(M), 1]

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

	for i in range(0,tauD):
		tValue = tValue[1:len(tValue)];
		tSen = tSen[0:len(tSen) - 1];
		meanResult[i] = np.mean(tValue - tSen);

#5. Find lag
#--------------------------------------------------------------------
	tauL = meanResult.argmin() #tauL = Lag time
	SenOP = dSen[dSen.size-tauL:dSen.size]
	timeOP = Time[dSen.size-tauL:dSen.size]

#6. Find the buy and sell triggers
#--------------------------------------------------------------------
	BuyTrigger = np.array(1)
	SellTrigger = np.array(1)
	
	#Theshold that generates buy and sell triggers
	Thresh = 0.98
	
	#Clear dat shit out
	BuyTrigger = []
	SellTrigger = []
	BuyTriggerMag = [] #This is a super balls hacky way, but I want to make it backwards compatable
	SellTriggerMag = []

	for i in range(0,len(SenOP)):
		if SenOP[i] > max(SenOP) * Thresh:
			BuyTrigger = np.append(BuyTrigger, i)
			BuyTriggerMag = np.append(BuyTriggerMag, SenOP[i])

		if SenOP[i] < (min(SenOP) * Thresh):
			SellTrigger = np.append(SellTrigger,  i)
			SellTriggerMag = np.append(SellTriggerMag, SenOP[i])

	if Debug:
		push.dump('Time(hr):' + str(BuyTrigger*SamplesTohr) + 'Mags:' + str(BuyTriggerMag) ,'BuyTgr_tauL = ' + str(tauL*SamplesTohr))
		push.dump('Time(hr):' + str(SellTrigger*SamplesTohr) + 'Mags:' + str(SellTriggerMag) ,'SellTgr_tauL = ' + str(tauL*SamplesTohr))
		push.dump(str(sum(SenOP) / len(SenOP)), 'Average Sent')
