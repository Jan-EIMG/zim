import time
import datetime

Notbetrieb          = 0
Normalbetrieb       = 1
Sicherheitsbetrieb  = 2
Energieüberschuss   = 3
betriebart = ["Notbetrieb", "Normalbetrieb", "Sicherheitsbetrieb", "Energieüberschuss"]

ipAdress = "192.168.81.174"


def startloop(loop, myOPCUA,modul):
	i = 0
	start_time1 = 0.0
	stopp_time1 = 0.0
	start_time2 = 0.0
	stopp_time2 = 0.0
	time.sleep(1-(datetime.datetime.now().microsecond/1000000))	#s
	while True:
		i += 1
		start_time2neu = time.time()
		opcjson = myOPCUA.pull_data()
		opcjson["Girea-Module"][modul]["live bit"].set_value(not opcjson["Girea-Module"][modul]["live bit"].get_value())
		opcjson["Girea-Module"][modul]["zyklus"].set_value(i)
		opcjson["Girea-Module"][modul]["core-time"].set_value(stopp_time1-start_time1)
		opcjson["Girea-Module"][modul]["zyklus-time"].set_value(stopp_time2-start_time2)

		start_time2 = start_time2neu

		start_time1 = time.time()
		loop(opcjson)
		stopp_time1 = time.time()

		myOPCUA.push_data()
		stopp_time2 = time.time()
		time.sleep(1-(datetime.datetime.now().microsecond/1000000))	#s
	

def initDaten():    ###  initalisiere geräte parameter & debug log
	### Log.txt saven und löschen
	File = ""
	try:
		with open("Log.txt", "r", encoding='utf-8') as inFile:
			File = inFile.read()
		with open("Log.txt", "w", encoding='utf-8') as outfile:
			outfile.write("")
	except:
		with open("Log.txt", "x", encoding='utf-8') as outfile:
			outfile.write("")

	try:
		with open("Log_historie.txt", "a", encoding='utf-8') as outfile:
			outfile.write(File)
	except:
		with open("Log_historie.txt", "x", encoding='utf-8') as outfile:
			outfile.write(File)

def log(text):
	if not isinstance(text, str):
		text = str(text)
	print("Log "+text)
	try:
		with open("Log.txt", "x", encoding='utf-8') as outfile:
			now = datetime.datetime.now()
			# outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")
			outfile.write("Log date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n\t" +text+"\n")
	except:
		with open("Log.txt", "a", encoding='utf-8') as outfile:
			now = datetime.datetime.now()
			# outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")
			outfile.write("Log date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n\t" +text+"\n")