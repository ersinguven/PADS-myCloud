import rpyc
import pickle
import time
import random
import os
from rpyc.utils.server import ThreadedServer

class Controller(rpyc.Service):

	def refresh_server_file(self):
		if os.path.getsize(self.server_file) > 0:
			f = open(self.server_file, 'rb')
			self.server_table = pickle.load(f)
			f.close()
		else:
			self.server_table = {}
			
	def refresh_data_file(self):
		if os.path.getsize(self.data_file) > 0:
			f = open(self.data_file, 'rb')
			self.data_table = pickle.load(f)
			f.close
		else:
			self.data_table = {}
			
	def push_server_file(self):
		f = open(self.server_file, 'wb')
		pickle.dump(self.server_table, f)
		f.close()
		
	def push_data_file(self):
		f = open(self.data_file, 'wb')
		pickle.dump(self.data_table, f)
		f.close()
		
	
	def on_connect(self, conn):
		self.server_file = conn._config["server_table"]
		self.data_file = conn._config["file_table"]
		self.refresh_server_file()
		self.refresh_data_file()
		
	def exposed_add_server(self, server_info):
		self.refresh_server_file()
		self.server_table[server_info["id"]] = {"info":server_info, "last_heartbeat":time.time()}
		self.push_server_file()
		
	def get_random_server(self):
		servers = self.server_table.keys()
		return random.choice(list(servers))
	
	def find_server(self, path):
		self.refresh_data_file()
		server_list = self.server_table.get(path)
		if not server_list:
			self.server_table[path] = [self.get_random_server()]
			server_list = self.server_table.get(path)
			self.push_server_file()
		serverID = server_list[0]
		server_machine = self.server_table[serverID]
		return server_machine
		
	def connect_server(self, server):
		return rpyc.connect(server["info"]["ip"],server["info"]["port"])
		
	
	def exposed_mkdir(self, path, mode):
		print("Controller Here-1")
		serverID = self.get_random_server()
		self.data_table[path] = [serverID]
		server = self.server_table[serverID]
		conn = self.connect_server(server)
		self.push_data_file()
		print("Controller Here-2")
		return conn.root.mkdir(path, mode)
		
	def exposed_readdir(self, path, fh):
		self.refresh_server_file()
		servers = self.server_table.values()
		directory = ['.','..']
		for server in servers:
			conn = self.connect_server(server)
			content = conn.root.readdir(path, fh)
			for c in content:
				if c not in directory:
					directory.append(c)
		return directory
			
		
		
		
		
