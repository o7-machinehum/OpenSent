from stocktalk import streaming

# Credentials to access Twitter API 
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
credentials = [API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]

# First element must be ticker/name, proceeding elements are extra queries

#Popular
BTC = ['BTC', 'Bitcoin']
LTC = ['LTC', 'Litecoin']
ETH = ['ETH', 'Ethereum']
BTS = ['BTS', 'BitShares']
XRP = ['XRP', 'Ripple']
XMR = ['XMR', 'Monero']
DASH = ['DASH', 'Dash']
ETC = ['ETC', 'Ethereum Classic']
BCH = ['BCH', 'Bitcoin Cash']
LSK = ['LSK', 'Lisk']
DOGE = ['DOGE', 'Dogecoin']

tickers = [BTC, LTC, ETH]  # Used for identification purposes
queries =  BTC +LTC + ETH  # Filters tweets containing one or more query 

#Undersground
NOTE = ['NOTE', 'Dnotes'] #Too common
SBD = ['SBD', 'Steem Dollars']
BELA = ['BELA', 'Bela'] #Too common (Spanish for beautiful)
NAUT = ['NAUT', 'Nautiluscoin']
NEOS = ['NEOS', 'Neoscoin']
SJCX = ['SJCX', 'Storjcoin X']

#tickers = [SBD, NAUT, NEOS, SJCX]  # Used for identification purposes
#queries =  SBD + NAUT + NEOS + SJCX  # Filters tweets containing one or more query

refresh = 30                     # Process and log data every x seconds

# Create a folder to collect logs and temporary files
#path = "/home/pi/Stocktalk/data/"
path = "data/"

streaming(credentials, tickers, queries, refresh, path, realtime=True, logTracker=True, logTweets=True, logSentiment=True, debug=True)
