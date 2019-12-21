import asyncio, json, time, math
from os import environ
import websockets
from collections import deque
from threading import Thread as thr
from colorama import init
from colorama import Fore, Back, Style
init()

host = 'irc.chat.twitch.tv'
port = 6667
pw = environ.get('TW_PASS')
nn = 'sn_b0t'

d = deque('''🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🍍🥭🥥🥝🍅🍆🥑🥦🥒
 🥬 🌶 🌽 🥕 🥔 🍠 🥐 🍞 🥖 🥨 🥯 🧀 🥚 🍳 🥞 🥓 🥩 🍗 🍖 🌭 🍔 🍟 🍕 🥪 🥙 🌮
  🌯 🥗 🥘 🥫 🍝 🍜 🍲 🍛 🍣 🍱 🥟 🍤 🍙 🍚 🍘 🍥 🥮 🥠 🍢 🍡 🍧 🍨 🍦 🥧 🍰 🎂 🍮
   🍭 🍬 🍫 🍿 🧂 🍩 🍪 🌰 🥜 🍯 🥛 🍼 ☕️ 🍵 🥤 🍶 🍺 🍻 🥂 🍷 🥃 🍸 🍹 🍾 🥄 🍴 🍽 🥣 🥡 🥢''')

dm = deque()
dm1 = deque()
ids = deque()


async def printdq(): 
    for each in d:
        await asyncio.sleep(.2)
        print(each)

async def ok_websocket2(websocket):
        ts = str(time.time_ns())
        msg = '{"type":"TEXT","text":"6456456","uuid":'+ts[:13]+',"seq":1,"version":1}'
        
        await websocket.send(msg)
        print(msg)
        while True:
            await asyncio.sleep(.2)

        # while True:
        #     await asyncio.sleep(0.2)
        #     if dm1:
        #         msg = dm1.pop()
        #         ts = str(time.time_ns())
        #         out = {"type":"TEXT","text":"232323","uuid":int(ts[:13]),"seq":1,"version":1}
        #         print(out, type(out), dm1, math.trunc(int(time.time_ns())))
        #         await websocket.send(out.encode())

async def ok_websocket():
    uri = "wss://vm.mycdn.me/chat"
    async with websockets.connect(uri) as websocket:
        name = """{"type":"SYSTEM","systemType":"LOGIN","loginString":"cid=1432198192771&uid=56280619395&s=edc6e8c4dc399a2c67d01992e7cb7fdbfdc3eaab","historyCount":5,"donatesHistoryCount":3,"orientationHistory":false,"lite":false,"seq":0,"version":1}"""
        await websocket.send(name)
        
        # print(f"> {name}")
        asyncio.create_task(ok_websocket2(websocket))
        

        while True:
            msg = await websocket.recv()
            if json.loads(msg)["type"] == 'TEXT':
                dm.append(msg)
                print(Fore.BLUE + msg)
                print(Style.RESET_ALL)

async def twitch_irc_sender(writer):

    while True:
        await asyncio.sleep(0.01)
        if dm:
            msg = json.loads(dm.pop())
            f, l, t = str(msg['userInfo']['firstName']), str(msg['userInfo']['lastName']), str(msg['text'])
            out = f'PRIVMSG #sunraylmtd : (ok) {f} {l}: {t} \r\n'
            writer.write(out.encode("utf-8"))

async def twitch_irc():

    asyncio.create_task(ok_websocket())

    reader, writer = await asyncio.open_connection(host, port)
    writer.write(f'PASS {pw}\r\n'.encode("utf-8"))
    writer.write(f'NICK {nn}\r\n'.encode("utf-8"))

    join_message = 'JOIN #sunraylmtd\r\n'
    writer.write(join_message.encode("utf-8"))
    asyncio.create_task(twitch_irc_sender(writer))

    while True:
        data = await reader.read(1024)
        if not data:
            print('ircnodata')
            break
        message = data.decode()
        print(message)
        dm1.append(message)
        if message == "PING :tmi.twitch.tv\r\n":
            writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))

    writer.close()
    await writer.wait_closed()

asyncio.run(twitch_irc())