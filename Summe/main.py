#-*- coding: utf-8-*-
import sys
from opcua import ua,Client
from opcua.common.node import Node
import time
import datetime
import json

from globals.OPCUA import OPCUA
from globals.globals import *



# def modulSumme(opcjson, modul="Verbraucher" ):

# 	mini = opcjson["Girea-SPS"][modul]["min index"].get_value()
# 	maxi = opcjson["Girea-SPS"][modul]["max index"].get_value()


# 	leistunglist = sum(opcjson["Girea-SPS"][modul][f"[{id}]"]["kW"].get_value() for id in range(mini,maxi+1))
	
# 	opcjson["Girea-SPS"][modul]["gesamt kW"].set_value(leistunglist)
# 	opcjson["Girea-HMI"][modul]["gesamt kW"].set_value(round(leistunglist,2))


def loop(opcjson):
	module=["Verbraucher","Erzeuger","Speicher","Netzanbieter"]
	
	for modul in module:
		# modulSumme(opcjson, modul)
		mini = opcjson["Girea-SPS"][modul]["min index"].get_value()
		maxi = opcjson["Girea-SPS"][modul]["max index"].get_value()

		print([opcjson["Girea-SPS"][modul][f"[{id}]"]["kW"].get_value() for id in range(mini,maxi+1)])
		leistunglist = sum(opcjson["Girea-SPS"][modul][f"[{id}]"]["kW"].get_value() for id in range(mini,maxi+1))
		print(leistunglist)
		opcjson["Girea-SPS"][modul]["gesamt kW"].set_value(leistunglist)
		opcjson["Girea-HMI"][modul]["gesamt kW"].set_value(round(leistunglist,2))


if __name__ == '__main__':
	initDaten()
	myOPCUA = OPCUA()
	startloop(loop, myOPCUA,"Summe")


