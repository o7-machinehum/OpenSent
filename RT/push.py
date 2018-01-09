from pushover import init, Client

def dump(message,title):
	init("")
	Client("").send_message(message, title=title)
