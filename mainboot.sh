#!/bin/bash

echo "les go";

screen -d -m -S buildprice ./buildPrice.py
screen -d -m -S mainSen ./run.sh
screen -d -m -S RT ./RT/Notifier.py

while(true) do
	sleep 1
 
	if screen -ls | grep RT > /dev/null 
	then
	: #Do nothing
	else
		echo "RT Restarted at:";
		date
		screen -d -m -S RT ./RT/Notifier.py
	fi

	if screen -ls | grep buildprice > /dev/null 
	then
	: #Do nothing
	else
		echo "Price Restarted at:";
		date
		screen -d -m -S buildprice ./buildPrice.py
	fi

	if screen -ls | grep mainSen > /dev/null 
	then
	: #Do nothing
	else
		echo "Price Restarted at:";
		date
		screen -d -m -S mainSen ./run.sh
	fi
done
]0;machinehum@wlkr: ~/cryptosmachinehum@wlkr:~/cryptos$ screne[K[Ken -ls
There is a screen on:
	31023.pts-1.wlkr	(20/11/17 09:48:25 PM)	(Attached)
1 Socket in /run/screen/S-machinehum.
]0;machinehum@wlkr: ~/cryptosmachinehum@wlkr:~/cryptos$ exit
exit
