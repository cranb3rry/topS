import socket, platform, time, select, asyncio
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

channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangal__official',
	'kolya_incorporated']

s = socket.socket()
s.connect((HOST, PORT))
s.send('PASS {}\r\n'.format(PASS).encode("utf-8"))
s.send('NICK {}\r\n'.format(NICK).encode("utf-8"))

def tw_irc_format(message, message_type):
	channel = ''
	t = time.ctime().split()[3]
	if message_type == 'PRIVMSG':
		text = message[message.find(' :')+2:]
		# print(text)
		user = message[1:message.find('!')]
		# print(user)
		channel = message[message.find('#')+1:].split()[0]
		# print(channel)

		print(Fore.WHITE+t, Fore.CYAN+user+Fore.RED+'@'+
			Fore.MAGENTA+channel+':', Fore.YELLOW+text)
		

	if message_type == 'JOIN':
		channel = message[message.find('#'):].split()[0]
		print(Fore.WHITE+'Join', Fore.MAGENTA+channel)

	#if message_type == 'unknown':

		#print(Fore.WHITE+message)

	ukr(channel, message)

	return

def tw_irc_type(message):

	message_type = 'unknown'

	# keep PRIVMSG last to overwrite user input
	known_types = ['JOIN', 'PING', 'PRIVMSG']

	for kt in known_types:
		if kt in message:
			message_type = kt

	return message_type

def ukr(ch, m):
	if 'Слава Україні!' in m:
		msg = "PRIVMSG #"+ch+" :Героям слава!\r\n"
		s.send(msg.encode("utf-8"))
		print(Fore.RED+msg[:-2])
	return	

for channel in channels:
	join_message = 'JOIN #'+channel+'\r\n'
	s.send(join_message.encode("utf-8"))




while True:

	message = s.recv(1024).decode("utf-8")
	if not message: break
	if message == "PING :tmi.twitch.tv\r\n":
		s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))

	messages = message.splitlines()
	for message in messages:

		message_type = tw_irc_type(message)
		tw_irc_format(message, message_type)
		#print(message)
		# sp = e.find(' :')
		# if sp>0:
		# 	print(Fore.RED + e[:sp], Fore.BLUE + e[sp+2:], 
		# 		Fore.YELLOW + message_type)
		# else:
		# 	print(Fore.RED + e, Fore.YELLOW + message_type)