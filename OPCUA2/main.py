import os.path
import sys
sys.path.insert(0, "..")
import time
import datetime
import matlab
import matlab.engine

from opcua import ua, Server
from opcua.server.user_manager import UserManager
from opcua.common.xmlexporter import XmlExporter

from opcua.common.type_dictionary_buider import DataTypeDictionaryBuilder, get_ua_class

from IPython import embed
import json

from opcua import uamethod

Lizens = {
    "Erzeuger": 3,
    "Verbraucher": 12,
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



# method to be exposed through server

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


@uamethod
def schedule(parent, Pel_max,storageCapacity, SOC, pl_min):
    print("Schedule Input parameter : ", Pel_max,storageCapacity, SOC, pl_min)
    eng = matlab.engine.start_matlab()
    ret = eng.schedule(Pel_max,storageCapacity, SOC, pl_min)
    print(ret)
    return ret


if __name__ == "__main__":
    initDaten()
    # setup our server
    server = Server()    

    # server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    # load server certificate and private key. This enables endpoints
    # with signing and encryption.
    uri = "urn:freeopcua:python:server"
    # uri = "urn:freeopcua:python:Model1"
    # uri = "urn:MyCompany:UaServer:Model1"
    server.set_application_uri(uri)
    # server.load_certificate("EIMG.cer")
    # server.load_certificate("my_cert1.der")
    # server.load_private_key("EIMG.pem")
    # server.load_private_key("my_private_key1.pem")

    # policyIDs = ["Username"]
    # server.set_security_IDs(policyIDs)
    # server.user_manager.set_user_manager(user_manager)

 

    # server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4848")
    # server.set_endpoint("opc.tcp://192.168.81.174:4840")

    # setup our own namespace, not really necessary but should as spec
    # idx_name = "http://examples.freeopcua.github.io"
    idx_name = "urn:MyCompany:UaServer:Model1"
    idx = server.register_namespace(idx_name)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()



    subobjects = objects.add_object(idx, "GIREA-SPS")
    for modul,length in Lizens.items():
        Verbraucher = subobjects.add_object(idx, modul)
        namelist = ["ist An","Soll An","Live Bit","verdrahtet","simuliert","automatik","start","stopp"]
        for name in namelist:
            arr = Verbraucher.add_variable(idx, name, [False]*length)
            arr.set_writable()
        arr = Verbraucher.add_variable(idx, "kW", [0.0]*length)
        arr.set_writable()



    # server.import_xml(os.path.join(os.path.dirname(__file__), "OPC-UA.xml"))

    arr = objects.add_variable(idx, "myArray", [1, 2, 6])
    arr.set_writable()

    arr = objects.add_variable(idx, "myArray16", [1, 2, 6], ua.VariantType.Int16)
    arr.set_writable()

    # arr = objects.add_variable(idx, "myArray16V2", [1, 2, 6], [ua.VariantType.Int16]*3)
    # arr.set_writable()

    arr = objects.add_variable(idx, "myArraybool", [False, True, False, True])
    arr.set_writable()

    arr = objects.add_variable(idx, "myArraybool2", [False]*5)
    arr.set_writable()

    myvar = objects.add_variable(idx, "Myint16", 6, ua.VariantType.Int16)
    myvar.set_writable()
    myvar = objects.add_variable(idx, "Myint23", 6, ua.VariantType.Int32)
    myvar.set_writable()
    myvar = objects.add_variable(idx, "Myint64", 6, ua.VariantType.Int64)
    myvar.set_writable()

    myvar = objects.add_variable(idx, "MyVariable", 6.7)
    myvar.set_writable()

    # myvar = objects.add_variable(idx, "MyVariable", 6.7)
    # myvar.set_writable()

    mysin = objects.add_variable(idx, "MyFloat", 6.7, ua.VariantType.Float)
    mysin.set_writable()

    
    mystringvar = objects.add_variable(idx, "MyStringVariable", "Really nice string")
    mystringvar.set_writable()

    myarrayvar = objects.add_variable(idx, "myarrayvar", [6.7, 7.9])
    myarrayvar = objects.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))

    mymethod = objects.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    multiply_node = objects.add_method(idx, "multiply", multiply, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])


    arr = objects.add_variable(idx, "testArray", [1, 2, 6], ua.VariantType.Int16)
    arr.set_writable()

    arr0 = arr.add_variable(idx, "Array[0]", 1, ua.VariantType.Int16)
    arr0.set_writable()
    arr1 = arr.add_variable(idx, "Array[1]", 2, ua.VariantType.Int16)
    arr1.set_writable()
    arr2 = arr.add_variable(idx, "Array[2]", 6, ua.VariantType.Int16)
    arr2.set_writable()

    myarrayvar = objects.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))


    inargx = ua.Argument()
    inargx.Name = "Pel_max"
    inargx.DataType = ua.NodeId(ua.ObjectIds.Float)
    inargx.ValueRank = -1
    inargx.ArrayDimensions = []
    inargx.Description = ua.LocalizedText("Pel der KA in kW")
    inargy = ua.Argument()
    inargy.Name = "storageCapacity"
    inargy.DataType = ua.NodeId(ua.ObjectIds.Float)
    inargy.ValueRank = -1
    inargy.ArrayDimensions = []
    inargy.Description = ua.LocalizedText("nutzbare Speicherkapazität in kWh")
    inargz = ua.Argument()
    inargz.Name = "SOC"
    inargz.DataType = ua.NodeId(ua.ObjectIds.Float)
    inargz.ValueRank = -1
    inargz.ArrayDimensions = []
    inargz.Description = ua.LocalizedText("Aktueller Speicherladezustand [0...1]")
    inargw = ua.Argument()
    inargw.Name = "pl_min"
    inargw.DataType = ua.NodeId(ua.ObjectIds.Float)
    inargw.ValueRank = -1
    inargw.ArrayDimensions = []
    inargw.Description = ua.LocalizedText("Mindestmodulationsgrad der KA")
    outarg = ua.Argument()
    outarg.Name = "ModulationVec"
    outarg.DataType = ua.NodeId(ua.ObjectIds.Double)
    outarg.ValueRank = -1
    outarg.ArrayDimensions = []
    outarg.Description = ua.LocalizedText("24 Std. Fahrplan")

    schedule_node = myobj.add_method(idx, "schedule", schedule, [inargx, inargy, inargz, inargw], [outarg])


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




