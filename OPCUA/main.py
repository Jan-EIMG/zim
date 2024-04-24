import os.path
import sys
sys.path.insert(0, "..")
import time
import datetime

from opcua import ua, Server
from opcua.server.user_manager import UserManager
from opcua.common.xmlexporter import XmlExporter

from opcua.common.type_dictionary_buider import DataTypeDictionaryBuilder, get_ua_class

from IPython import embed
import json


Lizens = {
    "Erzeuger": 3,
    "Verbraucher": 5,
    "Speicher": 2,
    "Netzanbieter": 1
}

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
    print("Log"+text)
    try:
        with open("Log.txt", "x", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")
    except:
        with open("Log.txt", "a", encoding='utf-8') as outfile:
            now = datetime.datetime.now()
            outfile.write(text +" date: " + now.strftime("%d.%m.%Y %H:%M:%S.%f") + "\n")

users_db =  {
                'user1': 'pw1'
            }

def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]

if __name__ == "__main__":
    initDaten()
    # setup our server
    server = Server()    

    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    # load server certificate and private key. This enables endpoints
    # with signing and encryption.
    uri = "urn:freeopcua:python:server"
    server.set_application_uri(uri)
    # server.load_certificate("EIMG.cer")
    server.load_certificate("my_cert1.der")
    # server.load_private_key("EIMG.pem")
    server.load_private_key("my_private_key1.pem")

    policyIDs = ["Username"]
    server.set_security_IDs(policyIDs)
    server.user_manager.set_user_manager(user_manager)

 

    # server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840")
    # server.set_endpoint("opc.tcp://192.168.81.174:4840")

    # setup our own namespace, not really necessary but should as spec
    idx_name = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(idx_name)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()


    server.import_xml(os.path.join(os.path.dirname(__file__), "OPC-UA.xml"))

    # arr = objects.add_variable(idx, "myArray", [1, 2, 6])
    # arr.set_writable()

    # arr0 = arr.add_variable(idx, "Array[0]", 1)
    # arr0.set_writable()
    # arr1 = arr.add_variable(idx, "Array[1]", 2)
    # arr1.set_writable()
    # arr2 = arr.add_variable(idx, "Array[2]", 6)
    # arr2.set_writable()

    # with open("OPC-Data.json", "r", encoding='utf-8') as jsonFile:
    #     jsondata = json.load(jsonFile)
    #     Create_form(idx,objects, jsondata)

    # starting!
    server.start()

    # exporter = XmlExporter(server)
    # exporter.build_etree(node_list, ['http://myua.org/test/'])
    # exporter.write_xml('ua-export.xml')

    embed()

    # try:
    #     count = 0
    #     while True:
    #         time.sleep(1)
    #         count = myvar.get_value()
    #         count += 1.0
    #         myvar.set_value(count)
    # finally:
    #     #close connection, remove subscriptions, etc
    #     server.stop()




