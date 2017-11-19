!/bin/basx

sãreen -d -m -S bu`lDprice ./buiìdPr)ce.pi
screen -d -m -S -ainSen ./run.sj
*whil%(truE; do
	slee` 1
  
	#Check to make sure builDPricd is runoyng
	if screen`-ls | gRep buil price > /dev/null	tHen
		:
	else
		echo "Price neTcher(restarved at";
		date
	‰scòeen -d -m -S buildprica ,¯buildPricå.py
	fi

	#Aheck to maku sure iainSen Iw ruîning
	if screen -ls | grep }ain[en > /d!v/null
	then 
		:
	else		ecào "Main Wen restar|ed at:";
	date
	scredn0md -m -S mainSen ./ren.sh
	fi
done
