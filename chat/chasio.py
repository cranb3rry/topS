import asyncio
import logging
import sys, time
from aio_pika import connect_robust, Message
import colorama
from colorama import init, Fore, Back, Style
init()

passw = 'PASS oauth:17gvf82i0pjx40ffg5qdilvnm8rzem\r\n'.encode()
nick = 'NICK sn_b0t\r\n'.encode()
channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangal__official',
	'kolya_incorporated']

login = [
	passw,
	nick
]

cache = []

SERVER_ADDRESS = ('irc.chat.twitch.tv', 6667)

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

logging.basicConfig(
	level=logging.DEBUG,
	format='%(name)s: %(message)s',
	stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

async def echo_client(address, login):

	connection = await connect_robust("amqp://guest:guest@127.0.0.1/", loop=event_loop)

	queue_name = "test_queue"
	routing_key = "test_queue"

	# Creating channel
	channel = await connection.channel()

	# Declaring exchange
	exchange = await channel.declare_exchange('direct', auto_delete=True)

	# Declaring queue
	queue = await channel.declare_queue(queue_name, auto_delete=True)

	# Binding queue
	await queue.bind(exchange, routing_key)

	await exchange.publish(
		Message(
			bytes('Hello', 'utf-8'),
			content_type='text/plain',
			headers={'foo': 'bar'}
		),
		routing_key
	)

	# Receiving message
	incoming_message = await queue.get(timeout=5)

	# Confirm message
	incoming_message.ack()

	await queue.unbind(exchange, routing_key)
	await queue.delete()
	await connection.close()

	log = logging.getLogger('echo_client')
	log.debug('connecting to {} port {}'.format(*address))
	reader, writer = await asyncio.open_connection(*address)
	# This could be writer.writelines() except that
	# would make it harder to show each part of the message
	# being sent.
	for msg in login:
		writer.write(msg)
		#log.debug('sending {!r}'.format(msg))
	for channel in channels:
		join_message = 'JOIN #'+channel+'\r\n'
		writer.write(join_message.encode("utf-8"))

	#if writer.can_write_eof():
	#writer.write_eof()

	await writer.drain()

	log.debug('waiting for response')

	while True:
		data = await reader.read(1024)

		if data:
			#log.debug('received {!r}'.format(data))
			data = data.decode()
			if data == "PING :tmi.twitch.tv\r\n":
				writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
				#log.debug('sending pong')
			messages = data.splitlines()
			for message in messages:
				message_type = tw_irc_type(message)
				tw_irc_format(message, message_type)
		else:
			log.debug('closing')
			writer.close()
			return

try:
	event_loop.run_until_complete(
		echo_client(SERVER_ADDRESS, login)
	)
finally:
	log.debug('closing event loop')
	event_loop.close()