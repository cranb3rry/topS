from googleapiclient.discovery import build
import asyncio

HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
NICK = 'sn_b0t'

irc_channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangal__official',
    'kolya_incorporated', 'xoaliro']

async def irc():
    print('startirc')
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
    writer.write('NICK {}\r\n'.format(NICK).encode("utf-8"))
    writer.write('JOIN #sunraylmtd\r\n'.encode("utf-8"))
    while True:
    	data = await reader.read(1024)

    	print(f'Received: {data.decode()!r}')


service = build('youtube', 'v3')
waittime = 30000

logged_ids = []

def log_messages(message, id):
	if id not in logged_ids:
		print(message)
		logged_ids.append(id)

async def chat():

	while True:

		response = service.liveChatMessages().list(liveChatId=
			'EiEKGFVDWnUtSlAxcGxjNVZsQlExZC1lRzdjURIFL2xpdmU',
			part='snippet, id, authorDetails',
			maxResults=500).execute()
		waittime = response['pollingIntervalMillis']
		count = response['pageInfo']['totalResults']

		print(count, waittime)

		for e in response['items']:
			message = [ # id, text, date, channel, name
			e['id'],
			e['snippet']['textMessageDetails']['messageText'],
			e['snippet']['publishedAt'],
			e['authorDetails']['channelId'],
			e['authorDetails']['displayName'],
			]
			log_messages(message, message[0])

		await asyncio.sleep(waittime/1000)

async def main(loop):
	task = asyncio.create_task(chat())
	task2 = asyncio.create_task(irc())
	#task2 = asyncio.create_task(irc())
	await task, task2
	print('tasks')

event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

asyncio.run(main())