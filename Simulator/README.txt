Goal is to create a crypto currency market simulator based on recorded data. The data will include the value of various crypto currencies and associated sentiment. The API will sumulate a market where cc (crypto currencies) can be sold and baught and it will track the CAD you have in your accunt as well as the total cc you have. Other features include:

- limiting trading frequency (max number of transactions per day frequency for example)
- adding a transaction feee
- variable input data format
- Object orient based design
- settings file to set various market parameters




Description:

 The main class is the Market class. A market object has the following member functions:

 - getCAD(): returns the current CAD balance
 - getCC(idx): returns the current CC of given index (BT, ETH, etc)

 - deposit_CAD(value): can deposit CAD directly to you account
 - deposit_CC(idx, value): can deposit CC of given idx directly to your account

 - get_CC_value(idx): returns the current value of the specified CC in CAD
 - get_time(): returns the current simulation time in unix



 - get_transactions(): returns the number of transactions made in that day

 - inc_time(dt): increments the simulator into the future by dt 

 - sell_CC(idx, amount): sell a certian amount of CC

 - buy_CC(idx, amount): buy a certain amount of CC


 To instantiate the Market object:

 	Market market( data, starting_balance, settings):

 	- data: the data file that contains all the market data
 	- starting_balance: starting balance of the CAD account (assumes you want to start with 0 CC)
 	- settings: a settings file (for future development, can be left blank)

