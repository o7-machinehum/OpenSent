#!/usr/bin/python3 -i
#Super dogshit code, just set up for BTC rn

import urllib.request
import pdb

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
	Cryptos = LoadFromHTML()
	return(Cryptos[1])

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
	elif Cryptos[0] == ('None' or 'N/A'):
		BadDataFrame = True
	elif Cryptos[1] == ('None' or 'N/A'):
		BadDataFrame = True
	elif Cryptos[3] == ('None' or 'N/A'):
		BadDataFrame = True
	elif Cryptos[4] == ('None' or 'N/A'):
		BadDataFrame = True
	else:
		BadDataFrame = False
	
	return BadDataFrame

