#!/usr/bin/python3 -i
#wlkr's bot

from Market import Market
from random import randint
from scipy import signal
from scipy.signal import butter, lfilter, freqz

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

file = "../Datasets/Oct"
BTC = 0 #Index value

sim = Market(file, 1000)

#We need an initial amount of data to calculate the lag
RequiredLag = 10*2*60 #10hrs * 2 * 60 to get to elements

M = np.arange(2*RequiredLag, dtype = np.float).reshape(RequiredLag, 2)

#Initial lag finder
for i in range(0, RequiredLag):
	M[i,0] = sim.get_CC_value(BTC)
	M[i,1] = sim.get_sentiment(BTC)
	sim.inc_time(30)

Value = M[1:len(M), 0]
Sen = M[1:len(M), 1]

#TODO
#1. Fitler both, sentiment is butter, cost should be moving average
b, a = butter(3, 0.1, btype='low')
Sen = lfilter(b, a, Sen)

plt.plot(Sen)
plt.show()

#2. Diff
#3. Time Corr Vector
#4. Find lag

