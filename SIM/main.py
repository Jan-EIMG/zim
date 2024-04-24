#-*- coding: utf-8-*-
import sys
from opcua import ua,Client
from opcua.common.node import Node
import time
import datetime
import json

from globals.OPCUA import OPCUA
from globals.globals import *

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


def init_OPCUA():
	# url = "opc.tcp://192.168.0.1:4840"
	# url = "opc.tcp://192.168.81.174:4840"
	url = "opc.tcp://opcua:4840"
	url = "opc.tcp://192.168.81.174:4840"
	# url = "opc.tcp://test:test@192.168.0.1:4840"
	# url = "opc.tcp://OPCUser01:11223344Ki@192.168.1.232:4840"
	# security_string = "Basic256Sha256,SignAndEncrypt," + "OPC_UA\\cient_X.509 Certificate_4.der" + "," + "OPC_UA\\cient_X.509 Certificate_4.pem"
	# security_string = "Basic256Sha256,SignAndEncrypt," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.der" + "," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.pem"
	security_string = "Basic256Sha256,SignAndEncrypt," + "my_cert2.der" + "," + "my_private_key2.pem"

	def browse_recursive(node, json = {}):
		chillist = node.get_children()
		try:
			chillist.remove(client.get_node("i=2253"))
		except:
			pass
		for childId in chillist:
			ch = client.get_node(childId)
			if ch.get_node_class() == ua.NodeClass.Object:
				name = ch.get_browse_name().Name.split("_")[-1]
				json[name] = {}
				browse_recursive(ch, json[name])
			elif ch.get_node_class() == ua.NodeClass.Variable:
				try:
					name = ch.get_browse_name().Name.split("_")[-1]
					json[name] = ch
				except ua.uaerrors._auto.BadWaitingForInitialData:
					pass
		return json
			# .get_value()


	try:
		client = Client(url)
		client.set_security_string(security_string)
		# client._username = "user1"
		# client._password = "pw1"
		client.connect()
		client.load_type_definitions()
		log("Connected to OPC UA Server")
	except Exception as err:
		log("server not found")
		sys.exit(1)
	return browse_recursive(client.get_objects_node())


def init_SIM_Speicher(opcjson, id, kWh=100):
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["Geändert durch"].set_value("SIM Speicher")
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["Name"].set_value("SIM Speicher")
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["Kennzeichnung"].set_value("id 0")
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max kW/h"].set_value(kWh)
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["anlauf-zeit in s"].set_value(0.05)
	opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["verdrahtet"].set_value(True)
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max lade kW"].set_value(500)
	opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max etlade kW"].set_value(500)

	# opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]
	# opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]


def SIM_Speicher(opcjson, id, leistung=0):
	maxkWh = opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max kW/h"].get_value()
	
	erzeugerkW = opcjson["Girea-SPS"]["Erzeuger"]["gesamt kW"].get_value()		# Negativ
	verbraucherkW = opcjson["Girea-SPS"]["Verbraucher"]["gesamt kW"].get_value()	# Positiv
	speicherkW = 0 #opcjson["Girea-SPS"]["Speicher"]["gesamt kW"].get_value() - opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW"].get_value()
	netzanbieterkW = 0 #opcjson["Girea-SPS"]["Netzanbieter"]["gesamt kW"].get_value()

	Ladeleistung = sum([erzeugerkW, verbraucherkW, speicherkW, netzanbieterkW, leistung*-1])
	Cyclus_zeit_in_s = 1#0
	s_in_Stunden = 0.000277778
	

	maxladekW = opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max lade kW"].get_value()
	maxetladekW = opcjson["Girea-HMI"]["Speicher"][f"[{id}]"]["Parameter"]["max etlade kW"].get_value()

	print(maxladekW, maxetladekW*-1, Ladeleistung)
	if abs(maxetladekW)*-1 > Ladeleistung:
		Ladeleistung = abs(maxetladekW)*-1
	if abs(maxladekW) < Ladeleistung:
		Ladeleistung = abs(maxladekW)


	LevelkWh = opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW/h"].get_value()
	LevelkWh1 = LevelkWh
	LevelkWh1 += Ladeleistung * Cyclus_zeit_in_s * s_in_Stunden / 1000.0

	# print(LevelkWh1, maxkWh)
	if LevelkWh1 > maxkWh:
		tempkWh = maxkWh - LevelkWh1 
		Ladeleistung += tempkWh / Cyclus_zeit_in_s / s_in_Stunden * 1000.0
		# print(tempkWh, Cyclus_zeit_in_s, s_in_Stunden)

	if LevelkWh1 < 0:
		tempkWh = LevelkWh1 - 0
		Ladeleistung -= tempkWh / Cyclus_zeit_in_s / s_in_Stunden * 1000.0

	LevelkWh += Ladeleistung * Cyclus_zeit_in_s * s_in_Stunden / 1000.0

	Level = 100/maxkWh*LevelkWh

	opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW/h"].set_value(LevelkWh)
	opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["Level in %"].set_value(Level)

	opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW"].set_value(Ladeleistung*-1)

	# return (Ladeleistung*-1) - opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW"].get_value()
	return opcjson["Girea-SPS"]["Speicher"][f"[{id}]"]["kW"].get_delta()#*-1

