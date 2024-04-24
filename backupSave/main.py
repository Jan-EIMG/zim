
#-*- coding: utf-8-*-
import sys
from opcua import ua,Client
from opcua.common.node import Node
import time
import datetime
import json


from globals.OPCUA import OPCUA
from globals.globals import *



if __name__ == '__main__':
	initDaten()
	myOPCUA = OPCUA()
	# opcplot = myOPCUA.pull_data()
	opcplot = myOPCUA.pull_plot()
	# print(opcplot)

	
	wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
	wochentag = wochentage[datetime.datetime.now().weekday()]

	try:
		with open(f"saves/opc_UA_{wochentag}.json", "w", encoding='utf-8') as outfile:
			# outfile.write(opcplot)
			json.dump(opcplot, outfile, default=str, indent=4, ensure_ascii=False)
	except:
		with open(f"saves/opc_UA_{wochentag}.json", "x", encoding='utf-8') as outfile:
			# outfile.write(opcplot)
			json.dump(opcplot, outfile, default=str, indent=4, ensure_ascii=False)
	
	del myOPCUA