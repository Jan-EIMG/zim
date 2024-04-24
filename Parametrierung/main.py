
#-*- coding: utf-8-*-
import sys
from opcua import ua,Client
from opcua.common.node import Node
import time
import datetime
import json

from Parameter import *

from globals.OPCUA import OPCUA
from globals.globals import *

def laden(opcjson):
	stringID = opcjson["Girea-HMI"]["Parameter"]["ID"].get_value()
	id = int(stringID[1:])
	Aggregat = kennbuchstaben[stringID[0]]
	for paramterKey in vParameter.keys():
		position = vParameter[paramterKey]["position"]
		wert = opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"][paramterKey].get_value()
		opcjson["Girea-HMI"]["Parameter"][f"{position} Bezeichnung"].set_value(vParameter[paramterKey]["Anzeige bezeichnung"])
		opcjson["Girea-HMI"]["Parameter"][f"{position} Wert"].set_value(wert)
		opcjson["Girea-HMI"]["Parameter"][f"{position} info"].set_value(vParameter[paramterKey]["Info Text"])
		opcjson["Girea-HMI"]["Parameter"][f"{position} Falsche eingabe"].set_value(False)
		
		if "??-" in opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["Komponenten art"].get_value():
			opcjson["Girea-HMI"]["Parameter"][f"{18} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{19} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{20} Wert"].set_value(False)
		
		elif opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["abschaltbar"].get_value() == False and opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["ueberschuss"].get_value() == False:
			opcjson["Girea-HMI"]["Parameter"][f"{18} Wert"].set_value(True)
			opcjson["Girea-HMI"]["Parameter"][f"{19} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{20} Wert"].set_value(False)
		
		elif opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["abschaltbar"].get_value() == True:
			opcjson["Girea-HMI"]["Parameter"][f"{18} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{19} Wert"].set_value(True)
			opcjson["Girea-HMI"]["Parameter"][f"{20} Wert"].set_value(False)

		elif opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["ueberschuss"].get_value() == True:
			opcjson["Girea-HMI"]["Parameter"][f"{18} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{19} Wert"].set_value(False)
			opcjson["Girea-HMI"]["Parameter"][f"{20} Wert"].set_value(True)
		
		
		

		

def Speichern(opcjson):
	stringID = opcjson["Girea-HMI"]["Parameter"]["ID"].get_value()
	id = int(stringID[1:])
	Aggregat = kennbuchstaben[stringID[0]]
	fehlerfrei = True
	for paramterKey in vParameter.keys():
		position = vParameter[paramterKey]["position"]
		if opcjson["Girea-HMI"]["Parameter"][f"{position} Wert"].get_value()== "":
			fehlerfrei = False
			opcjson["Girea-HMI"]["Parameter"][f"{position} Falsche eingabe"].set_value(True)
		else:
			opcjson["Girea-HMI"]["Parameter"][f"{position} Falsche eingabe"].set_value(False)

	if fehlerfrei:
		for paramterKey in vParameter.keys():
			position = vParameter[paramterKey]["position"]
			wert = opcjson["Girea-HMI"]["Parameter"][f"{position} Wert"].get_value()
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"][paramterKey].set_value(wert)

		if opcjson["Girea-HMI"]["Parameter"][f"{18} Wert"].get_value():
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["Komponenten art"].set_value("NO- ")
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["abschaltbar"].set_value(False)
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["ueberschuss"].set_value(False)
		elif opcjson["Girea-HMI"]["Parameter"][f"{19} Wert"].get_value():
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["Komponenten art"].set_value("N - ")
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["abschaltbar"].set_value(True)
		elif opcjson["Girea-HMI"]["Parameter"][f"{20} Wert"].get_value():
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["Komponenten art"].set_value("Ü - ")
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["ueberschuss"].set_value(True)
		else:
			opcjson["Girea-HMI"][Aggregat][f"[{id}]"]["Parameter"]["Komponenten art"].set_value("??- ")

def loop(opcjson):
	if opcjson["Girea-HMI"]["Parameter"]["Laden"].get_value() == True:
		print("Laden")
		laden(opcjson)
		opcjson["Girea-HMI"]["Parameter"]["Laden"].set_value(False)

	if opcjson["Girea-HMI"]["Parameter"]["Speichern"].get_value() == True:
		print("Speichern")
		Speichern(opcjson)
		opcjson["Girea-HMI"]["Parameter"]["Speichern"].set_value(False) 

	
	# myOPCUA.push_data()
	# Zeit synkronisieren
	# time.sleep(1-(datetime.datetime.now().microsecond/1000000))	#s


if __name__ == '__main__':
	initDaten()
	myOPCUA = OPCUA()

	kennbuchstaben = {
		"v": "Verbraucher",
		"e": "Erzeuger",
		"s": "Speicher",
	}
	
		
	startloop(loop, myOPCUA,"Parameter")