import socket
import select
import struct


class MCRconException(Exception):
    pass


class MCRcon:
    socket = None
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
    
    def disconnect(self):
        self.socket.close()
        self.socket = None
    
    def send(self, out_type, out_data):
        if self.socket is None:
            raise MCRconException("Must connect before sending data")

        # Send a request packet
        out_payload = struct.pack('<ii', 0, out_type) + out_data.encode('utf8') + b'\x00\x00'
        out_length = struct.pack('<i', len(out_payload))
        self.socket.send(out_length + out_payload)

        # Read response packets
        in_data = ""
        while True:
            # Read a packet
            in_length, = struct.unpack('<i', self.socket.recv(4))
            in_payload = self.socket.recv(in_length)
            in_id, in_type = struct.unpack('<ii', in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]

            # Sanity checks
            if in_padding != b'\x00\x00':
                raise MCRconException("Incorrect padding")
            if in_id == -1:
                raise MCRconException("Login failed")

            # Record the response
            in_data += in_data_partial.decode('utf8')

            # If there's nothing more to receive, return the response
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return in_data

    def command(self, command):
        return self.send(2, command)

    def login(self, password):
        return self.send(3, password)