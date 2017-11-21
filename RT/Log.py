import datetime

Logdir = 'log/'

def getTime():
	now = datetime.datetime.now()
	return str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)

#Get the date in format year-month-day
def getDate():
	now = datetime.datetime.now()
	return str(now.year) + '-' + str(now.month) + '-' + str(now.day)

#Log to a file
def Write(string):
	f = open(Logdir + getDate(), mode='a')
	f.write(getTime() + ':' + string)
	f.close()
