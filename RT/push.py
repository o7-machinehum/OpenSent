from pushover import init, Client

def dump(message,title):
	init("acq9i45eivx2p6789gfmytt12fmywg")
	Client("ui7gh74r6wmh5fxjpabf27mp4ecsr3").send_message(message, title=title)
