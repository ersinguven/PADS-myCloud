import os
import sys
import errno
import rpyc

from fuse import FUSE, FuseOSError, Operations

HOST = '192.168.1.46'
PORT = 21078

class Passthrough(Operations):
	def __init__(self):
		self.conn = rpyc.connect(HOST, PORT)
		
	def _full_path(self, partial):
		if partial.startswith("/"):
			partial = partial[1:]
		path = os.path.join(self.root, partial)
		return path
		
	def readdir(self, path, fh):
		print("Method Invoked: 'readdir'")
		return self.conn.root.readdir(path, fh)
		
	def rmdir(self, path):
		print("Method Invoked: 'rmdir'")
		return self.conn.root.rmdir(path)
		
	def mkdir(self, path, mode):
		print("Method Invoked: 'mkdir'")
		print(path)
		return self.conn.root.mkdir(path, mode)
		
		
	def open(self, path, flags, mode=None):
		print("Method Invoked: 'open'")
		return self.conn.root.open(path, flags, mode)
		
	def unlink(self, path):
		print("Method Invoked: 'unlink'")
		return self.conn.root.unlink(path)
	
def mount(ls):
	if len(ls) < 2:
		print('Wrong Format\ne.g:', ls[0],'<mount dir>')
	real_path = os.path.abspath(ls[1])
	
	if not os.path.isdir(real_path):
		print('Error! Mount Point does not exist')
		sys.exit(0)
	if len(os.listdir(real_path)) > 0:
		print('Error! Mount point must be empty')
		sys.exit(0)
		
	FUSE(Passthrough(), ls[1], nothreads=True, foreground=True)
	
if __name__ == '__main__':
	mount(sys.argv)
	
