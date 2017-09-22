from stocktalk import visualize

# Make sure these variables are consistent with streaming.py
tickers = ['TSLA','SNAP','AAPL','AMZN']
refresh = 1
path = "/home/pi/Stocktalk/data/"

visualize(tickers, refresh, path)
