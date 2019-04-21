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

asyncio.run(irc())