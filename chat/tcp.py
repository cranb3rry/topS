#!/usr/bin/env python
import socket

TCP_IP = '46.188.104.83'
TCP_PORT = 5000
BUFFER_SIZE = 4
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# while True:

s.send('3333333'.encode())
print(s.recv(BUFFER_SIZE))