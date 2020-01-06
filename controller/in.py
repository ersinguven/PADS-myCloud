import rpyc
import services
import os
from rpyc.utils.server import ThreadedServer

server_table_path = 'data/server_table'
file_table_path = 'data/file_table'
PORT = 21079

def start_controller():
	control_server = ThreadedServer(services.Controller, port=PORT, protocol_config={
					"server_table":server_table_path,
					"file_table":file_table_path,
					"allow_pickle":True,
					"allow_public_attrs":True
					})
	print("Started")
	control_server.start()
	
	
if __name__ == '__main__':
	start_controller()
