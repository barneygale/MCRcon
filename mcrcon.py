import socket
import select
import struct
import time

class McRconException(Exception):
    pass

class McRcon(object):
    #https://wiki.vg/RCON - check packet format, if anytihing need.

    def __init__(self, host, port, password):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send(3, password)

    def disconnect(self):
        """Close the socket"""
        self.socket.close()

    def read(self, length):
        """Read bytes in length size

        Arguments:
        length -- size of bytes to read
        """
        data = b""
        while len(data) < length:
            data += self.socket.recv(length - len(data))
        return data

    def send(self, type, data):
        """Send payload to server

        Arguments:
        type -- 3 for login, 2 to run a command, 0 for a multi-packet response, may be int
        data -- ASCII text, may be byte[]
        """
        payload = struct.pack('<ii', 0, type) + data.encode('utf8') + b'\x00\x00'
        length = struct.pack('<i', len(payload))
        self.socket.send(length+payload)

        #Reading data
        out_data = ''
        while True:
            out_length, = struct.unpack('<i', self.read(4))  #check length
            out_payload = self.read(out_length)  #read payload size with length
            request_id, out_type = struct.unpack('<ii', out_payload[:8])
            data_partial, padding = out_payload[8:-2], out_payload[-2:]

            # Sanity checks
            if padding != b'\x00\x00':
                raise McRconException("Incorrect padding")
            if request_id == -1:
                raise McRconException("Login failed")

            # Record the response
            out_data += data_partial.decode('utf8')

            # If there's nothing more to receive, return the response
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return out_data

    def command(self, command):
        result = self.send(2, command)
        time.sleep(0.003) # MC-72390 workaround
        return result