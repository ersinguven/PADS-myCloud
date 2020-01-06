import rpyc
import services
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process
import os
import socket


HOST = "localhost"
CONTROLLER_PORT = 21079

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

def connect_controller():
	conn = None
	while conn == None:
		try:
			conn = rpyc.connect(HOST,CONTROLLER_PORT)
			print("CONNECTED to CONTROLLER")
		except Exception:
			print('Cannot connect to the controller')
			conn = None
	conn.root.add_server(get_server_info())

def start_server():
	port = 21269
	server = ThreadedServer(services.serverService, port=port, protocol_config={
					"allow_pickle":True,
					"allow_public_attrs":True})
	server.start()

def get_server_info():
	return {
		"id":socket.gethostname(),
		"ip":socket.gethostbyname(socket.gethostname()),
		"port":21269
		}

if __name__ == "__main__":
	server = Process(target=start_server)
	to_controller = Process(target=connect_controller)

	server.start()
	to_controller.start()

	server.join()
	to_controller.join()



	
