
#-*- coding: utf-8-*-
import sys
from opcua import ua,Client
from opcua.common.node import Node
import time
import datetime
import json


from globals.OPCUA import OPCUA
from globals.globals import *

def update_dict(original, new):
	for key, value in new.items():
		# print(key,value, original[key])
		if isinstance(value, dict):
			update_dict(original[key], value)
		else:
			if isinstance(original[key], OPCUA._mytype):
				original[key].set_value(value)

if __name__ == '__main__':
	# initDaten()
	myOPCUA = OPCUA()
	opcjson = myOPCUA.pull_data()
	# opcplot = myOPCUA.pull_plot()
	# print(opcplot)

	# with open("saves/opc_UA_Dienstag.json", "r", encoding='utf-8') as infile:
	with open("saves\opc_UA_Mittwoch.json", "r", encoding='utf-8') as infile:
		json_data = json.load(infile)
		
	update_dict(opcjson, json_data)
	myOPCUA.push_data()

	del myOPCUA
