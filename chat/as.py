# import asyncio


# async def tcp_echo_client(message, loop):
#     reader, writer = await asyncio.open_connection('irc.chat.twitch.tv', 6667,
#                                                    loop=loop)

#     PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
#     NICK = 'sn_b0t'

#     #print('Send: %r' % message)
#     #writer.write(message.encode())
#     writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
#     writer.write('NICK {}\r\n'.format(NICK).encode("utf-8"))

#     message = await reader.read(1024)
#     print('Received: %r' % message.decode())


#     if message.decode() == "PING :tmi.twitch.tv\r\n":
#         writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))

#     #print('Close the socket')
#     #writer.close()


# message = 'Hello World!'
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tcp_echo_client(message, loop))
# #loop.close()

import asyncio, time
PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
NICK = 'sn_b0t'
channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangai',
	'lolyoudie_']

async def tcp_echo_client(message, loop):

	reader, writer = await asyncio.open_connection('irc.chat.twitch.tv', 6667,
		loop=loop)

	print('Send: %r' % message)
	writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
	writer.write('NICK {}\r\n'.format(PASS).encode("utf-8"))
	for channel in channels:
		join_message = 'JOIN #'+channel+'\r\n'
		writer.write(join_message.encode("utf-8"))

	while True:

		data = await reader.read(100)
		print('Received: %r' % data.decode())



message = 'Hello World!'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()

def fs():
	print(5)
	time.sleep(5)
