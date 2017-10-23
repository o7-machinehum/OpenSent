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
RequiredLag = 10*2*60 #10hrs * 2 * 60 to get to elements
MaxShiftLen = 5*2*60

M = np.arange(2*RequiredLag, dtype = np.float).reshape(RequiredLag, 2)

#Initial lag finder
for i in range(0, RequiredLag):
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

meanResult = np.zeros(MaxShiftLen)

for i in range(0,MaxShiftLen) :
	tValue = tValue[1:len(tValue)];
	tSen = tSen[0:len(tSen) - 1];
	meanResult[i] = np.mean(tValue - tSen);

#4. Find lag
#plt.plot(meanResult)
plt.plot(dSen)
plt.show()

#-----------------------Part Two (This is where the magic happens)------------------

#1. Calculate lag (Done above)
#2. Inc a fixed point in time (Lets start with 30 mins), filter the sentament, diff
#3. If the slope is considered to be high (above a threshold) just buy or sell
#4. Wait the time lag, sell or buy if money has been made


