#!/usr/bin/env python2
 

import sys, socket, time

sleep_time = 0
file_to_save = "file.txt"

class mysocket:

	def __init__(self,ip = None ,port = None, sock=None,timeout=1):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		self.sock.settimeout(timeout)
		self.connection = False
		if type(ip) == str and type(port) == int:
			self.connection = self.connect(ip,port)
		
	def connect(self, host, port):
		try:
			self.sock.connect((host, port))
			return True
		except:
			return False

	def send(self, msg = "", n = None):
		if type(n) == int:
			msg = msg[:n]
		try :
			if self.sock.send(msg) == 0:
				return False
			return True
		except:
			return False
		
	def receive(self):
		msg = ""
		c = self.get_one_char()
		while (c != "\n") \
		and (c != False):
			msg = msg + c
			c = self.get_one_char()
		if msg == "":
			return False
		return msg

	def get_data(self):
		msg = ""
		tm = self.receive()
		while tm :
			msg = msg + tm + "\n" 
			tm = self.receive()
		if msg == "":
			return False
		return msg
		
	def get_one_char(self):
		try:
			c = self.sock.recv(1)
		except:
			c = False
		return c
	
	def comunicate(self,msg=None):
		try:
			if type(msg) == str:
				connection.send(msg+"\n")
			return connection.get_data()
		except:
			return False

def nums_only(string):
	nstr = ""
	for c in string:
		for n in "0123456789":
			if n == c:
				nstr = nstr + n
				break
	return nstr

def extract_numbers(string):
	if type(string) != str:
		return False
	t = string.split(" ")
	if t[0] != "Nope,":
		return False
	sys.stdout.flush()
	return nums_only(t[8])

def append_to_file(toappend):
	f = open(file_to_save, "a")
	f.write(toappend+"\n")
	f.close()

def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

if __name__ == "__main__":

	try:
		connection = mysocket(sys.argv[1],int(sys.argv[2]))
	except:	
		connection = mysocket('127.0.0.1',8888)
		
	if connection.connection:
		set_keepalive_linux(connection.sock)
		#print "timeout : '" + str(connection.sock.gettimeout()) + "'"
		#print connection.comunicate()
		connection.comunicate()
		while True:
			rep = extract_numbers(connection.comunicate(""))
			if rep == False:
				print "error comunicating"
				break
			append_to_file(rep)
			print  rep
			time.sleep(sleep_time)
		
	else:
		print "no connection, start server first" 
