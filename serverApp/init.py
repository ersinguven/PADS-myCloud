import rpyc
import services
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process
import os
import socket
import netifaces as ni

HOST = "192.168.1.46"
CONTROLLER_PORT = 21078

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
	port = 11269
	server = ThreadedServer(services.serverService, port=port, protocol_config={
					"allow_pickle":True,
					"allow_public_attrs":True})
	server.start()

def get_server_info():
	return {
		"id":socket.gethostname(),
		"ip":ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr'],
		"port":11269
		}

if __name__ == "__main__":
	server = Process(target=start_server)
	to_controller = Process(target=connect_controller)

	server.start()
	to_controller.start()

	server.join()
	to_controller.join()



	
