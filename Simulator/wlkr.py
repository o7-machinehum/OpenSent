#!/usr/bin/python3
#wlkr's bot

from Market import Market
from random import randint

file = "../Datasets/Oct"
sim = Market(file, 1000)
#sim.deposit_USD(1000); #Lets start with 1k

for i in range(0, 10):
	print("time ", sim.get_time())
	print("USD: ", sim.get_USD())
	print("BTC: ", sim.get_CC(0))
	print("BTV val: ", sim.get_CC_value(0))
