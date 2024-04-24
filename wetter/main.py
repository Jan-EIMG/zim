#!/usr/bin/env python3
import sys
from opcua import ua,Client
from opcua.common.node import Node
import json
import time
import requests
import datetime
import re


wettertextDE={
    200:"Gewitter mit leichtem Regen",
	201:"Gewitter mit Regen",
	202:"Gewitter mit starkem Regen",
	210:"leichtes Gewitter",
	211:"Gewitter",
	212:"schweres Gewitter",
	221:"zerklüftetes Gewitter",
	230:"Gewitter mit leichtem Nieselregen",
	231:"Gewitter mit Nieselregen",
	232:"Gewitter mit starkem Nieselregen",

	300:"leichter Nieselregen",
	301:"Nieselregen",
	302:"Nieselregen mit starker Intensität",
	310:"leichter Nieselregen Regen",
	311:"Nieselregen",
	312:"starker Nieselregen Regen",
	313:"Schauer Regen und Nieselregen",
	314:"Starker Schauer Regen und Nieselregen",
	321:"Dusche Nieselregen",

	500:"leichter Regen",
	501:"mäßiger Regen",
	502:"starker Regen",
	503:"sehr starker Regen",
	504:"extremer Regen",
	511:"gefrierender Regen",
	520:"Regenschauer mit geringer Intensität",
	521:"Regenschauer",
	522:"Regenschauer mit hoher Intensität",
	531:"Starker Regenschauer",

	600:"leichter Schnee",
	601:"Schnee",
	602:"starker Schneefall",
	611:"Graupel",
	612:"leichter Graupelschauer",
	613:"Graupelschauer",
	615:"leichter Regen und Schnee",
	616:"Regen und Schnee",
	620:"leichter Schauer Schnee",
	621:"Schneeschauer",
	622:"starker Schneeschauer",

	701:"Nebel",
	711:"Rauch",
	721:"Dunst",
	731:"Sand-/Staubverwirbelungen",
	741:"Nebel",
	751:"Sand",
	761:"Staub",
	762:"vulkanische Asche",
	771:"Sturmböen",
	781:"Tornado",
	
    800:"klarer Himmel",

	801:"wenige Wolken: 11-25%",
	802:"aufgelockerte Bewölkung: 25-50%",
	803:"durchbrochene Wolken: 51-84%",
	804:"bedeckte Wolken: 85-100%"
}


def dict_set_value(overwrite,indict):
    # print(overwrite,indict)
    pattern = r'\[(\d+)\]'
    for key in overwrite.keys():
        # print(key)
        if isinstance(overwrite[key], dict):
            # if isinstance(indict[key], dict):
            if re.search(pattern, key):
                key2 = int(re.search(pattern, key).group(1))
                print(key2)
                dict_set_value(overwrite[key],indict[key2])
            
            elif indict.get(key) is not None:
                dict_set_value(overwrite[key],indict[key])


        elif isinstance(overwrite[key], list):
            subobjects = {}
            # for index, item in enumerate(overwrite[key]):
            for i in range(len(overwrite[key])):
                dict_set_value(overwrite[key][i],indict[key][i])
        else:
            # if indict.has_key(key):
            if indict.get(key) is not None:
                overwrite[key].set_value(indict[key])
        

# def liveweather(opcuadata,weatherdata):
#     # for key in opcuadata.keys():
#     opcuadata["weather"][0] = weatherdata["weather"][0]
#     opcuadata["main"] = weatherdata["main"]
#     opcuadata["wind"] = weatherdata["wind"]
#     opcuadata["rain"] = weatherdata["rain"]
#     opcuadata["clouds"] = weatherdata["clouds"]


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

def log(name):
    print("Log"+name)
    try:
        with open("Log.txt", "x", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(name +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")
    except:
        with open("Log.txt", "a", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(name +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")


def thunderstorm(lat, lon, API_KEY, weatherIDs):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")

        if response.status_code == 200:
            weatherdata = response.json()

            return (weatherdata, weatherdata["weather"][0]["id"] in weatherIDs)
            # return data["weather"][0]["icon"] == '03d'
        else:
            log("influxDB web error: "+str(response.status_code))
    except:
        log("thunderstorm ERROR:")




if __name__ == '__main__':
    initDaten()

    API_KEY = "f79c04f7bc0fbf2c634c6b6139e93533"
    lat = "51.4771333"
    lon = "6.7203372"

    weatherIDs = [200,201,202,210,211,212,221,230,231,232,502,503,504,511,522,531,781]


    url = "opc.tcp://opcua:4840"
    url = "opc.tcp://192.168.1.101:4840"
    url = "opc.tcp://192.168.81.174:4840"
    # url = "opc.tcp://test:test@192.168.0.1:4840"
    # url = "opc.tcp://OPCUser01:11223344Ki@192.168.1.232:4840"
    # security_string = "Basic256Sha256,SignAndEncrypt," + "OPC_UA\\cient_X.509 Certificate_4.der" + "," + "OPC_UA\\cient_X.509 Certificate_4.pem"
    # security_string = "Basic256Sha256,SignAndEncrypt," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.der" + "," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.pem"
    security_string = "Basic256Sha256,SignAndEncrypt," + "my_cert2.der" + "," + "my_private_key2.pem"

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
    myjson = browse_recursive(client.get_objects_node())

    
    
    lastbit = None
    ### Mein Loop
    i = 0.0
    time.sleep(60-(datetime.datetime.now().second+datetime.datetime.now().microsecond/1000000))
    while(True):
        myjson["Girea-Module"]["Wetter"]["live bit"].set_value(not myjson["Girea-Module"]["Wetter"]["live bit"].get_value())
        myjson["Girea-Module"]["Wetter"]["zyklus"].set_value(i)

        ## Wetterdaten
        weatherdata, unwetter = thunderstorm(lat, lon, API_KEY, weatherIDs)
        if lastbit != unwetter:
            myjson["Girea-Module"]["Wetter"]["unwetter"].set_value(unwetter)
            myjson["Girea-HMI"]["Wetter"]["unwetter"].set_value(unwetter)
        # try:
        dict_set_value(myjson["Girea-HMI"]["Wetter"],weatherdata)

        myjson["Girea-HMI"]["Wetter"]["weather"]["[0]"]["description-DE"].set_value(wettertextDE[weatherdata["weather"][0]["id"]])
        # except:
        #     print("weatherdata error:")

        time.sleep(60-(datetime.datetime.now().second+datetime.datetime.now().microsecond/1000000))
        i += 1.0