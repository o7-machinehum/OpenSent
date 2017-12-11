#!/usr/bin/python3 -i
#Super dogshit code, just set up for BTC rn

import urllib.request
import Log
import pdb
import time

Host = '192.168.10.12'

def LoadFromHTML(): 
	fp = urllib.request.urlopen('http://' + Host + '/data/updates.txt1l')
	mybytes = fp.read()

	mystr = mybytes.decode("utf8")
	fp.close()

	mystr = mystr.replace('\n','') #Remove unwanted CRs
	mystr = mystr.replace(' ','') #Remove unwanted CRs
	Cryptos = mystr.split(",")
	Cryptos = Cryptos[0:-1]

	return Cryptos

def get_time():
	Timeout = 0
	
	while True:
		Cryptos = LoadFromHTML()
		try:
			Time = Cryptos[1]
			Timeout = 0
			break
		except:
			Log.Write('ERROR: Time Value Exception')	
			time.sleep(30)
			Timeout += 1
		
		if Timeout > 10:
			Log.Write('ERROR: Time: Timeout Exception')	
			break
			
	return(Time)

def get_CC():
	Cryptos = LoadFromHTML()
	return(Cryptos[5])

def get_sentiment():
	Cryptos = LoadFromHTML()
	return(Cryptos[4])

def CheckDataFrame():
	BadDataFrame = True
	
	Cryptos = LoadFromHTML()

	if len(Cryptos) != 14:
		BadDataFrame = True
		Log.Write('ERROR: Length Mismatch')	
	elif Cryptos[0] == 'None' or  Cryptos[0] == 'N/A' or Cryptos[0] == '':
		BadDataFrame = True
		Log.Write('ERROR: Data Invalid')	
	elif Cryptos[1] == 'None' or  Cryptos[1] == 'N/A' or Cryptos[1] == '':
		BadDataFrame = True
		Log.Write('ERROR: Data Invalid')	
	elif Cryptos[3] == 'None' or  Cryptos[3] == 'N/A' or Cryptos[3] == '':
		BadDataFrame = True
		Log.Write('ERROR: Data Invalid')	
	elif Cryptos[4] == 'None' or  Cryptos[4] == 'N/A' or Cryptos[4] == '':
		BadDataFrame = True
		Log.Write('ERROR: Data Invalid')	
	else:
		BadDataFrame = False

	return BadDataFrame

