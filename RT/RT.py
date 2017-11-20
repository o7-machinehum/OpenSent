#!/usr/bin/python3 -i
#Super dogshit code, just set up for BTC rn

import urllib.request

def LoadFromHTML(): 
    fp = urllib.request.urlopen("http://192.168.10.11/data/updates.txt1l")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    mystr = mystr.replace('\n','') #Remove unwanted CRs
    mystr = mystr.replace(' ','') #Remove unwanted CRs
    Cryptos = mystr.split(",")
    
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
