#coms.py

import cfg
import banwords
import socket
import re
import random
import time

def chat(soc, msg):
	soc.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

def timeout(soc, user, time=600):
	chat(soc, ".timeout {} {}".format(user, time))

def ban(soc, user):
	chat(soc, ".ban {}".format(user))
	
def scan(soc, user, msg):
	if cfg.MODDING.count(cfg.CHAN) > 0:
		if langScan(soc, user, msg):
			if capsScan(soc, user,msg):
				pass
	reneeSpam(soc, user, msg)

def langScan(soc, user, msg):
	safeLang = True
	if cfg.ENABLE_LANGFIL == 1:
		for word in banwords.FILTER:
			if re.search(word, msg, re.IGNORECASE):
				timeout(soc, user, 30)
				chat(soc, (user + ": " + banwords.FILPHRASE(random.randint[0, len(banwords.FILPHRASE) - 1]) + " (No racial/homophobic language) (Warning)"))
				safeLang = False
				break
	return safeLang

def capsScan(soc, user, msg):
	safeCaps = True
	if cfg.ENABLE_CAPSFIL == 1:
		capcheck = (4 + (len(re.findall(r"\w", msg)) / 2)) / len(r"[A-Z]")
		if capcheck <= 1:
			timeout(soc, user, 10)
			chat(soc, (user + ": " + banwords.CAPPHRASE(random.randint[0, len(banwords.CAPPHRASE) - 1]) + " (Excessive caps) (Warning)"))
			safeCaps = False
	return safeCaps

def reneeSpam(soc, user, msg, secs=50, delay=3):
	if user == "thatguyfromtv" and re.search("!renaySpam", msg):
		i = secs
		l = -1
		stopCheck = False
		while i > 0 and not stopCheck:
			c = delay
			r = random.randint(0, len(cfg.RENEEPHRASE) - 1)
			while r == l:
				r = random.randint(0, len(cfg.RENEEPHRASE) - 1)
			chat(soc, cfg.RENEEPHRASE[r])
			l = r
			while c > 0 and not stopCheck:
#				stopCheck = stopSpam(soc)
				c -= cfg.RATE
				time.sleep(cfg.RATE)
#			i -= 3
#			time.sleep(3)

def stopSpam(soc):
	stopCheck = False
	chatmsg = soc.recv(2048).decode("utf-8")
	single = re.split(r"\r\n", chatmsg, 0)
	i = 0
	j = len(single) - 1
	while i < j:
		if re.search(r"\w+", single[i], re.MULTILINE) != None:
			user = re.search(r"\w+", single[i], re.MULTILINE).group(0)
			mess = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :", re.MULTILINE).sub("", single[i])
			if user == "thatguyfromtv" and mess == "!stopSpam":
				stopCheck = True
				break
		i += 1
	return stopCheck