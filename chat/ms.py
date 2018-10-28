import socket

HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
NICK = 'sn_b0t'

s = socket.socket()
s.connect((HOST, PORT))
s.send('PASS {}\r\n'.format(PASS).encode("utf-8"))
s.send('NICK {}\r\n'.format(NICK).encode("utf-8"))

msg = "PRIVMSG #sunraylmtd :"+input()+'\r\n'
s.send(msg.encode("utf-8"))