def SIM_Verbraucher(opcjson, id):
	if opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["start"].get_value():
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["soll an"].set_value(True)
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["start"].set_value(False)

	if opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["stopp"].get_value():
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["soll an"].set_value(False)
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["stopp"].set_value(False)


	kW = opcjson["Girea-HMI"]["Verbraucher"][f"[{id}]"]["Parameter"]["DSW kW"].get_value()
	if opcjson["Girea-HMI"]["Verbraucher"][f"[{id}]"]["SIMstartstopp"].get_value() == 0:		# hand aus
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["ist an"].set_value(False)
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["kW"].set_value(0)
	elif opcjson["Girea-HMI"]["Verbraucher"][f"[{id}]"]["SIMstartstopp"].get_value() == 1:	# hand an
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["ist an"].set_value(True)
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["kW"].set_value(abs(kW)*-1)
	elif opcjson["Girea-HMI"]["Verbraucher"][f"[{id}]"]["SIMstartstopp"].get_value() == 2:	# auto
		# opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["ist an"].set_value(opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["soll an"].get_value())
		soll = opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["soll an"].get_value()
		opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["ist an"].set_value(soll)
		if soll:
			opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["kW"].set_value(abs(kW)*-1)
		else:
			opcjson["Girea-SPS"]["Verbraucher"][f"[{id}]"]["kW"].set_value(0)


def SIM_Erzeuger(opcjson, id):
	if opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["start"].get_value():
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["soll an"].set_value(True)
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["start"].set_value(False)

	if opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["stopp"].get_value():
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["soll an"].set_value(False)
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["stopp"].set_value(False)


	kW = opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["Parameter"]["DSW kW"].get_value()
	if opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["SIMstartstopp"].get_value() == 0:		# hand aus
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["ist an"].set_value(False)
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(0)
	elif opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["SIMstartstopp"].get_value() == 1:	# hand an
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["ist an"].set_value(True)
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(abs(kW))
	elif opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["SIMstartstopp"].get_value() == 2:	# auto
		soll = opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["soll an"].get_value()
		opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["ist an"].set_value(soll)
		if soll:
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(abs(kW))
		else:
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(0)

	elif opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["SIMstartstopp"].get_value() == 3:	# sim Sägezahn
		if opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].get_value() <= 0:
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(abs(kW))
		else:
			temp = opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].get_value()
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(temp-1)

	elif opcjson["Girea-HMI"]["Erzeuger"][f"[{id}]"]["SIMstartstopp"].get_value() == 4:	# sim Treppe
		if opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].get_value() <= 0:
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(abs(kW))
		else:
			temp = opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].get_value()
			opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].set_value(temp-20)


	return opcjson["Girea-SPS"]["Erzeuger"][f"[{id}]"]["kW"].get_delta()

def SIM_Netzanbieter(opcjson, id, leistung=0):
	erzeugerkW = opcjson["Girea-SPS"]["Erzeuger"]["gesamt kW"].get_value()		# Negativ
	verbraucherkW = opcjson["Girea-SPS"]["Verbraucher"]["gesamt kW"].get_value()	# Positiv
	speicherkW = opcjson["Girea-SPS"]["Speicher"]["gesamt kW"].get_value()
	# netzanbieterkW = 0 #opcjson["Girea-SPS"]["Netzanbieter"]["gesamt kW"].get_value()
	if opcjson["Girea-HMI"]["Netzanbieter"][f"[{id}]"]["SIMstartstopp"].get_value() == 0:	# hand aus
		opcjson["Girea-SPS"]["Netzanbieter"][f"[{id}]"]["ist an"].set_value(False)
		opcjson["Girea-SPS"]["Netzanbieter"][f"[{id}]"]["kW"].set_value(0)
	elif opcjson["Girea-HMI"]["Netzanbieter"][f"[{id}]"]["SIMstartstopp"].get_value() == 1:	# hand an
		opcjson["Girea-SPS"]["Netzanbieter"][f"[{id}]"]["ist an"].set_value(True)
		Ladeleistung = sum([erzeugerkW, verbraucherkW, speicherkW, leistung])
		opcjson["Girea-SPS"]["Netzanbieter"][f"[{id}]"]["kW"].set_value(Ladeleistung*-1)

def modulSumme(opcjson, modul="Verbraucher" ):

	mini = opcjson["Girea-SPS"][modul]["min index"].get_value()
	maxi = opcjson["Girea-SPS"][modul]["max index"].get_value()

	leistung = sum(opcjson["Girea-SPS"][modul][f"[{id}]"]["kW"].get_value() for id in range(mini,maxi+1))
	
	opcjson["Girea-SPS"][modul]["gesamt kW"].set_value(leistung)
	opcjson["Girea-HMI"][modul]["gesamt kW"].set_value(round(leistung,2))
	return leistung

def loop(opcjson):
	leistung = 0
	for j in range(12):
		SIM_Verbraucher(opcjson, j)
	leistung += modulSumme(opcjson, modul="Verbraucher")

	for j in range(3):
		SIM_Erzeuger(opcjson, j)
	leistung += modulSumme(opcjson, modul="Erzeuger")

	SIM_Speicher(opcjson, 0, 0)
	leistung += modulSumme(opcjson, modul="Speicher")
	SIM_Netzanbieter(opcjson, 0, 0)
	leistung += modulSumme(opcjson, modul="Netzanbieter")

	# print(leistung)	#muss 0 sein



if __name__ == '__main__':
	initDaten()
	myOPCUA = OPCUA()
	opcjson = myOPCUA.pull_data()
	# opcjson = init_OPCUA()
	# init_SIM_Speicher(opcjson, 0)		# auskomentieren wenn daten geladen wurden

	### Init temp
	for j in range(12):
		opcjson["Girea-HMI"]["Verbraucher"][f"[{j}]"]["Parameter"]["DSW kW"].set_value(100)
	for j in range(3):
		opcjson["Girea-HMI"]["Erzeuger"][f"[{j}]"]["Parameter"]["DSW kW"].set_value(1000)

	startloop(loop, myOPCUA,"SIM")


