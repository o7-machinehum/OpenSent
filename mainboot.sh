#!/bin/bash

screen -d -m -S buildprice ./buildPrice.py
screen -d -m -S mainSen ./run.sh
while(true) do
	sleep 1
  
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
