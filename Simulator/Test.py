from Market import Market




file = "/home/divgill/Documents/Crypto/cryptos/Datasets/Oct"

sim = Market(file, 1000)

for i in range(0, 10):
    print("time ", sim.get_time())
    print(" USD: ", sim.get_USD())
    print(" BTC: ", sim.get_CC(0))
    print(" BTV val: ", sim.get_CC_value(0))

    sim.buy_CC(0, 50)

    sim.inc_time(30)
