import socket
import select
import struct
import re

class MCRcon:
	token = 0

	def __init__(self, host, port, password):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host, port))
		self.send_real(3, password)
	
	def close(self):
		self.s.close()
	
	def send(self, command):
		return self.send_real(2, command)
	
	def send_real(self, out_id, out_data):
		#Get a new token
		self.token += 1
		out_token = self.token
		
		#Send the data
		buff = struct.pack('iii', 
			10+len(out_data),
			out_token,
			out_id) + out_data + "\x00\x00"
		self.s.send(buff)
		
		#Receive a response
		in_data = ''
		ready = True
		while ready:
			#Receive an item
			tmp_len, tmp_token, tmp_id = struct.unpack('iii', self.s.recv(12))
			tmp_data = self.s.recv(tmp_len-8) #-8 because we've already read the 2nd and 3rd integer fields

			#Strip pad bytes
			assert tmp_data[-2:] == '\x00\x00'
			tmp_data = tmp_data[:-2]
			
			#Error-check
			if tmp_token == -1:
				raise Exception('auth failure')
			elif tmp_token != out_token:
				raise Exception('protocol error')
			m = re.match('^Error executing: %s \((.*)\)$' % out_data, tmp_data)
			if m:
				raise Exception('command failure', m.group(1))
			
			#Append
			in_data += tmp_data

			#Check if more data ready...
			ready = select.select([self.s], [], [], 0)[0]
		
		return in_data
