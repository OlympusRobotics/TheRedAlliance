from tra.server import *

def main():
	db.create_all()
	app.debug = True
	app.run(host="127.0.0.1", port = 5000)