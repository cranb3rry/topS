import socket, platform
if 'Windows' in platform.system():
	import win_unicode_console
	win_unicode_console.enable()

import colorama
from colorama import init, Fore, Back, Style
init()

HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
NICK = 'sn_b0t'
CHNAME = 'sunraylmtd' 

s = socket.socket()
s.connect((HOST, PORT))
s.send('PASS {}\r\n'.format(PASS).encode("utf-8"))
s.send('NICK {}\r\n'.format(NICK).encode("utf-8"))

s.send('JOIN #{}\r\n'.format(CHNAME).encode("utf-8"))
s.send('JOIN #mangal_official\r\n'.encode("utf-8"))
s.send('JOIN #cranb3rry\r\n'.encode("utf-8"))
s.send('JOIN #f0ck_the_system\r\n'.encode("utf-8"))
s.send('JOIN #lolyoudie_\r\n'.encode("utf-8"))

while True:
 	r = s.recv(1024).decode("utf-8")
 	print(Fore.GREEN + r)
 	r.split()
 	#print(Style.RESET_ALL)

 	if r == "PING :tmi.twitch.tv\r\n":
 		s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))