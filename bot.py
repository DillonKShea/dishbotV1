# bot.py

import cfg
import socket
import time
import re
import coms

CHAT_EX = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :", re.MULTILINE)
#CHAT_FULL = r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :.+\r\n"
CHAT_INI1 = re.compile(r"^:tmi\.twitch\.tv \d{3} \w+ :", re.MULTILINE)
CHAT_INI2 = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv ", re.MULTILINE)
CHAT_INI3 = re.compile(r"^:\w+\.tmi\.twitch\.tv \d{3} \w+ =?\s?", re.MULTILINE)

sock = socket.socket()
sock.connect((cfg.HOST, cfg.PORT))
sock.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
sock.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
sock.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))
while True:
	chatmsg = sock.recv(2048).decode("utf-8")
	if chatmsg == "PING :tmi.twitch.tv\r\n":
		sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
	elif re.search(r"^:tmi\.twitch\.tv", chatmsg, re.MULTILINE) != None:
		init = CHAT_INI1.sub("", chatmsg)
		print(init)
	#	print(chatmsg)
	elif re.search(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv JOIN", chatmsg, re.MULTILINE) != None:
		init = CHAT_INI2.sub("", chatmsg)
		init = CHAT_INI3.sub("", init)
		print(init)
	#	print(chatmsg)
	else:
		single = re.split(r"\r\n", chatmsg, 0)
		i = 0
		j = len(single) - 1

		while i < j:
			if re.search(r"\w+", single[i], re.MULTILINE) != None:
				user = re.search(r"\w+", single[i], re.MULTILINE).group(0)
				mess = CHAT_EX.sub("", single[i])
				print(user + ": " + mess)
				coms.scan(sock, user, mess)
			i += 1
	time.sleep(cfg.RATE)