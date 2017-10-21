from Market import Market

from random import randint


file = "/home/divgill/Documents/Crypto/cryptos/Datasets/Oct"

sim = Market(file, 1000)

for i in range(0, 10):
    print("time ", sim.get_time())
    print("USD: ", sim.get_USD())
    print("BTC: ", sim.get_CC(0))
    print("BTV val: ", sim.get_CC_value(0))

    rand = randint(0, 100)

    if rand < 25:
        print("Buy!!!!!!!!!!")
        sim.buy_CC(0, rand)

    sim.inc_time(10*60*60)
    print("****")

print("Final Sale")
sim.sell_CC(0, sim.get_CC(0)) # SELL EVERYTHING
print("USD: ", sim.get_USD())
print("BTC: ", sim.get_CC(0))

#sim.plot_trading_stats(0)
sim.data.frame['btc_val'].plot()

