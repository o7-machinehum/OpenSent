#!/usr/bin/python3

from Market import Market

from random import randint


file = "../Datasets/Oct"

sim = Market(file, 1000)

for i in range(0, 40):
    print("time ", sim.get_time())
    print("USD: ", sim.get_USD())
    print("BTC: ", sim.get_CC(0))
    print("BTV val: ", sim.get_CC_value(0))

    rand = randint(0, 100)

    if rand > 75:
        print("Buy!!!!!!!!!!")
        sim.buy_CC(0, rand * 4)
    elif rand > 35 & rand < 65:
        print("Sell!!!!!!!!!")
        sim.sell_CC(0, sim.get_CC(0) * (rand / 100.0))

    sim.inc_time(10*60*60)
    print("****")

print("Final Sale")
sim.sell_CC(0, sim.get_CC(0)) # SELL EVERYTHING
print("USD: ", sim.get_USD())
print("BTC: ", sim.get_CC(0))

sim.plot_trading_stats(0) # 0 is the index for bitcoin



