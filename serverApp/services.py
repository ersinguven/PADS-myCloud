import rpyc
import os
import pickle

data_path = "/home/ersin-2/Desktop/serverApp"
class serverService(rpyc.Service):
	def on_connect(self, conn):
		pass
	
	def on_disconnect(self, conn):
		pass

	def abs_path(self, p_path):
		if p_path.startswith("/"):
			p_path = p_path[1:]
		return os.path.join(data_path, p_path)
		
	def exposed_mkdir(self, path, mode):
		print("Server Here-1")
		a_path = self.abs_path(path)
		print(a_path)
		return os.mkdir(a_path, mode)
		
	def exposed_rmdir(self, path):
		a_path = self.abs_path(path)
		return os.rmdir(a_path)
		
	def exposed_open(self, path, flags, mode):
		a_path = self.abs_path(path)
		return os.open(a_path, flags, mode)
		
	def exposed_readdir(self, path, fh):
		a_path = self.abs_path(path)
		return os.listdir(a_path)
		
	def exposed_echo(self, text):
		return text
		
