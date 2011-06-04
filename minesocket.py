from __future__ import print_function
import socket

class InputServer():
    def __init__(self, infile, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.infile = infile
        self.addr = addr

    def run(self):
        self.sock.bind(self.addr)
        while True:
            data, address = self.sock.recvfrom(256)
            print(data, file=self.infile)
            self.sock.sendto(b"echo: " + data, address)
    
    def close(self):
        self.sock.close()
